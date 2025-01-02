class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        if tag == None and value == None and children == None and props == None:
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
            self.props = None

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return "No props to parse"
        element_props = ""
        for prop in self.props:
            element_props += f' {prop}="{self.props[prop]}"'
        return element_props

    def __repr__(self):
        repr = "HTMLNode {\n"
        if self.tag:
            repr += f"\ttag: {self.tag}\n"
        if self.value:
            repr += f"\tvalue: {self.value}\n"
        if self.children:
            repr += f"\tchildren: {self.children}\n"
        if self.props:
            repr += f"\tprops: {self.props_to_html()}\n"
        repr += "}"

        return repr
