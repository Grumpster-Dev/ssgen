from split_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType  # Import both TextNode and TextType


def test_split_nodes_delimiter():
    # Test case 1: Basic split with plain text
    node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
    assert len(new_nodes) == 3
    assert new_nodes[0].text == "This is text with a "
    assert new_nodes[0].text_type == TextType.PLAIN_TEXT
    assert new_nodes[1].text == "code block"
    assert new_nodes[1].text_type == TextType.CODE_TEXT
    assert new_nodes[2].text == " word"
    assert new_nodes[2].text_type == TextType.PLAIN_TEXT

    # Test case 2: No delimiter in text
    node = TextNode("No special formatting here", TextType.PLAIN_TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
    assert len(new_nodes) == 1
    assert new_nodes[0].text == "No special formatting here"
    assert new_nodes[0].text_type == TextType.PLAIN_TEXT

    # Test case 3: Multiple delimiters
    node = TextNode("Start `code` middle `code` end", TextType.PLAIN_TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
    assert len(new_nodes) == 5
    assert new_nodes[0].text == "Start "
    assert new_nodes[0].text_type == TextType.PLAIN_TEXT
    assert new_nodes[1].text == "code"
    assert new_nodes[1].text_type == TextType.CODE_TEXT
    assert new_nodes[2].text == " middle "
    assert new_nodes[2].text_type == TextType.PLAIN_TEXT
    assert new_nodes[3].text == "code"
    assert new_nodes[3].text_type == TextType.CODE_TEXT
    assert new_nodes[4].text == " end"
    assert new_nodes[4].text_type == TextType.PLAIN_TEXT

    node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
    print(split_nodes_delimiter([node], "`", TextType.CODE_TEXT))