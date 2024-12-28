import requests
import websockets
from .messages import Message


class SignalAPIError(Exception):
    pass


class NativeEngine:
    def __init__(self, base_url) -> None:
        self.base_url = base_url

    def _requests_wrap(codes=[200, 201, 204]):
        def decorator(func):
            def _wrapper(self, url, *args, **kwargs):
                endpoint_url = f"http://{self.base_url}/{url}"
                resp = func(self, endpoint_url, *args, **kwargs)
                if resp.status_code not in codes:
                    if resp.text:
                        raise SignalAPIError(resp.text)
                    json_resp = resp.json()
                    if "error" in json_resp:
                        raise SignalAPIError(json_resp["error"])
                    if "text" in json_resp:
                        raise SignalAPIError(json_resp["text"])
                    raise SignalAPIError(
                        f"Unknown Signal error accessing {endpoint_url}"
                    )
                return resp

            return _wrapper

        return decorator

    @_requests_wrap()
    def get(self, url, *args, **kwargs):
        return requests.get(url, *args, **kwargs)

    @_requests_wrap()
    def post(self, url, *args, **kwargs):
        return requests.post(url, *args, **kwargs)

    @_requests_wrap()
    def put(self, url, *args, **kwargs):
        return requests.put(url, *args, **kwargs)

    @_requests_wrap()
    def delete(self, url, *args, **kwargs):
        return requests.delete(url, *args, **kwargs)


class JsonRPCEngine(NativeEngine):
    async def fetch(self, number):
        self.connection = websockets.connect(
            f"ws://{self.base_url}/v1/receive/{number}", ping_interval=None
        )
        async with self.connection as websocket:
            async for raw_message in websocket:
                yield Message.from_json(raw_message)
