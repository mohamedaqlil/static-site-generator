from enum import Enum

from htmlnode import ParentNode, HTMLNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown):
    # Handle empty input to avoid IndexError
    if not markdown:
        return BlockType.PARAGRAPH

    # Check for code blocks
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE

    # Check for quote blocks
    lines = markdown.split("\n")  # Split the markdown into lines
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Check for unordered lists
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Check for ordered lists
    if all(
        line.split(". ")[0].isdigit() and f"{index + 1}. " in line
        for index, line in enumerate(lines)
    ):
        return BlockType.ORDERED_LIST

    # Check for headings
    count = 0
    for c in markdown:
        if c == "#":
            count += 1
        else:
            break

    # If there are no '#'s or too many '#'s, it's not a heading
    if count == 0 or count > 6:
        return BlockType.PARAGRAPH

    # Ensure the count of '#' is followed by a space
    if count < len(markdown) and markdown[count] == " ":
        return BlockType.HEADING

    # If nothing matches, it's a paragraph
    return BlockType.PARAGRAPH

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    
    if block_type == BlockType.PARAGRAPH:
        # Replace newlines with spaces before processing
        block = block.replace("\n", " ")
        text_nodes = text_to_textnodes(block)
        html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
        return ParentNode("p", children=html_nodes)
    
    elif block_type == BlockType.HEADING:
        # Count the number of # at the beginning
        level = 0
        for char in block:
            if char == '#':
                level += 1
            else:
                break
        # Extract the heading text and convert it
        heading_text = block[level:].strip()
        text_nodes = text_to_textnodes(heading_text)
        html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
        return ParentNode(f"h{level}", children=html_nodes)
    
    elif block_type == BlockType.CODE:
        # Remove the ``` delimiters and create a code block
        code_content = "\n".join(block.split("\n")[1:-1])  # Remove first and last lines
        return ParentNode("pre", children=[LeafNode("code", code_content)])
    
    elif block_type == BlockType.QUOTE:
        # Remove the '>' prefix from each line
        lines = block.split("\n")
        quote_content = "\n".join([line[2:] if line.startswith("> ") else line[1:] for line in lines])
        text_nodes = text_to_textnodes(quote_content)
        html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
        return ParentNode("blockquote", children=html_nodes)
    elif block_type == BlockType.UNORDERED_LIST:
        lines = block.split("\n")
        items = []
        for line in lines:
            # Remove the list marker and any leading space
            content = line[2:].strip()
            text_nodes = text_to_textnodes(content)
            html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
            items.append(ParentNode("li", children=html_nodes))
        return ParentNode("ul", children=items)

    elif block_type == BlockType.ORDERED_LIST:
        lines = block.split("\n")
        items = []
        for line in lines:
            # Find the first period to remove the number and period
            period_index = line.find(".")
            if period_index != -1:
                content = line[period_index + 1:].strip()
                text_nodes = text_to_textnodes(content)
                html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
                items.append(ParentNode("li", children=html_nodes))
        return ParentNode("ol", children=items)
    else:
        # Handle any unexpected block types
        print(f"WARNING: Unknown block type: {block_type}")
        return ParentNode("div", children=[LeafNode("span", block)])

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children=children)
    