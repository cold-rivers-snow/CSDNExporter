"""
Parser Factory Tests
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.factory import ParserFactory


class TestParserFactory(unittest.TestCase):
    """Test ParserFactory detection and creation"""
    
    def test_csdn_detection(self):
        """Test CSDN URL detection"""
        url = "https://blog.csdn.net/user/article/details/123456"
        parser_name = ParserFactory.auto_detect(url)
        self.assertEqual(parser_name, 'csdn')
    
    def test_jianshu_detection(self):
        """Test JianShu URL detection"""
        url = "https://www.jianshu.com/p/abc123"
        parser_name = ParserFactory.auto_detect(url)
        self.assertEqual(parser_name, 'jianshu')
    
    def test_segmentfault_detection(self):
        """Test SegmentFault URL detection"""
        url = "https://segmentfault.com/a/119000001"
        parser_name = ParserFactory.auto_detect(url)
        self.assertEqual(parser_name, 'segmentfault')
    
    def test_oschina_detection(self):
        """Test OSChina URL detection"""
        url = "https://my.oschina.net/u/123456/blog/789012"
        parser_name = ParserFactory.auto_detect(url)
        self.assertEqual(parser_name, 'oschina')
    
    def test_zhihu_detection(self):
        """Test Zhihu URL detection"""
        url = "https://zhuanlan.zhihu.com/p/123456789"
        parser_name = ParserFactory.auto_detect(url)
        self.assertEqual(parser_name, 'zhihu')
    
    def test_tencent_detection(self):
        """Test Tencent Cloud URL detection"""
        url = "https://cloud.tencent.com/developer/article/1234567"
        parser_name = ParserFactory.auto_detect(url)
        self.assertEqual(parser_name, 'tencent')
    
    def test_meituan_detection(self):
        """Test Meituan Tech URL detection"""
        url = "https://tech.meituan.com/2024/01/01/article.html"
        parser_name = ParserFactory.auto_detect(url)
        self.assertEqual(parser_name, 'meituan')
    
    def test_cloudflare_detection(self):
        """Test CloudFlare Blog URL detection"""
        url = "https://blog.cloudflare.com/announcing-new-feature"
        parser_name = ParserFactory.auto_detect(url)
        self.assertEqual(parser_name, 'cloudflare')
    
    def test_cnblogs_detection(self):
        """Test CnBlogs URL detection"""
        url = "https://www.cnblogs.com/tangge/p/19620738"
        parser_name = ParserFactory.auto_detect(url)
        self.assertEqual(parser_name, 'cnblogs')
    
    def test_lofter_detection(self):
        """Test Lofter URL detection"""
        url = "https://username.lofter.com/post/abc123"
        parser_name = ParserFactory.auto_detect(url)
        self.assertEqual(parser_name, 'lofter')
    
    def test_feishu_detection(self):
        """Test Feishu URL detection"""
        url = "https://feishu.cn/content/abc123"
        parser_name = ParserFactory.auto_detect(url)
        self.assertEqual(parser_name, 'feishu')
    
    def test_wordpress_detection(self):
        """Test WordPress URL detection"""
        url = "https://example.wordpress.com/2024/01/01/article"
        parser_name = ParserFactory.auto_detect(url)
        self.assertEqual(parser_name, 'wordpress')
    
    def test_hexo_detection(self):
        """Test Hexo URL detection"""
        url = "https://example.hexo.io/article"
        parser_name = ParserFactory.auto_detect(url)
        self.assertEqual(parser_name, 'hexo')
    
    def test_wechat_detection(self):
        """Test WeChat URL detection"""
        url = "https://mp.weixin.qq.com/s/abc123"
        parser_name = ParserFactory.auto_detect(url)
        self.assertEqual(parser_name, 'wechat')
    
    def test_list_parsers(self):
        """Test listing all registered parsers"""
        parsers = ParserFactory.list_parsers()
        self.assertIsInstance(parsers, list)
        self.assertGreater(len(parsers), 0)
    
    def test_create_parser_by_name(self):
        """Test creating parser by name"""
        from parsers.csdn import CSDNParser
        parser = ParserFactory.create('csdn', html="<html></html>", url="http://test.com")
        self.assertIsInstance(parser, CSDNParser)


if __name__ == '__main__':
    unittest.main()
