# Hive Plug & Play [ALPHA]

**Customizable block streaming and parsing microservice for custom_json ops on Hive.**

*Warning: this project is still under heavy development. It is not yet suitable for buidling production apps with.*

## Development

- Python 3.6 required
- PostgreSQL 10+

**Dependencies:**

- Ubuntu: `sudo apt install python3 python3-pip`

**Installation:**

- Clone the repo
- `cd hive-plug-play`
- `pip3 install -e .`

**Run:**

*From command:*

`hive_plug_play`

*Or from dir:*

- `cd hive_plug_play`
- `python3 run.py`

The node does not currently sync from the first block. It syncs from block `50924300` to aid the iterative stage of development it's in.