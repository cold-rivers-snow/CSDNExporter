"""
Other Site Parsers Tests (OSChina, Zhihu, Lofter, Feishu, WeChat)
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.oschina import OSChinaParser
from parsers.zhihu import ZhihuParser
from parsers.lofter import LofterParser
from parsers.feishu import FeishuParser
from parsers.wechat import WeChatParser


class TestOSChinaParser(unittest.TestCase):
    """Test OSChina Parser"""
    
    SAMPLE_HTML = """
    <html>
    <body>
        <h1 class="title">开源中国文章</h1>
        <span class="date">2024-01-15</span>
        <a class="author">作者甲</a>
        <a class="tag">开源</a>
        <div class="blog-content">
            <p>这是开源中国文章内容...</p>
        </div>
    </body>
    </html>
    """
    
    def test_get_metadata(self):
        """Test metadata extraction"""
        parser = OSChinaParser(self.SAMPLE_HTML, "https://my.oschina.net/u/123/blog/789")
        metadata = parser.get_metadata()
        
        self.assertEqual(metadata.title, "开源中国文章")
        self.assertEqual(metadata.author, "作者甲")
    
    def test_get_content(self):
        """Test content extraction"""
        parser = OSChinaParser(self.SAMPLE_HTML, "https://oschina.net/article")
        content = parser.get_content()
        
        self.assertIn("这是开源中国文章内容", content)


class TestZhihuParser(unittest.TestCase):
    """Test Zhihu Parser"""
    
    SAMPLE_HTML = """
    <html>
    <body>
        <h1 class="Post-Index-Title">知乎文章</h1>
        <span class="Date">2024-01-15</span>
        <span class="author">作者乙</span>
        <a class="tag">科技</a>
        <div class="ArticleItem">
            <p>这是知乎文章内容...</p>
        </div>
    </body>
    </html>
    """
    
    def test_get_metadata(self):
        """Test metadata extraction"""
        parser = ZhihuParser(self.SAMPLE_HTML, "https://zhuanlan.zhihu.com/p/123456789")
        metadata = parser.get_metadata()
        
        self.assertEqual(metadata.title, "知乎文章")
    
    def test_get_content(self):
        """Test content extraction"""
        parser = ZhihuParser(self.SAMPLE_HTML, "https://zhihu.com/article")
        content = parser.get_content()
        
        self.assertIn("这是知乎文章内容", content)


class TestLofterParser(unittest.TestCase):
    """Test Lofter Parser"""
    
    SAMPLE_HTML = """
    <html>
    <body>
        <h1 class="title">Lofter 帖子</h1>
        <span class="date">2024-01-15</span>
        <span class="nickname">作者丙</span>
        <a class="tag">摄影</a>
        <div class="post-content">
            <p>这是 Lofter 内容...</p>
        </div>
    </body>
    </html>
    """
    
    def test_get_metadata(self):
        """Test metadata extraction"""
        parser = LofterParser(self.SAMPLE_HTML, "https://username.lofter.com/post/abc")
        metadata = parser.get_metadata()
        
        self.assertEqual(metadata.title, "Lofter 帖子")
        self.assertEqual(metadata.author, "作者丙")
    
    def test_detect_site(self):
        """Test site detection"""
        self.assertTrue(LofterParser.detect_site("https://username.lofter.com/post/abc"))
        self.assertFalse(LofterParser.detect_site("https://csdn.net/"))


class TestFeishuParser(unittest.TestCase):
    """Test Feishu Parser"""
    
    SAMPLE_HTML = """
    <html>
    <body>
        <h1 class="docx-title">飞书文档</h1>
        <span class="publish-time">2024-01-15</span>
        <span class="author">作者丁</span>
        <div class="docx-body">
            <p>这是飞书文档内容...</p>
        </div>
    </body>
    </html>
    """
    
    def test_get_metadata(self):
        """Test metadata extraction"""
        parser = FeishuParser(self.SAMPLE_HTML, "https://feishu.cn/content/abc")
        metadata = parser.get_metadata()
        
        self.assertEqual(metadata.title, "飞书文档")
    
    def test_get_content(self):
        """Test content extraction"""
        parser = FeishuParser(self.SAMPLE_HTML, "https://feishu.cn")
        content = parser.get_content()
        
        self.assertIn("这是飞书文档内容", content)


class TestWeChatParser(unittest.TestCase):
    """Test WeChat Parser"""
    
    SAMPLE_HTML = """
    <html>
    <body>
        <h1 id="activity-name">微信公众号文章</h1>
        <span id="publish_time">2024-01-15</span>
        <span id="author_name">作者戊</span>
        <div id="js_content">
            <p>这是微信公众号文章内容...</p>
            <img src="https://mmbiz.qpic.cn/test.jpg" />
        </div>
    </body>
    </html>
    """
    
    def test_get_metadata(self):
        """Test metadata extraction"""
        parser = WeChatParser(self.SAMPLE_HTML, "https://mp.weixin.qq.com/s/abc123")
        metadata = parser.get_metadata()
        
        self.assertEqual(metadata.title, "微信公众号文章")
        self.assertEqual(metadata.author, "作者戊")
    
    def test_get_content(self):
        """Test content extraction"""
        parser = WeChatParser(self.SAMPLE_HTML, "https://mp.weixin.qq.com/s/abc")
        content = parser.get_content()
        
        self.assertIn("这是微信公众号文章内容", content)
        self.assertIn("mmbiz.qpic.cn", content)
    
    def test_detect_site(self):
        """Test site detection"""
        self.assertTrue(WeChatParser.detect_site("https://mp.weixin.qq.com/s/abc123"))
        self.assertTrue(WeChatParser.detect_site("https://weixin.qq.com/article"))


if __name__ == '__main__':
    unittest.main()
