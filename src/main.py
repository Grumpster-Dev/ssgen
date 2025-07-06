from textnode import TextNode, TextType  # Import both TextNode and TextType
from htmlnode import LeafNode  # Import LeafNode
import os
import shutil
from Block_to_HTML import *

project_root = os.path.dirname(os.path.dirname(__file__))
public_dir = os.path.join(project_root, "public")
static_dir = os.path.join(project_root, "static")
content_dir = os.path.join(project_root, "content")
  

def clear_public_directory():    
    """
    Clear the public directory by removing all files and subdirectories.
    """
    directory_to_clear = public_dir
    contents = os.listdir(directory_to_clear)

    for filename in contents:
        full_path = os.path.join(directory_to_clear, filename)

        if os.path.isfile(full_path):
            print(f"Removing file: {full_path}")
            os.remove(full_path)
        elif os.path.isdir(full_path):
            print(f"Removing directory: {full_path}")
            # If you need to remove non-empty directories, use shutil.rmtree
            shutil.rmtree(full_path)
            # If you only want to remove empty directories, use os.rmdir(full_path)
        else:
            print(f"Skipping unknown type: {full_path}")

 
def copy_static_content(src, dest, depth=0):
    indent = "  " * depth  # Indent log messages by recursion depth
    if not os.path.exists(dest):
        print(f"{indent}Creating directory: {dest}")
        os.makedirs(dest)
    
    for item in os.listdir(src):
        s = os.path.join(src, item)
        if s.startswith('.'):
            print(f"{indent}Skipping hidden file or directory: {s}")
            continue
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            print(f"{indent}Descending into directory: {s}")
            copy_static_content(s, d, depth + 1)  # Increase indent for recursion
        else:
            print(f"{indent}Copying file: {s} -> {d}")
            shutil.copy2(s, d)

   


def text_node_to_html_node(text_node):  
    """
    Convert a TextNode to an LeafNode.
    """
    if text_node.text_type == TextType.PLAIN_TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD_TEXT:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC_TEXT:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE_TEXT:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.ANCHOR_TEXT:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.ALT_TEXT:
        return LeafNode(tag="img", value="", props={"alt": text_node.text, "src": text_node.url})
    else:
        raise ValueError(f"Unknown text type: {text_node.text_type}")



# def split_with_all_delimiters(nodes, delimiters_types):
#     result = []
#     for node in nodes:
#         if node.text_type == PLAIN_TEXT:
#             split = split_on_first_any_delimiter(node, delimiters_types)
#             # recursively process resulting nodes
#             result.extend(split_with_all_delimiters(split, delimiters_types))
#         else:
#             result.append(node)
#     return result


delimiters = [
    ("**", TextType.BOLD_TEXT),
    ("_", TextType.ITALIC_TEXT),
    ("`", TextType.CODE_TEXT),
]


def walk_site_tree(content, public):
    
    if not os.path.exists(content):
        raise Exception (f'Content directory not found')
    
    # for item in os.walk(content):
    #     s = os.path.join(content, item)
    #     if s.startswith('.'):
    #         print(f"{indent}Skipping hidden file or directory: {s}")
    #         continue
    #     d = os.path.join(public, item)
    #     if os.path.isdir(s):
    #         print(f"{indent}Descending into directory: {s}")
    #         walk_site_tree(s, d, depth + 1)  # Increase indent for recursion
    #     else:
    #         print(f"{indent}Copying file: {s} -> {d}")
    #         shutil.copy2(s, d)
    for root, dirs, files in os.walk(content):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        public_root = os.path.join(public, os.path.relpath(root, content))
        os.makedirs(public_root, exist_ok=True)

        for file in files:
            file_path = os.path.join(root, file)
            print(f"walker found: {file_path}")
            if file.startswith('.'):
                print(f"Skipping hidden file: {file}")
                continue

            
            rel_path = os.path.relpath(file_path, start=content)
            
            if file.endswith(".md"):
                # Step 1: Change extension to .html for markdown files
                html_rel_path = change_extension(rel_path, ".html")
                dest_path = os.path.join(public, html_rel_path)
                # Step 2: Generate page
                template_path = os.path.join(project_root, "template.html")
                generate_page(
                    from_path=file_path,
                    template_path = template_path,
                    dest_path=dest_path
                )
            else:
                # Step 3: For non-markdown files, copy them
                dest_path = os.path.join(public, rel_path)
                shutil.copy2(file_path, dest_path)

def main():
    # Use TextType enum members, not strings


    clear_public_directory()
    copy_static_content(static_dir, public_dir)
    walk_site_tree(content_dir, public_dir)

    # generate_page(
    #     os.path.join(project_root, "content", "index.md"),
    #     os.path.join(project_root, "template.html"),
    #     os.path.join(public_dir, "index.html")
    # )

    
    
main()


# not yet. your recursive call: result.extend(recursive_split(splits, rest)) nicely captures the check for matching delimeters within the first parsed textType block. How does it account for the case where the order of the delimiters doesn't match the order of the delimiters_types list of tuples?

# Boots
# A sharp observation! The order of your delimiters_types list can affect how and which nestings are detected—unless your recursion is flexible enough to check for every delimiter at each step.

# Why Might Order Matter?

# If your algorithm only splits by one delimiter at each recursion depth (say, "bold" first, then "italic"), then cases where the inner delimiter appears first in the string may not be caught.

