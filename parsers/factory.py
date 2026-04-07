"""
Parser Factory - Auto-detect and create appropriate parser
"""
import re
from typing import Optional, Type, List
from .base import SiteParser


class ParserFactory:
    """Factory class for creating site-specific parsers"""
    
    _parsers: List[Type[SiteParser]] = []
    _domain_mapping = {}
    
    @classmethod
    def register(cls, parser_class: Type[SiteParser]):
        """Register a parser class"""
        cls._parsers.append(parser_class)
        for domain in parser_class.SITE_DOMAINS:
            cls._domain_mapping[domain] = parser_class
    
    @classmethod
    def get_parser(cls, url: str, html: str = "", **kwargs) -> SiteParser:
        """Get appropriate parser based on URL or HTML content"""
        url = url.lower()
        
        # Try URL-based detection first
        for domain, parser_class in cls._domain_mapping.items():
            if domain in url:
                if html:
                    return parser_class(html, url, **kwargs)
                return parser_class
        
        # Fallback: try content-based detection
        if html:
            return cls._detect_from_content(html, url, **kwargs)
        
        # Default to CSDN parser
        from .csdn import CSDNParser
        return CSDNParser
    
    @classmethod
    def _detect_from_content(cls, html: str, url: str, **kwargs) -> SiteParser:
        """Detect parser from HTML content structure"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # CSDN detection
        if soup.find('h1', {'class': 'title-article'}):
            from .csdn import CSDNParser
            return CSDNParser
        
        # JianShu detection
        if soup.find('div', {'class': 'note-text'}):
            from .jianshu import JianShuParser
            return JianShuParser
        
        # SegmentFault detection
        if soup.find('div', {'class': 'article__content'}):
            from .segmentfault import SegmentFaultParser
            return SegmentFaultParser
        
        # 知乎 detection
        if soup.find('div', {'class': 'ArticleItem'}):
            from .zhihu import ZhihuParser
            return ZhihuParser
        
        # 开源中国 detection
        if soup.find('div', {'class': 'blog-content'}):
            from .oschina import OSChinaParser
            return OSChinaParser
        
        # 腾讯云 detection
        if soup.find('div', {'class': 'article-info'}):
            from .tencent import TencentCloudParser
            return TencentCloudParser
        
        # 美团技术 detection
        if soup.find('article', {'class': 'article'}):
            from .meituan import MeituanParser
            return MeituanParser
        
        # CloudFlare detection
        if soup.find('article', {'class': 'Blog'}):
            from .cloudflare import CloudFlareParser
            return CloudFlareParser
        
        # WordPress detection
        if soup.find('article') or soup.find('div', {'class': 'entry-content'}):
            from .wordpress import WordPressParser
            return WordPressParser
        
        # Default fallback - use generic parser
        from .csdn import CSDNParser
        return CSDNParser
    
    @classmethod
    def create(cls, parser_name: str, html: str = "", url: str = "", **kwargs) -> SiteParser:
        """Create parser by name"""
        parser_map = {
            'csdn': ('csdn', CSDNParser),
            'jianshu': ('jianshu', JianShuParser),
            'segmentfault': ('segmentfault', SegmentFaultParser),
            'oschina': ('oschina', OSChinaParser),
            'zhihu': ('zhihu', ZhihuParser),
            'tencent': ('tencent', TencentCloudParser),
            'meituan': ('meituan', MeituanParser),
            'cloudflare': ('cloudflare', CloudFlareParser),
            'lofter': ('lofter', LofterParser),
            'feishu': ('feishu', FeishuParser),
            'cnblogs': ('cnblogs', CnBlogsParser),
            'wordpress': ('wordpress', WordPressParser),
            'hexo': ('hexo', HexoParser),
            'hugo': ('hugo', HugoParser),
            'vuepress': ('vuepress', VuePressParser),
        }
        
        if parser_name.lower() in parser_map:
            _, parser_class = parser_map[parser_name.lower()]
            return parser_class(html, url, **kwargs)
        
        raise ValueError(f"Unknown parser: {parser_name}")
    
    @classmethod
    def list_parsers(cls) -> List[str]:
        """List all registered parser names"""
        return list(cls._domain_mapping.keys())
    
    @classmethod
    def auto_detect(cls, url: str) -> str:
        """Auto-detect site type from URL"""
        url = url.lower()
        
        mappings = {
            'csdn.net': 'csdn',
            'jianshu.com': 'jianshu',
            'jianshu.io': 'jianshu',
            'segmentfault.com': 'segmentfault',
            'oschina.net': 'oschina',
            'my.oschina.net': 'oschina',
            'zhihu.com': 'zhihu',
            'zhuanlan.zhihu.com': 'zhihu',
            'cloud.tencent.com': 'tencent',
            'console.cloud.tencent.com': 'tencent',
            'tech.meituan.com': 'meituan',
            'meituan.com': 'meituan',
            'blog.cloudflare.com': 'cloudflare',
            'lofter.com': 'lofter',
            'lauxiang.net': 'lofter',
            'feishu.cn': 'feishu',
            'feishu.com': 'feishu',
            'mp.weixin.qq.com': 'wechat',
            'weixin.qq.com': 'wechat',
            'cnblogs.com': 'cnblogs',
            'wp-admin': 'wordpress',
            'wordpress.com': 'wordpress',
            'hexo.io': 'hexo',
            'gohugo.io': 'hugo',
            'vuepress.vuejs.org': 'vuepress',
        }
        
        for domain, parser_name in mappings.items():
            if domain in url:
                return parser_name
        
        return 'csdn'  # default


# Import all parsers for registration
from .csdn import CSDNParser
from .jianshu import JianShuParser
from .segmentfault import SegmentFaultParser
from .oschina import OSChinaParser
from .zhihu import ZhihuParser
from .tencent import TencentCloudParser
from .meituan import MeituanParser
from .cloudflare import CloudFlareParser
from .lofter import LofterParser
from .feishu import FeishuParser
from .wordpress import WordPressParser
from .hexo import HexoParser
from .hugo import HugoParser
from .vuepress import VuePressParser
from .wechat import WeChatParser
from .cnblogs import CnBlogsParser

# Auto-register all parsers
for parser in [CSDNParser, JianShuParser, SegmentFaultParser, OSChinaParser, 
               ZhihuParser, TencentCloudParser, MeituanParser, CloudFlareParser,
               LofterParser, FeishuParser, WordPressParser, HexoParser, 
               HugoParser, VuePressParser, WeChatParser, CnBlogsParser]:
    try:
        ParserFactory.register(parser)
    except:
        pass
