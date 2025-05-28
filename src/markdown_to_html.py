from htmlnode import ParentNode
from textnode import TextType, TextNode, text_node_to_html_node
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from inline_markdown import text_to_textnodes
import re


def markdown_to_html_node(markdown):
    """
    Converts a full markdown document into a single parent HTMLNode. 
    That one parent HTMLNode should (obviously) contain many child HTMLNode objects 
    representing the nested elements."""
    
    # this list will hold all of the block HTMLNodes
    # this list will become the children for the master ParentNode
    block_html_node_list = []

    # Split the markdown into block
    blocks = markdown_to_blocks(markdown)

    # Loop over each block
    for block in blocks:
        
        # Determine the type of block
        block_type = block_to_block_type(block)

        # Based on the type of block, create a new HTMLNode with the proper data
        match block_type:
            case BlockType.PARAGRAPH:
                children = text_to_children(block)
                parent = ParentNode(
                    block_to_block_html_tags(block),
                    children,
                    None
                )
            case BlockType.HEADING:
                # remove the heading prefix before processing for children
                # e.g. "### Heading" -> "Heading"
                children = text_to_children(strip_heading_prefix(block))
                parent = ParentNode(
                    block_to_block_html_tags(block),
                    children,
                    None
                )
            case BlockType.CODE:
                # remove the first and last lines of the code block
                # to get the inner text
                lines = block.split("\n")
                cleaned_lines = lines[1:-1]
                cleaned_text = "\n".join(cleaned_lines) + "\n"
                # custom building of children to account for code block special case
                # no inline processing
                children = [text_node_to_html_node(TextNode(cleaned_text, TextType.CODE))]
                parent = ParentNode(
                    "pre",
                    children,
                    None
                )
            case BlockType.QUOTE:
                # removing leading ">" on each line before processing quoted text
                # note that any leading or trailing spaces are stripped in the processing
                lines = block.split("\n")
                cleaned_lines = []
                for line in lines:
                    cleaned_lines.append(line[1:])
                cleaned_text = "\n".join(cleaned_lines)
                children = text_to_children(cleaned_text)
                parent = ParentNode(
                    block_to_block_html_tags(block),
                    children,
                    None
                )
            case BlockType.OLIST:
                # remove the number prefixes on each line
                cleaned_block = strip_prefixes_from_ordered_list_md(block)
                lines = cleaned_block.split("\n")
                children = []
                for line in lines:
                    children.append(
                        ParentNode(
                            "li",
                            text_to_children(line),
                            None
                        )
                    )
                parent = ParentNode(
                    block_to_block_html_tags(block),
                    children,
                    None
                )
            case BlockType.ULIST:
                # remove the list prefix on each line
                cleaned_block = strip_prefixes_from_unordered_list_md(block)
                lines = cleaned_block.split("\n")
                children = []
                for line in lines:
                    children.append(
                        ParentNode(
                            "li",
                            text_to_children(line),
                            None
                        )
                    )
                parent = ParentNode(
                    block_to_block_html_tags(block),
                    children,
                    None
                )
            case _:
                raise Exception("problem parsing markdown")
        
        # adds this block's HTMLNode representation to the master list
        block_html_node_list.append(parent)

        """
        Assign the proper child HTMLNode objects to the block node. 
        I created a shared text_to_children(text) function that works for all block types. 
        It takes a string of text and returns a list of HTMLNodes that represent 
        the inline markdown using previously created functions (think TextNode -> HTMLNode).
        """

        """
        The "code" block is a bit of a special case: 
        it should not do any inline markdown parsing of its children. 
        I didn't use my text_to_children function for this block type, 
        I manually made a TextNode and used text_node_to_html_node
        """
    
    # Make all the block nodes children 
    # under a single parent HTML node (which should just be a div) and return it.
    return ParentNode("div", block_html_node_list, None)


def text_to_children(text):
    # takes in a block, which is a string of markdown
    # returns a list of HTMLNodes that represent the inline markdown
    # using previous created functions
    # (think TextNode -> HTMLNode)
    children = []
    # replace newlines with spaces in the text before processing
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line.strip())
    cleaned_text = " ".join(cleaned_lines)
    text_nodes = text_to_textnodes(cleaned_text)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def block_to_block_html_tags(block):
    """ takes in a block, which is a string of markdown, returns a string holding the opening html tag (as a string) required for that block """
    
    block_type = block_to_block_type(block)

    match block_type:
        case BlockType.PARAGRAPH:
            # Paragraphs should be surrounded by a <p> tag.
            return "p"
        case BlockType.HEADING:
            # Headings should be surrounded by a <h1> to <h6> tag, depending on the number of # characters.
            pattern = r"^(#+) "
            match = re.search(pattern, block)
            heading_substring = match.group()
            heading_size = len(heading_substring) - 1
            return f"h{heading_size}"
        case BlockType.CODE:
            # Code blocks should be surrounded by a <code> tag nested inside a <pre> tag.
            return "code"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.OLIST:
            return "ol"
        case BlockType.ULIST:
            return "ul"
        

def strip_heading_prefix(text):
    pattern = r"^(#+) "
    match = re.search(pattern, text)
    heading_substring = match.group()
    heading_length = len(heading_substring)
    return text[heading_length:]


def extract_title(markdown):
    """
    It should pull the h1 header from the markdown file (the line that starts with a single #) and return it.
    If there is no h1 header, raise an exception.
    extract_title("# Hello") should return "Hello" (strip the # and any leading or trailing whitespace)
    """
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return strip_heading_prefix(line).strip()
    raise Exception("Markdown file does not contain an h1 header!")


def strip_prefixes_from_ordered_list_md(md):
    lines = md.split("\n")
    cleaned_lines = []
    for i in range(len(lines)):
        j = len(str(i))
        cleaned_lines.append(lines[i][j+2:])
    cleaned_md = "\n".join(cleaned_lines)
    return cleaned_md


def strip_prefixes_from_unordered_list_md(md):
    lines = md.split("\n")
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line[2:])
    return "\n".join(cleaned_lines)