"""Plug endpoints for community ops."""

from hive_plug_play.engine.plugs.community import SearchOps
from hive_plug_play.server.system_status import SystemStatus
from hive_plug_play.server.normalize import populate_by_schema

async def get_subscribe_ops(context, community, block_range=None):
    """Returns a list of community subscribe ops within the specified block."""
    db = context['db']
    sql = SearchOps.subscribe(community, block_range=block_range)
    result = []
    if sql:
        res = db.db.select(sql)
        for entry in res:
            result.append(populate_by_schema(
                entry, ['account']
            ))
    return result

async def get_unsubscribe_ops(context, community, block_range=None):
    """Returns a list of community unsubscribe ops within the speicified block range."""
    db = context['db']
    sql = SearchOps.unsubscribe(community, block_range=block_range)
    result = []
    if sql:
        res = db.db.select(sql)
        for entry in res:
            result.append(populate_by_schema(
                entry, ['account']
            ))
    return result