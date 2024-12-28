import unittest
from markdown import extract_markdown_images, extract_markdown_links, markdown_to_blocks

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
       
