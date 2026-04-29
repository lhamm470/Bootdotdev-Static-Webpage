import unittest

from generate_webpage import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_generate_webpage_invalid(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "Invalid header")


    def test_generate_webpage(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

# Header 1 is this line.

- This is a list
- with items
"""
        self.assertEqual(extract_title(md), "Header 1 is this line.")

    def test_generate_webpage_hello(self):
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")