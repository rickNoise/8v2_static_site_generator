import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("a", "link_value", None, props)
        expected_result = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(
            node.props_to_html(),
            expected_result
        )
    
    def test_props_to_html_empty_props(self):
        props = None
        node = HTMLNode()
        expected_result = ""
        self.assertEqual(
            node.props_to_html(),
            expected_result
        )

    def test_props_to_html_2(self):
        props = {
            "src": "url/of/image.jpg",
            "alt": "Description of image",
        }
        node = HTMLNode("img", None, None, props)
        expected_result = ' src="url/of/image.jpg" alt="Description of image"'
        self.assertEqual(
            node.props_to_html(),
            expected_result
        )
 
    def test_repr(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("a", "link_value", None, props)
        expected_result = "HTMLNode(tag=a, value=link_value, children=None, props={'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(node.__repr__(), expected_result)


class TestLeafNode(unittest.TestCase):
    def test_leaf_node_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(
            node.to_html(),
            "<p>This is a paragraph of text.</p>"
        )
    
    def test_leaf_node_to_html_2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )
    
    def test_leaf_node_to_html_3(self):
        node = LeafNode(None, "Hello world!")
        self.assertEqual(
            node.to_html(),
            "Hello world!"
        )
    
    def test_leaf_node_repr(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.__repr__(),
            "LeafNode(a, Click me!, {'href': 'https://www.google.com'})"
        )
 

class TestParentNode(unittest.TestCase):
    def test_parent_node_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
    
    def test_parent_node_with_props_to_html(self):
        node = ParentNode(
            "a", 
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {
                "href": "www.google.com"
            }
        )
        self.assertEqual(
            node.to_html(),
            '<a href="www.google.com"><b>Bold text</b>Normal text<i>italic text</i>Normal text</a>'
        )
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
