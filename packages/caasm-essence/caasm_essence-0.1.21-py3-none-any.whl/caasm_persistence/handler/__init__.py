from caasm_tool.constants import StrEnum

DEFAULT_CLIENT = None


class TableName(StrEnum):
    adapter = "adapter"
    adapter_instance = "adapter_instance"
    manufacturer = "manufacturer"
    file = "file"

    fetch_record = "fetch.record"
    merge_record = "merge.record"
    convert_record = "convert.record"

    inventory = "inventory"
    inventory_error_data = "inventory.error_data"
    inventory_config = "inventory.config"
    inventory_asset_type = "inventory.asset_types"

    sequence = "sequence"

    task = "task"

    job = "job"

    setting = "setting"
    user_aql_collect = "user.user_aql_collect"
    user_aql_history = "user.user_aql_history"

    snapshots = "snapshots"

    aql_scene = "aql_scene"

    business = "operation.businesses"
    department = "operation.departments"
    owner = "operation.owners"
    realm = "operation.realms"

    enforcement_set = "enforcement.enforcement_sets"
    enforcement_task = "enforcement.enforcement_tasks"

    permission = "permission"

    meta_entity_view_config = "meta.view_configs"

    variable = "variable"

    asset = "inventory"
