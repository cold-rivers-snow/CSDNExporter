"""
WeChat (公众号) Parser
Note: WeChat articles require special handling as they use JS rendering
This parser expects the HTML already rendered (e.g., via Playwright/Selenium)
"""
import re
from .base import SiteParser, ArticleMetadata


class WeChatParser(SiteParser):
    """Parser for WeChat (微信公众平台) articles"""
    
    SITE_NAME = "微信公众平台"
    SITE_DOMAINS = ['mp.weixin.qq.com', 'weixin.qq.com']
    
    SELECTORS = {
        'title': ['h1#activity-name', '.title', 'h1'],
        'content': ['div#js_content', 'div.article-content', 'div.content'],
        'publish_time': ['span#publish_time', 'span.time', '.date'],
        'author': ['span#author_name', '.author', '.name'],
        'category': ['div#meta_content', '.category'],
        'tags': ['div#js_tags', '.tags'],
    }
    
    def get_metadata(self) -> ArticleMetadata:
        soup = self.soup
        
        # Title
        title = ""
        title_tag = soup.find('h1', {'id': 'activity-name'})
        if not title_tag:
            title_tag = soup.find('h1')
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # Publish time
        publish_time = ""
        time_tag = soup.find('span', {'id': 'publish_time'})
        if not time_tag:
            time_tag = soup.find('span', {'class': 'time'})
        if time_tag:
            publish_time = time_tag.get_text(strip=True)
        
        # Author
        author = ""
        author_tag = soup.find('span', {'id': 'author_name'})
        if author_tag:
            author = author_tag.get_text(strip=True)
        
        # Tags
        tags = []
        tag_container = soup.find('div', {'id': 'js_tags'})
        if tag_container:
            tag_links = tag_container.find_all('a')
            tags = [a.get_text(strip=True) for a in tag_links]
        
        return ArticleMetadata(
            title=title,
            publish_time=publish_time,
            author=author,
            tags=tags,
            url=self.url
        )
    
    def get_content(self) -> str:
        content = ""
        
        content_tags = self.soup.find_all('div', {'id': 'js_content'})
        if not content_tags:
            content_tags = self.soup.find_all('div', {'class': 'article-content'})
        
        for tag in content_tags:
            content += str(tag)
        
        return content
    
    @staticmethod
    def detect_site(url: str) -> bool:
        """Check if URL is from WeChat"""
        return 'mp.weixin.qq.com' in url.lower() or 'weixin.qq.com' in url.lower()
