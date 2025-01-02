import unittest
from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
