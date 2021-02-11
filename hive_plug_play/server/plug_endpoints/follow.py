"""Plug endpoints for community ops."""

from hive_plug_play.engine.plugs.follow import SearchOps
from hive_plug_play.server.system_status import SystemStatus
from hive_plug_play.server.normalize import populate_by_schema

async def get_follow_ops(context, follower=None, followed=None,  block_range=None):
    """Returns a list of global follow ops within the specified block or time range."""
    db = context['db']
    sql = SearchOps.follow(
        follower_account=follower,
        followed_account=followed,
        block_range=block_range
    )
    result = []
    if sql:
        res = db.db.select(sql)
        for entry in res:
            result.append(populate_by_schema(
                entry, ['acc_auths', 'following', 'follower']
            ))
    return result

async def get_reblog_ops(context, reblog_account=None, author=None, permlink=None, block_range=None):
    """Returns a list of global reblog ops within the specified block or time range."""
    db = context['db']
    sql = SearchOps.reblog(
        reblog_account=reblog_account,
        blog_author=author,
        blog_permlink=permlink,
        block_range=block_range
    )
    result = []
    if sql:
        res = db.db.select(sql)
        for entry in res:
            result.append(populate_by_schema(
                entry, ['acc_auths', 'account', 'author', 'permlink']
            ))
    return result