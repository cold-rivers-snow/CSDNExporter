"""
SegmentFault Parser
"""
from .base import SiteParser, ArticleMetadata


class SegmentFaultParser(SiteParser):
    """Parser for SegmentFault (思否) blogs"""
    
    SITE_NAME = "SegmentFault"
    SITE_DOMAINS = ['segmentfault.com']
    
    SELECTORS = {
        'title': ['h1.title', '.article-title', '.post-title'],
        'content': ['div.article__content', 'div.post-content', 'div.content'],
        'publish_time': ['time', 'span.date', '.publish-time'],
        'author': ['a.author', '.username', '.nickname'],
        'category': ['div.tags', 'a.tag'],
        'tags': ['div.tag-list', 'a.tag'],
    }
    
    def get_metadata(self) -> ArticleMetadata:
        soup = self.soup
        
        # Title
        title = ""
        title_tag = soup.find('h1', {'class': 'title'})
        if not title_tag:
            title_tag = soup.find('h1')
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # Publish time
        publish_time = ""
        time_tag = soup.find('time')
        if time_tag:
            publish_time = time_tag.get('datetime', time_tag.get_text(strip=True))
        
        # Author
        author = ""
        author_tag = soup.find('a', {'class': 'author'})
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
        
        content_tags = self.soup.find_all('div', {'class': 'article__content'})
        if not content_tags:
            content_tags = self.soup.find_all('div', {'class': 'post-content'})
        
        for tag in content_tags:
            content += str(tag)
        
        return content
