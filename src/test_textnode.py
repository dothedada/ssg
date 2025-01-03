import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node_a = TextNode("This is a bold node", TextType.BOLD)
        node_b = TextNode("This is a bold node", "bold")
        self.assertEqual(node_a, node_b)

    def test_eq_link(self):
        node_a = TextNode("link node", TextType.LINK, "https://mmejia.com")
        node_b = TextNode("link node", "links", "https://mmejia.com")
        self.assertEqual(node_a, node_b)

    def test_diff_eq(self):
        node_a = TextNode("This is a bold node", TextType.BOLD)
        node_b = TextNode("This is another bold node", "bold")
        self.assertNotEqual(node_a, node_b)

    def test_diff_link(self):
        node_a = TextNode("link node", TextType.LINK, "https://mmejia.com")
        node_b = TextNode("other link node", "links", "https://cv.mmejia.com")
        self.assertNotEqual(node_a, node_b)

    def test_TextType_validation_exeption(self):
        with self.assertRaises(ValueError):
            TextNode("test", "wrongType")


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_only_accepst_TextNode(self):
        with self.assertRaises(TypeError):
            text_node_to_html_node("noup")

    def test_none_input(self):
        with self.assertRaises(TypeError):
            text_node_to_html_node(None)

    def test_create_raw_text_node(self):
        text_node = TextNode("sample text", TextType.NORMAL)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "")
        self.assertEqual(html_node.value, "sample text")

    def test_create_bold_text_node(self):
        text_node = TextNode("sample bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "sample bold text")

    def test_create_italic_text_node(self):
        text_node = TextNode("sample italic text", "italic")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "sample italic text")

    def test_create_link_text_node(self):
        text_node = TextNode("sample link text", "links", "https://cv.mmejia.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "sample link text")
        self.assertTrue('href="https://cv.mmejia.com"' in html_node.to_html())

    def test_create_image_text_node(self):
        text_node = TextNode(
            "this is the alt text", TextType.IMAGE, "https://this.is.the/source/text"
        )
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertTrue('alt="this is the alt text"' in html_node.to_html())
        self.assertTrue('src="https://this.is.the/source/text"' in html_node.to_html())


if __name__ == "__main__":
    unittest.main()
