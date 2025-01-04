import unittest
from splitnodesdelimiter import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestNodesSplitter(unittest.TestCase):
    def test_right_assignation_with_word_in_middle(self):
        text_node = TextNode("text **bold** more text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertTrue(new_nodes[1].text_type == TextType.BOLD)

    def test_right_assignation_with_word_at_start(self):
        text_node = TextNode("**bold** more text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        self.assertTrue(new_nodes[0].text_type == TextType.BOLD)

    def test_right_assignation_with_word_at_end(self):
        text_node = TextNode("some text **bold**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        self.assertTrue(new_nodes[1].text_type == TextType.BOLD)

    def test_multiple_styled_texts(self):
        text_node = TextNode(
            "text *italic* more text, *another italic*", TextType.NORMAL
        )
        new_nodes = split_nodes_delimiter([text_node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 4)
        self.assertTrue(new_nodes[1].text_type == TextType.ITALIC)
        self.assertTrue(new_nodes[3].text_type == TextType.ITALIC)

    def test_handle_multiple_TextNode(self):
        text_node_a = TextNode("text `code`, more text", TextType.NORMAL)
        text_node_b = TextNode("more text `more code`.", TextType.NORMAL)
        new_nodes = split_nodes_delimiter(
            [text_node_a, text_node_b], "`", TextType.CODE
        )
        self.assertEqual(len(new_nodes), 6)
        self.assertTrue(new_nodes[1].text_type == TextType.CODE)
        self.assertTrue(new_nodes[4].text_type == TextType.CODE)

    def test_raise_error_unpaired_delimiters(self):
        text_node = TextNode("text **bold, more text", TextType.NORMAL)
        with self.assertRaises(Exception):
            split_nodes_delimiter([text_node], "**", TextType.BOLD)

    def test_ignores_empty_delimiters(self):
        text_node = TextNode("text ** **, more text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)

    def text_empty_nodes_list_return_empty_list(self):
        new_nodes = split_nodes_delimiter([], "**", TextType.BOLD)
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


class SplitNodesForImages(unittest.TestCase):
    def test_TextNode_without_images(self):
        node = TextNode("no images in this text", TextType.NORMAL)
        self.assertEqual(split_nodes_image([node]), [node])

    def test_TextNode_with_one_image_at_middle(self):
        node = TextNode("one links ![alt_text](www.url.com).", TextType.NORMAL)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("one links ", TextType.NORMAL),
                TextNode("alt_text", TextType.IMAGE, "www.url.com"),
                TextNode(".", TextType.NORMAL),
            ],
        )

    def test_TextNode_with_one_image_at_start(self):
        node = TextNode("![alt_text](www.url.com), text.", TextType.NORMAL)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("alt_text", TextType.IMAGE, "www.url.com"),
                TextNode(", text.", TextType.NORMAL),
            ],
        )

    def test_TextNode_with_one_image_at_end(self):
        node = TextNode("some text ![alt_text](www.url.com)", TextType.NORMAL)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("some text ", TextType.NORMAL),
                TextNode("alt_text", TextType.IMAGE, "www.url.com"),
            ],
        )

    def test_TextNode_with_multiple_images(self):
        node = TextNode(
            "text ![alt_text](www.url.com)more text![alt_text2](www.url2.com)",
            TextType.NORMAL,
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("text ", TextType.NORMAL),
                TextNode("alt_text", TextType.IMAGE, "www.url.com"),
                TextNode("more text", TextType.NORMAL),
                TextNode("alt_text2", TextType.IMAGE, "www.url2.com"),
            ],
        )

    def test_TextNode_with_multiple_images_text_between(self):
        node = TextNode(
            "![alt_text](www.url.com) more text ![alt_text2](www.url2.com)",
            TextType.NORMAL,
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("alt_text", TextType.IMAGE, "www.url.com"),
                TextNode(" more text ", TextType.NORMAL),
                TextNode("alt_text2", TextType.IMAGE, "www.url2.com"),
            ],
        )

    def test_TextNode_with_multiple_images_no_text_between(self):
        node = TextNode(
            "![alt_text](www.url.com)![alt_text2](www.url2.com)",
            TextType.NORMAL,
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("alt_text", TextType.IMAGE, "www.url.com"),
                TextNode("alt_text2", TextType.IMAGE, "www.url2.com"),
            ],
        )

    def test_TextNode_with_mixed_content_a(self):
        node = TextNode(
            "![alt_text](www.url.com) and [link](www.url2.com)",
            TextType.NORMAL,
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("alt_text", TextType.IMAGE, "www.url.com"),
                TextNode(" and [link](www.url2.com)", TextType.NORMAL),
            ],
        )

    def test_TextNode_with_mixed_content_b(self):
        node = TextNode(
            "[link](www.url2.com) and ![alt_text](www.url.com)",
            TextType.NORMAL,
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("[link](www.url2.com) and ", TextType.NORMAL),
                TextNode("alt_text", TextType.IMAGE, "www.url.com"),
            ],
        )


class SplitNodesForLinks(unittest.TestCase):
    def test_TextNode_without_links(self):
        node = TextNode("no links in this text", TextType.NORMAL)
        self.assertEqual(split_nodes_link([node]), [node])

    def test_TextNode_with_one_link_at_middle(self):
        node = TextNode("one [link](www.url.com).", TextType.NORMAL)
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("one ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "www.url.com"),
                TextNode(".", TextType.NORMAL),
            ],
        )

    def test_TextNode_with_one_link_at_start(self):
        node = TextNode("[link](www.url.com), text.", TextType.NORMAL)
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("link", TextType.LINK, "www.url.com"),
                TextNode(", text.", TextType.NORMAL),
            ],
        )

    def test_TextNode_with_one_link_at_end(self):
        node = TextNode("some text [link](www.url.com)", TextType.NORMAL)
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("some text ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "www.url.com"),
            ],
        )

    def test_TextNode_with_multiple_links(self):
        node = TextNode(
            "text [link](www.url.com)more text[link2](www.url2.com)",
            TextType.NORMAL,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("text ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "www.url.com"),
                TextNode("more text", TextType.NORMAL),
                TextNode("link2", TextType.LINK, "www.url2.com"),
            ],
        )

    def test_TextNode_with_multiple_links_text_between(self):
        node = TextNode(
            "[link](www.url.com) more text [link2](www.url2.com)",
            TextType.NORMAL,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("link", TextType.LINK, "www.url.com"),
                TextNode(" more text ", TextType.NORMAL),
                TextNode("link2", TextType.LINK, "www.url2.com"),
            ],
        )

    def test_TextNode_with_multiple_images_no_text_between(self):
        node = TextNode(
            "[link](www.url.com)[link2](www.url2.com)",
            TextType.NORMAL,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("link", TextType.LINK, "www.url.com"),
                TextNode("link2", TextType.LINK, "www.url2.com"),
            ],
        )

    def test_TextNode_with_mixed_content_a(self):
        node = TextNode(
            "[link](www.url.com) and ![alt_text](www.url2.com)",
            TextType.NORMAL,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("link", TextType.LINK, "www.url.com"),
                TextNode(" and ![alt_text](www.url2.com)", TextType.NORMAL),
            ],
        )

    def test_TextNode_with_mixed_content_b(self):
        node = TextNode(
            "![alt_text](www.url2.com) and [link](www.url.com)",
            TextType.NORMAL,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("![alt_text](www.url2.com) and ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "www.url.com"),
            ],
        )


class TextToTextnode(unittest.TestCase):
    def test_print(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEquals(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
