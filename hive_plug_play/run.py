import os
from threading import Thread


from hive_plug_play.config import Config
from hive_plug_play.database.handlers import PlugPlayDb
from hive_plug_play.database.setup import DbSetup
from hive_plug_play.engine.processor import BlockProcessor
from hive_plug_play.hive.blocks import BlockStream
from hive_plug_play.hive.server_requests import make_request
from hive_plug_play.server.serve import run_server
from hive_plug_play.utils.tools import START_BLOCK

config = Config.config


def read_block_direct(block_num):
    resp = make_request("block_api.get_block", {"block_num": block_num})
    block = resp['block']
    return block

def do_fork_check(db):
    db_head = db.get_db_head()
    if not db_head: return None
    db_block_num = db_head[0]
    db_block_hash = db_head[1]
    next_block = read_block_direct(db_block_num + 1)
    if next_block['previous'] == db_block_hash:
        print("DB fork check passed")
        return db_head
    else:
        print(f"DB fork detected. Shutting down")
        os._exit(1) # TODO: safe shut down feature

def start_sync_service(config):
    print("Sync service running")
    db = PlugPlayDb(config)
    db_head = do_fork_check(db)
    if not db_head:
        stream = BlockStream(START_BLOCK)
    else:
        block_num = db_head[0] + 1
        stream = BlockStream(block_num)

def run():
    print("---   Hive Plug & Play started   ---")
    DbSetup.check_db(config)
    BlockProcessor.init(config)
    Thread(target=start_sync_service, args=(config,)).start()
    run_server(config)


if __name__ == "__main__":
    run()