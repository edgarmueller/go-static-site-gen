from enum import Enum

class TextType(Enum):
	HEADING_1 = "heading1"
	HEADING_2 = "heading2"
	HEADING_3 = "heading3"
	HEADING_4 = "heading4"
	HEADING_5 = "heading5"
	HEADING_6 = "heading6"
	PARAGRAPH = "paragraph"
	BOLD = "bold"
	ITALIC = "italic"
	LINK = "link"
	IMAGE = "image"
	UNORDERED_LIST = "unordered-list"
	ORDERED_LIST = "ordered-list"
	LIST_ITEM = "list-item"
	QUOTE = "blockquote"
	CODE = "code"

class TextNode:
	def __init__(self, text_type, text, url = None):
		self.text_type = text_type
		self.text = text
		self.url = url

	def __eq__(self, value):
		return self.text_type == value.text_type and self.text == value.text and self.url == value.url

	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
	