from typing import Dict

from marshmallow import Schema, fields, ValidationError, post_load
from marshmallow_enum import EnumField

from caasm_aql.aql import (
    AqlLogicQuery, AqlAdapterTarget,
)
from caasm_aql.asql_field import AqlFieldTarget, AsqlFieldLogicQuery
from caasm_aql.base import AqlLogicalGroup, AqlOperator, AqlLogicalOperand, AqlGroupItem, AqlItemType, AqlLogicalCall, \
    AqlTargetItem, AqlTargetType, AqlCallType, AqlValueType, AqlOperatorCall, AqlMethodCall, AqlValue, AqlTarget, \
    AqlInventoryTarget


class AqlItemSchema(Schema):
    item_type = EnumField(
        AqlItemType,
        by_value=True,
        attribute="item_type",
        data_key="type",
        required=True,
    )


class AqlGroupItemSchema(AqlItemSchema):
    group = fields.Nested("AqlLogicalGroupSchema", required=True)

    @post_load
    def make_obj(self, data: dict, **kwargs):
        group_item = AqlGroupItem()
        group_item.group = data["group"]
        return group_item


class AqlTargetItemSchema(AqlItemSchema):
    target = fields.Method("serialize_target", "deserialize_target", required=True)

    @staticmethod
    def serialize_target(obj: AqlTargetItem):
        target = obj.target
        if isinstance(target, AqlInventoryTarget):
            schema = AqlInventoryTargetSchema()
        elif isinstance(target, AqlAdapterTarget):
            schema = AqlAdapterTargetSchema()
        else:
            schema = AqlFieldTargetSchema()
        return schema.dump(target)

    @staticmethod
    def deserialize_target(value: dict):
        target_type = AqlTargetType(value["type"])
        if target_type == AqlTargetType.INVENTORY:
            schema = AqlInventoryTargetSchema()
        elif target_type == AqlTargetType.ADAPTER:
            schema = AqlAdapterTargetSchema()
        else:
            schema = AqlFieldTargetSchema()
        return schema.load(value)

    @post_load
    def make_obj(self, data: dict, **kwargs):
        target_item = AqlTargetItem()
        target_item.target = data["target"]
        return target_item


class AqlTargetSchema(Schema):
    target_type = EnumField(
        AqlTargetType,
        by_value=True,
        required=True,
        data_key="type",
        attribute="target_type",
    )
    field_name = fields.String(required=True)
    call = fields.Method("serialize_call", "deserialize_call", required=True)

    @staticmethod
    def serialize_call(obj: AqlTarget):
        call = obj.call
        if isinstance(call, AqlOperatorCall):
            schema = AqlOperatorCallSchema()
        elif isinstance(call, AqlMethodCall):
            schema = AqlMethodCallSchema()
        else:
            schema = AqlLogicalCallSchema()
        dumped = schema.dump(call)
        return dumped

    @staticmethod
    def deserialize_call(value: dict):
        call_type = AqlCallType(value["type"])
        if call_type == AqlCallType.OPERATOR:
            schema = AqlOperatorCallSchema()
        elif call_type == AqlCallType.METHOD:
            schema = AqlMethodCallSchema()
        else:
            schema = AqlLogicalCallSchema()
        return schema.load(value)


class AqlInventoryTargetSchema(AqlTargetSchema):
    @post_load
    def make_obj(self, data: dict, **kwargs):
        target = AqlInventoryTarget()
        target.call = data["call"]
        target.field_name = data["field_name"]
        return target


class AqlAdapterTargetSchema(AqlTargetSchema):
    adapter_dataset = fields.String(required=True, data_key="adapter", attribute="adapter_dataset")

    @post_load
    def make_obj(self, data: dict, **kwargs):
        target = AqlAdapterTarget()
        target.adapter_dataset = data["adapter_dataset"]
        target.field_name = data["field_name"]
        target.call = data["call"]
        return target


class AqlFieldTargetSchema(AqlTargetSchema):
    @post_load
    def make_obj(self, data: dict, **kwargs):
        target = AqlFieldTarget()
        target.field_name = data["field_name"]
        target.call = data["call"]
        return target


class AqlCallSchema(Schema):
    call_type = EnumField(
        AqlCallType,
        by_value=True,
        required=True,
        data_key="type",
        attribute="call_type",
    )


