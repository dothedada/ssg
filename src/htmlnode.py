class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        if tag is None and value is None and children is None and props is None:
            raise Exception("HTMLNode cannot be empty")
        self.tag = tag
        self.value = value
        if isinstance(children, list):
            self.children = children
        else:
            self.children = None
        if isinstance(props, dict):
            self.props = props
        else:
            self.props = ""

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return self.props
        element_props = ""
        for prop in self.props:
            element_props += f' {prop}="{self.props[prop]}"'
        return element_props

    def __repr__(self):
        repr = "HTMLNode {\n"

        for key, value in self.__dict__.items():
            if not value:
                continue
            if key == "props":
                repr += f"\tprops: {self.props_to_html()}\n"
            else:
                repr += f"\t{key}: {value}\n"
        repr += "}"

        return repr


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("A leaf node must have a value")
        if not self.tag:
            return f"{self.value}"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def __render_childs(self):
        childs_rendered = ""
        for child in self.children:
            if not isinstance(child, HTMLNode):
                raise TypeError(f"Child nodes must be HTMLNode instances: {child}.")
            childs_rendered += child.to_html()
        return childs_rendered

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children or not len(self.children):
            raise ValueError("ParentNode must have at least one child node")
        return f"<{self.tag}{self.props}>{self.__render_childs()}</{self.tag}>"
