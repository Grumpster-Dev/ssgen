# Import your classes
from htmlnode import HTMLNode, LeafNode, ParentNode
# (Replace 'your_main_file' with whatever your file is actually named)

# Test the example from the lesson
node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)

print("Expected: <p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
print("Actual:  ", node.to_html())