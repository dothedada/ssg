import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, type_text):
    new_nodes = []

    if not len(old_nodes):
        return new_nodes

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        text_split = node.text.split(delimiter)

        if len(text_split) % 2 == 0:
            raise Exception("Invalid Markdown syntax, not closed section")

        for i in range(len(text_split)):
            if not text_split[i]:
                continue

            if not len(text_split[i].strip()):
                last_string = new_nodes[len(new_nodes) - 1].text
                text_split[i + 1] = last_string + text_split[i + 1]
                new_nodes.pop(len(new_nodes) - 1)
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(text_split[i], TextType.NORMAL))
            else:
                new_nodes.append(TextNode(text_split[i], type_text))

    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    images_data = re.findall(pattern, text)
    for _, link in images_data:
        if link == "":
            raise ValueError("Image url cannot be empty")

    return images_data


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    links_data = re.findall(pattern, text)
    for i in range(len(links_data)):
        if links_data[i][1] == "":
            raise ValueError("link url cannot be empty")
        if links_data[i][0] == "":
            links_data[i] = (links_data[i][1], links_data[i][1])

    return links_data


def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        images_data = extract_markdown_images(text)

        if len(images_data) == 0:
            new_nodes.append(old_node)
            continue

        for image in images_data:
            sections = text.split(f"![{image[0]}]({image[1]})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))

            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

            text = sections[1]

        if text != "":
            new_nodes.append(TextNode(text, TextType.NORMAL))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        links = extract_markdown_links(text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link in links:
            sections = text.split(f"[{link[0]}]({link[1]})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))

            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            text = sections[1]

        if text != "":
            new_nodes.append(TextNode(text, TextType.NORMAL))

    return new_nodes


def text_to_textnodes(text):
    nodes = []
    nodes.append(TextNode(text, TextType.NORMAL))
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)

    print(nodes)
    return nodes
