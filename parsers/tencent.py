"""
Tencent Cloud Parser
"""
from .base import SiteParser, ArticleMetadata


class TencentCloudParser(SiteParser):
    """Parser for Tencent Cloud (腾讯云) blogs"""
    
    SITE_NAME = "腾讯云"
    SITE_DOMAINS = ['cloud.tencent.com', 'console.cloud.tencent.com']
    
    SELECTORS = {
        'title': ['h1.article-info__title', '.article-title', 'h1'],
        'content': ['div.article-info', 'div.article-content', 'div.content'],
        'publish_time': ['span.article-info__date', '.publish-time', 'time'],
        'author': ['span.article-info__author', '.author', '.username'],
        'category': ['div.article-label', '.category', '.tag'],
        'tags': ['div.label-list', 'a.tag'],
    }
    
    def get_metadata(self) -> ArticleMetadata:
        soup = self.soup
        
        # Title
        title = ""
        title_tag = soup.find('h1', {'class': 'article-info__title'})
        if not title_tag:
            title_tag = soup.find('h1')
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # Publish time
        publish_time = ""
        time_tag = soup.find('span', {'class': 'article-info__date'})
        if not time_tag:
            time_tag = soup.find('time')
        if time_tag:
            publish_time = time_tag.get_text(strip=True)
        
        # Author
        author = ""
        author_tag = soup.find('span', {'class': 'article-info__author'})
        if author_tag:
            author = author_tag.get_text(strip=True)
        
        # Category/Tags
        tags = []
        tag_list = soup.find_all('a', {'class': lambda x: x and 'tag' in x if x else False})
        tags = [a.get_text(strip=True) for a in tag_list if a.get_text(strip=True)]
        
        return ArticleMetadata(
            title=title,
            publish_time=publish_time,
            author=author,
            tags=tags,
            url=self.url
        )
    
    def get_content(self) -> str:
        content = ""
        
        content_tags = self.soup.find_all('div', {'class': 'article-info'})
        if not content_tags:
            content_tags = self.soup.find_all('div', {'class': 'article-content'})
        
        for tag in content_tags:
            content += str(tag)
        
        return content
