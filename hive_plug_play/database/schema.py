
DB_VERSION = 1

class DbSchema:
    def __init__(self):
        self.tables = {}
        self.indexes = {}
        self._populate_tables()

    def _populate_tables(self):
        # blocks table
        blocks = """
            CREATE TABLE IF NOT EXISTS blocks (
                num integer PRIMARY KEY,
                hash char(40) NOT NULL,
                prev char(40),
                timestamp timestamp NOT NULL
            );"""
        self.tables['blocks'] = blocks

        custom_json_ops = """
            CREATE TABLE IF NOT EXISTS custom_json_ops (
                id serial PRIMARY KEY,
                block_num integer NOT NULL REFERENCES blocks (num),
                transaction_id char(40) NOT NULL,
                req_auths varchar(16)[],
                req_posting_auths varchar(16)[],
                op_id varchar(128) NOT NULL,
                op_json json NOT NULL
            );"""
        self.tables['custom_json_ops'] = custom_json_ops

        global_props = """
            CREATE TABLE IF NOT EXISTS global_props (
                db_version smallint
            );"""
        self.tables['global_props'] = global_props

    def _create_indexes(self):
        blocks_ix_num = """
            CREATE INDEX blocks_ix_num
            ON blocks (num)
        ;"""
        self.indexes['blocks_ix_num'] = blocks_ix_num

        custom_json_ops_ix_block_num = """
            CREATE INDEX custom_json_ops_ix_block_num
            ON custom_json_ops (block_num)
        ;"""
        self.indexes['custom_json_ops_ix_block_num'] = custom_json_ops_ix_block_num
