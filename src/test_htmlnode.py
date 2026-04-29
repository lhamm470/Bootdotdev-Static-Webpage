import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextType, TextNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode(props=
        {"href": "https://www.google.com",
        "target": "_blank",}
        )
        self.assertEqual(node1.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_None_props_to_html(self):
        node1 = HTMLNode()
        self.assertEqual(node1.props_to_html(), "")

    def test_repr(self):
        node1 = HTMLNode("sample_tag", "sample_value")
        self.assertEqual(repr(node1), f'HTMLNode(sample_tag, sample_value, None, None)')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_empty_tag_leaf_to_html(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_full_leaf_to_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leafnode_repr(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(repr(node), "LeafNode(a, Click me!, {'href': 'https://www.google.com'})")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "firstchild")
        child_node2 = LeafNode("b", "secondchild")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>firstchild</span><b>secondchild</b></div>"
        )

    def test_to_html_with_multiple_grandchildren_and_children(self):
        grandchild_node1 = LeafNode("span", "firstgrandchild")
        grandchild_node2 = LeafNode("b", "secondgrandchild")
        child_node1 = ParentNode("a", [grandchild_node1])
        child_node2 = ParentNode("c", [grandchild_node2])
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><a><span>firstgrandchild</span></a><c><b>secondgrandchild</b></c></div>"
        )

    def test_to_html_with_multiple_grandchildren(self):
        grandchild_node1 = LeafNode("span", "firstgrandchild")
        grandchild_node2 = LeafNode("b", "secondgrandchild")
        child_node1 = ParentNode("a", [grandchild_node1, grandchild_node2])
        parent_node = ParentNode("div", [child_node1])
        self.assertEqual(
            parent_node.to_html(),
            "<div><a><span>firstgrandchild</span><b>secondgrandchild</b></a></div>"
        )

    def test_to_html_with_multiple_children_with_multiple_grandchildren(self):
        grandchild_node1 = LeafNode("span", "firstgrandchild")
        grandchild_node2 = LeafNode("b", "secondgrandchild")
        grandchild_node3 = LeafNode("f", "thirdgrandchild")
        grandchild_node4 = LeafNode("bold", "fourthgrandchild")
        child_node1 = ParentNode("a", [grandchild_node1, grandchild_node2])
        child_node2 = ParentNode("italic", [grandchild_node3, grandchild_node4])
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><a><span>firstgrandchild</span><b>secondgrandchild</b></a><italic><f>thirdgrandchild</f><bold>fourthgrandchild</bold></italic></div>"
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode("noparent", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "Children is empty")
        

if __name__ == "__main__":
    unittest.main()