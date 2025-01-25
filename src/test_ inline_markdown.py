import unittest
from inline_markdown import split_nodes_delimiter
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

if __name__ == "__main__":
    unittest.main()