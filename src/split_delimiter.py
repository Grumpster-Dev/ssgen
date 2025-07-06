from textnode import * # Import both TextNode and TextType 
from htmlnode import *
from md_process import extract_markdown_images, extract_markdown_links

import re



# def split_nodes_delimiter(old_nodes, delimiter, text_type):
#     new_nodes = []
#     for old_node in old_nodes:
#         if old_node.text_type != TextType.PLAIN_TEXT:
#             new_nodes.append(old_node)
#             continue
#         split_nodes = []
#         sections = old_node.text.split(delimiter)
#         if len(sections) % 2 == 0:
#             raise ValueError("invalid markdown, formatted section not closed")
#         for i in range(len(sections)):
#             if sections[i] == "":
#                 continue
#             if i % 2 == 0:
#                 split_nodes.append(TextNode(sections[i], TextType.PLAIN_TEXT))
#             else:
#                 split_nodes.append(TextNode(sections[i], text_type))
#         new_nodes.extend(split_nodes)
#     return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):     
    """
    Split a list of nodes by a delimiter.
    """

    new_nodes = []
    
    for node in old_nodes:
        
        if not node.text_type == TextType.PLAIN_TEXT:
            # if node is not plain text, add it directly to new_nodes
            new_nodes.append(node)
            continue
        temp_node = node.text.split(delimiter)
        if len(temp_node) % 2 == 0:
            raise Exception("Delimiter missing a closing Delimiter")
        for index,sub_node in enumerate(temp_node): #(check if the index is even or odd)
            if index % 2 == 0:
                # even index, add to current_node
                new_nodes.append(TextNode(sub_node, TextType.PLAIN_TEXT))
            else:
                # odd index, create a new TextNode with the current_node and add it to new_nodes
                
                new_nodes.append(TextNode(sub_node, text_type))
                
    return new_nodes
    
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        
        if not node.text_type == TextType.PLAIN_TEXT:
            # if node is not plain text, add it directly to new_nodes
            new_nodes.append(node)
            continue

        original_text = node.text
        images= extract_markdown_images(original_text)
        if len(images) == 0:
            if  node.text !="":#test if node is empty
                new_nodes.append(node)
            continue
        for image in images:
            
            parts = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(parts) != 2:
                #an image was found, but something went wrong.
                raise ValueError("Image delimiter missing a closing Delimiter")
            if parts[0] != "":  
                new_nodes.append(TextNode(parts[0], TextType.PLAIN_TEXT))
            new_nodes.append(TextNode(image[0], TextType.ALT_TEXT, image[1]))
            original_text = parts[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.PLAIN_TEXT))
    return new_nodes

    

def split_nodes_link(old_nodes):
    """
    Split a list of nodes by a link delimiter.
    """
    new_nodes = []
    
    for node in old_nodes:
        if  node.text_type != TextType.PLAIN_TEXT:
            # if node is not plain text, add it directly to new_nodes
            new_nodes.append(node)
            continue
        
        original_text = node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            if original_text != "":
                new_nodes.append(node)
            continue
        for link in links:
            parts = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(parts)  != 2:
                raise Exception("Link delimiter missing a closing Delimiter")
            if parts[0] != "":  
                new_nodes.append(TextNode(parts[0], TextType.PLAIN_TEXT))
            new_nodes.append(TextNode(link[0], TextType.ANCHOR_TEXT, link[1]))
            original_text = parts[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.PLAIN_TEXT))
        
    
    return new_nodes


# def test_split_images(self):
#     node = TextNode(
#         "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
#         TextType.TEXT,
#     )
#     new_nodes = split_nodes_image([node])
#     self.assertListEqual(
#         [
#             TextNode("This is text with an ", TextType.TEXT),
#             TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
#             TextNode(" and another ", TextType.TEXT),
#             TextNode(
#                 "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
#             ),
#         ],
#         new_nodes,
#     )

#     test_split_images()


def text_to_textnodes(text):
    """
    Convert a plain text string to a list of TextNode objects.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    # First step is to creat an input list of TextNode objects
    input_nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    italic_nodes = split_nodes_delimiter(input_nodes, "_", TextType.ITALIC_TEXT) 
    
    bold_nodes = split_nodes_delimiter(italic_nodes, "**", TextType.BOLD_TEXT)
    code_nodes = split_nodes_delimiter(bold_nodes, "`", TextType.CODE_TEXT)
    
    image_nodes = split_nodes_image(code_nodes)
    link_nodes = split_nodes_link(image_nodes)
    # print(link_nodes)
    return link_nodes

    
# def test_example():
#     input_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
#     result = text_to_textnodes(input_text)
#     # Print or compare with expected result

# test_example()
def markdown_to_blocks(markdown):
    valid_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block.strip() == "":
            continue

        valid_blocks.append(block.strip())
    # print(valid_blocks)
    return valid_blocks



# markdown = """This is **bolded** paragraph

# This is another paragraph with _italic_ text and `code` here
# This is the same paragraph on a new line

# - This is a list
# - with items"""
    
# markdown_to_blocks(markdown)

def block_to_block_type(block):
    """
    Convert a block of text to a BlockType.
    """
    if block.startswith(("# ","## ","### ","#### ","##### ","###### ")) and re.search(r'\w' ,(block.split("# ")[1])):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in block.split("\n")):
     return BlockType.QUOTE
    elif all(line.startswith("- ") for line in block.split("\n")):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
   

def is_ordered_list(block):
   # Assuming 'block' is your input string
    lines = block.split("\n")
    expected_number = 1

    for line in lines:
        parts = line.split(". ", 1) # Use maxsplit=1 to handle cases like "1.1. nested"

        # --- Step 1: Basic format check ---
        # Does it have at least two parts after splitting?
        # Is the first part a digit?
        # Does the line actually start with the number and a dot (e.g., "1.")?
        # This might require checking if len(parts) is 2, and parts[0].isdigit()

        if not (len(parts) == 2 and parts[0].isdigit() and line.startswith(f"{parts[0]}.")):
            # If it doesn't match the basic format, it's not an ordered list
            # What should we do here? (Hint: it's not an ordered list)
            return False # Or whatever indicates failure for ordered list check

        # --- Step 2: Convert and compare number ---
        current_number = int(parts[0])

        if current_number != expected_number:
            # If the number isn't what we expected, it's not an ordered list
            return False # Or whatever indicates failure

        # --- Step 3: Prepare for the next line ---
        expected_number += 1

    # If the loop finishes, it means all lines passed all checks
    return True # It IS an ordered list!