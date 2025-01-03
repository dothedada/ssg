from textnode import TextNode


def split_nodes_delimiter(old_nodes, delimiter, type_text):
    new_nodes = []

    if not len(old_nodes):
        return new_nodes

    for node in old_nodes:
        text_split = node.text.split(delimiter)

        if len(text_split) % 2 == 0:
            raise Exception("Invalid Markdown syntax, text types must be paired")

        base_type = node.text_type
        for i in range(len(text_split)):
            if not text_split[i]:
                continue

            if not len(text_split[i].strip()):
                last_string = new_nodes[len(new_nodes) - 1].text
                text_split[i + 1] = last_string + text_split[i + 1]
                new_nodes.pop(len(new_nodes) - 1)
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(text_split[i], base_type))
            else:
                new_nodes.append(TextNode(text_split[i], type_text))

    return new_nodes
