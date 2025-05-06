from enum import Enum
from functools import reduce

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    children = reduce(lambda acc, x: acc + x, map(block_to_html_node, blocks), [])
    return ParentNode("div", children)


def block_to_html_node(block):
    block_type: BlockType = block_to_block_type(block)
    match (block_type):
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.OLIST:
            return olist_to_html_node(block)
        case BlockType.ULIST:
            return ulist_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case _:
            raise ValueError("invalid block type")


def paragraph_to_html_node(block):
    paragraph = block.replace("\n", " ")
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")

    def item_to_li(item):
        text = item[3:]
        children = text_to_children(text)
        return ParentNode("li", children)

    children = list(reduce())
    return ParentNode(
        "ol",
    )


def ulist_to_html_node(block):
    pass


def quote_to_html_node(block):
    pass

    html_nodes = []
    for block in blocks:
        block_type: BlockType = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            block = block.replace("\n", " ")
        if block_type != BlockType.CODE:
            children = text_to_children(block)
        match (block_type):
            case BlockType.CODE:
                node = text_node_to_html_node(
                    TextNode(block.strip("```").strip() + "\n", TextType.CODE)
                )
                parent = ParentNode("pre", [node])
            case BlockType.PARAGRAPH:
                parent = ParentNode("p", children)
            case BlockType.QUOTE:
                parent = ParentNode("blockquote", children)
            case BlockType.HEADING:
                cnt = count_heading(block)
                parent = ParentNode(f"h{cnt}", children)
            case BlockType.ULIST | BlockType.OLIST:
                tagged_children = list(map(lambda x: ParentNode("li", x), children))
                tag = "ul" if block_type == BlockType.ULIST else "ol"
                parent = ParentNode(tag, tagged_children)
        html_nodes.append(parent)
    parent = ParentNode("div", html_nodes)
    return parent


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = list(map(text_node_to_html_node, text_nodes))
    return html_nodes


def count_heading(text):
    cnt = 0
    for char in text:
        if char == "#":
            cnt += 1
        else:
            break
    return cnt
    # Determine the type of block (you already have a function for this)
    # Based on the type of block, create a new HTMLNode with the proper data
    # Assign the proper child HTMLNode objects to the block node. I created a shared text_to_children(text) function that works for all block types. It takes a string of text and returns a list of HTMLNodes that represent the inline markdown using previously created functions (think TextNode -> HTMLNode).
    # The "code" block is a bit of a special case: it should not do any inline markdown parsing of its children. I didn't use my text_to_children function for this block type, I manually made a TextNode and used text_node_to_html_node.
    # Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.
    # Create unit tests. Here are two to get you started:


# Quote blocks should be surrounded by a <blockquote> tag.
# Unordered list blocks should be surrounded by a <ul> tag, and each list item should be surrounded by a <li> tag.
# Ordered list blocks should be surrounded by a <ol> tag, and each list item should be surrounded by a <li> tag.
# Code blocks should be surrounded by a <code> tag nested inside a <pre> tag.
# Headings should be surrounded by a <h1> to <h6> tag, depending on the number of # characters.
# Paragraphs should be surrounded by a <p> tag.
