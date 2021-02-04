import json

from hive_plug_play.database.setup import DbSession

class PlugPlayDb:
    """Avails method handlers for common DB operations and also exposes direct
       DB actions through `self.db.select`, `self.db.execute` and `self.db.execute_immediate`"""

    def __init__(self, config):
        self.db = DbSession(config)
        self.config = config
        self.schema = self.db.live_schema

    # TOOLS

    def _populate_by_schema(self, data, fields):
        result = {}
        for i in range(len(fields)):
            result[fields[i]] = data[i]
        return result


    # ACCESS METHODS

    def _select(self, table, columns=None, col_filters=None, order_by=None, limit=None):
        if columns:
            _columns = ', '.join(columns)
        else:
            _columns = "*"

        sql = f"SELECT {_columns} FROM {table}"

        if isinstance(col_filters, dict):
            _filters = []
            for col, value in col_filters.items():
                _filters.append (f"{col} = '{value}'")
            _final_filters = ' AND '.join(_filters)
            sql += f" WHERE {_final_filters}"
        elif isinstance(col_filters, str):
            sql += f" WHERE {col_filters}"
        if order_by:
            sql += f" ORDER BY {order_by}"
        if limit:
            sql += f" LIMIT {limit}"
        sql += ";"
        return self.db.select(sql)
    
    def _select_one(self, table, col_filters):
        sql = f"SELECT 1 FROM {table}"
        if isinstance(col_filters, dict):
            _filters = []
            for col, value in col_filters.items():
                _filters.append (f"{col} = '{value}'")
            _final_filters = ' AND '.join(_filters)
            sql += f" WHERE {_final_filters}"
        elif isinstance(col_filters, str):
            sql += f" WHERE {col_filters}"
        return bool(self.db.select(sql))

    def _insert(self, table, data):
        _columns = []
        _values = []
        for col in data:
            _columns.append(col)
            _values.append(f"%({col})s")
        columns = ', '.join(_columns)
        values = ', '.join(_values)
        sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        sql += ";"
        self.db.execute(sql, data)

    def _update(self, table, data, col_filters= {}):
        _values = []
        for col, value in data.items():
            if value is None: continue
            _values.append (f"{col} = %({col})s")
        _final_values = ', '.join(_values)

        sql = f"UPDATE {table} SET {_final_values}"

        if isinstance(col_filters, dict):
            _filters = []
            for col, value in col_filters.items():
                _filters.append (f"{col} = %(f_{col})s")
                data[f"f_{col}"] = col_filters[col]
            _final_filters = ' AND '.join(_filters)
            sql += f" WHERE {_final_filters}"
        sql += ";"
        self.db.execute(sql, data)
    
    def _delete(self, table, col_filters):
        sql = f"DELETE FROM {table}"
        if isinstance(col_filters, dict):
            _filters = []
            for col in col_filters:
                _filters.append (f"{col} = %({col}s")
            _final_filters = ' AND '.join(_filters)
            sql += f" WHERE {_final_filters}"
        elif isinstance(col_filters, str):
            sql += f" WHERE {col_filters}"
        sql += ";"
        self.db.execute(sql, col_filters)

    def _save(self):
        self.db.commit()

    # GLOBAL PROPS

    def get_db_head(self):
        res = self._select('blocks', ['num', 'hash'], order_by="num DESC", limit=1)
        if res:
            return res[0]
        else:
            return None

    def get_db_version(self):
        res = self._select('global_props', ['db_version'])
        return res[0]

    def has_global_props(self):
        res = self._select('global_props')
        if res:
            return True
        else:
            return False

    # BLOCKS

    def add_block(self, block_num, block_hash, prev, created_at):
        self._insert('blocks', {
            'num': block_num,
            'hash': block_hash,
            'prev': prev,
            'timestamp': created_at

        })

    def get_block_range(self, start_time, end_time):
        query = f"""
                    SELECT min(num), max(num) FROM blocks
                        WHERE timestamp BETWEEN {start_time} AND {end_time};
                """
        res = self.db.select(query)
        return res


    
    # CUSTOM JSON OPS

    def add_op(self, block_num, transaction_id, op):
        self._insert('custom_json_ops', {
            'block_num': block_num,
            'transaction_id': transaction_id,
            'req_auths': op['required_auths'],
            'req_posting_auths': op['required_posting_auths'],
            'op_id': op['id'],
            'op_json': op['json']
        })
    
    def get_ops_by_block(self, block_num):
        cols = ['req_auths', 'req_posting_auths', 'op_id', 'op_json']
        _res = self._select('custom_json_ops', columns=cols, col_filters={'block_num': block_num})
        if _res is None: return []
        result = []
        for r in _res:
            result.append(self._populate_by_schema(r, cols))
        return result