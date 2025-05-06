import re
from functools import reduce
from typing import List

from textnode import TextNode, TextType


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
):
    # Helper function to split a single node's text
    def process_node(node):
        if node.text_type != TextType.TEXT:
            return [node]

        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")

        def process_section(args):
            i, section = args
            if section == "":
                return None
            if i % 2 == 0:
                return TextNode(section, TextType.TEXT)
            else:
                return TextNode(section, text_type)

        return list(
            filter(lambda x: x is not None, map(process_section, enumerate(sections)))
        )

    # Flatten the list of lists into a single list of nodes
    return reduce(lambda acc, x: acc + x, map(process_node, old_nodes), [])


def process_node_link(node: TextNode, text_type: TextType):
    if node.text_type != TextType.TEXT:
        return [node]
    is_image = text_type == TextType.IMAGE
    text_left = node.text
    prefix = "!" if is_image else ""

    matches = (
        extract_markdown_images(text_left)
        if is_image
        else extract_markdown_links(text_left)
    )
    nodes = []
    for match in matches:
        alt, link = match
        text, text_left = text_left.split(f"{prefix}[{alt}]({link})", 1)
        if text != "":
            nodes.append(TextNode(text))
        nodes.append(TextNode(alt, text_type, link))
    if text_left != "":
        nodes.append(TextNode(text_left))
    return nodes


def split_nodes_image(old_nodes):
    return reduce(
        lambda acc, x: acc + x,
        map(lambda x: process_node_link(x, TextType.IMAGE), old_nodes),
        [],
    )


def split_nodes_link(old_nodes):
    return reduce(
        lambda acc, x: acc + x,
        map(lambda x: process_node_link(x, TextType.LINK), old_nodes),
        [],
    )


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
