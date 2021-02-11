from hive_plug_play.server.system_status import SystemStatus

class SearchOps:

    @classmethod
    def follow(cls, follower_account=None, followed_account=None, block_range=None):
        """
            "follow" | {"follower":"idwritershive","following":"olgavita","what":["blog"]}
        """
        if block_range is None:
            latest = SystemStatus.get_latest_block()
            if not latest: return None # TODO: notify??
            block_range = [latest - 28800, latest]
        query = f"""
            SELECT *  
            FROM (
                SELECT req_posting_auths,
                    op_json -> 1 -> 'following'::text,
                    op_json -> 1 -> 'follower'::text,
                    op_json -> 1 -> 'what'
                FROM custom_json_ops
                WHERE op_id = 'follow'
                    AND (op_json -> 0)::text = '"follow"'
                    AND block_num BETWEEN {block_range[0]} and {block_range[1]}
        """
        if follower_account:
            query += f"""
            AND (op_json -> 1 -> 'follower'):: text = '"{follower_account}"'
            """
        if followed_account:
            query += f"""
            AND (op_json -> 1 -> 'following'):: text = '"{followed_account}"'
            """
        query += ")AS follow_ops;"

        return query
    
    @classmethod
    def reblog(cls, reblog_account=None, blog_author=None, blog_permlink=None, block_range=None):
        """
            "reblog" | {
                "account":"nataly2317",
                "author":"coininstant",
                "permlink":"it-s-time-to-buy-sats-satoshin-token-on-uniswap-to-the-moon"
            }
        """
        if block_range is None:
            latest = SystemStatus.get_latest_block()
            if not latest: return None # TODO: notify??
            block_range = [latest - 28800, latest]
        query = f"""
            SELECT *  
            FROM (
                SELECT req_posting_auths,
                    op_json -> 1 -> 'account'::text,
                    op_json -> 1 -> 'author'::text,
                    op_json -> 1 -> 'permlink'::text
                FROM custom_json_ops
                WHERE op_id = 'follow'
                    AND (op_json -> 0)::text = '"reblog"'
                    AND block_num BETWEEN {block_range[0]} and {block_range[1]}
        """
        if reblog_account:
            query += f"""
            AND (op_json -> 1 -> 'account'):: text = '"{reblog_account}"'
            """
        if blog_author:
            query += f"""
            AND (op_json -> 1 -> 'author'):: text = '"{blog_author}"'
            """
        if blog_permlink:
            query += f"""
            AND (op_json -> 1 -> 'blog_permlink'):: text = '"{blog_permlink}"'
            """
        query += ")AS reblog_ops;"

        return query