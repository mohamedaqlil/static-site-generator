from textnode import *
import shutil
import os
from copy_static import copy_recursive
from generate_page import generate_page, generate_pages_recursive

def main():
    # Create output directory structure
    if os.path.exists("public"):
        # Delete anything in the public directory
        shutil.rmtree("public")
    
    # Create the public directory
    os.makedirs("public", exist_ok=True)
    
    # Copy static files
    if os.path.exists("static"):
        # Copy all static files to public
        copy_recursive("static", "public")
    
    # Generate the index page
    generate_pages_recursive(
        dir_path_content="content",
        template_path="template.html",
        dest_dir_path="public"
    )

if __name__ == "__main__":
    main()