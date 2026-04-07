"""
WordPress Parser - Generic WordPress blogs
"""
from .base import SiteParser, ArticleMetadata


class WordPressParser(SiteParser):
    """Parser for WordPress blogs (generic)"""
    
    SITE_NAME = "WordPress"
    SITE_DOMAINS = ['wordpress.com', 'wp-admin', 'wp-content']
    
    SELECTORS = {
        'title': ['h1.entry-title', '.entry-title', 'h1.post-title'],
        'content': ['article', 'div.entry-content', 'div.post-content', 'div.content'],
        'publish_time': ['time.entry-date', 'time', 'span.date', '.publish-time'],
        'author': ['a.author-name', 'span.author', '.byline'],
        'category': ['span.cat-links', 'div.category', 'a.category'],
        'tags': ['span.tag-links', 'div.tags', 'a.tag'],
    }
    
    def get_metadata(self) -> ArticleMetadata:
        soup = self.soup
        
        # Title
        title = ""
        title_tag = soup.find('h1', {'class': 'entry-title'})
        if not title_tag:
            title_tag = soup.find('h1', {'class': 'post-title'})
        if not title_tag:
            title_tag = soup.find('h1')
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # Publish time
        publish_time = ""
        time_tag = soup.find('time', {'class': 'entry-date'})
        if not time_tag:
            time_tag = soup.find('time')
        if time_tag:
            publish_time = time_tag.get('datetime', time_tag.get_text(strip=True))
        
        # Author
        author = ""
        author_tag = soup.find('span', {'class': 'byline'})
        if not author_tag:
            author_tag = soup.find('a', {'class': 'author-name'})
        if author_tag:
            author = author_tag.get_text(strip=True)
        
        # Category
        category = ""
        cat_tag = soup.find('span', {'class': 'cat-links'})
        if cat_tag:
            links = cat_tag.find_all('a')
            if links:
                category = links[0].get_text(strip=True)
        
        # Tags
        tags = []
        tag_list = soup.find_all('span', {'class': 'tag-links'})
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
        
        # Try article tag first
        content_tags = self.soup.find_all('article')
        if not content_tags:
            # Try entry-content
            content_tags = self.soup.find_all('div', {'class': 'entry-content'})
        if not content_tags:
            content_tags = self.soup.find_all('div', {'class': 'post-content'})
        if not content_tags:
            content_tags = self.soup.find_all('div', {'class': 'content'})
        
        for tag in content_tags:
            content += str(tag)
        
        return content
