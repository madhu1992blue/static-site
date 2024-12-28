import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_node_to_html(self):
        in_expected = [
            (TextNode("plain text", TextType.TEXT),"plain text"),
            (TextNode("bold text", TextType.BOLD),"<b>bold text</b>"),
            (TextNode("italic text", TextType.ITALIC),"<i>italic text</i>"),
            (TextNode("some bash code", TextType.CODE),'<code>some bash code</code>'),
            (TextNode("Text Linked", TextType.LINK,"https://example.com"),'<a href="https://example.com">Text Linked</a>'),
            (TextNode("This is alt text", TextType.IMAGE, "https://example.com"), '<img src="https://example.com" alt="This is alt text"></img>')
        ]
        for in_node, expected in in_expected:
            self.assertEqual(text_node_to_html_node(in_node).to_html(), expected)

    def test_split_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        for i in range(len(expected)):
            self.assertEqual(actual[i], expected[i])


        node = TextNode("This is text with a **bold phrase**", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold phrase", TextType.BOLD),
        ]
        print(actual, expected)
        self.assertEqual(len(actual), len(expected))
        for i in range(len(expected)):
            self.assertEqual(actual[i], expected[i])

        node = TextNode("**bold phrase** started", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("bold phrase", TextType.BOLD),
            TextNode(" started", TextType.TEXT),
        ]
        print(actual, expected)
        self.assertEqual(len(actual), len(expected))
        for i in range(len(expected)):
            self.assertEqual(actual[i], expected[i])

        node = TextNode("****", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = []
        self.assertEqual(len(actual), len(expected))

        with self.assertRaises(Exception):
            node = TextNode("**", TextType.TEXT)
            actual = split_nodes_delimiter([node], "**", TextType.BOLD)

        

if __name__ == "__main__":
    unittest.main()