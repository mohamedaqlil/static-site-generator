import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node2", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(node, node2)
    
    def test_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "link")
        node2 = TextNode("This is a text node", TextType.BOLD, url = None)
        self.assertNotEqual(node, node2)

    def test_all_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url = None)
        node2 = TextNode("This is a text node", TextType.BOLD, url = None)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, Bold, https://www.boot.dev)", repr(node)
        )

class TestTextNodeToHTMLNode(unittest.TestCase):

    def setUp(self):
        # Reusable sample value
        self.sample_url = "http://example.com"

    def test_text_type_text(self):
        # Mock a TextNode for TEXT type
        text_node = TextNode(text="Hello", text_type=TextType.TEXT)
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, None)
        self.assertEqual(result.value, "Hello")
        self.assertEqual(result.props, None)

    def test_text_type_bold(self):
        # Mock a TextNode for BOLD type
        text_node = TextNode(text="Bold Text", text_type=TextType.BOLD)
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, "b")
        self.assertEqual(result.value, "Bold Text")
        self.assertEqual(result.props, None)

    def test_text_type_link(self):
        # Mock a TextNode for LINK type
        text_node = TextNode(text="Click here", text_type=TextType.LINK, url=self.sample_url)
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, "a")
        self.assertEqual(result.value, "Click here")
        self.assertEqual(result.props, {"href": self.sample_url})

if __name__ == "__main__":
    unittest.main()
