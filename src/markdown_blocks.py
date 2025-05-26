from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith((
        "# ",
        "## ",
        "### ",
        "#### ",
        "##### ",
        "###### ",
    )):
        return BlockType.HEADING
    if (
        len(lines) > 1 
        and lines[0].startswith("```")
        and lines[-1].startswith("```")
    ):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        current_number = 1
        for line in lines:
            if not line.startswith(f"{str(current_number) + ". "}"):
                return BlockType.PARAGRAPH
            current_number += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    pre_stripped_blocks = markdown.split("\n\n")
    stripped_blocks = []
    for pre_stripped_block in pre_stripped_blocks:
        if pre_stripped_block != "":
            stripped_blocks.append(pre_stripped_block.strip())
    return stripped_blocks
