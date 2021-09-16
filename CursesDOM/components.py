import curses
import abc

class EventTarget(abc.ABC):

    def addEventListener(self, *args):
        pass

    def removeEventListener(self, *args):
        pass

    def dispatchEvent(self, *args):
        pass


class HTMLElement(EventTarget):
    
    def __init__(self, parent: "HTMLElement"):
        self.parent = parent
        
    @abc.abstractmethod
    @property
    def window(self) -> curses.window:
        """Returns the underlying curses window object"""
        pass
    
    @property
    def width(self):
        self.window.getmaxyx()[1]
    
    @property
    def height(self):
        self.window.getmaxyx()[0]
    
    @property
    def pos(self):
        return self.window


class Button(HTMLElement):
    pass


class Form(HTMLElement):
    pass


class TextInput(HTMLElement):
    pass


class RadioInput(HTMLElement):
    pass


class CheckboxInput(HTMLElement):
    pass

