import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestMarkdownParser(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_empty_markdown(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_block(self):
        md = "Just one block with no newlines"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one block with no newlines"])

    def test_multiple_newlines_between_blocks(self):
        md = "First block\n\n\n\nSecond block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_leading_and_trailing_newlines(self):
        md = "\n\nMiddle block\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Middle block"])

    def test_code_blocks(self):
        md = "```python\ndef hello():\n    print('Hello')\n```"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["```python\ndef hello():\n    print('Hello')\n```"])

    def test_mixed_content(self):
        md = "# Heading\n\nParagraph with **bold** and _italic_\n\n- List item 1\n- List item 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading", 
                "Paragraph with **bold** and _italic_", 
                "- List item 1\n- List item 2"
            ]
        )
    
    def test_heading(self):
        # Single-level heading
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        # Multi-level heading
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        # Invalid heading (too many #)
        self.assertEqual(block_to_block_type("####### Invalid Header"), BlockType.PARAGRAPH)
        # Invalid heading (no space after #)
        self.assertEqual(block_to_block_type("###NoSpace"), BlockType.PARAGRAPH)

    def test_code_block(self):
        # Simple inline code block
        self.assertEqual(block_to_block_type("```\nprint('code')\n```"), BlockType.CODE)
        # Not a code block (no closing backticks)
        self.assertEqual(block_to_block_type("```\nprint('missing backticks')"), BlockType.PARAGRAPH)

    def test_quote(self):
        # Proper quote
        self.assertEqual(block_to_block_type("> A wise saying"), BlockType.QUOTE)
        # Multi-line quote
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2"), BlockType.QUOTE)
        # Invalid quote (does not start with >)
        self.assertEqual(block_to_block_type("Not a quote"), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        # Proper unordered list
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST)
        # Invalid unordered list (missing '- ')
        self.assertEqual(block_to_block_type("Not a list\n- Still not a list"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        # Proper ordered list
        self.assertEqual(block_to_block_type("1. First\n2. Second\n3. Third"), BlockType.ORDERED_LIST)
        # Invalid ordered list (skips a number)
        self.assertEqual(block_to_block_type("1. First\n3. Third"), BlockType.PARAGRAPH)
        # Invalid ordered list (non-numeric starting points)
        self.assertEqual(block_to_block_type("A. Not a list\nB. Still not a list"), BlockType.PARAGRAPH)
        # Invalid ordered list (missing space after '.')
        self.assertEqual(block_to_block_type("1.First\n2.Second"), BlockType.PARAGRAPH)

    def test_paragraph(self):
        # Simple paragraph
        self.assertEqual(block_to_block_type("Just a regular paragraph of text."), BlockType.PARAGRAPH)
        # Empty string
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
        # Paragraph that looks like a heading (missing space)
        self.assertEqual(block_to_block_type("##Heading"), BlockType.PARAGRAPH)


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )

def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

if __name__ == "__main__":
    unittest.main()