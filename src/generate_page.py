import os
from extract_title import extract_title
from markdown_blocks import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    # Print status message
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, "r") as file:
        markdown_content = file.read()
    
    # Read the template file
    with open(template_path, "r") as file:
        template_content = file.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract the title
    title = extract_title(markdown_content)
    
    # Replace placeholders in the template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write to the destination file
    with open(dest_path, "w") as file:
        file.write(final_html)