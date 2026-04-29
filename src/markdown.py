from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise ValueError("Invalid node: Closing delimiter not found")
            for i in range(len(split_text)):
                if split_text[i] == "":
                    continue
                if i % 2 == 0:
                    result.append(TextNode(split_text[i], TextType.TEXT))
                else:
                    result.append(TextNode(split_text[i], text_type))
    return result

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
        else:
            matches = extract_markdown_images(node.text)
            remaining_text = node.text
            if not matches:
                result.append(node)
            while matches:
                image_alt = matches[0][0]
                image_link = matches[0][1]
                split = remaining_text.split(f"![{image_alt}]({image_link})", 1)
                if split[0] != "":
                    result.append(TextNode(split[0], TextType.TEXT))
                result.append(TextNode(image_alt, TextType.IMAGE, image_link))
                remaining_text = split[1]
                matches = matches[1:]
                if not matches:
                    if split[1] != "":
                        result.append(TextNode(split[1], TextType.TEXT))
    return result

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
        else:
            matches = extract_markdown_links(node.text)
            remaining_text = node.text
            if not matches:
                result.append(node)
            while matches:
                link_alt = matches[0][0]
                link_link = matches[0][1]
                split = remaining_text.split(f"[{link_alt}]({link_link})", 1)
                if split[0] != "":
                    result.append(TextNode(split[0], TextType.TEXT))
                result.append(TextNode(link_alt, TextType.LINK, link_link))
                remaining_text = split[1]
                matches = matches[1:]
                if not matches:
                    if split[1] != "":
                        result.append(TextNode(split[1], TextType.TEXT))
    return result

def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]
    new_node = split_nodes_delimiter(node, "**", TextType.BOLD)
    new_node = split_nodes_delimiter(new_node, "`", TextType.CODE)
    new_node = split_nodes_delimiter(new_node, "_", TextType.ITALIC)
    new_node = split_nodes_image(new_node)
    new_node = split_nodes_link(new_node)
    return new_node
