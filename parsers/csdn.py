"""
CSDN Parser
"""
import re
from typing import List
from .base import SiteParser, ArticleMetadata
from bs4 import NavigableString


class CSDNParser(SiteParser):
    """Parser for CSDN blogs"""
    
    SITE_NAME = "CSDN"
    SITE_DOMAINS = ['csdn.net']
    
    SELECTORS = {
        'title': ['h1.title-article'],
        'content': ['div#content_views'],
        'publish_time': ['span.time'],
        'author': ['a.author-name', 'a.name'],
        'category': ['span.tit'],
        'tags': ['div.tag_box'],
    }
    
    def get_metadata(self) -> ArticleMetadata:
        soup = self.soup
        
        # Title
        title = ""
        title_tag = soup.find('h1', {'class': 'title-article'})
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # Publish time
        publish_time = ""
        time_tag = soup.find('span', {'class': 'time'})
        if time_tag:
            time_text = time_tag.get_text(strip=True)
            match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', time_text)
            if match:
                publish_time = match.group()
        
        # Author
        author = ""
        author_tag = soup.find('a', {'class': 'author-name'})
        if not author_tag:
            author_tag = soup.find('a', {'class': 'name'})
        if author_tag:
            author = author_tag.get_text(strip=True)
        
        # Category/Tags
        category = ""
        category_tag = soup.find('span', {'class': 'tit'})
        if category_tag:
            category = category_tag.get_text(strip=True)
        
        tags = []
        tag_box = soup.find('div', {'class': 'tag-box'})
        if tag_box:
            tag_links = tag_box.find_all('a')
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
        # Remove svg elements
        for svg in self.soup.find_all('svg'):
            svg.extract()
        
        content = ""
        
        # Get title section if needed
        title_box = self.soup.find_all('div', {'class': 'article-title-box'})
        for box in title_box:
            content += str(box)
        
        # Main content
        content_views = self.soup.find_all('div', {'id': 'content_views'})
        for cv in content_views:
            content += str(cv)
        
        return content
    
    def _handle_code_block(self, tag):
        """Handle CSDN specific code blocks"""
        language = 'bash'
        if 'class' in tag.attrs:
            classes = ' '.join(tag.attrs['class'])
            for lang in ['cpp', 'bash', 'python', 'java', 'javascript', 'go', 'rust', 'c', 'shell']:
                if lang in classes:
                    language = lang
                    break
        
        tag.contents.insert(0, NavigableString(f'\n```{language}\n'))
        tag.contents.append(NavigableString('\n```\n'))
