import os

from htmlnode import HTMLNode
from markdown_blocks import extract_title, markdown_to_html_node


def generate_page(from_path, template_path, dest_path, basePath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        md = file.read()
    with open(template_path, "r") as file:
        template = file.read()
    html_node: HTMLNode = markdown_to_html_node(md)
    html = html_node.to_html()
    title = extract_title(md)
    new_html = (
        template.replace("{{ Title }}", title)
        .replace(("{{ Content }}"), html)
        .replace('href="/', f'href="{basePath}')
        .replace('src="/', f'src="{basePath}')
    )
    with open(dest_path, "w") as file:
        file.write(new_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basePath):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        html_file_name = filename.replace(".md", ".html")
        dest_path = os.path.join(dest_dir_path, html_file_name)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            generate_page(from_path, template_path, dest_path, basePath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basePath)
