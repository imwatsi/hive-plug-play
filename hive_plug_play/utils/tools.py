import json

HIVE_NODES = [
    "https://api.hive.blog", "https://anyx.io", "https://api.openhive.network",
    "https://hive.roelandp.nl", "https://rpc.ausbit.dev", "https://api.pharesim.me",
    "https://api.deathwing.me"
]
START_BLOCK = 51250000

UTC_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"

def check_required_keys(required, provided_keys, op_context):
    missing = []
    for k in required:
        if k not in provided_keys:
            missing.append(k)
    assert len(missing) == 0, f"missing keys for {op_context}: {missing}"

def check_allowed_keys(allowed, provided_keys, op_context):
    unsupported = []
    for k in provided_keys:
        if k not in allowed:
            unsupported.append(k)
    assert len(unsupported) == 0, f"unsupported keys provided for {op_context}: {unsupported}"

def get_cleaned_dict(og_values, keys, keep=False):
    result = {}
    for k in og_values:
        if (k in keys) == keep:
            result[k] = og_values[k]
    return result