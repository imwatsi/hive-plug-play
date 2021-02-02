from hive_plug_play.database.handlers import PlugPlayDb

class BlockProcessor:

    @classmethod
    def init(cls, config):
        cls.db = PlugPlayDb(config)
        cls.head_block = {}
        cls.block_num = 0
        cls.block_time = ''
    
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
                    cls.db.add_op(block_num, block['transaction_ids'][i], op['value'])
        cls.db._save()
        cls.block_num = block_num
        cls.block_time = timestamp