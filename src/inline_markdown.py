from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for node in old_nodes:
    if node.text_type is not TextType.TEXT:
      new_nodes.append(node)
      continue
    
    elif delimiter in node.text:
      parts = node.text.split(delimiter)
      if len(parts) % 2 == 0:
        raise ValueError("No closing delimiter found")
      
      for i, part in enumerate(parts):
        if part:
          if i % 2 == 0:
            new_nodes.append(TextNode(part, TextType.TEXT))
          else:
            new_nodes.append(TextNode(part, text_type))
    else:
      new_nodes.append(node)
      continue
  return new_nodes

def extract_markdown_images(text):
  return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
  return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