class AqlValueSchema(Schema):
    value_type = EnumField(
        AqlValueType,
        by_value=True,
        required=True,
        data_key="type",
        attribute="value_type",
    )
    value = fields.Method(required=True, serialize='serialize_value', deserialize='deserialize_value')

    @post_load
    def make_obj(self, data: dict, **kwargs):
        return AqlValue(data["value_type"], data["value"])

    def serialize_value(self, obj):
        if isinstance(obj, list):
            #   list暂时仅支持内部为值，不支持变量
            results = list()
            for item in obj:
                if isinstance(item, AqlValue):
                    if item.value_type == AqlValueType.VALUE:
                        results.append(item.value)
                else:
                    results.append(item)
            return results
        elif isinstance(obj, AqlValue):
            return self.serialize_value(obj.value)
        else:
            return obj

    def deserialize_value(self, value):
        if isinstance(value, list):
            results = list()
            for item in value:
                result = self.deserialize_value(item)
                results.append(result)
            return results
        else:
            return value


class AqlOperatorCallSchema(AqlCallSchema):
    operator = EnumField(AqlOperator, by_value=True, required=True)
    value = fields.Nested(AqlValueSchema, required=True)

    @post_load
    def make_obj(self, data: dict, **kwargs):
        call = AqlOperatorCall()
        call.value = data["value"]
        call.operator = data["operator"]
        return call


class AqlMethodCallSchema(AqlCallSchema):
    method = fields.String(required=True)
    param_list = fields.List(
        fields.Nested(AqlValueSchema, required=True),
        required=False,
        allow_none=True,
        default=list(),
    )

    @post_load
    def make_obj(self, data: dict, **kwargs):
        call = AqlMethodCall()
        call.method = data["method"]
        call.param_list = data["param_list"]
        return call


class AqlLogicalCallSchema(AqlCallSchema):
    logical_group = fields.Nested(
        "AqlLogicalGroupSchema",
        required=True,
        data_key="group",
        attribute="logical_group",
    )

    @post_load
    def make_obj(self, data: dict, **kwargs):
        call = AqlLogicalCall()
        call.logical_group = data["logical_group"]
        return call


class AqlLogicalGroupSchema(Schema):
    items = fields.Method("serialize_item", "deserialize_item", required=True)
    operand = EnumField(AqlLogicalOperand, by_value=True, required=True)
    not_boolean = fields.Boolean(required=True)

    @staticmethod
    def serialize_item(obj: AqlLogicalGroup):
        group_item_schema = AqlGroupItemSchema()
        target_item_schema = AqlTargetItemSchema()
        result = list()
        for item in obj.items:
            if isinstance(item, AqlGroupItem):
                schema = group_item_schema
            elif isinstance(item, AqlTargetItem):
                schema = target_item_schema
            else:
                raise ValueError("Wrong item type")
            result.append(schema.dump(item))
        return result

    @staticmethod
    def deserialize_item(value: dict):
        result = list()
        for item_dict in value:
            item_type_str = item_dict.get("type")
            if item_type_str is None:
                raise ValidationError("Item缺少类型，无法序列化")
            item_type: AqlItemType = AqlItemType(item_type_str)
            if item_type == AqlItemType.GROUP:
                schema = AqlGroupItemSchema()
            else:
                schema = AqlTargetItemSchema()
            item = schema.load(item_dict)
            result.append(item)
        return result

    @post_load
    def make_obj(self, data: dict, **kwargs):
        logical_group: AqlLogicalGroup = AqlLogicalGroup()
        logical_group.operand = data["operand"]
        logical_group.items = data["items"]
        logical_group.not_boolean = data["not_boolean"]
        return logical_group


class AqlLogicalGroupQuerySchema(Schema):
    aql = fields.String(required=False, allow_none=True)
    logical_group = fields.Nested(
        AqlLogicalGroupSchema,
        required=False,
        data_key="group",
        attribute="logical_group",
        allow_none=True,
    )

    @post_load
    def make_obj(self, data: dict, **kwargs):
        query: AqlLogicQuery = AqlLogicQuery()
        query.aql = data.get("aql")
        query.logical_group = data.get("logical_group")
        return query


class AsqlFieldLogicalGroupQuerySchema(Schema):
    logical_group = fields.Nested(
        AqlLogicalGroupSchema,
        required=True,
        data_key="group",
        attribute="logical_group",
        allow_none=True,
    )

    @post_load
    def make_obj(self, data: Dict, **kwargs):
        query: AsqlFieldLogicQuery = AsqlFieldLogicQuery()
        query.logical_group = data["logical_group"]
        return query
