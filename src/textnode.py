from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        if not isinstance(text_type, TextType):
            raise ValueError("text_type passed into TextNode must be a TextType enum")
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other_node):
        return (
            self.text == other_node.text
            and self.text_type == other_node.text_type
            and self.url == other_node.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    """
    It should handle each type of the TextType enum. 
    If it gets a TextNode that is none of those types, it should raise an exception. 
    Otherwise, it should return a new LeafNode object.

    TextType.TEXT: This should return a LeafNode with no tag, just a raw text value.
    TextType.BOLD: This should return a LeafNode with a "b" tag and the text
    TextType.ITALIC: "i" tag, text
    TextType.CODE: "code" tag, text
    TextType.LINK: "a" tag, anchor text, and "href" prop
    TextType.IMAGE: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
    """
    tag, value, props = None, None, None
    match text_node.text_type:
        case TextType.NORMAL:
            value = text_node.text
        case TextType.BOLD:
            tag, value = "b", text_node.text
        case TextType.ITALIC:
            tag, value = "i", text_node.text
        case TextType.CODE:
            tag, value = "code", text_node.text
        case TextType.LINK:
            tag, value, props = "a", text_node.text, { "href": text_node.url }
        case TextType.IMAGE:
            tag, value, props = "img", None, { "src": text_node.url, "alt": text_node.text }
        case _:
            raise ValueError("TextNode text_type must be a TextType enum")
    
    return LeafNode(tag, value, props)