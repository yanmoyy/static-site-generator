from htmlnode import HTMLNode
from markdown_blocks import extract_title, markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        md = file.read()
    with open(template_path, "r") as file:
        template = file.read()
    html_node: HTMLNode = markdown_to_html_node(md)
    html = html_node.to_html()
    title = extract_title(md)
    new_html = template.replace("{{ Title }}", title).replace(("{{ Content }}"), html)
    with open(dest_path, "w") as file:
        file.write(new_html)
