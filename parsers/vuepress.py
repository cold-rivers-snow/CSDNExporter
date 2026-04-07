"""
VuePress Parser - Generic VuePress static sites
"""
from .base import SiteParser, ArticleMetadata


class VuePressParser(SiteParser):
    """Parser for VuePress static site blogs"""
    
    SITE_NAME = "VuePress"
    SITE_DOMAINS = ['vuejs.org', 'vuepress.vuejs.org', '.vuepress.org']
    
    SELECTORS = {
        'title': ['h1.page-title', '.page-title', 'h1'],
        'content': ['div.theme-default-content', 'div.content__body', 'article'],
        'publish_time': ['time', 'span.date', '.page-meta'],
        'author': ['span.author', '.page-author', '.byline'],
        'category': ['span.category', '.page-category'],
        'tags': ['span.tags', '.page-tags'],
    }
    
    def get_metadata(self) -> ArticleMetadata:
        soup = self.soup
        
        # Title
        title = ""
        title_tag = soup.find('h1', {'class': 'page-title'})
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
        author_tag = soup.find('span', {'class': 'author'})
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
        
        content_tags = self.soup.find_all('div', {'class': 'theme-default-content'})
        if not content_tags:
            content_tags = self.soup.find_all('div', {'class': 'content__body'})
        if not content_tags:
            content_tags = self.soup.find_all('article')
        
        for tag in content_tags:
            content += str(tag)
        
        return content
