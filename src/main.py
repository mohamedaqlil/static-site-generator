from textnode import *
import shutil
import os
from copy_static import copy_recursive
from generate_page import generate_page

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
        shutil.copytree("static", "public", dirs_exist_ok=True)
    
    # Generate the index page
    generate_page(
        from_path="content/index.md",
        template_path="template.html",
        dest_path="public/index.html"
    )

if __name__ == "__main__":
    main()