#! /usr/bin/env python3.14

'''
Your task in this Bite is to create an http client that will asynchronously send
http requests and process responses.

This Bite is focused on using asyncio, so you are expected to write async
function.

To demonstrate power of asynchronous requests you will have to implement
function that is able to send 100 requests and get results in 0.5 seconds,
despite the fact that each request will take around 0.1 second for the server to
respond to!

This is impossible without concurrent requests. (The test server is able to
handle concurrent requests.)

For a detailed task description read the docstrings of the function that you are
supposed to implement:
get_results_from_urls

Useful links
- Python docs: asyncio — Asynchronous I/O
  (https://docs.python.org/3/library/asyncio.html)

- AIOHTTP docs (https://docs.aiohttp.org/en/stable/)

- Async IO in Python: A Complete Walkthrough
  (https://realpython.com/async-io-python/)
'''


import asyncio
from typing import Iterable, NamedTuple

from aiohttp import ClientSession


class Result(NamedTuple):
    status_code: int
    content: int


async def get_url(session: ClientSession, address: str) -> Result:
    async with session.get(address) as response:
        body = int(await response.text()) if (status := response.status) == 200 else 0
        return Result(status, body)


async def get_results_from_urls(address: str, port: int, slugs: list[int]) -> Iterable[Result]:
    """Get results from http responses.

    Get responses by making requests to urls.
    Construct url like this: {address}:{port}/{slug}, where address and port are constant, but slug changes.
    Result.status_code is status code of response.
    Result.content is content of response if status_code is 200, otherwise it is 0.
    Results must be ordered according to the order of slugs in list and their respective responses.
    Requests must be sent in a asynchronous way. (Can not be sequential and blocking.)
    """
    async with ClientSession() as session:
        tasks = [get_url(session, f'{address}:{port}/{slug}') for slug in slugs]

        return await asyncio.gather(*tasks)


if __name__ == '__main__':
    import sys
    print(sys.version)
