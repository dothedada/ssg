from enum import Enum
from htmlnode import LeafNode
from splitnodesdelimiter import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)


class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "links"
    IMAGE = "images"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        if isinstance(text_type, TextType):
            self.text_type = text_type
        else:
            try:
                self.text_type = TextType(text_type)
            except ValueError:
                raise ValueError(f"Invalid text type: {text_type}")
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise TypeError(f"The argument {text_node} is not a TextNode type")

    match (text_node.text_type):
        case TextType.NORMAL:
            return LeafNode(tag="", value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img",
                value="",
                props={"src": text_node.url, "alt": text_node.text},
            )


def text_to_textnodes(text):
    nodes = TextNode(text, TextType.NORMAL)
    nodes = split_nodes_delimiter([nodes], "**", TextType.BOLD)
    nodes = split_nodes_delimiter([nodes], "*", TextType.ITALIC)
    nodes = split_nodes_delimiter([nodes], "`", TextType.CODE)
    nodes = split_nodes_image([nodes])
    nodes = split_nodes_link([nodes])

    return nodes
