"""
SegmentFault Parser Tests
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.segmentfault import SegmentFaultParser


class TestSegmentFaultParser(unittest.TestCase):
    """Test SegmentFault Parser"""
    
    SAMPLE_HTML = """
    <html>
    <body>
        <h1 class="title">如何学习 Python</h1>
        <time datetime="2024-01-15">2024-01-15</time>
        <a class="author">王五</a>
        <a class="tag">Python</a>
        <a class="tag">教程</a>
        <div class="article__content">
            <p>这是 SegmentFault 文章内容...</p>
        </div>
    </body>
    </html>
    """
    
    def test_get_metadata(self):
        """Test metadata extraction"""
        parser = SegmentFaultParser(self.SAMPLE_HTML, "https://segmentfault.com/a/119000001")
        metadata = parser.get_metadata()
        
        self.assertEqual(metadata.title, "如何学习 Python")
        self.assertEqual(metadata.author, "王五")
        self.assertIn("Python", metadata.tags)
    
    def test_get_content(self):
        """Test content extraction"""
        parser = SegmentFaultParser(self.SAMPLE_HTML, "https://segmentfault.com/a/119000001")
        content = parser.get_content()
        
        self.assertIn("这是 SegmentFault 文章内容", content)
    
    def test_detect_site(self):
        """Test site detection"""
        self.assertTrue(SegmentFaultParser.detect_site("https://segmentfault.com/a/119000001"))
        self.assertFalse(SegmentFaultParser.detect_site("https://csdn.net/"))


if __name__ == '__main__':
    unittest.main()
