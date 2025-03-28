import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, markdown_to_blocks
from textnode import TextNode, TextType

class Test_split_delimiter(unittest.TestCase):
  def test_split_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ]) 
        
  def test_split_delimiter_bold(self):
        node = TextNode("This is text with a **bold phrase** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold phrase", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ])
        
  def test_split_delimiter_italic(self):
        node = TextNode("This is text with a *italic phrase* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            ])

  def test_split_no_delimiter(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is plain text", TextType.TEXT)
            ]) 
        
  def test_multiple_delimiters(self):
    node = TextNode("Text with `code` and more `code`", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertEqual(new_nodes, [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and more ", TextType.TEXT),
            TextNode("code", TextType.CODE)
            ]) 
    
  def test_invalid_delimiter(self):
      node = TextNode("Text with `code", TextType.TEXT)
      with self.assertRaises(ValueError):
        split_nodes_delimiter([node], "`", TextType.CODE)

  def test_non_text_node(self):
    node = TextNode("**bold text**", TextType.BOLD)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertEqual(new_nodes, [
        TextNode("**bold text**", TextType.BOLD, None)
        ])

  def test_empty_nodes_list(self):
    new_nodes = split_nodes_delimiter([], "`", TextType.CODE)
    self.assertEqual(new_nodes, [])

class Test_extract_markdown(unittest.TestCase):
    def test_strings_malformed(self):
        text = "Oops [broken](link and ![forgot](https://image)"
        self.assertEqual(extract_markdown_links(text), [])
        self.assertEqual(extract_markdown_images(text), [])

    def test_mixed_links_and_images(self):
        text = "Both here [text](link) and ![image](image_link) exist."
        self.assertEqual(extract_markdown_links(text), [("text", "link")])
        self.assertEqual(extract_markdown_images(text), [("image", "image_link")])

    def test_empty_content(self):
        text = "![](image_link) or [text]()"
        self.assertEqual(extract_markdown_links(text), [("text", "")])
        self.assertEqual(extract_markdown_images(text), [("", "image_link")])

class Test_split_nodes(unittest.TestCase):
    def test_split_nodes_image():
        # Test 1: Basic image
        node = TextNode("This is ![image](url.png) test", TextType.TEXT)
        nodes = split_nodes_image([node])
        assert len(nodes) == 3
        assert nodes[0].text == "This is "
        assert nodes[1].text == "image"
        assert nodes[1].url == "url.png"
        assert nodes[2].text == " test"

        # Test 2: Multiple images
        node = TextNode("![1](url1) ![2](url2)", TextType.TEXT)
        nodes = split_nodes_image([node])
        assert len(nodes) == 2
        assert nodes[0].text == "1"
        assert nodes[1].text == "2"

        # Test 3: No images
        node = TextNode("Plain text", TextType.TEXT)
        nodes = split_nodes_image([node])
        assert len(nodes) == 1
        assert nodes[0].text == "Plain text"

    def test_split_nodes_link():
        # Test 1: Basic link
        node = TextNode("This is [link](url) test", TextType.TEXT)
        nodes = split_nodes_link([node])
        assert len(nodes) == 3
        assert nodes[0].text == "This is "
        assert nodes[1].text == "link"
        assert nodes[1].url == "url"
        assert nodes[2].text == " test"

        # Test 2: Multiple links
        node = TextNode("[1](url1) [2](url2)", TextType.TEXT)
        nodes = split_nodes_link([node])
        assert len(nodes) == 2
        assert nodes[0].text == "1"
        assert nodes[1].text == "2"

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

if __name__ == "__main__":
    unittest.main()