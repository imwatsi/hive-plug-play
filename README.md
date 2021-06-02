# Hive Plug & Play

**Customizable block streaming and parsing microservice for custom_json ops on Hive.**


## Documentation

- [Hive Plug & Play API Documentation](/docs/api/api.md)

## Development

### Dependencies:
- Python 3.6 required
- PostgreSQL 10+<br/>

**Install depencencies**<br/>
- Python3 : `sudo apt install python3 python3-pip`
- PostgreSQL, install with either:

| Local Server  | Client Only (Remote server) |
| ------------- | ------------- |
| ```sudo apt install postgresql-all```  | ```sudo apt install postgresql```  |

### Configure PostgreSQL:
- Configure postgresql for remote [Authentication]
  - Update the file [pg_hba.conf](https://stackoverflow.com/a/18664239)
- **OR** <br/>For default postgres installs on localhost, at a minimum **CHANGE THE PASSWORD!**
  1. Update the password for the posgres database user
  ```
  sudo -i -u postgres
  ```
  ```
  \password
  ```
  2. Update the password for the Linux User acount with the same postgresql password `sudo passwd postgres`
- Back in terminal (`\q` to leave psql prompt) restart the PosgreSQL service
  ```
  sudo systemctl stop postgresql
  sudo systemctl start postgresql
  ```
  Check status with `sudo systemctl status postgresql`

- Create empty database, open postgresql 
  ```
  sudo -i -u postgres
  ```
  Create datbase, and setup permissions
  ```
  CREATE DATABASE plug_play;
  GRANT ALL PRIVILEGES ON DATABASE plug_play TO postgres;
  ```
  Verify database was created with `\l`

### Configure Hive Plug & Play
Change user to your postgres account `su postgres` (this shouldn't be required if authenticating via certificate)

**TLDR** build `config.ini` file:
This one-liner from the terminal creates the required `config.ini` file, sets the environment variable and opens nano to edit. <br/>Make your updates then use <kbd>ctl</kbd>+<kbd>s</kbd> to save and <kbd>ctl</kbd>+<kbd>x</kbd> to close.
```
mkdir -p ~/.config/hive-plug-play && export PLUG_PLAY_HOME=~/.config/hive-plug-play && ([ -f ~/.config/hive-plug-play/config.ini ] || echo $'db_username=postgres\ndb_password=password\nserver_host=127.0.0.1\nserver_port=5432\nssl_cert=\nssl_key=\nstart_block=54000984\nop_ids=["podping","hive-hydra"]' > ~/.config/hive-plug-play/config.ini) && nano ~/.config/hive-plug-play/config.ini
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
  server_port=5432
  ssl_cert=
  ssl_key=
  start_block=54000984
  op_ids=["community","notify"]
  ```

### Configure data collection for a specific project or application
Project specific op_ids

|Project Name| Value |
|----------------|-------------|
| [podping](podping.cloud) | podping,hive-hydra |
| 3speak | 3speak-publish |
| actifit | actifit |
| DCity | dcity, dcity-bg-save, dcitystats |
| peakd | peakd_notify |
| reblog | reblog |
| CBM | cbm__backpack__drink_beer,	cbm__balance__deposit,	cbm__building__rent,	cbm__building__restore_condition,	cbm__craft__claim,	cbm__craft__finish_now,	cbm__craft__start,	cbm__daily_quests__claim,	cbm__daily_quests__finish_now,	cbm__daily_quests__start,	cbm__enhancer__claim,	cbm__enhancer__start,	cbm__market__completed_purchase,	cbm__market__completed_sale,	cbm__market__placed_a_sell_order,	cbm__pub__drink_beer,	cbm__pub__sold_beer,	cbm__referral__claim |
| many more exist | (hundreds) |

Podping specific op_ids are `op_ids=["podping","hive-hydra"]`

### Installation:

- Clone the repo
- `cd hive-plug-play`
- `pip3 install -e .`
### Optionally install with
- `sudo python3 setup.py install`

### Run:

*From command:*
Change user to your postgres account `su postgres` (this shouldn't be required if authenticating via certificate)
`hive_plug_play`

*Or from dir:*

- `cd hive_plug_play`
- `python3 run.py`

### Resource Links (Developer documentation)
- [hive.io](https://developers.hive.io/)
- [postgresql](https://www.postgresql.org/docs/)
- [python3](https://docs.python.org/3/)
