from collections import defaultdict
import curses
import asyncio
from typing import TYPE_CHECKING, DefaultDict, Iterable, Callable, Union, Optional
import logging


loop = asyncio.get_event_loop()
logger = logging.getLogger(__name__)


        
EVENTS: DefaultDict[int, asyncio.Condition] = defaultdict(asyncio.Condition)

def init_key_listener(getfn, ignore: Optional[set] = None):
    if ignore is None: 
        ignore = set()
    else:
        ignore.add(curses.ERR)

    async def get_key():
        while True:
            result = getfn()
            if result != curses.ERR:
                logger.debug(f"{result}")
                cond = EVENTS[result]
                async with cond:
                    cond.notify_all()
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


if TYPE_CHECKING:
    from .dom import Document

_document: "Document" = None

def set_current_document(document: "Document") -> None:
    global _document
    _document = document

def get_current_document() -> "Document":
    return _document
