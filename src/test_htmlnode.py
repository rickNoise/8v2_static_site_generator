import unittest

from htmlnode import HTMLNode


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
        

if __name__ == "__main__":
    unittest.main()
