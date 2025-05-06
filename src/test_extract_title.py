import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_basic_title(self):
        markdown = "# Hello, World!"
        self.assertEqual(extract_title(markdown), "Hello, World!")
    
    def test_title_with_extra_whitespace(self):
        markdown = "#     Lots of spaces     "
        self.assertEqual(extract_title(markdown), "Lots of spaces")
    
    def test_multiline_markdown(self):
        markdown = """# This is the title
        
        This is a paragraph.
        
        ## This is a subheading
        """
        self.assertEqual(extract_title(markdown), "This is the title")
    
    def test_no_title(self):
        markdown = "This is just text\n## This is a subheading"
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_title_not_at_beginning(self):
        markdown = "Some text first\n# Title in the middle\nMore text"
        self.assertEqual(extract_title(markdown), "Title in the middle")

if __name__ == "__main__":
    unittest.main()