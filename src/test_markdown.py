import unittest
from markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

from textnode import extract_markdown_images, extract_markdown_links
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

        code = """
```
> quote
```
""".strip()
        self.assertEqual(block_to_block_type(code), BlockType.Code)

        malformed_code = """
```b
""".strip()
        self.assertEqual(block_to_block_type(malformed_code), BlockType.Paragraph)


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


    def test_markdown_to_html(self):
        message = """
# This is a heading

## This is a second level heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.


* This is the first list item in a list block
* This is a list item
* This is another list item

1. This is the first list item in a ordered list block
2. This is a list item
3. This is another list item

> This is some quote
> actually a big one

```bash
echo $PATH
```
""".strip()
        expected="""<div><h1>This is a heading</h1><h2>This is a second level heading</h2><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul><ol><li> This is the first list item in a ordered list block</li><li> This is a list item</li><li> This is another list item</li></ol><blockquote> This is some quote
 actually a big one</blockquote><pre><code>bash
echo $PATH
</code></pre></div>"""
        print(markdown_to_html_node(message).to_html())
        self.assertEqual(markdown_to_html_node(message).to_html(), expected)