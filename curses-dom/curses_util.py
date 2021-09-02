import curses
import asyncio
from typing import Iterable, Callable
loop = asyncio.get_event_loop()

def init_event_listener(
        getfn: Callable[[], None],
        handlers: Iterable[Callable[[int], None]],
        interval=1/60
) -> asyncio.Task:

    async def get_input():
        while True:
            result = getfn()
            if result != curses.ERR:
                for handler in handlers:
                    handler(result)

            await asyncio.sleep(interval)
    
    return loop.create_task(get_input())
