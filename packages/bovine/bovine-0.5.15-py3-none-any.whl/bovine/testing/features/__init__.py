"""
Helpers for BDD. To use the helpers that provide
a session use an environment file
such as

```python title="features/environment.py"
--8<-- "./features/environment.py"
```

"""

import aiohttp

import asyncio


def before_all(context):
    """Creates necessary variables to store stuff in"""
    context.session = None
    context.responses = {}


async def create_client_session(context):
    context.session = aiohttp.ClientSession()


def before_scenario(context, scenario):
    """Ensures an [aiohttp.ClientSession][] is present"""
    if context.session is None:
        asyncio.get_event_loop().run_until_complete(create_client_session(context))

    context.responses = {}


def after_scenario(context, scenario):
    """Closes the [aiohttp.ClientSession][]  if present"""
    if context.session:
        asyncio.get_event_loop().run_until_complete(context.session.close())
        context.session = None