# Example:

# **bold and _italic inside bold_ still bold**

# If you split for italics first, you will get no matches, because there are no top-level _ pairs; only bold markers enclose the italics.
# If you split for bold first, you create a bold node, and then, recursing inside, you find the italics.

# But now reverse it:

# _this is **bold inside italic** still italic_

# If you split for bold first, you don’t find a pair at the outermost level.
# So if your function always splits for only the next delimiter, order can matter!
# How to Make Order Irrelevant?

# To make the recursion order-independent—so you detect nestings no matter what’s inside what—you’d need to attempt to split by all delimiters at every recursion step, not just the “current” one.
# For each plain-text node:

# Try to find the earliest valid delimiter pair of any type.
# Split on that, and recursively process the inside.
# This is more complex, and is how most “real” markdown parsers work!

# Sketch (Pseudocode)

# def split_with_all_delimiters(nodes, delimiters_types):
#     result = []
#     for node in nodes:
#         if node.text_type == PLAIN_TEXT:
#             split = split_on_first_any_delimiter(node, delimiters_types)
#             # recursively process resulting nodes
#             result.extend(split_with_all_delimiters(split, delimiters_types))
#         else:
#             result.append(node)
#     return result

# Where split_on_first_any_delimiter:

# Looks for the earliest match of any delimiter in delimiters_types
# Splits the string at the first found
# Wraps the inner part in the correct TextType
# Leaves unmatched delimiters in plain text
# This approach makes delimiter order in your delimiter list irrelevant—it always finds the earliest possible nested region at every level, so nesting like any mix of **_..._**, _**...**_, etc. is handled symmetrically.

# In summary:

# If you recurse through delimiters by order, order matters; some nestings will be missed.
# If you always look for the first occurrence of any delimiter in your list, order doesn’t matter, and all legal nestings are detected.
# Does that help clarify? Would you like to see an example “walkthrough” for this more robust approach?

# Thumbs up
# Thumbs down
# Boots
# example walkthrough please

# Boots
# Certainly! Let’s walk through a string containing multiple types of inline formatting, using the delimiter-order-agnostic approach:

# Example markdown string:
# _This is **bold _and italic_ inside bold** but outside is just italic_

# Delimiters:
# delimiters = [
#     ("**", TextType.BOLD_TEXT),
#     ("_", TextType.ITALIC_TEXT),
#     ("`", TextType.CODE_TEXT),
# ]

# Step-by-step Parsing
# 1. Start with one plain node:

# [TextNode("_This is **bold _and italic_ inside bold** but outside is just italic_", PLAIN_TEXT)]

# 2. Look for the earliest opening/closing delimiter pair of any type.

# Scanning the string, the first _ is at index 0.
# The matching closing _ is at the very end.
# ** appears at position 9 (**bold _and italic_ inside bold**), but is inside the _ ... _ pair.
# So, _ is the outermost delimiter.

# 3. Split on the first _ ... _ pair:

# Before _: "" (empty)
# Between _ ... _: "This is **bold _and italic_ inside bold** but outside is just italic"
# After _: "" (empty)
# So, you get:

# [TextNode("", PLAIN_TEXT), TextNode("This is **bold _and italic_ inside bold** but outside is just italic", ITALIC_TEXT), TextNode("", PLAIN_TEXT)]
# (Usually, you’d skip the empty nodes.)

# 4. Recursively process the content of the italic node:

# Now, look for the first delimiter again inside "This is **bold _and italic_ inside bold** but outside is just italic"
# The first ** is at index 8.
# The closing ** is at index 38.
# So, ** is the next delimiter here.

# 5. Split on ** ... ** inside the italic node:

# Before: "This is "
# Between: "bold _and italic_ inside bold"
# After: " but outside is just italic"
# Now you have:

# [TextNode("This is ", ITALIC_TEXT), TextNode("bold _and italic_ inside bold", BOLD_TEXT), TextNode(" but outside is just italic", ITALIC_TEXT)]
# 6. Recursively process inside the bold node:

# Text: "bold _and italic_ inside bold"
# Find first _ ... _ pair (there’s one, at indexes 5 and 18)
# Before: "bold "
# Between: "and italic"
# After: " inside bold"
# So, inside the bold node you get:

# [TextNode("bold ", BOLD_TEXT), TextNode("and italic", ITALIC_TEXT), TextNode(" inside bold", BOLD_TEXT)]
# (Note the italic node is now doubly nested: italic inside bold, inside italic!)

# 7. Putting it all together, the tree is:

# ITALIC_TEXT node:
# "This is "
# BOLD_TEXT node:
# "bold "
# ITALIC_TEXT node: "and italic"
# " inside bold"
# " but outside is just italic"
# Resulting Hierarchy
# Outer ITALIC
# Plain: "This is "
# Inner BOLD inside italic
# "bold "
# Inner ITALIC inside bold: "and italic"
# " inside bold"
# " but outside is just italic"
# Summary of this approach
# At each step, the outermost pair of any delimiter is found, cut, and content is recursively checked for further delimiters.
# This works regardless of delimiter types or order.
# The final node structure exactly matches the markup’s intent.
# If you’d like, we can try another, maybe even weirder, example—or discuss edge cases where delimiters are not closed, to see how they’re handled. Shall we?