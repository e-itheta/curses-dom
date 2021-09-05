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
    
    if args["<url>"] is not None:
        from . import url_util
        handler = url_util.FileSchemeHandler()
        data = url_util.get_resource_from_url(args["<url>"], handler)
    else:
        data = ""
    
    if args["--level"] is not None:
        rlog.setLevel(getattr(logging, args["--level"]))
 
    with open("/dev/null" if args["--log"] is None else args["--log"], "w") as fp:
        handler = logging.StreamHandler(fp)
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        rlog.addHandler(handler)
        


        @curses.wrapper
        def _main(stdscr: curses.window):
            parser = dom.Parser()
            domroot = dom.DOMElement("body", [])
            parser.parse(data, domroot)

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

            curses_util.init_key_listener(stdscr.getch)
            
            async def quit():
                await curses_util.EVENTS[ord("q")].wait()
                exit()
            
            async def refresh():
                while True:
                    await curses_util.EVENTS[curses.KEY_RESIZE].wait()
                    stdscr.clear()
                    stdscr.resize(*stdscr.getmaxyx())
                    stdscr.box("|", "-")
                    stdscr.refresh()

                
            
            stdscr.box("|", "-")
            
            loop.create_task(quit())
            loop.create_task(refresh())

            loop.run_forever()
