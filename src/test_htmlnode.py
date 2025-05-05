import unittest
from htmlnode import LeafNode, ParentNode, HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        expected = " href=\"https://example.com\" target=\"_blank\""
        self.assertEqual(node1.props_to_html(), expected)
        
    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"class": "text-bold"})
        expected = " class=\"text-bold\""
        self.assertEqual(node.props_to_html(), expected)
    def test_repr(self):
        node = HTMLNode(tag="p", value="Hello World", children=[], props={"class": "text"})
        expected = "HTMLNode(p, Hello World, [], {\'class\': \'text\'})"
        self.assertEqual(expected, repr(node))

    def test_repr_with_none_values(self):
        node = HTMLNode()  
        expected = "HTMLNode(None, None, None, None)"
        self.assertEqual(expected, repr(node))

    def test_leafnode_with_tag_and_value(self):
        node = LeafNode(tag="span", value="Hello")
        expected = "<span>Hello</span>"
        self.assertEqual(node.to_html(), expected)

    def test_leafnode_without_tag(self):
        node = LeafNode(value="Raw text")
        expected = "Raw text"
        self.assertEqual(node.to_html(), expected)

    def test_leafnode_with_props(self):
        node = LeafNode(tag="a", value="Click me!", props={"href": "https://example.com"})
        expected = '<a href="https://example.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)

    def test_leafnode_repr(self):
        node = LeafNode(tag="p", value="Leaf node", props={"class": "leaf"})
        expected = "HTMLNode(p, Leaf node, None, {'class': 'leaf'})"
        self.assertEqual(repr(node), expected)

    def test_leafnode_missing_value(self):
        with self.assertRaises(ValueError) as context:
            LeafNode(tag="p", value=None)  # Instantiation should fail directly
            self.assertEqual(str(context.exception), "A LeafNode must have a value")
    
    def test_parentnode_with_tag_and_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text")
                ]
                )
        expected = "<p><b>Bold text</b></p>"
        self.assertEqual(node.to_html(), expected)

    def test_parentnode_without_tag(self):
        with self.assertRaises(ValueError) as context:
            ParentNode(tag=None, children=[LeafNode("b", "Bold text")])  # Instantiation should fail directly
            self.assertEqual(str(context.exception), "A ParentNode must have a tag")

    def test_parentnode_without_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode(tag="p", children=None)  # Instantiation should fail directly
            self.assertEqual(str(context.exception), "children is a missing value")

    def test_multiple_children_parentnode(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                ],
                )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_parentnode_repr(self):
        node = ParentNode(
            tag="p",
            children=[LeafNode("b", "Bold text")],
            props={"class": "parent"}
            )
        expected = "HTMLNode(p, None, [HTMLNode(b, Bold text, None, None)], {'class': 'parent'})"
        self.assertEqual(repr(node), expected)

    def test_nested_parentnode(self):
        inner_node = ParentNode(
            "p",
            [LeafNode("b", "Bold text")]
            )
        outer_node = ParentNode(
            "div",
            [inner_node]
            )
        expected = "<div><p><b>Bold text</b></p></div>"
        self.assertEqual(outer_node.to_html(), expected)

if __name__ == "__main__":
    unittest.main()