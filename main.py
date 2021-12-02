import os

from aiohttp import web
from aioredis import create_redis_pool

from converter_currency.routes import create_routes


async def on_cleanup(app):
    redis_conn = app['redis']
    redis_conn.close()
    await redis_conn.wait_closed()


async def init():
    redis_conn = await create_redis_pool(os.getenv('ADDRESS'))
    routes = create_routes(redis_conn)
    app = web.Application()
    app['redis'] = redis_conn
    app.add_routes(routes)
    app.on_cleanup.append(on_cleanup)
    return app


if __name__ == '__main__':
    web.run_app(init())
