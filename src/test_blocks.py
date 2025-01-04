import unittest
from blocks import markdown_to_blocks


class MD_to_Blocks(unittest.TestCase):
    def test_correct_amount_of_blocks(self):
        markdown = """
# blok 1

block 2

* block 3
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 3)

    def test_triple_or_more_spaces_count_as_double(self):
        markdown = """
# blok 1


block 2



* block 3
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 3)

    def test_empty_document_create_empty_block(self):
        markdown = ""

        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 0)

    def test_single_break_doesnot_create_new_block(self):
        markdown = """
block1
block1
block1
"""

        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 1)
