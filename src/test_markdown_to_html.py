import unittest

from markdown_to_html import (
    markdown_to_html_node,
    block_to_block_html_tags,
    text_to_children,
    strip_heading_prefix,
    strip_prefixes_from_ordered_list_md,
    strip_prefixes_from_unordered_list_md,
)

from htmlnode import LeafNode, ParentNode


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_heading(self):
        md = """
### Heading level 3

And then some paragraph text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>Heading level 3</h3><p>And then some paragraph text</p></div>"
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_quoted_block(self):
        md = """
>This is a block
> of quoted text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a block of quoted text</blockquote></div>"
        )

    def test_olist_block(self):
        md = """
1. **bold**
2. _italic_
3. `code`
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li><b>bold</b></li><li><i>italic</i></li><li><code>code</code></li></ol></div>"
        )
    
    def test_ulist_block(self):
        md = """
- **bold**
- _italic_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><b>bold</b></li><li><i>italic</i></li></ul></div>"
        )

class TestHelperFunctions(unittest.TestCase):
    def test_text_to_children_paragraph(self):
        text = "this is a **paragraph**"
        children = text_to_children(text)
        children_as_html = []
        for child in children:
            children_as_html.append(child.to_html())
        exp_out = [LeafNode(None, "this is a ", None).to_html(), LeafNode("b", "paragraph", None).to_html()]
        self.assertListEqual(
            children_as_html,
            exp_out
        )


    def test_block_to_block_html_tags_paragraph(self):
        block = "this is a \nparagraph"
        exp_out = "p"
        self.assertEqual(block_to_block_html_tags(block), exp_out)

    def test_block_to_block_html_tags_heading(self):
        block = "### Size 3 Heading"
        exp_out = "h3"
        self.assertEqual(block_to_block_html_tags(block), exp_out)

    def test_block_to_block_html_tags_code(self):
        block = "```\nthis is a code block\nsecond line of code\n```"
        exp_out = "code"
        self.assertEqual(block_to_block_html_tags(block), exp_out)

    def test_block_to_block_html_tags_quote(self):
        block = ">This is a quote block \n> with a few lines\n>In the block"
        exp_out = "blockquote"
        self.assertEqual(block_to_block_html_tags(block), exp_out)
    
    def test_block_to_block_html_tags_olist(self):
        block = "1. This is an ordered list\n2. with three\n3. lines"
        exp_out = "ol"
        self.assertEqual(block_to_block_html_tags(block), exp_out)
    
    def test_block_to_block_html_tags_ulist(self):
        block = "- This is an unordered list\n- with three\n- lines"
        exp_out = "ul"
        self.assertEqual(block_to_block_html_tags(block), exp_out)


    def test_strip_heading_prefix(self):
        text = "### This is a level 3 heading"
        exp_out = "This is a level 3 heading"
        self.assertEqual(strip_heading_prefix(text), exp_out)
    

    def test_strip_prefixes_from_ordered_list_md(self):
        md = """
1. **bold**
2. _italic_
3. `code`
4. four
5. five
6. six
7. seven
8. eight
9. nine
10. ten
11. eleven
"""
        exp_out = """
**bold**
_italic_
`code`
four
five
six
seven
eight
nine
ten
eleven
"""
        self.assertEqual(
            strip_prefixes_from_ordered_list_md(md),
            exp_out
        )
    

    def test_strip_prefixes_from_unordered_list_md(self):
        md = """
- one
- two
"""
        exp_out = """
one
two
"""
        self.assertEqual(
            strip_prefixes_from_unordered_list_md(md), 
            exp_out
        )