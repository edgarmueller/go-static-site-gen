from enum import StrEnum
from htmlnode import LeafNode

class TextType(StrEnum):
    PARAGRAPH = "paragraph"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    LINK = "link"
    IMAGE = "image"
    #UNORDERED_LIST = "unordered-list"
    #ORDERED_LIST = "ordered-list"
    LIST_ITEM = "LIST_ITEM"
    QUOTE = "blockquote"
    CODE = "CODE"
    TEXT = "TEXT"

class TextNode:
  def __init__(self, text, text_type, url=None):
      self.text = text
      self.text_type = text_type
      self.url = url

  def __eq__(self, value):
    return (
      self.text_type == value.text_type
      and self.text == value.text
      and self.url == value.url
    )

  def __repr__(self):
    return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

  def to_html_node(self):
    match self.text_type:
        case TextType.TEXT:
            return LeafNode(None, self.text)
        case TextType.BOLD:
            return LeafNode("b", self.text)
        case TextType.ITALIC:
            return LeafNode("i", self.text)
        case TextType.LINK:
            return LeafNode("a", self.text, props={"href": self.url})
        case TextType.IMAGE:
            return LeafNode("img", None, props={"src": self.url})
        case TextType.CODE:
            return LeafNode("code", self.text)
        case TextType.LIST_ITEM:
            return LeafNode("li", self.text)
        case _:
            raise ValueError("Invalid text type")
