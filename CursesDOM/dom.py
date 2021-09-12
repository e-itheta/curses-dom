import collections
import logging
from html.parser import HTMLParser
from typing import *
import re
from xml import dom
import cssutils

strip_white_space = re.compile(r"\s{2,}")
logger = logging.getLogger(__name__)


class DOMElement:

    def __init__(
        self, tag: str, 
        attrs: DefaultDict[str, str], 
        parent: Optional["DOMElement"] = None, 
        **kwargs
    ) -> None:
        self.parent = parent
        self.children: List[Union[DOMElement, str]] = []
        self.tag = tag
        self.attrs = attrs
 
    def __str__(self):
        return f"<{self.tag}>"

    def render(self):
        pass


class DOMElementVisitor:
    """Traverse and visit each node of DOMElement"""

    def visit(self, node: DOMElement):
        if hasattr(self, f"visit_{node.tag}"):
            getattr(self, f"visit_{node.tag}")(node)
        
        for node in filter(lambda x: isinstance(x, DOMElement), node.children):
            self.visit(node)


class DOMElementTransformer:
    """Traverse and mutate each node of DOMElement"""

    def visit(self, node: DOMElement) -> DOMElement:
        if hasattr(self, f"visit_{node.tag}"):
            transformed: DOMElement = getattr(self, f"visit_{node.tag}")(node)
        
        for i in range(len(transformed.children)):
            child = transformed.children[i]
            if isinstance(child, DOMElement) and hasattr(self, f"visit_{child.tag}"):
                transformed.children[i] = getattr(self, f"visit_{child.tag}")(child)
        return transformed





class Document:

    def __init__(self, uri: str, documentElement: DOMElement):
        self._documentURI = uri 
        self._documentElement = documentElement
        self._children: Tuple[DOMElement] = tuple(documentElement.children)
        self._head = None
        self._body = None
        self._elements_by_id: Dict[str, DOMElement] = {}
        self._elements_by_class_name: Dict[str, List[DOMElement]] = collections.defaultdict(list)
        self._elements_by_tag_name: Dict[str, List[DOMElement]] = collections.defaultdict(list)
        self._scripts = []
        self._styleSheets = []
        

        cssparser = cssutils.CSSParser(logger)
        
        class Visitor(DOMElementVisitor):
            # self refers to closure variable ie the document object
            
            def visit_style(_, node: DOMElement):
                for child in filter(lambda x: isinstance(x, str), node.children):
                    self._styleSheets.append(cssparser.parseString(child))

            def visit_body(_, node: DOMElement):
                self._body = node
            
            def visit_head(_, node: DOMElement):
                self._head = node
            
            def visit_script(_, node: DOMElement):
                self._scripts = node
            

        Visitor().visit(documentElement)

        
        def get_attributes(node: DOMElement):
            # Recursively iterate through all nodes
            if node.attrs["id"]:
                self._elements_by_id[node.attrs["id"]] = node
            
            if node.attrs["class"]:
                self._elements_by_class_name[node.attrs["class"]].append(node)
            
            self._elements_by_tag_name[node.tag].append(node)
            for elt in filter(lambda x: isinstance(x, DOMElement), node.children):    
                get_attributes(elt)

        get_attributes(documentElement)
    
    @property
    def scripts(self):
        return tuple(self._scripts)
    
    @property
    def styleSheets(self):
        return tuple(self._styleSheets)

    @property
    def body(self):
        return self._body
    
    @property
    def head(self):
        return self._head

    @property
    def children(self):
        return self._children

    @property
    def documentURI(self):
        return self._documentURI
    
    @property
    def documentElement(self):
        return self._documentElement
    
    @property
    def links(self):
        return self._links
        

    def getElementById(self, id: str) -> Optional[DOMElement]:
        if id in self._elements_by_id:
            return self._elements_by_id[id]
        return None

    def getElementByClassName(self, name: str) -> Tuple[DOMElement]:
        return tuple(self._elements_by_class_name[name])


    def getElementsByTagName(self, name: str) -> Tuple[DOMElement]:
        return tuple(self._elements_by_tag_name[name])


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

        parent = self.stack[-1]
        elt = DOMElement(tag, collections.defaultdict(str, attrs), parent)
        parent.children.append(elt)

        # tags that don't have closing tags
        if tag not in {
            "br",
            "link",
        }:
            self.stack.append(elt)

    def handle_data(self, data:str) -> None:
        element = self.stack[-1]
        if data := strip_white_space.sub(" ", data.strip()):
            logger.debug(f"{data}")
            element.children.append(data)
    
    def handle_endtag(self, tag) -> None:
        logger.debug(f"</{tag}>")
        elt = self.stack.pop()


    def parse(self, data: str) -> DOMElement:
        self.stack.append(DOMElement("", collections.defaultdict(str)))
        self.feed(data)
        assert len(self.stack) == 1
        return self.stack.pop()

