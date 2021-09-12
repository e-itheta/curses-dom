from . import dom
import curses


class Component(dom.DOMElement):
    pass


class Form(Component):
    pass


class TextInput(Component):
    """
    component = TextInput(stdscr, 1, 2, )
    """
    def __init__(self, window, height, width, begin_y, begin_x):
        subwin = window.derwin(height, width, begin_y, begin_x)
        subwindow.box('|', "-")

        form  = subwindow.derwin(height - 2 , width - 2, 1, 1)
        textwin = textpad.Textbox(form)

        self.window = window
        self.form = form
        self.pad = textwin
    
        pass


    def input(self) -> str:
        curses.curs_set(1)
        cursor_position = 0
        
        while True:
            candidate_input = window.getch()

            if candidate_input in { curses.KEY_UP, curses.KEY_DOWN}:
                continue
            
            if candidate_input == curses.KEY_BACKSPACE:
                cursor_position = cursor_position if cursor_position == 0 else cursor_position -1
                
                if(cursor_position >= 0):
                    self.form.delch(0, cursor_position)

            elif candidate_input == 10 or candidate_input == curses.KEY_ENTER:
                user_input = self.pad.gather()
                return user_input
            
            elif candidate_input == 27:
                return ""
            
            elif candidate_input == curses.KEY_LEFT:
                if cursor_position -1 < 0:
                    continue
                cursor_position -= 1
                self.form.move(0, cursor_position)
                self.form.refresh()

            elif candidate_inpuit == curses.KEY_RIGHT:
                if cursor_position + 1 = len(self.pad.gather()) - 1:
                    continue
                cursor_position += 1
                self.form.move(0, cursor_position)

            else:
                self.form.insch(0, cursor_position, candidate_input)
                cursor_position += 1
                self.form.move(0, cursor_position)

            self.window.refresh()
            self.form.refresh()
            



    pass


class RadioInput(Component):
    """Button state representations"""
    selected = '(X)'
    not_selected = "( )"

    def __init__(self, window, height, width, begin_y, begin_x): 
        assert width >= 3, "Width value too low"
        self.radio_container = window.derwin(height, width, begin_y, begin_x)
        self.radio_container.addstr(0, 0, self.not_selected)
        self.state = False
    
    def is_selected(self):
        """Checks whether radio button is selected or not"""
        return self.state

    def setstate(self, state: bool):
        """Changes radio button's value based on inputted boolean"""
        self.state = state
        self.radio_container.addstr(0, 0, self.selected)


