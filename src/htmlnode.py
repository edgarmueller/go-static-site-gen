from functools import reduce
from block import BlockType
class HTMLNode:
	def __init__(self, tag = None, value = None, children = None, props = None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError
	
	def props_to_html(self):
		if self.props is None:
			return ""
		return reduce(lambda acc, k: acc + f" {k}=\"{self.props[k]}\"", self.props.keys(), "")

	def __eq__(self, value):
		return self.tag == value.tag and self.children == value.children and self.props == value.props
	
	def __repr__(self):
		return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
	def __init__(self, tag = None, value = None, props = None):
			super().__init__(tag, value, None, props)

	def to_html(self):
		if self.value is None:
			raise ValueError("LeafNode must have a value")
		if self.tag is None:
			return self.value
		return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props = None):
		super().__init__(tag, None, children, props)

	@staticmethod
	def from_block_type(block_type):
		match block_type:
			case BlockType.HEADING_1:
				return ParentNode("h1", None)
			case BlockType.HEADING_2:
				return ParentNode("h2", None)
			case BlockType.HEADING_3:
				return ParentNode("h3", None)
			case BlockType.HEADING_4:
				return ParentNode("h4", None)
			case BlockType.HEADING_5:
				return ParentNode("h5", None)
			case BlockType.HEADING_6:
				return ParentNode("h6", None)
			case BlockType.CODE:
				return ParentNode("pre", None)
			case BlockType.PARAGRAPH:
				return ParentNode("p", None)
			case BlockType.UNORDERED_LIST:
				return ParentNode("ul", None)
			case BlockType.ORDERED_LIST:
				return ParentNode("ol", None)
			case BlockType.QUOTE:
				return ParentNode("blockquote", None)
			case _:
				raise ValueError(f"Invalid block type {block_type}!")
  

	def to_html(self):
		if self.tag is None:
			raise ValueError("ParentNode must have a tag")
		if self.children is None:
			raise ValueError("ParentNode must have children")
		return f"<{self.tag}{self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"