"""
Base Parser Tests
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.base import SiteParser, ArticleMetadata


class TestArticleMetadata(unittest.TestCase):
    """Test ArticleMetadata dataclass"""
    
    def test_creation(self):
        """Test metadata creation"""
        metadata = ArticleMetadata(
            title="Test Title",
            publish_time="2024-01-15",
            author="Author",
            tags=["tag1", "tag2"],
            category="category",
            url="https://example.com"
        )
        
        self.assertEqual(metadata.title, "Test Title")
        self.assertEqual(metadata.publish_time, "2024-01-15")
        self.assertEqual(metadata.author, "Author")
        self.assertEqual(metadata.tags, ["tag1", "tag2"])
        self.assertEqual(metadata.category, "category")
        self.assertEqual(metadata.url, "https://example.com")
    
    def test_default_tags(self):
        """Test default tags value"""
        metadata = ArticleMetadata(title="Test", publish_time="2024-01-01")
        self.assertEqual(metadata.tags, [])


class TestSiteParser(unittest.TestCase):
    """Test SiteParser base class"""
    
    HTML_SAMPLE = """
    <html>
    <body>
        <h1>Title</h1>
        <p>Content</p>
        <a href="https://example.com">Link</a>
        <code>code</code>
        <img src="https://example.com/image.png" />
    </body>
    </html>
    """
    
    def test_sanitize_filename(self):
        """Test filename sanitization"""
        result = SiteParser._sanitize_filename("Test:File/Name")
        self.assertNotIn(":", result)
        self.assertNotIn("/", result)
        
        result = SiteParser._sanitize_filename("Test<>Name")
        self.assertNotIn("<", result)
        self.assertNotIn(">", result)
    
    def test_detect_site_classmethod(self):
        """Test detect_site class method"""
        class TestParser(SiteParser):
            SITE_NAME = "Test"
            SITE_DOMAINS = ['test.com', 'test.io']
        
        self.assertTrue(TestParser.detect_site("https://test.com/article"))
        self.assertTrue(TestParser.detect_site("https://test.io/article"))
        self.assertFalse(TestParser.detect_site("https://other.com/article"))


if __name__ == '__main__':
    unittest.main()
