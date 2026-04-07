"""
OSChina (开源中国) Parser
"""
from .base import SiteParser, ArticleMetadata


class OSChinaParser(SiteParser):
    """Parser for OSChina (开源中国) blogs"""
    
    SITE_NAME = "开源中国"
    SITE_DOMAINS = ['oschina.net', 'my.oschina.net']
    
    SELECTORS = {
        'title': ['h1.title', '.blog-title', 'h1'],
        'content': ['div.blog-content', 'div.content', 'article'],
        'publish_time': ['span.date', 'time', '.publish-time'],
        'author': ['a.author', '.username', '.blog-author'],
        'category': ['div.tags', 'a.tag'],
        'tags': ['div.tag-box', 'a.tag'],
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
        time_tag = soup.find('span', {'class': 'date'})
        if not time_tag:
            time_tag = soup.find('time')
        if time_tag:
            publish_time = time_tag.get_text(strip=True)
        
        # Author
        author = ""
        author_tag = soup.find('a', {'class': 'author'})
        if author_tag:
            author = author_tag.get_text(strip=True)
        
        # Tags
        tags = []
        tag_list = soup.find_all('a', {'class': lambda x: x and 'tag' in x.lower() if x else False})
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
        
        content_tags = self.soup.find_all('div', {'class': 'blog-content'})
        if not content_tags:
            content_tags = soup.find_all('div', {'class': 'content'})
        if not content_tags:
            content_tags = soup.find_all('article')
        
        for tag in content_tags:
            content += str(tag)
        
        return content
