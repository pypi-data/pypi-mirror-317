[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg)](https://stand-with-ukraine.pp.ua)

# pysignalapi

Simple yet powerful library to work with [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api). It supports both sync and async modes of Docker container and intends to provide closest to origin API.

## Example

```python
import asyncio
from pysignalapi import JsonRPCAPI, Message

api = JsonRPCAPI("localhost:8080")

@api.handler
def on_message(msg: Message):
    print(msg)

async def main():
    accounts = api.get_accounts()
    for account in accounts:
        await api.receive(account)

if __name__ in {"__main__", "__mp_main__"}:
    asyncio.run(main())
```

## Credits:

This project is heavily inspired by:

- [signalbot](https://github.com/filipre/signalbot)
- [pysignalclirestapi](https://github.com/bbernhard/pysignalclirestapi)
