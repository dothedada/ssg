import unittest
from splitnodesdelimiter import split_nodes_delimiter
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
