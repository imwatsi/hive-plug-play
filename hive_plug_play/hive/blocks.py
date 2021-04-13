import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from threading import Thread

from hive_plug_play.engine.processor import BlockProcessor
from hive_plug_play.hive.server_requests import make_request
from hive_plug_play.utils.tools import UTC_TIMESTAMP_FORMAT
from hive_plug_play.server.system_status import SystemStatus

BATCH_SIZE = 100
IRREVERSIBLE_GAP = 20
BLOCK_TIME_SECS = 3

class BlockStream:

    def __init__(self, start_block):
        self._start_block = start_block
        self._dynamic_global_props = {}
        self._buffer = {}
        self._cache = {}
        self._hive_head_block = None
        self._prev_hash = None
        Thread(target=self._start_stream).start()

    def _fetch_dynamic_global_props(self):
        props = make_request("condenser_api.get_dynamic_global_properties")
        self._hive_head_block = props['head_block_number']
        self._hive_block_time = datetime.strptime(props['time'], UTC_TIMESTAMP_FORMAT)
        self._irreversible_block = props['last_irreversible_block_num']
    
    def _fetch_block(self, block_num):
        while True:
            resp = make_request("block_api.get_block", {"block_num": block_num})
            if 'block' not in resp: continue
            block = resp['block']
            return [block_num, block]
    
    def _is_valid_block(self, num, block):
        if not self._prev_hash: return True # skip check for first block to be processed
        match = block['previous'] == self._prev_hash
        if match:
            return True
        else:
            print(f"Invalid block detected: {num}")
            return False
    
    def _fetch_multiple_blocks(self, start, end):
        """Retrieves blocks from `start` to `end`, inclusive."""
        print(f"\nFetching blocks: {start} to {end}")
        while True:
            upper = start + BATCH_SIZE if (end-start) > BATCH_SIZE else end
            blocks_expected = range(start, upper+1)
            timer_start = datetime.utcnow()
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = (executor.submit(self._fetch_block, block_num) for block_num in blocks_expected)
                for future in as_completed(futures):
                    res = future.result()
                    self._add_block_to_cache(res[0], res[1])
            timer_end = datetime.utcnow()
            remaining = end - upper
            timer_remaining = (((timer_end - timer_start).seconds)/ BATCH_SIZE) * remaining
            print(f"Remaining: {remaining} blocks  |  {str(timedelta(seconds=timer_remaining))}", end='\r')
            if remaining == 0: break
            start = upper
    
    def _add_block_to_cache(self, num, block):
        self._cache[num] = block

    def _wait_for_block(self, block_num):
        while True:
            self._fetch_dynamic_global_props()
            gap = self._hive_head_block - self._start_block
            if gap >= 0:
                return
            else:
                delay = abs(gap) * BLOCK_TIME_SECS
                print(f"Waiting for {delay} secs")
                time.sleep(delay)
    
    def is_behind_schedule(self):
        current_time = datetime.utcnow()
        if self._latest_block_time + timedelta(seconds=(BLOCK_TIME_SECS*3)) < current_time:
            return True
        else:
            return False
    
    def _prune_block(self, block_num):
        del self._cache[block_num]
    
    def _start_stream(self):
        self._fetch_dynamic_global_props()
        gap = self._hive_head_block - self._start_block
        if gap < 0:
            # a future block, wait
            self._wait_for_block(self._start_block)
            gap = self._hive_head_block - self._start_block
        print(f"DB is {gap} blocks behind.")
        Thread(target=self._feeder).start()
        self._fetch_multiple_blocks(self._start_block, self._hive_head_block)
        print("\nInitial blocks fetch complete.\n")
        time.sleep(5)
        Thread(target=self._streamer).start()

    def _streamer(self):
        # start the stream
        while True:
            current_time = datetime.utcnow()
            if current_time > self._latest_block_time + timedelta(seconds=(BLOCK_TIME_SECS*3)):
                next_block = self._latest_block + 1
                block = self._fetch_block(next_block)
                self._add_block_to_cache(next_block, block[1])
                SystemStatus.set_sync_status(
                    self._latest_block,
                    self._latest_block_time,
                    self.is_behind_schedule()
                )
            if (self._latest_block_time + timedelta(seconds=(BLOCK_TIME_SECS*6))) < current_time:
                # catchup if behind
                self._fetch_dynamic_global_props()
                self._fetch_multiple_blocks(
                    (self._latest_block + 1),
                    (self._hive_head_block)
                )
            time.sleep(0.3)
    
    def _feeder(self):
        block_to_push = self._start_block
        while True:
            while block_to_push not in self._cache:
                time.sleep(0.1)
            # check before pushing
            block = self._cache[block_to_push]
            if self._is_valid_block(block_to_push, block):
                self._prev_hash = block['block_id']
            else:
                print("Invalid block detected.")
                os._exit(1) # TODO: replace with standby
            BlockProcessor.process_block(block_to_push, self._cache[block_to_push])
            self._latest_block = block_to_push
            self._latest_block_time = datetime.strptime(
                block['timestamp'],
                UTC_TIMESTAMP_FORMAT
            )
            SystemStatus.set_sync_status(
                    self._latest_block,
                    self._latest_block_time,
                    self.is_behind_schedule()
            )
            self._prune_block(block_to_push)
            block_to_push += 1