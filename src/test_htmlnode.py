import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class HTMLNodeTest(unittest.TestCase):
    def test_node_not_empty(self):
        with self.assertRaises(Exception):
            HTMLNode()

    def test_to_html_not_implemented_on_parent(self):
        html_node = HTMLNode(tag="a")
        with self.assertRaises(NotImplementedError):
            html_node.to_html()

    def test_unfold_pops(self):
        dummy_props = {
            "url": "https://cv.mmejia.com",
            "alt": "My website",
        }
        html_node = HTMLNode(props=dummy_props)
        for key, value in dummy_props.items():
            self.assertTrue(key in html_node.props_to_html())
            self.assertTrue(value in html_node.props_to_html())

    def test_repr_with_all_properties(self):
        html_node = HTMLNode(
            tag="div",
            value="Hello",
            children=["child1", "child2"],
            props={"class": "container", "id": "main"},
        )
        expected = (
            "HTMLNode {\n"
            "\ttag: div\n"
            "\tvalue: Hello\n"
            "\tchildren: ['child1', 'child2']\n"
            '\tprops:  class="container" id="main"\n'
            "}"
        )
        self.assertEqual(repr(html_node), expected)


class LeafNodeTest(unittest.TestCase):
    def test_allways_passValue(self):
        with self.assertRaises(TypeError):
            LeafNode()

    def test_tag_empty_renders_text_with_no_tag(self):
        tag = ""
        text = "some random text"
        leaf_node = LeafNode(tag=tag, value=text)
        self.assertTrue(text in leaf_node.to_html())
        self.assertFalse("<" in leaf_node.to_html())

    def test_tag_none_renders_text(self):
        text = "some random text"
        leaf_node = LeafNode(tag=None, value=text)
        self.assertTrue(text in leaf_node.to_html())

    def test_tag_empty_string(self):
        tag = ""
        text = "some random text"
        leaf_node = LeafNode(tag=tag, value=text)
        self.assertFalse("<" in leaf_node.to_html())

    def test_tag_renders_html_label(self):
        tag = "a"
        text = "link"
        props = {"href": "https://mmejia.com", "target": "_blank"}
        leaf_node = LeafNode(tag=tag, value=text, props=props)
        self.assertEqual(
            leaf_node.to_html(), '<a href="https://mmejia.com" target="_blank">link</a>'
        )


class ParentNodeTest(unittest.TestCase):
    def test_ParentNode_is_instance_of_HTMLNode(self):
        parent_node = ParentNode(
            tag="p", children=[LeafNode(tag="b", value="some text")]
        )
        self.assertIsInstance(parent_node, HTMLNode)

    def test_tag_cannot_be_empty_string(self):
        tag = ""
        children = [
            LeafNode("a", "random text"),
        ]
        with self.assertRaises(ValueError):
            ParentNode(tag, children=children)

    def test_children_must_be_passed(self):
        tag = "div"
        children = []
        with self.assertRaises(ValueError):
            ParentNode(tag, children=children)

    def test_all_children_must_be_HTMLNode_instances(self):
        tag = "div"
        children = [
            LeafNode("a", "random text"),
            "abc",
            LeafNode("a", "more random text"),
        ]
        with self.assertRaises(TypeError):
            ParentNode(tag, children=children)

    def test_parent_can_handle_nested_ParentNode(self):
        leaf_nodes = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
        ]
        childs = []
        childs.append(ParentNode(tag="p", children=leaf_nodes))
        childs.append(LeafNode("p", "Normal text"))
        node = ParentNode(tag="div", children=childs)

        self.assertEqual(
            node.to_html(),
            "<div><p><b>Bold text</b>Normal text<i>italic text</i></p><p>Normal text</p></div>",
        )

    def test_parent_can_handle_multiple_LeafNode(self):
        child_nodes = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        node = ParentNode(
            tag="p",
            children=child_nodes,
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )


if __name__ == "__main__":
    unittest.main()
