


sample_markdown = """# My Title
This _is the **first** paragraph_.
This is the second paragraph.
# Another Heading
Yet another paragraph."""


# def split_nodes_image(old_nodes):
#     new_nodes = []
#     for node in old_nodes:
        
#         if not node.text_type == TextType.PLAIN_TEXT:
#             # if node is not plain text, add it directly to new_nodes
#             new_nodes.append(node)
#             continue

#         sections = node.text.split(extract_markdown_images(node), 1)
#         if sections == node:
#             if not node:#test if node is empty
#                continue
#             new_nodes.append(node)
#             continue
#         for section in sections:
#             sections = node.text.split(extract_markdown_images(node), 1)
#             if section.startswith("![") and section.endswith(")"):
#                 # Extract alt text and URL
#                 alt_text, url = extract_markdown_images(section)
#                 new_nodes.append(TextNode(alt_text, TextType.ALT_TEXT, url))
#             else:
#                 if section:# Add plain text sections
#                     new_nodes.append(TextNode(section, TextType.PLAIN_TEXT))


# string = "> this is some text \n> this is some more text\n> and this is even more text"
# parts = string.split("\n")
# print (string)
# print(parts)

# string = "## My Heading"
# parts = string.split("# ")
print(parts)# --- Let's assume this helper exists for now ---
class Block:
    def __init__(self, text, text_type):
        self.text = text
        self.text_type = text_type

def text_to_textnodes(markdown):
    lines = markdown.strip().split("\n")
    # We'll mock recognize just headings and paragraphs for simplicity
    blocks = []
    for line in lines:
        if line.startswith("# "):
            blocks.append(Block(line[2:], "heading"))
        else:
            blocks.append(Block(line, "paragraph"))
    return blocks
# ------------------------------------------------

def markdown_to_html(markdown):
    blocks = text_to_textnodes(markdown)
    for block in blocks:
        if block.text_type == "heading":
            yield f"<h1>{block.text}</h1>"
        elif block.text_type == "paragraph":
            yield f"<p>{block.text}</p>"
        else:
            yield f"<span>{block.text}</span>"

# # ---- Write markdown to a file ----
# sample_markdown = """# My Title
# This _is the **first** paragraph_.
# This is the second paragraph.
# # Another Heading
# Yet another paragraph."""

with open("example.md", "w") as f:
    f.write(sample_markdown)

# ---- Read the markdown file and process it ----
with open("example.md", "r") as f:
    md_content = f.read()

html_blocks = [block for block in markdown_to_html(md_content)]

# ---- Write the output HTML into a file ----
with open("output.html", "w") as f:
    for html_block in html_blocks:
        f.write(html_block + "\n")


# This script:

# Creates a simple markdown file.
# Reads the markdown content.
# Calls your generator-based markdown_to_html function and collects the results.
# Writes the resulting HTML blocks into an output file.