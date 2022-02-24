import nest_asyncio
import asyncio
from pprint import pprint
from fastapi import Response
import httpx
import requests


def read_vault_sync(env: str):
    url = f'http://127.0.0.1:8000/{env}'
    return requests.get(url).json()


async def read_vault(env: str):
    url = f'http://127.0.0.1:8000/{env}'

    async with httpx.AsyncClient(verify=False) as async_client:
        try:
            response: Response = await async_client.get(url)

            return response.json()
        except httpx.ConnectError as conn_err:
            print(
                f'Unable to connect the remote endpoint {conn_err.request.url!r}')
        except httpx.HTTPStatusError as stat_err:
            print(
                f'Error response {stat_err.status_code} while requesting {stat_err.request.url!r}')
        except httpx.RequestError as req_err:
            print(
                f'An error occurred while requesting {req_err.request.url!r}')


def main_reader(env):
    try:
        loop = asyncio.get_running_loop()

    except RuntimeError:  # 'RuntimeError: There is no current event loop...'
        loop = None
    if loop and loop.is_running():
        nest_asyncio.apply()

        #         print('Async event loop already running. Adding coroutine to the event loop.')
    return asyncio.run(read_vault(env))
# def main_reader(env):
#     print(f'Loading config for {env}')
#     try:
#         loop = asyncio.get_running_loop()

#     except RuntimeError:  # 'RuntimeError: There is no current event loop...'
#         loop = None

#     if loop and loop.is_running():
#         print('Async event loop already running. Adding coroutine to the event loop.')
#         task = loop.create_task(read_vault(env))
#         # ^-- https://docs.python.org/3/library/asyncio-task.html#task-object
#         # Optionally, a callback function can be executed when the coroutine completes
#         task.add_done_callback(
#             # lambda t: print(
#             # f'Task done with result={t.result()}  << return val of read_vault("{env}")')
#             lambda t: f'{t.result()}'
#         )
#         print({'task': task})
#     else:
#         print('Starting new event loop')
#         return asyncio.run(read_vault(env))
    # return await read_vault(env)


if __name__ == '__main__':
    # resp = asyncio.run(read_vault('prod'))  # dev | prod
    resp = main_reader('prod')
    pprint(resp)
    dev = main_reader('dev')
    pprint({'dev': dev})
