import copy


def merge_query(records):
    new_records = copy.deepcopy(records)

    if len(records) < 2:
        return records

    result = new_records.pop()

    while new_records:
        tmp_result = new_records.pop()

        merged_flag, result = _merge(result, tmp_result)

        if not merged_flag:
            return records
    return [result]


def _merge(src_dict, dst_dict):
    result = {}

    src_keys = src_dict.keys()
    dst_keys = dst_dict.keys()

    if src_keys - dst_keys or dst_keys - src_keys:
        return False, None

    for src_key, src_val in src_dict.items():
        dst_val = dst_dict.get(src_key)

        if not isinstance(src_val, (dict, list)):
            result[src_key] = src_val
            continue

        if isinstance(src_val, list):
            result[src_key] = src_val + dst_val
            continue
        if isinstance(src_val, dict):
            sub_flag, sub_result = _merge(src_val, dst_val)
            if not sub_flag:
                return sub_flag, None
            result[src_key] = sub_result
            continue

        if src_val != dst_val:
            return False, None
        result[src_key] = src_val

    return True, result
