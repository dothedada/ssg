import re
from enum import Enum


class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"


def markdown_to_blocks(markdown):
    pattern = r"\n[ \t]*\n"
    blocks = []

    for section in re.split(pattern, markdown):
        if section.strip(" \t\n") == "":
            continue
        else:
            blocks.append(section.strip(" \t\n"))

    return blocks


def check_all_lines(regex, text):
    lines = filter(lambda item: item != "", text.split("\n"))
    count = 1
    for line in lines:
        match = re.match(regex, line)
        if not match:
            return False
        counter = re.match(r"^\d+", match.group(0))
        if not counter:
            continue
        if int(counter.group(0)) != count:
            return False
        count += 1

    return True


def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return "heading"
    if re.match(r"^```[\s\S]*```$", block):
        return "code"
    if check_all_lines(r"^>", block):
        return "quote"
    if check_all_lines(r"^\* ", block):
        return "unordered_list"
    if check_all_lines(r"^\- ", block):
        return "unordered_list"
    if check_all_lines(r"^\d+\. ", block):
        return "ordered_list"

    return "paragraph"
