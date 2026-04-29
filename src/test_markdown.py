import unittest
import re

from textnode import TextType, TextNode
from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE), 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ])

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD), 
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ])

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with an _italic block_ word", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "_", TextType.ITALIC), 
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ])

    def test_split_nodes_delimiter_multiple_nodes(self):
        node1 = TextNode("This is text with an _italic block_ word", TextType.TEXT)
        node2 = TextNode("Here is another _italic block_ word", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node1, node2], "_", TextType.ITALIC), 
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
                TextNode("Here is another ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ])

    def test_split_nodes_delimiter_invalid_delimiters(self):
        node = TextNode("This is text with **no closing delimiter", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", TextType.ITALIC)
        self.assertEqual(str(context.exception), "Invalid node: Closing delimiter not found")

    def text_split_nodes_delimiter_invalid_TextType(self):
        node = TextNode("This is bold with **bold** text", TextType.BOLD)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD, 
            [
                TextNode("This is bold with **bold** text", TextType.BOLD)
            ])
            )

class TestRegexMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a [to boot dev](https://www.boot.dev) and a [to rick roll](https://www.rickroll.com)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to rick roll", "https://www.rickroll.com")], matches)

    def test_extract_markdown_image_and_link(self):
        image_matches = extract_markdown_images(
            "This is text with a [to boot dev](https://www.boot.dev) and a ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        link_matches = extract_markdown_links(
            "This is text with a [to boot dev](https://www.boot.dev) and a ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], image_matches)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], link_matches)

class TestSplitNodes(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) is an image, and another is: ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is an image, and another is: ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_none(self):
        node = TextNode(
            "There are no images here...",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("There are no images here...", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [second link](https://www.rickroll.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.rickroll.com"
                ),
            ],
            new_nodes,
        )

    def test_split_links_at_start(self):
        node = TextNode(
            "[link](https://www.boot.dev) is a link, and another is: [second link](https://www.rickroll.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" is a link, and another is: ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.rickroll.com"
                ),
            ],
            new_nodes,
        )

    def test_split_links_none(self):
        node = TextNode(
            "There are no links here...",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("There are no links here...", TextType.TEXT),
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_node = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_node,
        )

    def test_text_to_textnodes_extras(self):
        text = "_This_ is **text** with **multiple** types of `inline markdown types:` an _italic_ word and a ![jar jar image](https://i.imgur.com/gsdfhn3G.jpeg) `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) and _finally, for the finale:_ another **long bold sentence that just keeps going on and on and on and on and**"
        new_node = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This", TextType.ITALIC),
                TextNode(" is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with ", TextType.TEXT),
                TextNode("multiple", TextType.BOLD),
                TextNode(" types of ", TextType.TEXT),
                TextNode("inline markdown types:", TextType.CODE),
                TextNode(" an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("jar jar image", TextType.IMAGE, "https://i.imgur.com/gsdfhn3G.jpeg"),
                TextNode(" ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("finally, for the finale:", TextType.ITALIC),
                TextNode(" another ", TextType.TEXT),
                TextNode("long bold sentence that just keeps going on and on and on and on and", TextType.BOLD),
            ],
            new_node,
        )        