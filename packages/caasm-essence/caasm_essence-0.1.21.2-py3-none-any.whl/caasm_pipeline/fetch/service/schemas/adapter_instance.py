from caasm_persistence_base.schema.base import (
    EnumField,
    fields,
    DocumentSchema,
    DateTimeField,
    BaseSchema,
)
from caasm_service_base.constants.adapter import AdapterInstanceRunStatus, AdapterInstanceConnectionStatus

from caasm_common.service.constants.trigger import TriggerType
from caasm_pipeline.fetch.service.entities.adapter_instance import Trigger, AdapterInstance


class TriggerSchema(BaseSchema):
    entity_define = Trigger

    type = EnumField(TriggerType, load_default=TriggerType.CRON, by_value=True)
    value = fields.Dict()


class AdapterInstanceSchema(DocumentSchema):
    entity_define = AdapterInstance

    name = fields.String(description="实例名称", load_default=None)
    enabled = fields.Boolean(description="实例状态", load_default=None)
    adapter_name = fields.String(description="适配器名称", load_default="")
    properties = fields.List(fields.String(), load_default=None)
    ancestor_adapter_name = fields.String(description="实际的适配信息", load_default="")
    connection = fields.Dict(description="适配器参数", load_default=dict)
    trigger_type = fields.String(description="适配器名称", load_default="")
    trigger = fields.Nested(TriggerSchema, description="触发器", load_default=dict, allow_none=True)
    description = fields.String(description="描述信息", load_default="")
    debug = fields.Boolean(description="是否调试模式", load_default=False)
    proxy = fields.String(description="代理地址", load_default=None)
    is_complex = fields.Boolean(description="是否负载适配器", load_default=None)
    run_status = EnumField(
        AdapterInstanceRunStatus,
        load_default=AdapterInstanceRunStatus.WAIT,
        by_value=True,
        description="运行状态",
    )
    connect_status = EnumField(
        AdapterInstanceConnectionStatus,
        load_default=AdapterInstanceConnectionStatus.UNKNOWN,
        by_value=True,
        description="连接状态",
    )
    last_sync_time = DateTimeField(load_default=None, allow_none=None)
