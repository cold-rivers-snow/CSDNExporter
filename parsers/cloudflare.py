"""
CloudFlare Blog Parser
"""
from .base import SiteParser, ArticleMetadata


class CloudFlareParser(SiteParser):
    """Parser for CloudFlare Blog"""
    
    SITE_NAME = "CloudFlare"
    SITE_DOMAINS = ['blog.cloudflare.com']
    
    SELECTORS = {
        'title': ['h1.Blog-title', '.blog-title', 'h1'],
        'content': ['article.Blog', 'article', 'div.article-content', 'div.content'],
        'publish_time': ['time.Blog-date', '.blog-date', 'time'],
        'author': ['a.Blog-author', '.blog-author', '.author'],
        'category': ['div.Blog-tags', '.blog-tags', 'a.tag'],
        'tags': ['div.tag-list', 'a.tag'],
    }
    
    def get_metadata(self) -> ArticleMetadata:
        soup = self.soup
        
        # Title
        title = ""
        title_tag = soup.find('h1', {'class': 'Blog-title'})
        if not title_tag:
            title_tag = soup.find('h1')
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # Publish time
        publish_time = ""
        time_tag = soup.find('time', {'class': 'Blog-date'})
        if not time_tag:
            time_tag = soup.find('time')
        if time_tag:
            publish_time = time_tag.get('datetime', time_tag.get_text(strip=True))
        
        # Author
        author = ""
        author_tag = soup.find('a', {'class': 'Blog-author'})
        if not author_tag:
            author_tag = soup.find('span', {'class': 'blog-author'})
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
        
        content_tags = self.soup.find_all('article', {'class': 'Blog'})
        if not content_tags:
            content_tags = self.soup.find_all('article')
        if not content_tags:
            content_tags = self.soup.find_all('div', {'class': 'article-content'})
        
        for tag in content_tags:
            content += str(tag)
        
        return content
