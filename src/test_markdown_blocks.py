import unittest

from markdown_blocks import (
    markdown_to_blocks,
    BlockType,
    block_to_block_type,
)


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        md = "### Heading 3"
        er = BlockType.HEADING
        self.assertEqual(block_to_block_type(md), er)
    
    def test_code(self):
        md = "```\nthis is a \ncode block\n```"
        er = BlockType.CODE
        self.assertEqual(block_to_block_type(md), er)
    
    def test_quote(self):
        md = ">this is a quote\n> block\n>for testing"
        er = BlockType.QUOTE
        self.assertEqual(block_to_block_type(md), er)

    def test_ulist(self):
        md = "- This is a\n- unordered list\n- with three lines"
        er = BlockType.ULIST
        self.assertEqual(block_to_block_type(md), er)
    
    def test_olist(self):
        md = """1. one
2. two
3. three
4. four
5. five
6. six
7. seven
8. eight
9. nine
10. ten"""
        er = BlockType.OLIST
        self.assertEqual(block_to_block_type(md), er) 

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
       
    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
