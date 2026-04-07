"""
Zhihu Parser
"""
from .base import SiteParser, ArticleMetadata


class ZhihuParser(SiteParser):
    """Parser for Zhihu (知乎) articles"""
    
    SITE_NAME = "知乎"
    SITE_DOMAINS = ['zhihu.com', 'zhuanlan.zhihu.com']
    
    SELECTORS = {
        'title': ['h1.Post-Index-Title', '.Post-Index-Title', 'h1'],
        'content': ['div.ArticleItem', 'div.article-content', 'div.content'],
        'publish_time': ['span.Date', '.publish-time', 'time'],
        'author': ['a.Author', '.author', '.username'],
        'category': ['div.tags', 'a.tag'],
        'tags': ['div.tag-list', 'a.tag'],
    }
    
    def get_metadata(self) -> ArticleMetadata:
        soup = self.soup
        
        # Title
        title = ""
        title_tag = soup.find('h1', {'class': 'Post-Index-Title'})
        if not title_tag:
            title_tag = soup.find('h1')
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # Publish time
        publish_time = ""
        time_tag = soup.find('span', {'class': 'Date'})
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
        
        content_tags = self.soup.find_all('div', {'class': 'ArticleItem'})
        if not content_tags:
            content_tags = self.soup.find_all('div', {'class': 'article-content'})
        
        for tag in content_tags:
            content += str(tag)
        
        return content
