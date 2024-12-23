import unittest
from parser import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes,
    markdown_to_blocks,
    markdown_to_html,
)
from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode, HTMLNode

class TestConversion(unittest.TestCase):
    def test_conversion(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.children, None)

    def test_split_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertEqual(
            images,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        self.assertEqual(
            links,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_split_nodes_image(self):
        text = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([text])
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_text_to_textnodes_bold_only(self):
        text = """This is **text** with an"""
        new_nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_text_to_textnodes(self):
        text = """This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"""
        new_nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_markdown_to_blocks(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        blocks = markdown_to_blocks(text)
        self.assertEqual(len(blocks), 3)

    def test_markdown_to_blocks_2(self):
        text = """# This is a heading

        ## This is a subheading

        ```python
        print("Hello, world!")
        ```

        * This is the first list item in a list block
        * This is a list item
        * This is another list item

        . This is an ordered list item
        . This is another ordered list item
        . This is the last ordered list item
"""
        blocks = markdown_to_blocks(text)
        self.assertEqual(len(blocks), 5)

    def test_markdown_to_html(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        html = markdown_to_html(markdown)
        self.assertEqual(html, 
                         ParentNode(tag="div", children=[
                             ParentNode(tag="h1", children=[LeafNode(tag=None, value="This is a heading")]),
                             ParentNode(tag="p", children=[
                                 LeafNode(tag=None, value="This is a paragraph of text. It has some "),
                                 LeafNode(tag="b", value="bold"),
                                 LeafNode(tag=None, value=" and "),
                                 LeafNode(tag="i", value="italic"),
                                 LeafNode(tag=None, value=" words inside of it.")
                             ]),
                             ParentNode(tag="ul", children=[
                                 LeafNode(tag="li", value="This is the first list item in a list block"),
                                 LeafNode(tag="li", value="This is a list item"),
                                 LeafNode(tag="li", value="This is another list item"),
                             ])
                         ])
        )

if __name__ == "__main__":
    unittest.main()
