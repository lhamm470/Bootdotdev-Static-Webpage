import unittest

from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

def test_markdown_to_blocks_multiple_lists(self):
        md = """
- This is a list
- With many
- Items.
- Four to be precise
- Or was it five?

This is a paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is another list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "- This is a list\n- With many\n- Items.\n- Four to be precise\n- Or was it five?",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        markdown = """This is a normal paragraph.
Even though there are newlines, it is still a paragraph."""
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_heading(self):
        markdown = """### This is a heading.
Even though there are newlines, it is still a heading."""
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.HEADING
        )

    def test_block_to_block_type_code(self):
        markdown = """```
This is a code.
Even though there are newlines, it is still a code.```"""
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.CODE
        )

    def test_block_to_block_type_quote(self):
        markdown = """> Quote example.
>Can be with or without space after >.
> End of quote."""
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.QUOTE
        )

    def test_block_to_block_type_ulist(self):
        markdown = """- This is an unordered list.
- Starting with '- ' is how they work."""
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.ULIST
        )

    def test_block_to_block_type_olist(self):
        markdown = """1. This is an ordered list.
2. They need to start with 'i. ', where i starts at 1 and increments by +1 every line.
3. I will test going beyond single digits soon."""
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.OLIST
        )

    def test_block_to_block_type_heading_too_many_hashtags(self):
        markdown = """########### This will not be a heading.
Even though there are newlines, it is still not a heading."""
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_quote_with_missing_character(self):
        markdown = """> This should be a quote.
Oops I forgot a '>'.
Now it is a paragraph."""
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_olist_shuffled(self):
        markdown = """1. First sentence.
2. Second sentence.
4. Fourth sentence.
3. Third sentence."""
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.PARAGRAPH
        )

    def test_block_to_block_type_olist_large(self):
        markdown = """1. First sentence.
2. Second sentence.
3. Third sentence.
4. Fourth sentence.
5. Fifth sentence.
6. Sixth sentence.
7. Seventh sentence.
8. Eigth sentence.
9. Ninth sentence.
10. Tenth sentence.
11. Eleventh sentence.
12. Twelfth sentence."""
        self.assertEqual(
            block_to_block_type(markdown),
            BlockType.OLIST
        )

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_paragraphs_with_everything(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

This is another paragraph with an ![image](https:www.link), some **bold text** and a link: [link](link.link).

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p><p>This is another paragraph with an <img src="https:www.link" alt="image"></img>, some <b>bold text</b> and a link: <a href="link.link">link</a>.</p></div>',
        )