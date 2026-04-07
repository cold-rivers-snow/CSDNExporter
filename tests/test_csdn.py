"""
CSDN Parser Tests
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.csdn import CSDNParser


class TestCSDNParser(unittest.TestCase):
    """Test CSDN Parser"""
    
    SAMPLE_HTML = """
    <html>
    <body>
        <h1 class="title-article">Python 教程</h1>
        <span class="time">2024-01-15 10:30:00</span>
        <a class="author-name">张三</a>
        <span class="tit">Python</span>
        <div id="content_views">
            <p>这是文章内容...</p>
            <pre><code class="language-python">print("hello")</code></pre>
        </div>
    </body>
    </html>
    """
    
    def test_get_metadata(self):
        """Test metadata extraction"""
        parser = CSDNParser(self.SAMPLE_HTML, "https://blog.csdn.net/test/article/123")
        metadata = parser.get_metadata()
        
        self.assertEqual(metadata.title, "Python 教程")
        self.assertEqual(metadata.publish_time, "2024-01-15 10:30:00")
        self.assertEqual(metadata.author, "张三")
        self.assertEqual(metadata.category, "Python")
    
    def test_get_content(self):
        """Test content extraction"""
        parser = CSDNParser(self.SAMPLE_HTML, "https://blog.csdn.net/test/article/123")
        content = parser.get_content()
        
        self.assertIn("这是文章内容", content)
        self.assertIn("print", content)
    
    def test_detect_site(self):
        """Test site detection"""
        self.assertTrue(CSDNParser.detect_site("https://blog.csdn.net/test/article/123"))
        self.assertTrue(CSDNParser.detect_site("https://blog.csdn.net/"))
        self.assertFalse(CSDNParser.detect_site("https://jianshu.com/"))
    
    def test_site_domains(self):
        """Test site domains"""
        self.assertIn("csdn.net", CSDNParser.SITE_DOMAINS)


class TestCSDNParsing(unittest.TestCase):
    """Test CSDN HTML to Markdown conversion"""
    
    HTML_WITH_CODE = """
    <html>
    <body>
        <h1 class="title-article">Code Test</h1>
        <span class="time">2024-01-01 00:00:00</span>
        <div id="content_views">
            <pre><code class="prism language-python">def hello():
    print("world")</code></pre>
        </div>
    </body>
    </html>
    """
    
    def test_code_block_parsing(self):
        """Test code block parsing"""
        parser = CSDNParser(self.HTML_WITH_CODE, "http://test.com")
        content = parser.get_content()
        self.assertIn("pre", content)
    
    def test_image_handling(self):
        """Test image handling"""
        html = """
        <html>
        <body>
            <h1 class="title-article">Test</h1>
            <span class="time">2024-01-01 00:00:00</span>
            <div id="content_views">
                <img src="https://img-blog.csdnimg.cn/test.png" />
            </div>
        </body>
        </html>
        """
        parser = CSDNParser(html, "http://test.com")
        self.assertIsNotNone(parser.fig_dir)


if __name__ == '__main__':
    unittest.main()
