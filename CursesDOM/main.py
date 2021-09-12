"""Usage: curses-dom [ <url> ] [ --log=<path> ] [ --level=<level> ]"""

import logging
import curses
import docopt
import asyncio

from . import box
from . import curses_util
from . import dom


def main():
    rlog = logging.getLogger()
    args = docopt.docopt(__doc__)
    loop = asyncio.get_event_loop()
        
    if args["--level"] is not None:
        rlog.setLevel(getattr(logging, args["--level"]))
 
    with open("/dev/null" if args["--log"] is None else args["--log"], "w") as fp:
        handler = logging.StreamHandler(fp)
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        handler.setFormatter(formatter)
        rlog.addHandler(handler)


        @curses.wrapper
        def _main(stdscr: curses.window):
            parser = dom.Parser()
            if args["<url>"] is not None:
                from . import url_util
                handler = url_util.FileSchemeHandler()
                data = url_util.get_resource_from_url(args["<url>"], handler)
                dom_root = parser.parse(data)
                
                curses_util.set_current_document(
                    document := dom.Document(
                        args["<url>"],
                        dom_root,
                    )
                )
            
                rlog.debug(f"{document.getElementById('Hello')}")
                rlog.debug(f"{document.getElementsByTagName('div')}")
                rlog.debug(f"{document.styleSheets}")


            stdscr.nodelay(1)
            box.Box(
                stdscr,
                0,
                0, 
                content=5,
                margin=1,
                border=1,
                padding={ "top": 1, "left": 1 }
            )

            curses_util.init_key_listener(stdscr.getch, ignore={ curses.KEY_REFRESH })
            
            async def quit():
                cond = curses_util.EVENTS[ord("q")]
                async with cond:
                    await cond.wait()
                    exit()

            async def refresh():
                cond = curses_util.EVENTS[curses.KEY_RESIZE]
                while True:
                    async with cond:
                        await cond.wait()
                        
                        stdscr.clear()
                        stdscr.resize(*stdscr.getmaxyx())
                        stdscr.refresh()

            stdscr.box("|", "-")
            loop.create_task(quit())
            loop.create_task(refresh())
            loop.run_forever()
