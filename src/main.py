from textnode import TextNode, TextType
import os
from copystatic import move_directory
from generate_webpage import generate_page, generate_pages_recursive

def main():
    move_directory("./static", "./public")
    generate_pages_recursive("content", "template.html", "public")


main()