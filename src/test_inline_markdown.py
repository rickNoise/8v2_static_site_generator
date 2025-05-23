import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType, text_node_to_html_node


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("**this** is a **bold** text **node** node", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("this", TextType.BOLD),
                TextNode(" is a ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" text ", TextType.NORMAL),
                TextNode("node", TextType.BOLD),
                TextNode(" node", TextType.NORMAL)
            ]
        )

    def test_delim_italic(self):
        node = TextNode("this is _italic text_", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("this is ", TextType.NORMAL),
                TextNode("italic text", TextType.ITALIC),
            ]
        )
    
    def test_delim_code(self):
        node = TextNode("**bold** text followed by `code` and _italic_ text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("**bold** text followed by ", TextType.NORMAL),
                TextNode("code", TextType.CODE),
                TextNode(" and _italic_ text", TextType.NORMAL)
            ]
        )

    def test_all_three_delims(self):
        node = TextNode("**bold** text followed by `code` and _italic_ text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" text followed by ", TextType.NORMAL),
                TextNode("code", TextType.CODE),
                TextNode(" and ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.NORMAL)
            ]
        )