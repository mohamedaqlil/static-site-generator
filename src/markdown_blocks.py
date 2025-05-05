from enum import Enum

from htmlnode import ParentNode, HTMLNode
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

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    
