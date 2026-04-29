from markdown_blocks import markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
import os
from pathlib import Path

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("Invalid header")

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path) as f:
        markdown_content = f.read()
    with open(template_path, "r") as f:
        template_content = f.read()
    
    html = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)

    updated_template = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(updated_template)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content, item)
        if os.path.isfile(path):
            dest_path = Path(os.path.join(dest_dir_path, item)).with_suffix(".html")
            print(f"Writing: {dest_path}")
            generate_page(path, template_path, dest_path)
        elif os.path.isdir(path):
            generate_pages_recursive(path, template_path, os.path.join(dest_dir_path, item))