def markdown_to_blocks(markdown):
    blocks = []

    for section in markdown.split("\n\n"):
        if section.strip("\n ") == "":
            continue
        else:
            blocks.append(section)

    return blocks
