from hive_plug_play.server.system_status import SystemStatus

class SearchOps:

    @classmethod
    def subscribe(cls, community, block_range=None):
        """
            "subscribe"    | {"community":"hive-178179"}
        """
        if block_range is None:
            latest = SystemStatus.get_latest_block()
            if not latest: return None # TODO: notify??
            block_range = [latest - 28800, latest]
        query = f"""
            SELECT *  
            FROM (
                SELECT req_posting_auths [1]
                FROM custom_json_ops
                WHERE op_id = 'community'
                    AND (op_json -> 0)::text = '"subscribe"'
                    AND block_num BETWEEN {block_range[0]} and {block_range[1]} 
            )AS subscribe_ops;
        """
        return query
    
    @classmethod
    def unsubscribe(cls, community, block_range=None):
        """
            :unsubscribe"  | {"community":"hive-152200"}
        """
        if block_range is None:
            latest = SystemStatus.get_latest_block()
            if not latest: return None # TODO: notify??
            block_range = [latest - 28800, latest]
        query = f"""
            SELECT *  
            FROM (
                SELECT req_posting_auths [1]
                FROM custom_json_ops
                WHERE op_id = 'community'
                    AND (op_json -> 0)::text = '"unsubscribe"'
                    AND block_num BETWEEN {block_range[0]} and {block_range[1]} 
            )AS unsubscribe_ops;
        """
        return query