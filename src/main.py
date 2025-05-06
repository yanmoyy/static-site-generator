import os
import shutil

from copystatic import copy_files_recursive
from generate_page import generate_page

dir_path_static = "./static"
dir_path_public = "./public"
content_path = "./content/index.md"
template = "./template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_page(content_path, template, dir_path_public + "/index.html")


if __name__ == "__main__":
    main()
