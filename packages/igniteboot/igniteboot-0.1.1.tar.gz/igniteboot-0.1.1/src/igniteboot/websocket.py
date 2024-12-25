
class WebSocket:
    def __init__(self, path: str):
        self.path = path

    def __call__(self, func):
        async def wrapper(scope, receive, send):
            if scope["type"] == "websocket" and scope["path"] == self.path:
                await self.accept(send)
                try:
                    await func(scope, receive, send)
                except Exception as e:
                    await self.close(send, code=1011)
                    raise e
                await self.close(send)
            else:
                raise ValueError("Invalid scope or path for WebSocket connection")
        return wrapper

    async def accept(self, send):
        await send({
            "type": "websocket.accept"
        })

    async def close(self, send, code=1000):
        await send({
            "type": "websocket.close",
            "code": code
        })
