import re
from split_delimiter import split_nodes_delimiter,split_nodes_image,split_nodes_link,text_to_textnodes, block_to_block_type, BlockType, markdown_to_blocks
from textnode import  TextType, TextNode,  text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
import os



# This code was suggested by Boots.  See the convo in Scriv. Generator Functions


# def markdown_to_html(markdown):
#    blocks = text_to_textnodes(markdown)
#    html_blocks = [block for block in markdown_to_html(markdown)]:
#    if block.text_type == "heading":
#         yield f"<h1>{block.text}</h1>"
#    elif block.text_type == "paragraph":
#         yield f"<p>{block.text}</p>"
#    elif block.text_type == "code":
#         yield f"<pre><code>{block.text}</code></pre>"
#    elif block.text_type == "quote":
#         yield f"<blockquote>{block.text}</blockquote>"
#    elif block.text_type == "unordered_list":
#         yield f"<ul><li>{block.text}</li></ul>"
#    elif block.text_type == "ordered_list":
#         yield f"<ol><li>{block.text}</li></ol>"
#    else:
#         yield f"<span>{block.text}</span>"



# def markdown_to_html(markdown):
#     blocks = text_to_textnodes(markdown)
#     for block in blocks:
#         if block.text_type == "code":
#             yield f"{block.text}"
#         elif block.text_type == "heading":
#             yield f"{block.text}"
#         elif block.text_type == "paragraph":
#             yield f"{block.text}"
#         elif block.text_type == "quote":
#             yield f"{block.text}"
#         elif block.text_type == "unordered_list":
#             yield f"{block.text}"
#         elif block.text_type == "ordered_list":
#             yield f"{block.text}"
#         else:
#             yield f"{block.text}"

# # Now use the generator function and eagerly collect all output into a list:
# html_blocks = [block for block in markdown_to_html(markdown)]


def markdown_to_html_node(markdown):
    """
    Convert a markdown string to a list of HTML nodes.
    """
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    
    for block in blocks:
        html_node = block_to_html_node(block)
        html_nodes.append(html_node)
    return ParentNode(tag="div", children=html_nodes)

def block_to_html_node(block):
    """
    Convert a block of text to an HTMLNode.
    """
    block_type = block_to_block_type(block)
    
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        level = block.count("#")
        return heading_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        items = [item.lstrip("1. ").strip() for item in block.split("\n") if re.match(r'^\d+\.', item)]
        return olist_to_html_node(block)
    else:
        raise ValueError(f"Unknown block type: {block_type}")


# define helper functions to convert text to HTML nodes

def paragraph_to_html_node(block):
    """
    Convert a paragraph of text to an HTMLNode.
    """
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    """
    Convert a heading of text to an HTMLNode.
    """
    level = block.count("#")
    if level < 1 or level > 6:
        raise ValueError("heading level must be between 1 and 6")
    content = block.lstrip("# ").strip()
    return LeafNode(tag=f"h{level}", value=content)

def code_to_html_node(block):
    """
    Convert a code block of text to an HTMLNode.
    """
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.PLAIN_TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def quote_to_html_node(block):
    """
    Convert a quote block of text to an HTMLNode.
    """
    lines = block.split("\n")
    quoted_lines = [line.lstrip("> ").strip() for line in lines if line.startswith(">")]
    quoted_text = "\n".join(quoted_lines)
    text_nodes = text_to_children(quoted_text)
    return ParentNode(tag="blockquote", children=text_nodes)


def ulist_to_html_node(block):
    """
    Convert an unordered list block of text to an HTMLNode.
    """
    items = [item.lstrip("- ").strip() for item in block.split("\n") if item.startswith("-")]
    list_items = []
    for item in items:
        children = text_to_children(item)  # Handle inline formatting
        list_items.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ul", children=list_items)

def olist_to_html_node(block):
    """
    Convert an ordered list block of text to an HTMLNode.
    """
    items = [item.lstrip("1. ").strip() for item in block.split("\n") if re.match(r'^\d+\.', item)]
    list_items = []
    for item in items:
        children = text_to_children(item)  # Handle inline formatting
        list_items.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ol", children=list_items)


def text_to_children(text):
    """
    Convert a text string to a list of HTML nodes.
    """
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    
    for text_node in text_nodes:
        if text_node.text_type == TextType.PLAIN_TEXT:
            html_nodes.append(LeafNode(tag=None, value=text_node.text))
        elif text_node.text_type == TextType.BOLD_TEXT:
            html_nodes.append(LeafNode(tag="b", value=text_node.text))
        elif text_node.text_type == TextType.ITALIC_TEXT:
            html_nodes.append(LeafNode(tag="i", value=text_node.text))
        elif text_node.text_type == TextType.CODE_TEXT:
            html_nodes.append(LeafNode(tag="code", value=text_node.text))
        elif text_node.text_type == TextType.ANCHOR_TEXT:
            html_nodes.append(LeafNode(tag="a", value=text_node.text, props={"href": text_node.url}))
        elif text_node.text_type == TextType.ALT_TEXT:
            html_nodes.append(LeafNode(tag="img", value="", props={"alt": text_node.text, "src": text_node.url}))
        else:
            raise ValueError(f"Unknown text type: {text_node.text_type}")
    
    return html_nodes


def extract_title(markdown):
    """
    Extract the title from a markdown string.
    """
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:].strip()
    raise Exception ("No title found in markdown")



def generate_page(from_path, template_path, dest_path):
    """
    Generate a page from a markdown file using a template.
    """

    print(f"Generating page from {from_path} using template {template_path} to {dest_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    
    html_node = markdown_to_html_node(markdown)
    
    with open(template_path, "r") as f:
        template = f.read()
    
    html_content = template.replace("{{ Content }}", html_node.to_html())
    html_content = html_content.replace("{{ Title }}", extract_title(markdown))
    
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(html_content)


def change_extension(path, new_ext):
    base, _ = os.path.splitext(path)
    return base + new_ext
