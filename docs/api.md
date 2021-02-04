# API Documentation

## Standard endpoints

### ping

*Ping endpoint*

Example payload:

```
{
    "jsonrpc": "2.0",
    "method": "plug_play_api.ping",
    "id": 1
}
```

Example response:

```
{
    "jsonrpc": "2.0",
    "result": "pong",
    "id": 1
}
```

### get_sync_status

*Retrieves the node's sync status*

Example payload:

```
{
    "jsonrpc": "2.0",
    "method": "plug_play_api.get_sync_status",
    "id": 1
}
```

Example response:

```
{
    "jsonrpc": "2.0",
    "result": {
        "latest_block": 51044300,
        "latest_block_time": "2021-02-04T19:29:15",
        "behind": False
    },
    "id": 1
}
```

### get_ops_by_block

*Retrieves all custom_json ops within a specified block number*

```
{
    "jsonrpc": "2.0",
    "result": [
        {
            "req_auths": [],
            "req_posting_auths": ["gillianpearce"],
            "op_id": "sm_find_match",
            "op_json": {
                "match_type": "Ranked",
                "app": "steemmonsters/0.7.60"
            }
        }, 
        {
            "req_auths": [],
            "req_posting_auths": ["russia-btc"],
            "op_id": "sm_team_reveal",
            "op_json": {
                "trx_id": "444e927053d30eb0ddd43634ab91cd8a29b9d386",
                "summoner": "C1-5-58JL57PPV4",
                "monsters": [
                    "C3-82-0U3TJOKUKG",
                    "G3-247-SKY0PUZ9HC",
                    "C3-100-MSJKVG5LDC",
                    "C4-161-AXNW13MQTC",
                    "C4-197-18MERLDOFK",
                    "C3-131-0XHJ9UH3G0"
                ],
                "secret": "Cu41FYm29U",
                "app": "splinterlands/0.7.81"
            }
        },
        ...
    ],
    "id": 1
}
```

---

## Plugs

- [community](api/plugs/community.md): Hivemind communities protocol
