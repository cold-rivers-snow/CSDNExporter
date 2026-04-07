"""
CnBlogs (博客园) Parser
"""
import re
from .base import SiteParser, ArticleMetadata


class CnBlogsParser(SiteParser):
    """Parser for CnBlogs (博客园) blogs"""
    
    SITE_NAME = "博客园"
    SITE_DOMAINS = ['cnblogs.com', 'www.cnblogs.com']
    
    SELECTORS = {
        'title': ['span[role="heading"]', 'h1#post_title', '.postTitle', 'h1'],
        'content': ['div#cnblogs_post_body', 'div.postBody', 'div.content'],
        'publish_time': ['a.postTitle2', 'span.postfoot', 'div.postMeta'],
        'author': ['div#blog_title h2', '.author', '.blog-author'],
        'category': ['div#BlogPostCategory', '.category'],
        'tags': ['div#EntryTag', 'a.tag', '.tag-list'],
    }
    
    def get_metadata(self) -> ArticleMetadata:
        soup = self.soup
        
        # Title - find from span with role="heading" or h1
        title = ""
        title_tag = soup.find('span', {'role': 'heading'})
        if not title_tag:
            title_tag = soup.find('h1', {'id': 'post_title'})
        if not title_tag:
            title_tag = soup.find('span', {'class': 'postTitle2'})
        if not title_tag:
            title_tag = soup.find('h1')
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # Publish time - from postTitle2 anchor title attribute
        publish_time = ""
        time_tag = soup.find('a', {'class': 'postTitle2'})
        if time_tag:
            title_attr = time_tag.get('title', '')
            match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2})', title_attr)
            if match:
                publish_time = match.group(1)
        if not publish_time:
            time_tag = soup.find('span', {'class': 'postfoot'})
            if time_tag:
                text = time_tag.get_text(strip=True)
                match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2})', text)
                if match:
                    publish_time = match.group(1)
        
        # Author - from blog header h2
        author = ""
        blog_title = soup.find('div', {'id': 'blog_title'})
        if blog_title:
            h2 = blog_title.find('h2')
            if h2:
                author = h2.get_text(strip=True)
        if not author:
            author_tag = soup.find('div', {'class': 'postDesc'})
            if author_tag:
                text = author_tag.get_text(strip=True)
                if '作者' in text:
                    match = re.search(r'作者[：:]\s*(\S+)', text)
                    if match:
                        author = match.group(1)
        
        # Category
        category = ""
        cat_tag = soup.find('div', {'id': 'BlogPostCategory'})
        if cat_tag:
            links = cat_tag.find_all('a')
            if links:
                category = links[0].get_text(strip=True)
        
        # Tags
        tags = []
        tag_container = soup.find('div', {'id': 'EntryTag'})
        if tag_container:
            tag_links = tag_container.find_all('a')
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
        
        content_tags = self.soup.find_all('div', {'id': 'cnblogs_post_body'})
        if not content_tags:
            content_tags = self.soup.find_all('div', {'class': 'postBody'})
        
        for tag in content_tags:
            content += str(tag)
        
        return content
