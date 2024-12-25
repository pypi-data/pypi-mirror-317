import re
import traceback
import logging
from typing import Callable, Optional
from .config import settings

logger = logging.getLogger("ignite")

class Router:
    def __init__(self):
        self.routes = []

    def add_route(self, path: str, handler: Callable, methods=None):
        if methods is None:
            methods = ["GET"]
        self.routes.append({
            "path": re.compile(f"^{path}$"),
            "handler": handler,
            "methods": methods
        })

    def resolve(self, path: str, method: str) -> Optional[Callable]:
        for route in self.routes:
            if route["path"].match(path) and method in route["methods"]:
                return route["handler"]
        return None

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope["path"]
            method = scope["method"]

            try:
                handler = self.resolve(path, method)
                if handler:
                    response = await handler(scope, receive)
                    return await self._send_response(send, response)

                return await self._send_response(send, {
                    "status": 404,
                    "body": b"Not Found"
                })

            except Exception as e:
                logger.exception("Unhandled error in route")
                if settings.DEBUG:
                    tb_str = traceback.format_exc().encode("utf-8")
                    return await self._send_response(send, {
                        "status": 500,
                        "body": b"Internal Server Error\n" + tb_str
                    })
                else:
                    return await self._send_response(send, {
                        "status": 500,
                        "body": b"Internal Server Error"
                    })

        elif scope["type"] == "websocket":
            pass

    async def _send_response(self, send, response: dict):
        status = response.get("status", 200)
        body = response.get("body", b"")
        headers = response.get("headers", [(b"content-type", b"text/plain; charset=utf-8")])

        await send({
            "type": "http.response.start",
            "status": status,
            "headers": headers
        })
        await send({
            "type": "http.response.body",
            "body": body
        })

_route_registry = []

def route(path, methods=["GET"]):
    def decorator(func):
        _route_registry.append((path, func, methods))
        return func
    return decorator

def get_registered_routes():
    return _route_registry
