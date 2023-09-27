## rocketchat_API
Python Asynchronous API wrapper for [Rocket.Chat](https://developer.rocket.chat/reference/api/rest-api/)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/fff725d9a0974c6597c2dd007daaa86e)](https://www.codacy.com/app/jadolg/rocketchat_API?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jadolg/rocketchat_API&amp;utm_campaign=Badge_Grade) ![Test and publish](https://github.com/jadolg/rocketchat_API/workflows/Test%20and%20publish/badge.svg?branch=master) [![codecov](https://codecov.io/gh/jadolg/rocketchat_API/branch/master/graph/badge.svg)](https://codecov.io/gh/jadolg/rocketchat_API) ![PyPI](https://img.shields.io/pypi/v/rocketchat_API.svg) ![](https://img.shields.io/pypi/dm/rocketchat-api.svg)

### Installation
- From GitHub:
Clone our repository and `python3 setup.py install`

### Requirements
- [requests](https://github.com/kennethreitz/requests)

### Usage
```python
import asyncio
from rocketchat_API.rocketchat import RocketChat

async def main():
    rocket = RocketChat('user', 'pass', server_url='server_url')
    if rocket.login_task:
        await rocket.login_task
        print('Login successful!')

    # Use the methods to test
    response = await rocket.chat_post_message('test message using asynchronous library!', room_id='room_id')
    print(response.json())
    
asyncio.run(main())
```

*note*: every method returns a [requests](https://github.com/kennethreitz/requests) Response object.

#### Connection pooling
If you are going to make a couple of request, you can user connection pooling provided by `requests`. This will save significant time by avoiding re-negotiation of TLS (SSL) with the chat server on each call.

```python
import asyncio
import httpx
from rocketchat_API.rocketchat import RocketChat

async def main():
    async with httpx.AsyncClient() as client:
    rocket = RocketChat('user', 'pass', server_url='server_url', client=client)
    if rocket.login_task:
        await rocket.login_task
    
    print(rocket.channels_list().json())
    print(rocket.channels_history('GENERAL', count=5).json())

asyncio.run(main())
```
 
### Tests
We are actively testing :) 

Tests run on a Rocket.Chat Docker container so install Docker and docker-compose. 
1. To start test server do `docker-compose up` and to take test server down `docker-compose down`
2. To run the tests run `pytest` 

### Contributing
You can contribute by doing Pull Requests. (It may take a while to merge your code but if it's good it will be merged). Please, try to implement tests for all your code and use a PEP8 compliant code style.

Reporting bugs and asking for features is also contributing ;) Feel free to help us grow by registering issues.
