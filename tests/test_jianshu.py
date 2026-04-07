"""
JianShu Parser Tests
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.jianshu import JianShuParser


class TestJianShuParser(unittest.TestCase):
    """Test JianShu Parser"""
    
    SAMPLE_HTML = """
    <html>
    <body>
        <h1>我的第一篇文章</h1>
        <span class="time">2024-01-15</span>
        <span class="nickname">李四</span>
        <a class="category-link">技术</a>
        <a class="tag">Python</a>
        <a class="tag">编程</a>
        <div class="article-content">
            <p>这是简书文章内容...</p>
        </div>
    </body>
    </html>
    """
    
    def test_get_metadata(self):
        """Test metadata extraction"""
        parser = JianShuParser(self.SAMPLE_HTML, "https://www.jianshu.com/p/abc123")
        metadata = parser.get_metadata()
        
        self.assertEqual(metadata.title, "我的第一篇文章")
        self.assertEqual(metadata.author, "李四")
        self.assertIn("Python", metadata.tags)
        self.assertIn("编程", metadata.tags)
    
    def test_get_content(self):
        """Test content extraction"""
        parser = JianShuParser(self.SAMPLE_HTML, "https://www.jianshu.com/p/abc123")
        content = parser.get_content()
        
        self.assertIn("这是简书文章内容", content)
    
    def test_detect_site(self):
        """Test site detection"""
        self.assertTrue(JianShuParser.detect_site("https://www.jianshu.com/p/abc"))
        self.assertTrue(JianShuParser.detect_site("https://jianshu.io/p/abc"))
        self.assertFalse(JianShuParser.detect_site("https://csdn.net/"))


if __name__ == '__main__':
    unittest.main()
