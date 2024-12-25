import logging
import re
from typing import Dict

from IPy import IP

from caasm_aql.query_builders.fuzzy_provider import FuzzyProvider

log = logging.getLogger()


class BaseFuzzyProvider(FuzzyProvider):

    def __init__(self, category):
        self.category = category
        super(BaseFuzzyProvider, self).__init__(category)

    @property
    def pipelines(self):
        return []

    @classmethod
    def get_ip_equal_condition(cls, ip, aql):
        return {}

    @classmethod
    def get_ip_range_condition(cls, ip, aql):
        return {}

    @classmethod
    def _build_query(cls, fulltext):
        return [
            {"multi_match": {"query": fulltext, "fields": ["*"], "type": "phrase"}},
            {"term": {"__query__.keyword": fulltext}},
            {"wildcard": {"__query__.keyword": "*" + fulltext + "*"}},
            {"regexp": {"__query__": r".*" + re.escape(fulltext.lower()) + r".*"}},
        ]

    def provide(self, aql, additions) -> Dict:
        result = None
        if isinstance(aql, str):
            query = [
                {"multi_match": {"query": aql, "fields": ["*"], "type": "phrase"}},
                {"term": {"__query__.keyword": aql}},
                {"wildcard": {"__query__.keyword": "*" + aql + "*"}},
                {"regexp": {"__query__": r".*" + re.escape(aql.lower()) + r".*"}},
            ]
        elif isinstance(aql, list):
            sub_queries = []
            for segment in aql:
                sub_queries.extend(self._build_query(segment))
            query = [
                {
                    "bool": {
                        "should": sub_queries
                    }
                }
            ]
        else:
            query = []

        for parser in self.pipelines:
            try:
                tmp_query = parser(aql)
                if not tmp_query:
                    continue
            except Exception as e:
                log.warning(f"Parse({parser}) aql:({aql}) error({e})")
            else:
                query.append(tmp_query)

        condition_queries = additions if additions else []

        if query:
            condition_queries.append({"bool": {"should": query, "minimum_should_match": 1}})

        if condition_queries:
            result = {"bool": {"must": condition_queries}}

        log.debug(f"Full text query is {query}")
        return result


class IPFuzzyProvider(BaseFuzzyProvider):
    class _IPQueryType(object):
        FULL_IP = "full_ip"
        NET_IP = "net_ip"
        INCOMPLETE_IP = "incomplete_ip"

    @property
    def pipelines(self):
        return [self._build_ips]

    @classmethod
    def _build_ip(cls, aql) -> Dict:
        result = {}

        ip = cls.__convert_ip(aql)
        if not ip:
            return result

        # 需要判读是否是完整的IP
        ip_query_type = cls.__parse_ip_type(aql, ip.version())

        if ip_query_type in (cls._IPQueryType.FULL_IP, cls._IPQueryType.NET_IP):
            result = cls.get_ip_equal_condition(ip, aql)
        elif ip_query_type == cls._IPQueryType.INCOMPLETE_IP:
            result = cls.get_ip_range_condition(ip, aql)
        return result

    @classmethod
    def _build_ips(cls, aql) -> Dict:
        if isinstance(aql, str):
            return cls._build_ip(aql)
        elif isinstance(aql, list):
            results = []
            result = {
                "bool": {
                    "should": results
                }
            }
            for segment in aql:
                segment_result = cls._build_ip(segment)
                if segment_result:
                    results.append(segment_result)
            if results:
                return result
            else:
                return {}
        else:
            return {}

    @classmethod
    def __convert_ip(cls, aql):
        try:
            ip = IP(aql)
        except Exception as e:
            return None
        return ip

    @classmethod
    def __parse_ip_type(cls, aql, version):
        if "/" in aql:
            return cls._IPQueryType.NET_IP

        if version == 4:
            aql_records = aql.split(".")
            check_length = 4
        else:
            aql_records = aql.split(":")
            check_length = 8

        if len(aql_records) != check_length:
            return cls._IPQueryType.INCOMPLETE_IP

        return cls._IPQueryType.FULL_IP
