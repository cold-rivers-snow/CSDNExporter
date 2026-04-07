"""
Hugo Parser - Generic Hugo static sites
"""
from .base import SiteParser, ArticleMetadata


class HugoParser(SiteParser):
    """Parser for Hugo static site blogs"""
    
    SITE_NAME = "Hugo"
    SITE_DOMAINS = ['gohugo.io', 'hugo.net']
    
    SELECTORS = {
        'title': ['h1.entry-title', '.entry-title', 'h1'],
        'content': ['article', 'div.content', 'section.main-content'],
        'publish_time': ['time', 'span.date', '.publish-time'],
        'author': ['span.author', '.byline', '.author-name'],
        'category': ['span.category', 'a.category', '.taxonomies'],
        'tags': ['span.tags', 'a.tag', '.tags'],
    }
    
    def get_metadata(self) -> ArticleMetadata:
        soup = self.soup
        
        # Title
        title = ""
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
        author_tag = soup.find('span', {'class': 'author'})
        if not author_tag:
            author_tag = soup.find('span', {'itemprop': 'author'})
        if author_tag:
            author = author_tag.get_text(strip=True)
        
        # Category
        category = ""
        cat_tag = soup.find('span', {'class': 'category'})
        if cat_tag:
            category = cat_tag.get_text(strip=True)
        
        # Tags
        tags = []
        tag_list = soup.find_all('span', {'class': 'tags'})
        if tag_list:
            tag_links = tag_list[0].find_all('a')
            tags = [a.get_text(strip=True) for a in tag_links]
        
        return ArticleMetadata(
            title=title,
            publish_time=publish_time,
            author=author,
            tags=tags,
            category=category,
            url=self.url
        )
    
    def get_content(self) -> str:
        content = ""
        
        content_tags = self.soup.find_all('article')
        if not content_tags:
            content_tags = self.soup.find_all('div', {'class': 'content'})
        if not content_tags:
            content_tags = self.soup.find_all('section', {'class': 'main-content'})
        
        for tag in content_tags:
            content += str(tag)
        
        return content
