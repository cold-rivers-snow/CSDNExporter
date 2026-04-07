"""
CnBlogs Parser Tests
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.cnblogs import CnBlogsParser


class TestCnBlogsParser(unittest.TestCase):
    """Test CnBlogs (博客园) Parser"""
    
    SAMPLE_HTML = """
    <html>
    <body>
        <div id="blog_title">
            <h2>唐三三的博客</h2>
        </div>
        <h1 id="post_title">Oh-My-OpenCode 3.5.6 完整使用指南</h1>
        <span class="postfoot">发布于 2026-02-17 01:28</span>
        <div class="postDesc">作者：唐三三 浏览: 11991 评论: 0</div>
        <div id="BlogPostCategory">
            <a>OpenCode</a>
            <a>教程</a>
        </div>
        <div id="EntryTag">
            <a>OpenCode</a>
            <a>AI</a>
            <a>教程</a>
        </div>
        <div id="cnblogs_post_body">
            <p>这是博客园文章内容...</p>
            <pre><code class="language-python">print("hello")</code></pre>
            <img src="https://pic.cnblogs.com/test.png" />
        </div>
    </body>
    </html>
    """
    
    def test_get_metadata(self):
        """Test metadata extraction"""
        parser = CnBlogsParser(self.SAMPLE_HTML, "https://www.cnblogs.com/tangge/p/19620738")
        metadata = parser.get_metadata()
        
        self.assertEqual(metadata.title, "Oh-My-OpenCode 3.5.6 完整使用指南")
        self.assertIn("2026", metadata.publish_time)
        self.assertEqual(metadata.author, "唐三三的博客")
        self.assertIn("OpenCode", metadata.tags)
        self.assertIn("AI", metadata.tags)
    
    def test_get_content(self):
        """Test content extraction"""
        parser = CnBlogsParser(self.SAMPLE_HTML, "https://www.cnblogs.com/tangge/p/19620738")
        content = parser.get_content()
        
        self.assertIn("这是博客园文章内容", content)
        self.assertIn("print", content)
    
    def test_detect_site(self):
        """Test site detection"""
        self.assertTrue(CnBlogsParser.detect_site("https://www.cnblogs.com/tangge/p/19620738"))
        self.assertTrue(CnBlogsParser.detect_site("https://cnblogs.com/tangge/p/123"))
        self.assertTrue(CnBlogsParser.detect_site("https://www.cnblogs.com/"))
        self.assertFalse(CnBlogsParser.detect_site("https://csdn.net/"))
    
    def test_site_domains(self):
        """Test site domains"""
        self.assertIn("cnblogs.com", CnBlogsParser.SITE_DOMAINS)


if __name__ == '__main__':
    unittest.main()
