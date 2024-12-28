import unittest
from markdown import extract_markdown_images, extract_markdown_links, markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownParsing(unittest.TestCase):
    def test_image_extraction(self):
        altTextImages = extract_markdown_images("This contains image ![altText1](imageURL1) , ![altText2](imageURL2) here")
        expected = [('altText1', 'imageURL1'), ('altText2', 'imageURL2')]
        for i in range(len(expected)):
            self.assertEqual(expected[i], altTextImages[i])

    def test_link_extraction(self):
        altTextImages = extract_markdown_links("This contains image [value1](url1) , ![altText2](imageURL2) here")
        expected = [('value1', 'url1')]
        for i in range(len(expected)):
            self.assertEqual(expected[i], altTextImages[i])


class TestMarkdownBlock(unittest.TestCase):
    def test_markdown_blocks_create(self):
        message = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.


* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        blocks = markdown_to_blocks(message)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
* This is a list item
* This is another list item"""
        ]
        self.assertListEqual(blocks, expected)
       
    def test_block_type_detection(self):
        ul = """
* This is a ul
* This is a ul1
""".strip()
        self.assertEqual(block_to_block_type(ul), BlockType.UnorderedList)

        ul = """
- This is a ul
- This is a ul1
""".strip()
        self.assertEqual(block_to_block_type(ul), BlockType.UnorderedList)

        malformed_ul = """
- This is a ul
- This is a ul1
a
""".strip()
        self.assertEqual(block_to_block_type(malformed_ul), BlockType.Paragraph)

        heading = "# This is a heading"
        self.assertEqual(block_to_block_type(heading), BlockType.Heading)

        malformed_heading = """# this is a heading
        a"""
        self.assertEqual(block_to_block_type(malformed_heading), BlockType.Paragraph)
        
        quote = """
>Quote
> quote
""".strip()
        self.assertEqual(block_to_block_type(quote), BlockType.Quote)


        ol = """
1. This is nice
2. This is crazy
""".strip()
        self.assertEqual(block_to_block_type(ol), BlockType.OrderedList)

        malformed_ol = """
1. This is nice
1. This is not so nice
""".strip()
        self.assertEqual(block_to_block_type(malformed_ol), BlockType.Paragraph)


