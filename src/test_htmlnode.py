import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="div", props={"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')

    def test_repr(self):
        node = HTMLNode(tag="span", value="Hello", children=[], props={"style": "color: red;"})
        expected_repr = "HTMLNode(tag=span, value=Hello, children=[], props={'style': 'color: red;'})"
        self.assertEqual(repr(node), expected_repr)

    def test_to_html(self):
        node = HTMLNode(tag="p", value="This is a paragraph", props={"class": "text"})
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html_empty(self):
        node = HTMLNode(tag="div", props={})
        self.assertEqual(node.props_to_html(), "")


    def test_htmlnode_initialization(self):
        node = HTMLNode(tag="div", value="Content", children=[TextNode("Text", TextType.PLAIN_TEXT)], props={"id": "content"})
        self.assertEqual(node.value, "Content")
        self.assertEqual(len(node.children), 1)
        self.assertIsInstance(node.children[0], TextNode)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("span", "Styled text", props={"class": "highlight"})
        self.assertEqual(node.to_html(), '<span class="highlight">Styled text</span>')

    def test_leaf_to_html_no_value(self):
        node = LeafNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_value_none(self):
        node = LeafNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
     )
        
    def test_to_html_with_great_grandchildren(self):
        great_grandchild_node = LeafNode("a", "great_grandchild")
        grandchild_node = ParentNode("b", [great_grandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b><a>great_grandchild</a></b></span></div>",
     )


if __name__ == "__main__":
    unittest.main()

