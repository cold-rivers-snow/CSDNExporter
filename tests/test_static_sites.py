"""
Static Site Parser Tests (WordPress, Hexo, Hugo, VuePress)
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.wordpress import WordPressParser
from parsers.hexo import HexoParser
from parsers.hugo import HugoParser
from parsers.vuepress import VuePressParser


class TestWordPressParser(unittest.TestCase):
    """Test WordPress Parser"""
    
    SAMPLE_HTML = """
    <html>
    <body>
        <h1 class="entry-title">WordPress 文章</h1>
        <time class="entry-date" datetime="2024-01-15">2024-01-15</time>
        <span class="byline">作者八</span>
        <span class="cat-links"><a>技术</a></span>
        <span class="tag-links"><a>WordPress</a></span>
        <article>
            <div class="entry-content">
                <p>这是 WordPress 文章内容...</p>
            </div>
        </article>
    </body>
    </html>
    """
    
    def test_get_metadata(self):
        """Test metadata extraction"""
        parser = WordPressParser(self.SAMPLE_HTML, "https://example.wordpress.com/2024/01/15/article")
        metadata = parser.get_metadata()
        
        self.assertEqual(metadata.title, "WordPress 文章")
        self.assertEqual(metadata.author, "作者八")
        self.assertIn("WordPress", metadata.tags)
    
    def test_get_content(self):
        """Test content extraction"""
        parser = WordPressParser(self.SAMPLE_HTML, "https://example.com")
        content = parser.get_content()
        
        self.assertIn("这是 WordPress 文章内容", content)
    
    def test_detect_site(self):
        """Test site detection"""
        self.assertTrue(WordPressParser.detect_site("https://example.wordpress.com/article"))
        self.assertFalse(WordPressParser.detect_site("https://csdn.net/"))


class TestHexoParser(unittest.TestCase):
    """Test Hexo Parser"""
    
    SAMPLE_HTML = """
    <html>
    <body>
        <h1 class="post-title">Hexo 文章</h1>
        <time class="post-time" datetime="2024-01-15">2024-01-15</time>
        <span class="post-author">作者九</span>
        <div class="post-category"><a>技术</a></div>
        <div class="post-tags"><a>Hexo</a></div>
        <article class="post">
            <div class="post-content">
                <p>这是 Hexo 文章内容...</p>
            </div>
        </article>
    </body>
    </html>
    """
    
    def test_get_metadata(self):
        """Test metadata extraction"""
        parser = HexoParser(self.SAMPLE_HTML, "https://example.hexo.io/article")
        metadata = parser.get_metadata()
        
        self.assertEqual(metadata.title, "Hexo 文章")
        self.assertIn("Hexo", metadata.tags)
    
    def test_get_content(self):
        """Test content extraction"""
        parser = HexoParser(self.SAMPLE_HTML, "https://example.hexo.io")
        content = parser.get_content()
        
        self.assertIn("这是 Hexo 文章内容", content)


class TestHugoParser(unittest.TestCase):
    """Test Hugo Parser"""
    
    SAMPLE_HTML = """
    <html>
    <body>
        <h1>Hugo 文章</h1>
        <time datetime="2024-01-15">2024-01-15</time>
        <span class="author">作者十</span>
        <span class="category">技术</span>
        <span class="tags"><a>Hugo</a></span>
        <article>
            <div class="content">
                <p>这是 Hugo 文章内容...</p>
            </div>
        </article>
    </body>
    </html>
    """
    
    def test_get_metadata(self):
        """Test metadata extraction"""
        parser = HugoParser(self.SAMPLE_HTML, "https://example.com/article")
        metadata = parser.get_metadata()
        
        self.assertEqual(metadata.title, "Hugo 文章")
        self.assertEqual(metadata.author, "作者十")
    
    def test_get_content(self):
        """Test content extraction"""
        parser = HugoParser(self.SAMPLE_HTML, "https://example.com")
        content = parser.get_content()
        
        self.assertIn("这是 Hugo 文章内容", content)


class TestVuePressParser(unittest.TestCase):
    """Test VuePress Parser"""
    
    SAMPLE_HTML = """
    <html>
    <body>
        <h1 class="page-title">VuePress 文档</h1>
        <time datetime="2024-01-15">2024-01-15</time>
        <span class="author">作者十一</span>
        <span class="category">文档</span>
        <span class="tags"><a>VuePress</a></span>
        <div class="theme-default-content">
            <p>这是 VuePress 文档内容...</p>
        </div>
    </body>
    </html>
    """
    
    def test_get_metadata(self):
        """Test metadata extraction"""
        parser = VuePressParser(self.SAMPLE_HTML, "https://example.vuepress.io/guide")
        metadata = parser.get_metadata()
        
        self.assertEqual(metadata.title, "VuePress 文档")
        self.assertIn("VuePress", metadata.tags)
    
    def test_get_content(self):
        """Test content extraction"""
        parser = VuePressParser(self.SAMPLE_HTML, "https://example.vuepress.io")
        content = parser.get_content()
        
        self.assertIn("这是 VuePress 文档内容", content)


if __name__ == '__main__':
    unittest.main()
