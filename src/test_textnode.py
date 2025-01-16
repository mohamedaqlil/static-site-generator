import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "link")
        node2 = TextNode("This is a text node", TextType.BOLD, "link")
        self.assertEqual(node, node2)
    
    def test_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "link")
        node2 = TextNode("This is a text node", TextType.BOLD, url = None)
        self.assertNotEqual(node, node2)

    def test_all_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url = None)
        node2 = TextNode("This is a text node", TextType.BOLD, url = None)
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()