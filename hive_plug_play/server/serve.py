import ssl
from datetime import datetime
from aiohttp import web
from jsonrpcserver import method, async_dispatch as dispatch
from jsonrpcserver.methods import Methods
from hive_plug_play.database.handlers import PlugPlayDb
from hive_plug_play.server import api_endpoints
from hive_plug_play.server.system_status import SystemStatus
from hive_plug_play.server.normalize import normalize_types
from hive_plug_play.server.plug_endpoints import community, follow

def build_methods():
    methods = Methods()
    methods.add(**{'plug_play_api.' + method.__name__: method for method in (
        api_endpoints.ping,
        api_endpoints.get_sync_status,
        api_endpoints.get_ops_by_block
    )})
    methods.add(**{'plug_play_api.community.' + method.__name__: method for method  in (
        community.get_subscribe_ops,
        community.get_unsubscribe_ops,
        community.get_flag_post_ops
    )})
    methods.add(**{'plug_play_api.follow.' + method.__name__: method for method  in (
        follow.get_follow_ops,
        follow.get_reblog_ops
    )})

    return methods


def run_server(config):
    app = web.Application()
    app['db'] = PlugPlayDb(config)
    all_methods = build_methods()

    async def status_report(request):
        report = {
            'name': 'Hive Plug & Play',
            'sync': normalize_types(SystemStatus.get_sync_status()),
            'timestamp': datetime.utcnow().isoformat()
        }
        return web.json_response(status=200, data=report)
    
    async def handler(request):
        request = await request.text()
        response = await dispatch(request, methods=all_methods, debug=True, context=app)
        if response.wanted:
            return web.json_response(response.deserialized(), status=response.http_status)
        else:
            return web.Response()

    app.router.add_post("/", handler)
    app.router.add_get("/", status_report)
    if config['ssl_cert'] != '' and config['ssl_key'] != '':
        context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)
        context.load_cert_chain(
                config['ssl_cert'],
                config['ssl_key']
        )
    else:
        context = None
    web.run_app(
        app,
        host=config['server_host'],
        port=config['server_port'],
        ssl_context=context
    )