import re


def markdown_to_blocks(markdown):
    pattern = r"\n[ \t]*\n"
    blocks = []

    for section in re.split(pattern, markdown):
        if section.strip(" \t\n") == "":
            continue
        else:
            blocks.append(section.strip(" \t\n"))

    return blocks


def block_to_block_type(block):
    pattern = r"^(#{1,6}|```|>|[*-]|\d+\.) *\w"
    print(re.match(pattern, block))
