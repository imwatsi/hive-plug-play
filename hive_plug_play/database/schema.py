
DB_VERSION = 2

class DbSchema:
    def __init__(self):
        self.tables = {}
        self.indexes = {}
        self.views = {}
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

    def _create_views(self):

        podping_url_view =  """
            -- View: public.podping_urls

            -- DROP VIEW public.podping_urls;

            CREATE OR REPLACE VIEW public.podping_urls
            AS
            SELECT jo.id AS json_ops_id,
                json_array_elements_text((jo.op_json ->> 'urls'::text)::json) AS url
            FROM custom_json_ops jo;

            ALTER TABLE public.podping_urls
                OWNER TO postgres;
            COMMENT ON VIEW public.podping_urls
                IS 'expands all custom json arrays labled as ''urls'' to individual url elements';

            GRANT ALL ON TABLE public.podping_urls TO postgres;
            GRANT SELECT ON TABLE public.podping_urls TO PUBLIC;
        """
        self.indexes['podping_url'] = podping_url_view

        podping_url_timestamp="""
            -- View: public.podping_url_timestamp

            -- DROP VIEW public.podping_url_timestamp;

            CREATE OR REPLACE VIEW public.podping_url_timestamp
            AS
            SELECT b."timestamp",
                p.url,
                regexp_replace("substring"(p.url, '.*://([^/]*)'::text), '^www\.?'::text, ''::text) AS host
            FROM blocks b,
                custom_json_ops c,
                podping_urls p
            WHERE b.num = c.block_num AND c.id = p.json_ops_id;

            ALTER TABLE public.podping_url_timestamp
                OWNER TO postgres;

            GRANT ALL ON TABLE public.podping_url_timestamp TO postgres;
            GRANT SELECT ON TABLE public.podping_url_timestamp TO PUBLIC;
        """
        self.indexes['podping_url_timestamp']=podping_url_timestamp

        podping_host_summary = """
            -- View: public.podping_host_summary

            -- DROP VIEW public.podping_host_summary;

            CREATE OR REPLACE VIEW public.podping_host_summary
            AS
            SELECT DISTINCT p.host,
                count(p.host) AS count
            FROM podping_url_timestamp p
            WHERE p.host <> ''::text
            GROUP BY p.host
            ORDER BY (count(p.host)) DESC;

            ALTER TABLE public.podping_host_summary
                OWNER TO postgres;

            GRANT ALL ON TABLE public.podping_host_summary TO postgres;
            GRANT SELECT ON TABLE public.podping_host_summary TO pg_execute_server_program;
            """
        self.indexes['podping_host_summary']=podping_host_summary
        podping_count_time_of_day = """
            -- View: public.podping_count_time_of_day

            -- DROP VIEW public.podping_count_time_of_day;

            CREATE OR REPLACE VIEW public.podping_count_time_of_day
            AS
            SELECT DISTINCT date_part('hour'::text, p."timestamp") AS date_part,
                count(p."timestamp") AS count
            FROM podping_url_timestamp p
            GROUP BY (date_part('hour'::text, p."timestamp"))
            ORDER BY (date_part('hour'::text, p."timestamp"));

            ALTER TABLE public.podping_count_time_of_day
                OWNER TO postgres;
        """
        self.indexes['podping_count_time_of_day']=podping_count_time_of_day
