"""
Tencent Cloud Parser Tests
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.tencent import TencentCloudParser
from parsers.meituan import MeituanParser
from parsers.cloudflare import CloudFlareParser


class TestTencentCloudParser(unittest.TestCase):
    """Test Tencent Cloud Parser"""
    
    SAMPLE_HTML = """
    <html>
    <body>
        <h1 class="article-info__title">腾讯云教程</h1>
        <span class="article-info__date">2024-01-15</span>
        <span class="article-info__author">赵六</span>
        <a class="tag">云计算</a>
        <div class="article-info">
            <p>这是腾讯云文章内容...</p>
        </div>
    </body>
    </html>
    """
    
    def test_get_metadata(self):
        """Test metadata extraction"""
        parser = TencentCloudParser(self.SAMPLE_HTML, "https://cloud.tencent.com/dev/123")
        metadata = parser.get_metadata()
        
        self.assertEqual(metadata.title, "腾讯云教程")
        self.assertEqual(metadata.author, "赵六")
    
    def test_get_content(self):
        """Test content extraction"""
        parser = TencentCloudParser(self.SAMPLE_HTML, "https://cloud.tencent.com/dev/123")
        content = parser.get_content()
        
        self.assertIn("这是腾讯云文章内容", content)
    
    def test_detect_site(self):
        """Test site detection"""
        self.assertTrue(TencentCloudParser.detect_site("https://cloud.tencent.com/developer/article/123"))
        self.assertFalse(TencentCloudParser.detect_site("https://csdn.net/"))


class TestMeituanParser(unittest.TestCase):
    """Test Meituan Parser"""
    
    SAMPLE_HTML = """
    <html>
    <body>
        <h1 class="article-title">美团技术文章</h1>
        <span class="time">2024-01-15</span>
        <span class="author">孙七</span>
        <a class="tag">后端</a>
        <article class="article">
            <p>这是美团技术文章内容...</p>
        </article>
    </body>
    </html>
    """
    
    def test_get_metadata(self):
        """Test metadata extraction"""
        parser = MeituanParser(self.SAMPLE_HTML, "https://tech.meituan.com/2024/01/15/article")
        metadata = parser.get_metadata()
        
        self.assertEqual(metadata.title, "美团技术文章")
        self.assertEqual(metadata.author, "孙七")
    
    def test_get_content(self):
        """Test content extraction"""
        parser = MeituanParser(self.SAMPLE_HTML, "https://tech.meituan.com/article")
        content = parser.get_content()
        
        self.assertIn("这是美团技术文章内容", content)


class TestCloudFlareParser(unittest.TestCase):
    """Test CloudFlare Parser"""
    
    SAMPLE_HTML = """
    <html>
    <body>
        <h1 class="Blog-title">CloudFlare 新功能</h1>
        <time class="Blog-date" datetime="2024-01-15">2024-01-15</time>
        <a class="Blog-author">CloudFlare Team</a>
        <a class="tag">CDN</a>
        <article class="Blog">
            <p>这是 CloudFlare 博客内容...</p>
        </article>
    </body>
    </html>
    """
    
    def test_get_metadata(self):
        """Test metadata extraction"""
        parser = CloudFlareParser(self.SAMPLE_HTML, "https://blog.cloudflare.com/new-feature")
        metadata = parser.get_metadata()
        
        self.assertEqual(metadata.title, "CloudFlare 新功能")
        self.assertEqual(metadata.author, "CloudFlare Team")
    
    def test_get_content(self):
        """Test content extraction"""
        parser = CloudFlareParser(self.SAMPLE_HTML, "https://blog.cloudflare.com/article")
        content = parser.get_content()
        
        self.assertIn("这是 CloudFlare 博客内容", content)


if __name__ == '__main__':
    unittest.main()
