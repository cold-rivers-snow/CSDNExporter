"""
Meituan Tech Parser
"""
from .base import SiteParser, ArticleMetadata


class MeituanParser(SiteParser):
    """Parser for Meituan Tech (美团技术) blogs"""
    
    SITE_NAME = "美团技术"
    SITE_DOMAINS = ['tech.meituan.com', 'meituan.com']
    
    SELECTORS = {
        'title': ['h1.article-title', '.article-title', 'h1'],
        'content': ['article.article', 'div.article-content', 'div.content'],
        'publish_time': ['span.time', 'time', '.publish-time'],
        'author': ['span.author', '.author-name', '.username'],
        'category': ['div.category', 'a.category-link'],
        'tags': ['div.tags', 'a.tag'],
    }
    
    def get_metadata(self) -> ArticleMetadata:
        soup = self.soup
        
        # Title
        title = ""
        title_tag = soup.find('h1', {'class': 'article-title'})
        if not title_tag:
            title_tag = soup.find('h1')
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # Publish time
        publish_time = ""
        time_tag = soup.find('span', {'class': 'time'})
        if not time_tag:
            time_tag = soup.find('time')
        if time_tag:
            publish_time = time_tag.get_text(strip=True)
        
        # Author
        author = ""
        author_tag = soup.find('span', {'class': 'author'})
        if author_tag:
            author = author_tag.get_text(strip=True)
        
        # Tags
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
        
        content_tags = self.soup.find_all('article', {'class': 'article'})
        if not content_tags:
            content_tags = self.soup.find_all('div', {'class': 'article-content'})
        
        for tag in content_tags:
            content += str(tag)
        
        return content
