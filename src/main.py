import os
import shutil
import sys

from copystatic import copy_files_recursive
from generate_page import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"

template = "./template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    if len(sys.argv) >= 2:
        basePath = sys.argv[1]
    else:
        basePath = "/"

    generate_pages_recursive(dir_path_content, template, dir_path_public, basePath)


if __name__ == "__main__":
    main()
