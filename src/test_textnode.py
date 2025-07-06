import unittest

from textnode import * 
from split_delimiter import *
from main import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    # def test_eq(self):
    #     node = TextNode("This is a text node", TextType.BOLD_TEXT)
    #     node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
    #     self.assertEqual(node, node2)

    # def test_not_eq(self):
    #     node = TextNode("This is a text node", TextType.BOLD_TEXT)
    #     node2 = TextNode("This is a different text node", TextType.BOLD_TEXT)
    #     self.assertNotEqual(node, node2)

    # def test_is_true(self):
    #     node = TextNode("This is a text node", TextType.BOLD_TEXT)
    #     self.assertTrue(isinstance(node, TextNode))

    # def test_repr(self):
    #     node = TextNode("This is a text node", TextType.BOLD_TEXT, "http://example.com")
    #     expected_repr = "TextNode(text=This is a text node, text_type=bold, url=http://example.com)"
    #     self.assertEqual(repr(node), expected_repr)

    # def test_text(self):
    #     node = TextNode("This is a text node", TextType.PLAIN_TEXT)
    #     html_node = text_node_to_html_node(node)
    #     self.assertEqual(html_node.tag, None)
    #     self.assertEqual(html_node.value, "This is a text node")

    # def test_anchor(self):
    #     node = TextNode("Boot.dev", TextType.ANCHOR_TEXT, "https://boot.dev")
    #     html_node = text_node_to_html_node(node)
    #     self.assertEqual(html_node.tag, "a")
    #     self.assertEqual(html_node.value, "Boot.dev")
    #     self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    # def test_alt_text(self):
    #     node = TextNode("Boot.dev logo", TextType.ALT_TEXT, "https://boot.dev/logo.png")
    #     html_node = text_node_to_html_node(node)
    #     self.assertEqual(html_node.tag, "img")
    #     self.assertEqual(html_node.props, {"alt": "Boot.dev logo", "src": "https://boot.dev/logo.png"})
    #     self.assertEqual(html_node.value, "")

    # def test_bold_text(self):
    #     node = TextNode("Bold text", TextType.BOLD_TEXT)
    #     html_node = text_node_to_html_node(node)
    #     self.assertEqual(html_node.tag, "b")
    #     self.assertEqual(html_node.value, "Bold text")

    # def test_italic_text(self):
    #     node = TextNode("Italic text", TextType.ITALIC_TEXT)
    #     html_node = text_node_to_html_node(node)
    #     self.assertEqual(html_node.tag, "i")
    #     self.assertEqual(html_node.value, "Italic text")

    # def test_code_text(self):
    #     node = TextNode("Code text", TextType.CODE_TEXT)
    #     html_node = text_node_to_html_node(node)
    #     self.assertEqual(html_node.tag, "code")
    #     self.assertEqual(html_node.value, "Code text")

    # def test_unknown_text_type(self):
    #     node = TextNode("Unknown text", "unknown")
    #     with self.assertRaises(ValueError):
    #         text_node_to_html_node(node)

   def test_split_images(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.PLAIN_TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.PLAIN_TEXT),
            TextNode("image", TextType.ALT_TEXT, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN_TEXT),
            TextNode(
                "second image", TextType.ALT_TEXT, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )



if __name__ == "__main__":
    unittest.main()