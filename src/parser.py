from blocks import markdown_to_blocks, block_to_block_type
from htmlnode import ParentNode, HTMLNode
from splitnodesdelimiter import text_to_textnodes
from textnode import text_node_to_html_node


def text_to_children(text):
    textnodes_childs = text_to_textnodes(text)
    htmlnodes_childs = []
    for textnodes_child in textnodes_childs:
        htmlnodes_childs.append(text_node_to_html_node(textnodes_child))
    return htmlnodes_childs


def clean_text(text, chars):
    lines = text.split("\n")
    chars_to_clean = chars + " "
    new_lines = []
    for line in lines:
        new_lines.append(line.strip(chars_to_clean))

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
                text = clean_text(block, ">")
                block_childs = text_to_children(text)
                children.append(ParentNode("blockquote", block_childs))

            case "unordered_list":
                text = clean_text(block, "*-")
                items = []
                for item in text.split("\n"):
                    item_childs = text_to_children(item)
                    items.append(ParentNode("li", item_childs))
                children.append(ParentNode("ul", items))

            case "ordered_list":
                items = []
                for item in block.split("\n"):
                    _, text = item.split(" ", 1)
                    item_childs = text_to_children(text)
                    items.append(ParentNode("li", item_childs))
                children.append(ParentNode("ol", items))

            case "paragraph":
                children.append(ParentNode("p", text_to_children(block)))

    return ParentNode("div", children)
