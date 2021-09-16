import curses
from curses import wrapper
from curses import panel

def main():

  with open("/dev/pts/2", "w") as fp:
    println = lambda *args, **kwargs: print(*args, file=fp, **kwargs)

    @curses.wrapper
    def _main(stdscr):
        stdscr.box("|", "-")

        h, w, = stdscr.getmaxyx()
        stdscr.subpad(h-1, w-1)
        panel = curses.panel.new_panel(stdscr)

        curses.curs_set(1)
        curses.mousemask(1)
        cursor_position = 0
        while True:
          stdscr.refresh() 
          curses.doupdate()          
          curses.panel.update_panels()


def check_positiion(cursor_position):
  if len(form.gather()) == cursor_position:
    return True
    
      
if __name__ == "__main__":
  # Unreachable block on import  
  main()

 