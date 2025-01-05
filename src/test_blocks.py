import unittest
from blocks import markdown_to_blocks, block_to_block_type


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


class ToBlockType(unittest.TestCase):
    def test_return_heading_type(self):
        block_h1 = "# heading"
        block_h2 = "## heading"
        block_h3 = "### heading"
        block_h4 = "#### heading"
        block_h5 = "##### heading"
        block_h6 = "###### heading"
        self.assertEqual(block_to_block_type(block_h1), "heading")
        self.assertEqual(block_to_block_type(block_h2), "heading")
        self.assertEqual(block_to_block_type(block_h3), "heading")
        self.assertEqual(block_to_block_type(block_h4), "heading")
        self.assertEqual(block_to_block_type(block_h5), "heading")
        self.assertEqual(block_to_block_type(block_h6), "heading")

    def test_heading_hash_must_have_space_from_text(self):
        block = "#heading 1"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_code_block_must_have_opening_and_closing_backticks(self):
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), "code")

    def test_block_must_start_with_3backtick_to_evaluate_as_code_block(self):
        block_a = "``\nno code"
        self.assertEqual(block_to_block_type(block_a), "paragraph")

    def test_all_lines_must_start_morethan_to_make_quote(self):
        block_a = "> 1\n> 2\n> 3"
        block_b = "> 1\n>2\n>3"
        block_c = ">1\n2\n> 3"
        self.assertEqual(block_to_block_type(block_a), "quote")
        self.assertEqual(block_to_block_type(block_b), "quote")
        self.assertEqual(block_to_block_type(block_c), "paragraph")

    def test_all_lines_must_start_asteris_or_minus_and_space_to_make_ul(self):
        block_a = "* 1\n* 2\n* 3\n"
        block_b = "* 1\n*2a\n * 3\n"
        block_c = "* 1\n* 2\n 3\n"
        block_d = "- 1\n- 2\n- 3\n"
        block_e = "- 1\n-2a\n - 3\n"
        block_f = "- 1\n- 2\n 3\n"
        self.assertEqual(block_to_block_type(block_a), "unordered_list")
        self.assertEqual(block_to_block_type(block_b), "paragraph")
        self.assertEqual(block_to_block_type(block_c), "paragraph")
        self.assertEqual(block_to_block_type(block_d), "unordered_list")
        self.assertEqual(block_to_block_type(block_e), "paragraph")
        self.assertEqual(block_to_block_type(block_f), "paragraph")

    def test_all_items_in_ul_mustt_start_equal(self):
        block_g = "* 1\n* 2\n* 3\n"
        block_h = "- 1\n- 2\n- 3\n"
        block_i = "* 1\n- 2\n* 3\n"
        block_j = "- 1\n* 2\n- 3\n"
        self.assertEqual(block_to_block_type(block_g), "unordered_list")
        self.assertEqual(block_to_block_type(block_h), "unordered_list")
        self.assertEqual(block_to_block_type(block_i), "paragraph")
        self.assertEqual(block_to_block_type(block_j), "paragraph")

    def test_all_lines_must_start_number_point_space_to_make_ol(self):
        block_a = "1. a\n2. b\n3. c"
        block_b = "1 .a\n2. a\n3. c"
        block_c = "1.\n 2. 3"
        self.assertEqual(block_to_block_type(block_a), "ordered_list")
        self.assertEqual(block_to_block_type(block_b), "paragraph")
        self.assertEqual(block_to_block_type(block_c), "paragraph")

    def test_ol_must_start_1_and_add_1_in_each_item(self):
        block_a = "1. a\n2. b\n3. c"
        block_b = "2. a\n3. a\n4. c"
        block_c = "1. a\n2. b\n4. c"
        self.assertEqual(block_to_block_type(block_a), "ordered_list")
        self.assertEqual(block_to_block_type(block_b), "paragraph")
        self.assertEqual(block_to_block_type(block_c), "paragraph")
