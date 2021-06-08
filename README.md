# Hive Plug & Play

**Customizable block streaming and parsing microservice for custom_json ops on Hive.**


## Documentation

- [Hive Plug & Play API Documentation](/docs/api/api.md)

## Development

### Dependencies:
- Python 3.6 required
- PostgreSQL 10+<br/>

**Install depencencies**<br/>
- Python3 and PostgreSQL : 
```
sudo apt install python3 python3-pip postgresql
```

### Configure PostgreSQL:
- Configure postgresql for remote [Authentication]
  - Update the file [pg_hba.conf](https://stackoverflow.com/a/18664239)
- **OR** <br/>For default postgres installs on localhost, at a minimum **CHANGE THE PASSWORD!**
  a) Update the password for the Linux postgresql User acount 
    ```
    sudo passwd postgres
    ```
  b) change to the postgres user
    ```
    sudo -i -u postgres
    ```    
  c) start the postgresql database/service
    ```
    sudo systemctl start postgresql
    psql # Launch posgresql cli
    ```
  d) change the password in postgresql
    ```
    \password
    \q 
    ```
### Restart the PosgreSQL service
    ```
    exit # quit to linux original user account
    sudo systemctl stop postgresql
    sudo systemctl start postgresql
    # Check status with 
    sudo systemctl status postgresql
    ```
### Create empty database 
  ```
  sudo -i -u postgres
  psql # Launch posgresql cli
  ```
  ```
  CREATE DATABASE plug_play;
  GRANT ALL PRIVILEGES ON DATABASE plug_play TO postgres;
  # Verify database was created with list
  \l 
  # Exit postgresql cli
  \q
  ```

### Configure Hive Plug & Play
In terminal login to your postgres account `sudo -i -u postgres` 

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

### Configure data collection for a specific project
**Note** The following are some examples of know op_ids per project, this list is not all inclusive, and is likely missing ids for the projects listed, additional fields are required to be reviewed to get the correct project.

|Project Name| op_ids |
|----------------|-------------|
| [reblog post](https://developers.hive.io/tutorials-python/reblogging_post.html) | reblog |
| [podping](https://podping.cloud/) [earliest valid block:54000984](https://hiveblocks.com/tx/f8aa1880e913efe50c954675f8575f9f363a10d0) | podping,hive-hydra |
| [3speak](https://3speak.co/) | 3speak-publish |
| [actifit](https://actifit.io/) | actifit |
| [peakd](https://peakd.com/) | peakd_notify |
| DCity | dcity, dcity-bg-save, dcitystats |
| [splinderlands](https://splinterlands.com/) | sm_accept_challenge,	sm_add_wallet,	sm_advance_league,	sm_burn_cards,	sm_cancel_match,	sm_cancel_sell,	sm_card_update,	sm_claim_airdrop,	sm_claim_reward,	sm_combine_all,	sm_combine_cards,	sm_create_tournament,	sm_decline_challenge,	sm_delegate_cards,	sm_edit_guild,	sm_enter_tournament,	sm_external_payment,	sm_find_match,	sm_gift_cards,	sm_gift_packs,	sm_guild_accept,	sm_guild_brawl_settings,	sm_guild_contribution,	sm_guild_decline,	sm_guild_invite,	sm_guild_promote,	sm_guild_remove,	sm_join_guild,	sm_leave_guild,	sm_leave_tournament,	sm_lock_assets,	sm_market_purchase,	sm_open_all,	sm_open_pack,	sm_price_feed,	sm_purchase,	sm_purchase_dice,	sm_purchase_land,	sm_purchase_skin_set,	sm_refresh_quest,	sm_sell_cards,	sm_set_authority,	sm_start_match,	sm_start_quest,	sm_submit_team,	sm_surrender,	sm_team_reveal,	sm_token_award,	sm_token_transfer,	sm_undelegate_cards,	sm_unlock_assets,	sm_update_authority,	sm_update_price,	sm_upgrade_account |
| CBM | cbm__backpack__drink_beer,	cbm__balance__deposit,	cbm__building__rent,	cbm__building__restore_condition,	cbm__craft__claim,	cbm__craft__finish_now,	cbm__craft__start,	cbm__daily_quests__claim,	cbm__daily_quests__finish_now,	cbm__daily_quests__start,	cbm__enhancer__claim,	cbm__enhancer__start,	cbm__market__completed_purchase,	cbm__market__completed_sale,	cbm__market__placed_a_sell_order,	cbm__pub__drink_beer,	cbm__pub__sold_beer,	cbm__referral__claim |
| many more exist | (hundreds) |

### Installation:
- Install as a python package from directory (wherever it is)
  ```
  cd /data/hive-plug-play
  pip3 install -e .
  ```
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
