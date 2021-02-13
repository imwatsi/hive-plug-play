# Hive Plug & Play [ALPHA]

**Customizable block streaming and parsing microservice for custom_json ops on Hive.**

*Warning: this project is still under heavy development. It is not yet suitable for building production apps with.*

## Documentation

- [API Documentation](/docs/api.md)

## Development

- Python 3.6 required
- PostgreSQL 10+

**Dependencies:**

- Ubuntu: `sudo apt install python3 python3-pip`

**Installation:**

- Clone the repo
- `cd hive-plug-play`
- `pip3 install -e .`

**Configuration:**

Currently, the config is loaded from a `config.dat` file, which needs to be in the `hive-plug-play/hive_plug_play` root folder. A new config handling method will be released in the near future. Here's a sample config, for running a local node:

```
db_username=postgres
db_password=password
server_host=127.0.0.1
server_port=8080
ssl_cert=
ssl_key=
```

**Run:**

*From command:*

`hive_plug_play`

*Or from dir:*

- `cd hive_plug_play`
- `python3 run.py`

The node does not currently sync from the first block. It syncs from block `51250000` to aid the iterative stage of development it's in.