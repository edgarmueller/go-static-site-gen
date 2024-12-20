from functools import reduce

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
	
	def __repr__(self):
		return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"