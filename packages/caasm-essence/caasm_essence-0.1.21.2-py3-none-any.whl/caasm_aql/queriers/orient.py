import logging
import traceback
from datetime import datetime
from typing import List

from pyorient import OrientRecord
from pyorient.ogm.vertex import Vertex

from caasm_aql.aql import AsqlOption, AqlAddition
from caasm_aql.asgl import AsglQuery
from caasm_aql.querier import GraphQuerier, QuerierResult, LogicalGroupQuerier
from caasm_aql.query_builders.backend.orient import OrientGraphBuilder
from caasm_entity.service.services.asset_graph import EntityGraphHandler

log = logging.getLogger()


class OrientGraphQuerier(GraphQuerier):
    def __init__(self, logical_group_querier: LogicalGroupQuerier):
        super(OrientGraphQuerier, self).__init__(logical_group_querier)
        self.builder = OrientGraphBuilder()

    def _query_for_view(self, query: AsglQuery, result: QuerierResult, category: str, option: [AsqlOption, None] = None,
                        date_: datetime = None, additions: List[AqlAddition] = None, entity_ids=None):
        statement = self.builder.build_for_view(query)
        graph_handler = EntityGraphHandler(category)
        graph_handler.include_registry()

        # graph = graph_handler.graph
        entity_ids = list()
        try:
            try:
                result_obj = graph_handler.client.query(statement)
                for record in result_obj:
                    record: OrientRecord = record
                    entity_ids.append(record.oRecordData['entity_id'])
            except Exception as exc:
                result.errors.append('查询出现错误')
                log.exception(exc)
            if result.errors:
                return result

            return entity_ids
        finally:
            graph_handler.client.db_close()

    def _query_for_entity(self, entity_id: str, query: AsglQuery, result: QuerierResult, category: str,
                          option: [AsqlOption, None] = None, date_: datetime = None,
                          additions: List[AqlAddition] = None):
        statement, params = self.builder.build_for_entity(entity_id, query, option)
        graph_handler = None

        try:
            graph_handler = EntityGraphHandler(category, date_)
            graph_handler.include_registry()

            graph_client = graph_handler.client
            graph = graph_handler.graph

            result_obj = graph_client.query(statement)
            graphs = list()
            for record in result_obj:
                vertices = list()
                edges = list()
                record: OrientRecord = record
                root_id = None
                for ele_name, ele in record.oRecordData.items():
                    element = graph.get_element(ele)
                    values = element._props.copy()
                    if isinstance(element, Vertex):
                        vertex_type = values.pop('type')
                        if vertex_type == 'entity_root':
                            root_id = str(ele)
                            continue
                        vertex_data = values
                        if 'in_relation' in vertex_data:
                            vertex_data.pop('in_relation')
                        if 'out_relation' in vertex_data:
                            vertex_data.pop('out_relation')
                        if ele_name in query.vertex_defs:
                            ver_def = query.vertex_defs[ele_name]
                            trait = ver_def.trait
                        else:
                            trait = None
                        vertex = {
                            "id": str(ele),
                            "display_name": vertex_data["value"],
                            "type": type(element).__name__,
                            "data": vertex_data,
                            "trait": trait
                        }
                        vertices.append(vertex)
                    else:
                        source = element._out
                        target = element._in
                        if root_id in {source, target}:
                            continue
                        edge = {
                            'id': element._id,
                            'src': source,
                            'dst': target,
                            'type': 'Relation',
                            'display_name': values['relation']
                        }
                        edges.append(edge)
                graphs.append(
                    {
                        'vertices': vertices,
                        'edges': edges
                    }
                )
            result.data = graphs
            return result
        except Exception as e:
            log.warning(f"query orient error {e}, detail is {traceback.format_exc()}")
        finally:
            graph_handler.finish() if graph_handler else ...
