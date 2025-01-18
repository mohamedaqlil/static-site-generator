import unittest

from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()