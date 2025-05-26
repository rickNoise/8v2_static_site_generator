def markdown_to_blocks(markdown):
    pre_stripped_blocks = markdown.split("\n\n")
    stripped_blocks = []
    for pre_stripped_block in pre_stripped_blocks:
        if pre_stripped_block != "":
            stripped_blocks.append(pre_stripped_block.strip())
    return stripped_blocks