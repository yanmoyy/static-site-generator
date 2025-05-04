from functools import reduce
from typing import List

from textnode import TextNode, TextType


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
