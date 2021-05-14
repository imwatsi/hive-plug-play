from os import truncate
from hive_plug_play.database.handlers import PlugPlayDb

class BlockProcessor:

    @classmethod
    def init(cls, config):
        cls.config = config
        cls.db = PlugPlayDb(config)
        cls.head_block = {}
        cls.block_num = 0
        cls.block_time = ''
    
    @classmethod
    def check_op_id(cls, op_id):
        allowed_op_ids = cls.config['op_ids']
        if allowed_op_ids == []:
            return True
        else:
            return op_id in allowed_op_ids
    
    @classmethod
    def process_block(cls, block_num, block):
        prev = block['previous']
        block_hash = block['block_id']
        timestamp = block['timestamp']

        cls.db.add_block(block_num, block_hash, prev, timestamp)
        transactions = block['transactions']
        for i in range(len(transactions)):
            trans = transactions[i]
            for op in trans['operations']:
                if op['type'] == 'custom_json_operation':
                    if cls.check_op_id(op['value']['id']):
                        cls.db.add_op(block_num, block['transaction_ids'][i], op['value'])
        cls.db._save()
        cls.block_num = block_num
        cls.block_time = timestamp