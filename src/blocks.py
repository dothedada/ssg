import re

from htmlnode import ParentNode
from splitnodesdelimiter import text_to_textnodes
from textnode import text_node_to_html_node


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


def text_to_children(text):
    textnodes_childs = text_to_textnodes(text)
    htmlnodes_childs = []
    for textnodes_child in textnodes_childs:
        htmlnodes_childs.append(text_node_to_html_node(textnodes_child))
    return htmlnodes_childs


def clean_text(text, chars=""):
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip(chars).strip())

    return "\n".join(new_lines)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case "heading":
                h_level, text = block.split(" ", 1)
                block_childs = text_to_children(text)
                heading = ParentNode(f"h{len(h_level)}", block_childs)
                children.append(heading)

            case "code":
                block_childs = text_to_children(block.strip("`\n "))
                code = ParentNode("pre", [ParentNode("code", block_childs)])
                children.append(code)

            case "quote":
                clean_block = clean_text(block, ">")
                text = " ".join(clean_block.split("\n"))
                block_childs = text_to_children(text)
                children.append(ParentNode("blockquote", block_childs))

            case "unordered_list":
                items = []
                for item in block.split("\n"):
                    _, text = item.split(" ", 1)
                    item_childs = text_to_children(clean_text(text))
                    items.append(ParentNode("li", item_childs))
                children.append(ParentNode("ul", items))

            case "ordered_list":
                items = []
                for item in block.split("\n"):
                    _, text = item.split(" ", 1)
                    item_childs = text_to_children(clean_text(text))
                    items.append(ParentNode("li", item_childs))
                children.append(ParentNode("ol", items))

            case "paragraph":
                text = " ".join(block.split("\n"))
                children.append(ParentNode("p", text_to_children(text)))

    return ParentNode("div", children)
