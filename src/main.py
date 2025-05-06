from textnode import *
import shutil
import os
from copy_static import copy_recursive

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")

    copy_recursive("static", "public")
    
if __name__ == "__main__":
    main()