from textnode import TextNode, TextType
import re

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

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

def split_nodes_link(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
      continue
            
    # Find all links in the text
    links = extract_markdown_links(node.text)
    if not links:
      new_nodes.append(node)
      continue
            
    # Get the current text to process
    current_text = node.text
        
    # For each link found...
    for link_text, link_url in links:
          # Split around the full markdown link
          full_link = f"[{link_text}]({link_url})"
          parts = current_text.split(full_link, 1)

          # Add the text before the link if it exists
          if parts[0]:
            new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
          # Add the link node
          new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            
          # Update current_text to remaining text
          current_text = parts[1]
        
        # Add any remaining text after the last link
    if current_text:
      new_nodes.append(TextNode(current_text, TextType.TEXT))
            
  return new_nodes

def split_nodes_image(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
      continue
            
    # Find all images in the text
    images = extract_markdown_images(node.text)
    if not images:
      new_nodes.append(node)
      continue
            
    # Get the current text to process
    current_text = node.text
        
    # For each image found...
    for image_text, image_url in images:
          # Split around the full markdown image
          full_image = f"![{image_text}]({image_url})"
          parts = current_text.split(full_image, 1)

          # Add the text before the image if it exists
          if parts[0]:
            new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
          # Add the image node
          new_nodes.append(TextNode(image_text, TextType.IMAGE, image_url))
            
          # Update current_text to remaining text
          current_text = parts[1]
        
        # Add any remaining text after the last link
    if current_text:
      new_nodes.append(TextNode(current_text, TextType.TEXT))
            
  return new_nodes
