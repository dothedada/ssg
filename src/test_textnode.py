import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node_a = TextNode("This is a bold node", TextType.BOLD_TEXT)
        node_b = TextNode("This is a bold node", "bold")
        self.assertEqual(node_a, node_b)

    def test_eq_link(self):
        node_a = TextNode("This is a link node", TextType.LINKS, "https://mmejia.com")
        node_b = TextNode("This is a link node", "links", "https://mmejia.com")
        self.assertEqual(node_a, node_b)

    def test_eq(self):
        node_a = TextNode("This is a bold node", TextType.BOLD_TEXT)
        node_b = TextNode("This is another bold node", "bold")
        self.assertNotEqual(node_a, node_b)

    def test_diff_link(self):
        node_a = TextNode("This is a link", TextType.LINKS, "https://mmejia.com")
        node_b = TextNode("This is another link", "links", "https://cv.mmejia.com")
        self.assertNotEqual(node_a, node_b)


if __name__ == "__main__":
    unittest.main()
