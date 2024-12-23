from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode
from block import block_to_block_type
import re
	
MARKDOWN_IMAGE_PATTERN = r"!\[(.*?)\]\((.*?)\)"
MARKDOWN_LINK_PATTERN = r"\[(.*?)\]\((.*?)\)"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []
	pattern = r'(' + re.escape(delimiter) + '.*?' + re.escape(delimiter) + ')'
	for node in old_nodes:
		matches = re.findall(pattern, node.text)
		has_matches = len(matches) > 0
		if not has_matches:
			new_nodes.append(node)
		else:
			tokens = [segment for segment in re.split(pattern, node.text) if segment != '']
			for token in tokens:
				if token.startswith(delimiter):
					new_nodes.append(TextNode(token.replace(delimiter, ""), text_type))
				else:
					new_nodes.append(TextNode(token, TextType.TEXT))
	return new_nodes

def extract_markdown_images(text):
	return re.findall(MARKDOWN_IMAGE_PATTERN, text)

def extract_markdown_links(text):
	return re.findall(MARKDOWN_LINK_PATTERN, text)

def split_nodes_link(old_nodes):
	new_nodes = []
	for node in old_nodes:
		links = dict(extract_markdown_links(node.text))
		if len(links) == 0:
			new_nodes.append(node)
			continue
		tokens = [segment for segment in re.split(MARKDOWN_LINK_PATTERN, node.text) if segment != '']  # Remove empty strings
		i = 0
		while i < len(tokens):
			if tokens[i] in links:
				new_nodes.append(TextNode(tokens[i], TextType.LINK, links[tokens[i]]))
				i += 2
			else:
				new_nodes.append(TextNode(tokens[i], TextType.TEXT))
				i += 1
	return new_nodes
	
def split_nodes_image(old_nodes):
	new_nodes = []
	for node in old_nodes:
		images = dict(extract_markdown_images(node.text))
		if len(images) == 0:
			new_nodes.append(node)
			continue
		tokens = [segment for segment in re.split(MARKDOWN_IMAGE_PATTERN, node.text) if segment != '']  # Remove empty strings
		i = 0
		while i < len(tokens):
			if tokens[i] in images:
				new_nodes.append(TextNode(tokens[i], TextType.IMAGE, images[tokens[i]]))
				i += 2
			else:
				new_nodes.append(TextNode(tokens[i], TextType.TEXT))
				i += 1
	return new_nodes

def split_list_items(old_nodes):
	ordered_list_pattern = r"^\d+\. "
	new_nodes = []
	for node in old_nodes:
		if node.text.startswith("- ") or node.text.startswith("* ") or re.match(ordered_list_pattern, node.text):
			lines = node.text.split("\n")
			for line in lines:
				new_nodes.append(TextNode(line[2:].strip(), TextType.LIST_ITEM))
		else:
			new_nodes.append(node)
	return new_nodes

def text_to_textnodes(text):
	nodes = [TextNode(text, TextType.TEXT)]
	nodes = split_list_items(nodes)
	nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
	nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
	nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
	nodes = split_nodes_image(nodes)
	nodes = split_nodes_link(nodes)
	return nodes

def markdown_to_blocks(text):
	paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text)]
	return paragraphs

def text_to_children(text):
	text_nodes = text_to_textnodes(text)
	return [node.to_html_node() for node in text_nodes]

def trim_block(block):
	if block.startswith("#"):
		return block.replace("#", "", 6).strip()
	elif block.startswith("```"):
		return block.replace("```", "", 2).strip()
	elif block.startswith(">"):
		return block.replace(">", "", 1).strip()
	return block

def markdown_to_html(markdown):
	blocks = markdown_to_blocks(markdown)
	children = []
	for block in blocks:
		block_type = block_to_block_type(block)
		html_node = ParentNode.from_block_type(block_type)
		html_node.children = text_to_children(trim_block(block))
		children.append(html_node)
	return ParentNode("div", children)