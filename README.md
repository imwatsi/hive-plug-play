# Hive Plug & Play

**Customizable block streaming and parsing microservice for custom_json ops on Hive.**


## Documentation

- [API Documentation](/docs/api/api.md)

## Development

- Python 3.6 required
- PostgreSQL 10+

### Dependencies:
Ubuntu Examples:
- Python3 : `sudo apt install python3 python3-pip`
- PostgreSQL (install one of):

| Local Server  | Client Only (Remote server) |
| ------------- | ------------- |
| ```sudo apt install postgresql-all```  | ```sudo apt install postgresql```  |

### Configuration:
-For default postgres installs **CHANGE THE PASSWORD!**
```
sudo -i -u postgres
```
then:
```
\password
```
follow password prompts

**TLDR** build `config.ini` file:
This one-liner from the terminal creates the required `config.ini` file, sets the environment variable and opens nano to edit. <br/>Make your updates then use <kbd>ctl</kbd>+<kbd>s</kbd> to save and <kbd>ctl</kbd>+<kbd>x</kbd> to close.
```
mkdir -p ~/.config/hive-plug-play && export PLUG_PLAY_HOME=~/.config/hive-plug-play && ([ -f ~/.config/hive-plug-play/config.ini ] || echo $'db_username=postgres\ndb_password=password\nserver_host=127.0.0.1\nserver_port=8080\nssl_cert=\nssl_key=\nstart_block=53877365\nop_ids=["community","notify"]' > ~/.config/hive-plug-play/config.ini) && nano ~/.config/hive-plug-play/config.ini
```

**OR** step by step build `config.ini` file:

1. Hive Plug & Play requires a `config.ini` file to exist in either:
  - Default file location of `/etc/hive-plug-play` 
  - Or use any custom folder by setting an environment variable: `export PLUG_PLAY_HOME=~/.config/hive-plug-play`.
2. Build the file directory:
```
mkdir -p ~/.config/hive-plug-play
```
3. Create the `config.ini` file 
  - Any text editor should do:
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

### Installation:

- Clone the repo
- `cd hive-plug-play`
- `pip3 install -e .`

### Run:

*From command:*

`hive_plug_play`

*Or from dir:*

- `cd hive_plug_play`
- `python3 run.py`

## Development Documentation

- [postgresql](https://www.postgresql.org/docs/)
- [python3](https://docs.python.org/3/)
- [hive.io](https://developers.hive.io/)
