from nanoid import generate
from caasm_tool.util import extract

from caasm_pipeline.lineage.service.constants.lineage import LineageStageType
from caasm_pipeline.lineage.service.runtime import entity_type_lineage_stage_service, entity_lineage_fabric_stage_service, \
    value_lineage_fabric_stage_service


class LineageRecorder:
    def __init__(self):
        self._entity_lineages = {}
        self._value_lineages = {}
        self._lineage_trace_ids = set()
        self._adapter_tables = {}
        self._category = None
        self._date = None
        self._entity_lineages_initialized = False
        self._value_lineages_initialized = False

    def initialize(self, adapter_tables, category, date):
        self._adapter_tables = adapter_tables
        self._category = category
        self._date = date

    def record_entity_type_lineage(self, adapter_convert_data_by_mapper, entity_type):
        upstreams = []
        for k, v in adapter_convert_data_by_mapper.items():
            if v:
                table_name = self._adapter_tables.get(k)
                if table_name:
                    upstreams.append(table_name)
        if upstreams:
            entity_type_lineage_stage_service.save_direct(
                {
                    "table": "",
                    "type": LineageStageType.FABRIC,
                    "meta": {"date": self._date, "category": self._category, "entity_type": entity_type},
                    "upstreams": upstreams,
                }
            )

    def _record_non_fabric_lineages(self, adapter_name, sid, entity_id):
        self._entity_lineages[entity_id] = [{"adapter_name": adapter_name, "sid": sid}]
        if len(self._entity_lineages) >= 100:
            self.generate_entity_lineages(self._entity_lineages)

    def generate_entity_lineages(self, entity_lineages, force=False):
        if not force and len(entity_lineages) < 100:
            return
        if not self._entity_lineages_initialized:
            entity_lineage_fabric_stage_service.drop(
                entity_lineage_fabric_stage_service.get_table(self._category, self._date)
            )
            self._entity_lineages_initialized = True
        lineage_entities = []
        for entity_id, lineages in entity_lineages.items():
            if entity_id in self._lineage_trace_ids:
                print("实体血缘已存在：", entity_id)
            self._lineage_trace_ids.add(entity_id)
            upstreams = []
            for upstream in lineages:
                converted_table = self._adapter_tables.get(upstream["adapter_name"])
                if converted_table:
                    upstreams.append(
                        {
                            "table": converted_table,
                            "sid": upstream["sid"],
                        }
                    )
            lineage_entities.append(
                {
                    "table": "",
                    "type": LineageStageType.FABRIC,
                    "trace_id": entity_id,
                    "meta": {},
                    "upstreams": upstreams,
                }
            )
        if lineage_entities:
            self._save_entity_lineages(self._category, lineage_entities)
        entity_lineages.clear()

    def _save_entity_lineages(self, category, entity_lineages):
        if entity_lineages:
            entity_lineage_fabric_stage_service.save_multi_direct(
                entity_lineages, entity_lineage_fabric_stage_service.get_table(category, self._date)
            )

    def finish(self):
        if self._entity_lineages:
            self.generate_entity_lineages(self._entity_lineages, True)
        self._entity_lineages.clear()
        if self._value_lineages:
            self.save_value_lineages(True)
        self._value_lineages.clear()

    def record_lineages(self, convert_records, merged_record, value_lineages=None):
        #   记录实体血缘
        lineages = []
        for src_entity in convert_records:
            adapter_name = extract(src_entity, "base.adapter_name")
            sid = extract(src_entity, "_id")
            if not adapter_name or not sid:
                continue
            sid = str(sid)
            lineages.append({"adapter_name": adapter_name, "sid": sid})
        entity_id = extract(merged_record, "base.entity_id")
        if entity_id:
            self._entity_lineages[entity_id] = lineages
            self.generate_entity_lineages(self._entity_lineages)
            #   记录值血缘
            if value_lineages:
                self._value_lineages[entity_id] = value_lineages
            self.save_value_lineages()

    def save_value_lineages(self, force=False):
        if not force and len(self._value_lineages) < 100:
            return

        if not self._value_lineages_initialized:
            value_lineage_fabric_stage_service.drop(
                value_lineage_fabric_stage_service.get_table(self._category, self._date)
            )
            self._value_lineages_initialized = True
        lineage_values = []
        for entity_id, field_lineages in self._value_lineages.items():
            upstreams_dict = {}
            field_list = []
            value_lineage_stage_dict = {
                "table": None,
                "type": LineageStageType.FABRIC,
                "trace_id": entity_id,
                "meta": {},
                "fields": field_list,
            }
            for field, value_lineages in field_lineages.items():
                row_lineages_list = []
                field_value_lineage_dict = {"field": field, "rows": row_lineages_list}
                for row_index, upstreams in value_lineages.items():
                    value_row_upstreams = {}
                    for adapter_name, upstream_indices in upstreams.items():
                        if adapter_name not in self._adapter_tables:
                            continue
                        converted_table = self._adapter_tables[adapter_name]
                        for upstream_index in upstream_indices:
                            sid, index = upstream_index
                            key = f"{converted_table}-{str(sid)}"
                            if key in upstreams_dict:
                                upstream = upstreams_dict[key]
                            else:
                                new_id = generate()
                                upstream = {"table": converted_table, "sid": str(sid), "id": new_id}
                                upstreams_dict[key] = upstream
                            upstream_id = upstream["id"]
                            if upstream_id not in value_row_upstreams:
                                value_row_upstreams[upstream_id] = {"upstream": upstream_id, "indices": []}
                            value_row_upstreams_of_upstream_id = value_row_upstreams[upstream_id]
                            value_row_upstreams_of_upstream_id["indices"].append(index)
                    row_lineage = {"index": row_index, "upstreams": list(value_row_upstreams.values())}
                    row_lineages_list.append(row_lineage)
                field_list.append(field_value_lineage_dict)
            value_lineage_stage_dict["upstreams"] = list(upstreams_dict.values())
            lineage_values.append(value_lineage_stage_dict)
        value_lineage_fabric_stage_service.save_multi_direct(
            lineage_values, value_lineage_fabric_stage_service.get_table(self._category, self._date)
        )
        self._value_lineages.clear()
