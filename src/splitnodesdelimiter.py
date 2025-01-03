from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, type_text):
    new_nodes = []
    for node in old_nodes:
        text_split = node.text.split(delimiter)
        for i in range(len(text_split)):
            if not text_split[i]:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(text_split[i], TextType.NORMAL_TEXT))
            else:
                new_nodes.append(TextNode(text_split[i], type_text))
    return new_nodes
