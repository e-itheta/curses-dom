import collections
from html.parser import HTMLParser
from io import TextIOWrapper
from typing import *



class DOMElement:
    
    def __init__(self, tag, attrs, parent: Optional["DOMElement"] = None, **kwargs):
        self.parent = parent
        self.children = []
        self.tag = tag
        self.attrs = attrs
        
        if parent is not None:
            parent.children.append(self)


class Parser(HTMLParser):

    @staticmethod
    def strip_whitespace(data: str) -> str:
        return ""
        
    def __init__(self, logfp: TextIOWrapper):
        super().__init__()
        self.logfp = logfp
        self.stack: Deque[DOMElement] = collections.deque()
    
    def print(self, *args, **kwargs):
        print(*args, file=self.logfp, **kwargs)

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str]]) -> None:
        if tag == "body":
            self.stack.append(DOMElement(tag, attrs))
        else:
            self.stack.append(DOMElement(tag, attrs, self.stack[-1]))
    
    def handle_data(self, data):
        element = self.stack[-1]
        self.print(data)

    def handle_endtag(self, tag):
        self.stack.pop()
        
    def handle_data(self, data: str) -> None:
        self.print(data.strip())

