"""Usage: curses-dom [ <url> ] [ --log=<path> ]"""

import logging
import curses
import docopt
import asyncio

from . import box
from . import curses_util
from . import dom


def main():
    args = docopt.docopt(__doc__)
    loop = asyncio.get_event_loop()
    
    if args["<url>"] is not None:
        from . import url_util
        handler = url_util.FileSchemeHandler()
        data = url_util.get_resource_from_url(args["<url>"], handler)

    with open("/dev/null" if args["--log"] is None else args["--log"], "w") as fp:

        @curses.wrapper
        def _main(stdscr: curses.window):    
            parser = dom.Parser(fp)
            parser.feed(data)

            stdscr.nodelay(1)
            box.Box(stdscr, 0, 0, 
                content=5,
                margin=1,
                border=1,
                padding={ "top": 1, "left": 1 }
            )

            curses_util.init_event_listener(
                stdscr.getch,
                [ 
                    lambda ev: stdscr.addstr(chr(ev)),
                    lambda ev: exit(0) if chr(ev) == "q" else None
                ]
            )

            loop.run_forever()
