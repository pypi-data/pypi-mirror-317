from datetime import datetime, date
from typing import List

from caasm_aql.aql import AsqlOption, AqlQuery, AqlLogicQuery, AqlAddition
from caasm_aql.aql_resolver import AqlResolver
from caasm_aql.asgl import AsglQuery
from caasm_aql.asgl_resolver import AsglResolver
from caasm_aql.asql_plus import AsqlPlusResolver, AsqlPlusLogicalQuery


class QuerierResult:
    def __init__(self):
        self.data: list = list()
        self.cursor = None
        self.count: int = 0
        # 涉及到哪些数据集合
        self.datasets = []
        # 错误信息集合
        self.errors = []
        self.high_lights = []


class Querier:
    def __init__(self, meta_fields, *args, **kwargs):
        self.meta_fields = meta_fields

    def query(self, aql: str, result: QuerierResult, additions: List[AqlAddition]) -> QuerierResult:
        """
        查询满足条件的全量实体，供处置中心等使用
        :param aql: 查询语句
        :param result: 查询结果
        :param additions: 其他约束查询条件
        :return: 查询结果
        """
        resolver: AqlResolver = AqlResolver()
        query: AqlQuery = resolver.resolve(aql)
        return self._query(query, result, additions=additions)

    def query_for_view(
        self,
        aql: str,
        option: AsqlOption,
        date: datetime = None,
        additions: List[AqlAddition] = None,
    ) -> QuerierResult:
        """
        对视图查询，包含视图的分页等选项
        :param aql: 查询语句
        :param option: 视图选项，如分页等
        :param date: 查询快照的日期，如果不提供参数，则查询最新的资产库
        :param additions: 其他约束查询条件
        :return: 查询结果
        """
        result = QuerierResult()
        try:
            #   全文检索
            if aql.startswith("*") or not (
                aql.startswith("$")
                or aql.startswith("entity")
                or aql.startswith("@")
                or aql.startswith("adapters")
                or aql.startswith("where not")
                or aql.startswith("not")
                or aql.startswith("(")
            ):
                query: AqlQuery = AqlQuery()
                query.aql = aql
            else:
                resolver: AsqlPlusResolver = AsqlPlusResolver()
                query: AqlQuery = resolver.resolve(aql)
        except ValueError as ex:
            error = ex.args[0]
            if isinstance(error, list):
                result.errors.extend(error)
            else:
                result.errors.append(error)
            return result
        return self._query(query, result, option, date, additions=additions)

    def _query(
        self,
        query: AqlQuery,
        result: QuerierResult,
        option: [AsqlOption, None] = None,
        date: datetime = None,
        load=False,
        additions=None,
    ) -> QuerierResult:
        raise NotImplementedError()


class LogicalGroupQuerier:
    def __init__(self, meta_fields, *args, **kwargs):
        self.meta_fields = meta_fields

    def parse_aql(self, category, aql, option=None, additions=None, entity_ids=None):
        raise NotImplementedError

    def _construct_query(self, aql: str, option: AsqlOption = None, d: date = None) -> (AqlLogicQuery, QuerierResult):
        result = QuerierResult()
        try:
            resolver: AsqlPlusResolver = AsqlPlusResolver(as_fulltext=True)
            query: AsqlPlusLogicalQuery = resolver.resolve_logic_query(aql)
            return query, result
        except ValueError as ex:
            error = ex.args[0]
            if isinstance(error, list):
                result.errors.extend(error)
            else:
                result.errors.append(error)
            return None, result

    def query(
        self,
        aql: str,
        category: str,
        option: AsqlOption,
        d: datetime = None,
        additions: List[AqlAddition] = None,
        entity_ids=None,
    ) -> QuerierResult:
        """
        查询满足条件的全量资产，供处置中心等使用
        :param aql: 查询语句
        :param option: 查询选项
        :param category: 实体分类
        :param d: 查询日期
        :param additions: 额外限制条件
        :param entity_ids: 限定实体ID列表
        :return: 查询结果
        """
        option.page_size = None
        option.page_index = None

        query, result = self._construct_query(aql, option, d)
        return self._query(
            query,
            result,
            category,
            option=option,
            date_=d,
            load=False,
            additions=additions,
            entity_ids=entity_ids
        )

    def query_for_view(self, aql, category: str, option, d=None, additions=None, entity_ids=None) -> QuerierResult:
        query, result = self._construct_query(aql, option, d)
        if result.errors:
            return result
        return self._query(query, result, category, option, d, additions=additions, entity_ids=entity_ids)

    def _query(self, query, result, category, option=None, date_=None, additions=None, entity_ids=None):
        raise NotImplementedError()


class GraphQuerier:
    def __init__(self, logical_group_querier: LogicalGroupQuerier):
        self.logical_group_querier: LogicalGroupQuerier = logical_group_querier

    def _construct_query(self, asgl: str, option: AsqlOption, d: date = None):
        result = QuerierResult()
        try:
            resolver: AsglResolver = AsglResolver()
            query: AsglQuery = resolver.resolve(asgl)
            query.build()
            return query, result
        except ValueError as ex:
            error = ex.args[0]
            if isinstance(error, list):
                result.errors.extend(error)
            else:
                result.errors.append(error)
            return None, result

    def query_for_view(self, asgl, category, option: AsqlOption, d=None, additions=None, entity_ids=None):
        query, result = self._construct_query(asgl, option, d)
        if result.errors:
            return result
        entity_ids = self._query_for_view(query, result, category, option, d, additions)
        result: QuerierResult = result
        if result.errors:
            return result
        return self.logical_group_querier.query_for_view("", category, option, d, additions, entity_ids)

    def query_for_entity(self, entity_id, asgl, category, option=None, d=None, additions=None):
        query, result = self._construct_query(asgl, option, d)
        if result.errors:
            return result
        return self._query_for_entity(entity_id, query, result, category, option, d, additions)

    def _query_for_view(
        self,
        query: AsglQuery,
        result: QuerierResult,
        category: str,
        option: [AsqlOption, None] = None,
        date_: datetime = None,
        additions: List[AqlAddition] = None,
    ):
        raise NotImplementedError()

    def _query_for_entity(
        self,
        entity_id: str,
        query: AsglQuery,
        result: QuerierResult,
        category: str,
        option: [AsqlOption, None] = None,
        date_: datetime = None,
        additions: List[AqlAddition] = None,
    ):
        raise NotImplementedError()
