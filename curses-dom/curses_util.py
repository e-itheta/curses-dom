from collections import defaultdict
import curses
import asyncio
from typing import DefaultDict, Iterable, Callable, Union

loop = asyncio.get_event_loop()


        
EVENTS: DefaultDict[int, asyncio.Event] = defaultdict(asyncio.Event)

def init_key_listener(getfn):
    async def get_key():
        while True:
            result = getfn()
            if result == curses.ERR:
                EVENTS[result].clear()
            else:
                EVENTS[result].set()
            await asyncio.sleep(1/120)
    return loop.create_task(get_key())


def init_event_listener(
        getfn: Callable[[], None],
        event: asyncio.Event,
        key: Union[int, str],
        interval=1/60
) -> asyncio.Task:

    if type(key) is str:
        key = ord(key)

    async def get_input():
        while True:
            result = getfn()
            if result == key:
                event.set()
            else:
                event.clear()
            await asyncio.sleep(interval)
    return loop.create_task(get_input())




