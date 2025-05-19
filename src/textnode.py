from enum import Enum


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