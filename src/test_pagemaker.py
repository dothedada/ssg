import unittest
from pagemaker import extract_title


class PageMaker(unittest.TestCase):
    def test_returns_title_clean(self):
        markdown = "# title one"
        self.assertEqual(extract_title(markdown), "title one")

    def test_returns_title_when_is_in_other_line(self):
        markdown = "\n# title one"
        self.assertEqual(extract_title(markdown), "title one")

    def test_returns_title_when_is_in_middle(self):
        markdown = "some text\n\n# title one\n\nmore text"
        self.assertEqual(extract_title(markdown), "title one")

    def test_raise_exception_if_md_has_no_title(self):
        markdown = "## subtitle"
        with self.assertRaises(Exception):
            extract_title(markdown)
