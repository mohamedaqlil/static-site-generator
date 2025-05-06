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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Get all entries in the content directory
    entries = os.listdir(dir_path_content)
    
    for entry in entries:
        # Create full source path
        source_path = os.path.join(dir_path_content, entry)
        
        # Check if it's a file or directory
        if os.path.isfile(source_path):
            # If it's a markdown file, generate a page
            if source_path.endswith('.md'):
                # Calculate destination path (replace content dir with public dir and .md with .html)
                rel_path = os.path.relpath(source_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, rel_path.replace('.md', '.html'))
                
                # Generate the page
                generate_page(source_path, template_path, dest_path)
        else:
            # It's a directory, recursively process it
            new_content_dir = source_path
            new_dest_dir = os.path.join(dest_dir_path, entry)
            
            # Create the destination directory if it doesn't exist
            os.makedirs(new_dest_dir, exist_ok=True)
            
            # Recursive call
            generate_pages_recursive(new_content_dir, template_path, new_dest_dir)