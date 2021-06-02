# Hive Plug & Play

**Customizable block streaming and parsing microservice for custom_json ops on Hive.**


## Documentation

- [API Documentation](/docs/api/api.md)

## Development

- Python 3.6 required
- PostgreSQL 10+

**Dependencies:**
Ubuntu Examples:
- Python3 : `sudo apt install python3 python3-pip`
- PostgreSQL (install one of):

| Local Server  | Client Only (Remote server) |
| ------------- | ------------- |
| ```sudo apt install postgresql-all```  | ```sudo apt install postgresql```  |

**Configuration:**

Prior to installation build the `config.ini` file: 

1) Hive Plug & Play requires a `config.ini` file to exist in either:
  - Default file location of `/etc/hive-plug-play` 
  - Or use any custom folder by setting an environment variable: `export PLUG_PLAY_HOME=~/.config/hive-plug-play`.

1) Build the file directory:
```
mkdir -p ~/.config/hive-plug-play
```
1) Create the `config.ini` file 
  - Any editor should do...):
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
 - TLDR ::: here is a one-liner from the terminal, that creates the `config.ini` file, sets the environment variable and opens nano to edit. ({ctl}+s to save and {ctl}+x to close)
```
echo $'db_username=postgres\ndb_password=password\nserver_host=127.0.0.1\nssl_cert=\nssl_key=\nstart_block=53877365\nop_ids=["community","notify"]' > ~/.config/hive-plug-play/config.ini && export PLUG_PLAY_HOME=~/.config/hive-plug-play && nano ~/.config/hive-plug-play/config.ini
```

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
