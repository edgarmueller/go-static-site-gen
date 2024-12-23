import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "This is a text node", props = {"href": "https://www.boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev"')

    def test_leaf_node(self):
        node_a = LeafNode("p", "This is a paragraph of text.")
        node_b = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node_a.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(node_b.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_parent_node(self):
        node = ParentNode("div", [LeafNode("p", "This is a paragraph of text."), LeafNode("a", "Click me!", {"href": "https://www.google.com"})])
        self.assertEqual(node.to_html(), '<div><p>This is a paragraph of text.</p><a href="https://www.google.com">Click me!</a></div>')

if __name__ == "__main__":
    unittest.main()