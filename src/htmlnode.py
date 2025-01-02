class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        element_props = {}
        for prop in self.props:
            element_props += f' {prop}="{self.props[prop]}"'
        return element_props

    def __repr__(self):
        return (
            "HTMLNode {\n"
            f"\ttag: {self.tag}\n"
            f"\tvalue: {self.value}\n"
            f"\tchildren: {self.children}\n"
            f"\tprops: {self.props_to_html()}\n"
            "}"
        )
