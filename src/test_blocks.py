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

    def test_strips_whitespace(self):
        markdown = "  block1  \n\n   block2   \n\nblock3\t\n\nblock4\n"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(blocks[0], "block1")
        self.assertEqual(blocks[1], "block2")
        self.assertEqual(blocks[2], "block3")
        self.assertEqual(blocks[3], "block4")

    def test_mixed_whitespace(self):
        markdown = "\t  block1\n \t \n\nblock2\t \n"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "block1")
        self.assertEqual(blocks[1], "block2")

    def test_leading_blank_lines(self):
        markdown = """


        # First block"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0], "# First block")

    def test_trailing_blank_lines(self):
        markdown = """# Last block



        """
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0], "# Last block")

    def test_mixed_whitespace_between_blocks(self):
        markdown = """block1
     
    \t
    \t  
    block2"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "block1")
        self.assertEqual(blocks[1], "block2")

    def test_preserve_internal_whitespace(self):
        markdown = """# Block with    spaces
    and\ttabs
    intact

# Next block"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "# Block with    spaces\n    and\ttabs\n    intact")

    def test_complex_whitespace(self):
        markdown = """   
block1
\t  
   \t
block2
  """
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "block1")
        self.assertEqual(blocks[1], "block2")
