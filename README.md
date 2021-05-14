# Hive Plug & Play

**Customizable block streaming and parsing microservice for custom_json ops on Hive.**


## Documentation

- [API Documentation](/docs/api/api.md)

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

Hive Plug & Play looks for a `config.ini` file in `/etc/hive-plug-play` by default. To set a custom folder, use an environment variable: `export PLUG_PLAY_HOME=/home/ubuntu/.config/hive-plug-play`.

```
db_username=postgres
db_password=password
server_host=127.0.0.1
server_port=8080
ssl_cert=
ssl_key=
start_block=53877365
op_ids=["community","notify"]
```

**Run:**

*From command:*

`hive_plug_play`

*Or from dir:*

- `cd hive_plug_play`
- `python3 run.py`
