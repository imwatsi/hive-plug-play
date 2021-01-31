import os

import psycopg2

from hive_plug_play.database.schema import DbSchema, DB_VERSION


class DbSession:
    def __init__(self, config):
        # TODO: retrieve from env_variables
        self.conn = psycopg2.connect(f"dbname=plug_play user={config['db_username']} password={config['db_password']}")
        self.conn.autocommit = False
        self.cur = self.conn.cursor()
        self._schema = DbSchema()
        self.live_schema = {}
        self.get_schema()
    
    def select(self, sql):
        self.cur.execute(sql)
        res = self.cur.fetchall()
        if len(res) == 0:
            return None
        else:
            return res
    
    def execute_immediate(self, sql,  data):
        self.cur.execute(sql, data)
        self.conn.commit()
    
    def execute(self, sql, data):
        try:
            self.cur.execute(sql, data)
        except Exception as e:
            print(e)
            print(f"SQL:  {sql}")
            self.conn.rollback()
            raise Exception ('DB error occurred')
    
    def commit(self):
        self.conn.commit()
    
    def get_schema(self):
        for table in self._schema.tables:
            self.cur.execute(f"SELECT * FROM {table} LIMIT 0")
            colnames = [desc[0] for desc in self.cur.description]
            self.live_schema[table] = colnames


class DbSetup:

    @classmethod
    def check_db(cls, config):
        # check if it exists
        try:
            # TODO: retrieve authentication from config 
            cls.conn = psycopg2.connect(f"dbname=plug_play user={config['db_username']} password={config['db_password']}")
        except psycopg2.OperationalError as e:
            if "plug_play" in e.args[0] and "does not exist" in e.args[0]:
                print("No database found. Please create a 'plug_play' database in PostgreSQL.")
                os._exit(1)
            else:
                print(e)
                os._exit(1)
        # check global props
        cls.cur = cls.conn.cursor()
        current_version = cls._check_global_props()
        if current_version:
            if DB_VERSION != current_version:
                cls._migrate(cls.cur, current_version)
        else:
            schema = DbSchema()
            cls._build_db(schema)
            cls._set_version(DB_VERSION)
        cls.cur.close()
        cls.conn.close()

    @classmethod
    def _check_global_props(cls):
        sql = f"SELECT * FROM global_props;"
        try:
            cls.cur.execute(sql)
            _has_g_props = cls.cur.fetchone()
            return _has_g_props[0] if _has_g_props else False
        except psycopg2.Error as e:
            if e.pgcode == '42P01':
                cls.conn.rollback()
                return False
            else:
                print(e)
                os._exit(1)
            
    @classmethod
    def _set_version(cls, version):
        # set version
        sql = f"""INSERT INTO global_props (db_version)
                VALUES ({version})"""
        cls.cur.execute(sql)
        cls.conn.commit()

    @classmethod
    def _build_db(cls, schema):
        # create tables
        for table in schema.tables:
            print(f'Creating table: {table}... ', end='')
            sql_stat = schema.tables[table]
            cls.cur.execute(sql_stat)
            print('done')
        print('DB build complete.')
        cls.conn.commit()
    
    @classmethod
    def _migrate(cls, db_conn, current_version):
        pass # TODO migration