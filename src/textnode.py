from htmlnode import LeafNode
from enum import Enum

class TextType(Enum):
    TEXT = "text"
    NORMAL = "Normal"
    BOLD = "Bold"
    ITALIC = "Italic"
    CODE = "Code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if isinstance(other, TextNode):
            return self.text == other.text and self.text_type == other.text_type and self.url == other.url
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    if text_node.type == TextType.TEXT:
      return LeafNode(tag=None, value=text_node.value)
    elif text_node.type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.value)
    elif text_node.type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.value)
    elif text_node.type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.value)
    elif text_node.type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.value, props={"href": text_node.url})
    elif text_node.type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.alt_text})
    else:
        raise Exception(f"Unknown TextType: {text_node.type}")