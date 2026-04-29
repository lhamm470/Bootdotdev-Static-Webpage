from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node, TextNode
from markdown import text_to_textnodes
from textnode import TextType

def markdown_to_blocks(markdown):
    result = []
    blocks = markdown.split("\n\n")
    for i in range(len(blocks)):
        if blocks[i] == "":
            continue
        else:
            result.append(blocks[i].strip())
    return result

BlockType = Enum("BlockType", [
    "PARAGRAPH", 
    "HEADING", 
    "CODE", 
    "QUOTE", 
    "ULIST", 
    "OLIST"
    ]
    )

def block_to_block_type(markdown):
    lines = markdown.split("\n")
    
    if markdown == "":
        return BlockType.PARAGRAPH
    
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if markdown[:4] == "```\n" and markdown[-3:] == "```":
        return BlockType.CODE

    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
    if is_quote:
        return BlockType.QUOTE

    is_unordered_list = True
    for line in lines:
        if not line.startswith("- "):
            is_unordered_list = False
    if is_unordered_list:
        return BlockType.ULIST

    is_ordered_list = True
    for i in range(len(lines)):
        if not lines[i].startswith(f"{i + 1}. "):
            is_ordered_list = False
    if is_ordered_list:
        return BlockType.OLIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        lines = block.split("\n")
        stripped_text = ""

        if block_type == BlockType.PARAGRAPH:
            tag = "p"
            stripped_text = block.replace("\n", " ")
            block_children = text_to_children(stripped_text)

        elif block_type == BlockType.HEADING:
            heading_number = get_heading_number(block)
            tag = f"h{heading_number}"
            stripped_text = block[heading_number + 1:]
            block_children = text_to_children(stripped_text)

        elif block_type == BlockType.CODE:
            tag = "code"
            stripped_text = block[4:-3]
            text_node = TextNode(stripped_text, TextType.TEXT)
            code_html = text_node_to_html_node(text_node)
            code_node = ParentNode("code", [code_html])
            node = ParentNode("pre", [code_node])
            children.append(node)
            continue

        elif block_type == BlockType.QUOTE:
            tag = "blockquote"
            stripped_text = get_quote_stripped_text(lines)
            block_children = text_to_children(stripped_text)

        elif block_type == BlockType.ULIST:
            tag = "ul"
            li_nodes = get_ulist_li_nodes(lines)
            block_children = li_nodes

        elif block_type == BlockType.OLIST:
            tag = "ol"
            li_nodes = get_olist_li_nodes(lines)
            block_children = li_nodes

        node = ParentNode(tag, block_children)
        children.append(node)

    return ParentNode("div", children)

def text_to_children(text):
    nodes = text_to_textnodes(text)
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node)) 
    return html_nodes

def get_heading_number(block):
    heading_number = 0
    for char in block[:6]:
        if char == "#":
            heading_number += 1
        else:
            break
    return heading_number

def get_quote_stripped_text(lines):
    stripped_lines = []
    for line in lines:
        if line.startswith("> "):
            stripped_text = line[2:]
        elif line.startswith(">"):
            stripped_text = line[1:]
        stripped_lines.append(stripped_text)
    stripped_text = " ".join(stripped_lines)
    return stripped_text

def get_ulist_li_nodes(lines):
    li_nodes = []
    for line in lines:
        stripped_text = line[2:]
        li_child = text_to_children(stripped_text)
        li_nodes.append(ParentNode("li", li_child))
    return li_nodes

def get_olist_li_nodes(lines):
    li_nodes = []
    for line in lines:
        number_length = 0
        for character in line:
            if character.isdigit():
                number_length += 1
            else:
                break
        stripped_text = line[number_length + 2:]
        li_child = text_to_children(stripped_text)
        li_nodes.append(ParentNode("li", li_child))
    return li_nodes