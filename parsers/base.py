"""
Abstract base class for site parsers
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from bs4 import BeautifulSoup, Tag, NavigableString, Comment
import re
import os


@dataclass
class ArticleMetadata:
    """Article metadata structure"""
    title: str
    publish_time: str
    author: str = ""
    tags: List[str] = None
    category: str = ""
    url: str = ""
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class SiteParser(ABC):
    """Abstract base class for site-specific parsers"""
    
    # Site identification patterns
    SITE_NAME = ""
    SITE_DOMAINS = []
    
    # Common CSS selectors for different blog platforms
    SELECTORS = {
        'title': ['h1', 'title-article', 'article-title', 'post-title', '.title'],
        'content': ['div#content_views', 'div.article-content', 'div.post-content', 
                   'div.content', 'article', 'main', '.content', '#content'],
        'publish_time': ['span.time', 'time', 'span.date', '.publish-time', 
                        '[itemprop="datePublished"]', '.post-time'],
        'author': ['a.author-name', 'span.author', '.author', '[itemprop="author"]',
                  '.username', '.nickname'],
        'category': ['span.tit', 'div.category', '.tags', '.tag-list',
                    '[itemprop="articleSection"]'],
        'tags': ['div.tags', 'ul.tag-list', '.article-tags'],
    }
    
    def __init__(self, html: str, url: str = "", img_queue_downloader=None, is_win: bool = True):
        self.html = html
        self.url = url
        self.soup = BeautifulSoup(html, 'html.parser')
        self.img_queue_downloader = img_queue_downloader
        self.is_win = is_win
        self.outputs: List[str] = []
        self._init_fig_dir()
    
    def _init_fig_dir(self):
        """Initialize figure directory based on article title"""
        metadata = self.get_metadata()
        safe_title = self._sanitize_filename(metadata.title)
        self.fig_dir = f'./figures/{safe_title}'
    
    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """Sanitize filename by removing invalid characters"""
        filename = filename.replace('.', '').replace(':', ' ')
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = '_'.join(filename.split())
        return filename
    
    @abstractmethod
    def get_metadata(self) -> ArticleMetadata:
        """Extract article metadata (title, time, author, tags, etc.)"""
        pass
    
    @abstractmethod
    def get_content(self) -> str:
        """Extract main article content HTML"""
        pass
    
    def parse(self) -> str:
        """Main parsing method - converts HTML to Markdown"""
        content_html = self.get_content()
        metadata = self.get_metadata()
        return self._convert_to_markdown(content_html, metadata)
    
    def _convert_to_markdown(self, content_html: str, metadata: ArticleMetadata) -> str:
        """Convert HTML content to Markdown format"""
        from bs4 import NavigableString, Tag
        soup = BeautifulSoup(content_html, 'html.parser')
        self.outputs = []
        self._process_elements(soup)
        
        md_content = ''.join(self.outputs)
        
        md_output = f"---\n"
        md_output += f"title: {metadata.title}\n"
        md_output += f"date: {metadata.publish_time}\n"
        if metadata.author:
            md_output += f"author: {metadata.author}\n"
        if metadata.category:
            md_output += f"category: {metadata.category}\n"
        if metadata.tags:
            md_output += f"tags: {', '.join(metadata.tags)}\n"
        md_output += f"---\n\n"
        md_output += '<meta name="referrer" content="no-referrer" />\n\n'
        md_output += md_content
        
        return md_output
    
    def _process_elements(self, soup: BeautifulSoup):
        """Process HTML elements and convert to Markdown"""
        from bs4 import NavigableString, Tag, Comment
        
        if isinstance(soup, Comment):
            return
        elif isinstance(soup, NavigableString):
            self.outputs.append(str(soup))
        elif isinstance(soup, Tag):
            self._handle_tag(soup)
        
        if not hasattr(soup, 'children'):
            return
        for child in soup.children:
            self._process_elements(child)
    
    def _handle_tag(self, tag: Tag):
        """Handle specific HTML tags"""
        tag_name = tag.name
        
        # Headers
        if tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(tag_name[1])
            tag.contents.insert(0, NavigableString('#' * level + ' '))
            tag.contents.append(NavigableString('\n'))
        
        # Links
        elif tag_name == 'a' and 'href' in tag.attrs:
            tag.contents.insert(0, NavigableString('['))
            tag.contents.append(NavigableString(f"]({tag.attrs['href']})"))
        
        # Bold
        elif tag_name in ['b', 'strong']:
            tag.contents.insert(0, NavigableString('**'))
            tag.contents.append(NavigableString('**'))
        
        # Italic
        elif tag_name in ['em', 'i']:
            tag.contents.insert(0, NavigableString('*'))
            tag.contents.append(NavigableString('*'))
        
        # Code blocks
        elif tag_name == 'pre':
            self._handle_code_block(tag)
        
        # Inline code
        elif tag_name in ['code', 'tt']:
            if tag.parent and tag.parent.name != 'pre':
                tag.contents.insert(0, NavigableString('`'))
                tag.contents.append(NavigableString('`'))
        
        # Paragraphs
        elif tag_name == 'p':
            if not tag.parent or tag.parent.name != 'li':
                tag.contents.insert(0, NavigableString('\n'))
        
        # Lists
        elif tag_name in ['ol', 'ul']:
            tag.contents.insert(0, NavigableString('\n'))
            tag.contents.append(NavigableString('\n'))
        elif tag_name == 'li':
            tag.contents.insert(0, NavigableString('+ '))
            tag.contents.append(NavigableString('\n'))
        
        # Images
        elif tag_name == 'img':
            self._handle_image(tag)
        
        # Blockquote
        elif tag_name == 'blockquote':
            tag.contents.insert(0, NavigableString('\n> '))
            tag.contents.append(NavigableString('\n'))
        
        # Math (Katex)
        elif tag_name == 'span':
            if 'class' in tag.attrs:
                if 'katex--inline' in tag.attrs['class']:
                    self._handle_math(tag, inline=True)
                elif 'katex--display' in tag.attrs['class']:
                    self._handle_math(tag, inline=False)
    
    def _handle_code_block(self, tag: Tag):
        """Handle code blocks with syntax highlighting"""
        language = 'bash'
        if 'class' in tag.attrs:
            for lang in ['python', 'java', 'cpp', 'c', 'javascript', 'js', 'go', 'rust', 'bash', 'shell']:
                if lang in ' '.join(tag.attrs['class']):
                    language = lang
                    break
        
        tag.contents.insert(0, NavigableString(f'\n```{language}\n'))
        tag.contents.append(NavigableString('\n```\n'))
    
    def _handle_image(self, tag: Tag):
        """Handle image tags - download and embed"""
        src = tag.attrs.get('src', '')
        if not src:
            return
        
        if not os.path.exists(self.fig_dir):
            os.makedirs(self.fig_dir, exist_ok=True)
        
        # Extract filename
        filename = src.split('/')[-1].split('?')[0]
        if not filename:
            filename = 'image'
        save_path = os.path.join(self.fig_dir, filename).replace("\\", "/")
        
        # Add to download queue
        if self.img_queue_downloader:
            self.img_queue_downloader.add_task(src, save_path, self.is_win)
        
        # Reference local image
        img_name = os.path.basename(save_path)
        self.outputs.append(f'\n![{img_name}](.{save_path})\n')
    
    def _handle_math(self, tag: Tag, inline: bool = True):
        """Handle math equations (Katex)"""
        try:
            mathml = tag.find('span', {'class': 'katex-mathml'})
            if mathml and mathml.find('annotation'):
                equation = mathml.find('annotation').string.strip()
                if inline:
                    self.outputs.append(f'${equation}$')
                else:
                    self.outputs.append(f'\n\n$$\n{equation}\n$$\n\n')
        except:
            pass
    
    @classmethod
    def detect_site(cls, url: str) -> bool:
        """Check if this parser matches the given URL"""
        return any(domain in url.lower() for domain in cls.SITE_DOMAINS)
