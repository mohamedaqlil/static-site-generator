from textnode import *
import shutil
import os
from copy_static import copy_recursive
from generate_page import generate_page, generate_pages_recursive
import sys

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = '/'

    # Create output directory structure
    if os.path.exists("docs"):
        # Delete anything in the docs directory
        shutil.rmtree("docs")
    
    # Create the docs directory
    os.makedirs("docs", exist_ok=True)
    
    # Copy static files
    if os.path.exists("static"):
        # Copy all static files to docs
        copy_recursive("static", "docs")
    
    # Generate the index page
    generate_pages_recursive(
        dir_path_content="content",
        template_path="template.html",
        dest_dir_path="docs",
        basepath=basepath
    )

if __name__ == "__main__":
    main()