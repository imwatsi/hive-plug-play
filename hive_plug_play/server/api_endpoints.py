"""API endpoints."""

from hive_plug_play.server.system_status import SystemStatus
from hive_plug_play.server.normalize import normalize_types

async def ping(context):
    return "pong"

async def get_sync_status(context):
    return normalize_types(SystemStatus.get_sync_status())

async def get_ops_by_block(context, block_num):
    """Returns a list of ops within the specified block number."""
    db = context['db']
    status = SystemStatus.get_sync_status()
    if not status: return [] # TODO: error handling/reporting
    latest = status['latest_block']
    if block_num > latest: return []
    return db.get_ops_by_block(block_num)
