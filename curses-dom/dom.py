import collections
import logging
from html.parser import HTMLParser
from typing import *

logger = logging.getLogger(__name__)

class DOMElement:
    
    def __init__(
        self, tag: str, attrs: list, 
        parent: Optional["DOMElement"] = None, 
        **kwargs
    ) -> None:
        self.parent = parent
        self.children = []
        self.tag = tag
        self.attrs = attrs
        if parent is not None:
            parent.children.append(self)
        
        self.width = 0
        self.height = 0

    def render(self) -> None:
        pass


class Parser(HTMLParser):

    @staticmethod
    def strip_whitespace(data: str) -> str:
        return ""
        
    def __init__(self):
        super().__init__()
        self.stack: Deque[DOMElement] = collections.deque()
    
    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str]]) -> None:
        assert self.stack
        logger.debug(f"<{tag}>")
        self.stack.append(DOMElement(tag, attrs, self.stack[-1]))
    
    def handle_data(self, data) -> None:
        element = self.stack[-1]

    def handle_endtag(self, tag) -> None:
        logger.debug(f"</{tag}>")
        self.stack.pop()
        
    def handle_data(self, data: str) -> None:
        pass

    def parse(self, data: str, head: DOMElement) -> None:
        self.stack.append(head)
        self.feed(data)
        assert len(self.stack) == 1
        del self.stack[0]

