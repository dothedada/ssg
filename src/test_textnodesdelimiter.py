import unittest
from splitnodesdelimiter import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)
from textnode import TextNode, TextType


class TestNodesSplitter(unittest.TestCase):
    def test_right_assignation_with_word_in_middle(self):
        text_node = TextNode("text **bold** more text", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD_TEXT)
        self.assertEqual(len(new_nodes), 3)
        self.assertTrue(new_nodes[1].text_type == TextType.BOLD_TEXT)

    def test_right_assignation_with_word_at_start(self):
        text_node = TextNode("**bold** more text", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD_TEXT)
        self.assertEqual(len(new_nodes), 2)
        self.assertTrue(new_nodes[0].text_type == TextType.BOLD_TEXT)

    def test_right_assignation_with_word_at_end(self):
        text_node = TextNode("some text **bold**", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD_TEXT)
        self.assertEqual(len(new_nodes), 2)
        self.assertTrue(new_nodes[1].text_type == TextType.BOLD_TEXT)

    def test_multiple_styled_texts(self):
        text_node = TextNode(
            "text *italic* more text, *another italic*", TextType.NORMAL_TEXT
        )
        new_nodes = split_nodes_delimiter([text_node], "*", TextType.ITALIC_TEXT)
        self.assertEqual(len(new_nodes), 4)
        self.assertTrue(new_nodes[1].text_type == TextType.ITALIC_TEXT)
        self.assertTrue(new_nodes[3].text_type == TextType.ITALIC_TEXT)

    def test_handle_multiple_TextNode(self):
        text_node_a = TextNode("text `code`, more text", TextType.NORMAL_TEXT)
        text_node_b = TextNode("more text `more code`.", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter(
            [text_node_a, text_node_b], "`", TextType.CODE_TEXT
        )
        self.assertEqual(len(new_nodes), 6)
        self.assertTrue(new_nodes[1].text_type == TextType.CODE_TEXT)
        self.assertTrue(new_nodes[4].text_type == TextType.CODE_TEXT)

    def test_mantain_the_base_TextType(self):
        text_node = TextNode("text *italic*, more text", TextType.BOLD_TEXT)
        new_nodes = split_nodes_delimiter([text_node], "*", TextType.ITALIC_TEXT)
        self.assertEqual(len(new_nodes), 3)
        self.assertTrue(new_nodes[0].text_type == TextType.BOLD_TEXT)
        self.assertTrue(new_nodes[1].text_type == TextType.ITALIC_TEXT)
        self.assertTrue(new_nodes[2].text_type == TextType.BOLD_TEXT)

    def test_raise_error_unpaired_delimiters(self):
        text_node = TextNode("text **bold, more text", TextType.NORMAL_TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([text_node], "**", TextType.BOLD_TEXT)

    def test_ignores_empty_delimiters(self):
        text_node = TextNode("text ** **, more text", TextType.NORMAL_TEXT)
        new_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD_TEXT)
        self.assertEqual(len(new_nodes), 1)

    def text_empty_nodes_list_return_empty_list(self):
        new_nodes = split_nodes_delimiter([], "**", TextType.BOLD_TEXT)
        self.assertIsInstance(new_nodes, list)
        self.assertEqual(len(new_nodes), 0)


class ExtractMarkdownImg(unittest.TestCase):
    def test_returns_list_with_tuples(self):
        text = (
            "text ![alt_text_1](https://url.com/1) and ![alt_text_2](https://url.com/2)"
        )
        image_links = extract_markdown_images(text)
        self.assertEqual(len(image_links), 2)
        self.assertIsInstance(image_links, list)
        for link in image_links:
            self.assertIsInstance(link, tuple)

    def test_handle_images_without_altText(self):
        text = "text ![](https://url.com/1)"
        image_links = extract_markdown_images(text)
        self.assertEqual(len(image_links), 1)
        self.assertEqual(image_links[0][0], "")
        self.assertEqual(image_links[0][1], "https://url.com/1")

    def test_raise_error_for_images_without_url(self):
        text = "text ![alt_text_1]()"
        with self.assertRaises(ValueError):
            extract_markdown_images(text)

    def test_returns_empty_list_if_text_empty(self):
        text = ""
        image_links = extract_markdown_images(text)
        self.assertEqual(len(image_links), 0)

    def test_data_order_is_alt_text_followed_by_url(self):
        text = "text ![alt_text_1](https://url.com/1)"
        image_links = extract_markdown_images(text)
        self.assertEqual(image_links[0][0], "alt_text_1")
        self.assertEqual(image_links[0][1], "https://url.com/1")

    def test_dont_parse_links_data_type(self):
        text = "text [link_name](https://url.com/1)"
        image_links = extract_markdown_images(text)
        self.assertEqual(len(image_links), 0)


class ExtractMarkdownLink(unittest.TestCase):
    def test_returns_list_with_tuples(self):
        text = (
            "text [link_text_1](https://url.com/1) and [link_text_2](https://url.com/2)"
        )
        link_links = extract_markdown_links(text)
        self.assertEqual(len(link_links), 2)
        self.assertIsInstance(link_links, list)
        for link in link_links:
            self.assertIsInstance(link, tuple)

    def test_use_url_as_text_if_no_link_text_is_provided(self):
        text = "text [](https://url.com/1)"
        image_links = extract_markdown_links(text)
        self.assertEqual(len(image_links), 1)
        self.assertEqual(image_links[0][0], "https://url.com/1")
        self.assertEqual(image_links[0][1], "https://url.com/1")

    def test_raise_error_links_without_url(self):
        text = "text [alt_text_1]()"
        with self.assertRaises(ValueError):
            extract_markdown_links(text)

    def test_returns_empty_list_if_text_empty(self):
        text = ""
        link_links = extract_markdown_links(text)
        self.assertEqual(len(link_links), 0)

    def test_data_order_is_alt_text_followed_by_url(self):
        text = "text [link_text_1](https://url.com/1)"
        link_links = extract_markdown_links(text)
        self.assertEqual(link_links[0][0], "link_text_1")
        self.assertEqual(link_links[0][1], "https://url.com/1")

    def test_dont_parse_links_data_type(self):
        text = "text ![link_name](https://url.com/1)"
        link_links = extract_markdown_links(text)
        self.assertEqual(len(link_links), 0)
