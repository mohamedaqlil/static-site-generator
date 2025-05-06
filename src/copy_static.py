import shutil
import os

if os.path.exists("public"):
    shutil.rmtree("public")
os.mkdir("public")
def copy_recursive(src, dst):
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isfile(src_path):
          print(f"Copying file: {src_path} -> {dst_path}")
          shutil.copy(src_path, dst_path)
        if os.path.isdir(src_path):
           if not os.path.exists(dst_path):
              os.mkdir(dst_path)
           copy_recursive(src_path, dst_path)