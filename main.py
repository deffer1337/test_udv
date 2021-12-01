import os
from contextvars import ContextVar

from aiohttp import web
from aioredis import create_redis_pool

from converter_currency.routes import create_routes

redis_connection = ContextVar('redis_connection')


async def on_cleanup(app):
    redis_conn = redis_connection.get()
    redis_conn.close()
    await redis_conn.wait_closed()


async def init():
    redis_conn = await create_redis_pool(os.getenv('ADDRESS'))
    redis_connection.set(redis_conn)
    routes = create_routes(redis_connection.get())
    app = web.Application()
    app.add_routes(routes)
    app.on_cleanup.append(on_cleanup)
    return app


if __name__ == '__main__':
    web.run_app(init())
