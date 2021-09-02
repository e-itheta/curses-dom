from collections import defaultdict
import curses
from typing import DefaultDict, Optional, Union

Attributes = Union[DefaultDict[str, int], int]

def create_default(arg):
    if type(arg) is int:
        return defaultdict(lambda: arg)
    elif arg is None:
        return defaultdict(int)
    elif type(arg) is dict:
        return defaultdict(int, arg)

class Box:
    margin: curses.window
    border: curses.window
    padding: curses.window
    content: curses.window
    
    def __init__(self,
        parent: curses.window, 
        row: int,
        col: int,
        content: Optional[Attributes] = None,
        padding: Optional[Attributes] = None,
        border: Optional[Attributes] = None,
        margin: Optional[Attributes] = None,
        **style
    ) -> None:
        content = create_default(content)
        padding = create_default(padding)
        border = create_default(border)
        margin = create_default(margin)

        self.border = parent.subwin(
            border["top"] + padding["top"] + content["height"] + padding["bottom"] + border["bottom"], # nrows
            border["left"] + padding["left"] + content["width"] + padding["right"] + border["right"], # ncols

            row + margin["top"],
            col + margin["left"])
        
        self.padding = parent.subwin(
            padding["top"] + content["height"] + padding["bottom"],
            padding["left"] + content["width"] + padding["right"],
            row + margin["top"] + border["top"],
            col + margin["left"] + border["left"]
        ); self.padding.box("|", "-")

        self.content = parent.subpad(
            content["height"],
            content["width"],
            row + margin["top"] + border["top"] + padding["top"],
            col + margin["left"] + border["left"] + padding["left"],
        )

        self.content.box("c", "c")
