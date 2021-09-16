"""Usage: curses-dom [ <url> ] [ --log=<path> ] [ --level=<level> ]"""

import logging
import curses
import docopt
import asyncio

from curses import textpad
from curses import panel

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

            rlog.debug("hello")
            #stdscr.nodelay(1)
            stdscr.box()
            stdscr.addstr(1, 1, "stdscr")

            h, w, = stdscr.getmaxyx()
            window = stdscr.derwin(h//3, w//3, 1, 1)
            window.box()
            window.addstr(1, 1, "stdscr_win_1")
            panel = curses.panel.new_panel(window)
            
            stdscr_win_2 = stdscr.derwin(h//3, w//3, 1, w//3 + 1)
            stdscr_win_2.addstr(1, 1, "stdscr_win_2")
            stdscr_win_2.box()
            stdscr_win_2_panel = curses.panel.new_panel(stdscr_win_2)

            hw2, ww2 = stdscr_win_2.getmaxyx()
            
            stdscr_win_2_win = curses.newwin(hw2-2, ww2-2, 2, 1)
            stdscr_win_2_win.box()
            stdscr_win_2_win.addstr(1, 1, ("stdscr_win_2_win"))
            stdscr_win_2_win_panel = curses.panel.new_panel(stdscr_win_2_win)

            stdscr_win_2_win_panel.move(0, 0)
            

            while True:       
             
                curses.panel.update_panels()
                curses.doupdate()
                stdscr.refresh()
                stdscr.getch()

    