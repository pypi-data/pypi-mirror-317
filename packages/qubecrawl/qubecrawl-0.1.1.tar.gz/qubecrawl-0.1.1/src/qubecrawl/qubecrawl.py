import re
import json
import requests
import html2text
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class qubecrawl:
    def __init__(self, ignore_links=False, ignore_img=False, clean=True):
        """
        Initializes the qubecrawl class.

        Args:
            ignore_links (bool): Whether to ignore links in markdown. Defaults to False.
            ignore_img (bool): Whether to ignore images in markdown. Defaults to False.
            clean (bool): Whether to clean the HTML content. Defaults to True.
        """
        self.ignore_links = ignore_links
        self.ignore_img = ignore_img
        self.clean = clean
        self.patterns = {
            'nav', 'menu', 'navbar', 'sidebar', 'drawer', 'breadcrumb', 
            'side-nav', 'sidenav', 'header', 'footer', 'bottom-bar', 
            'top-bar', 'ad-', 'ads-', 'advertisement', 'banner', 'promo', 
            'sponsored', 'ads', 'popup', 'modal', 'overlay', 'dialog', 
            'toast', 'alert', 'notification', 'tracking', 'analytics', 
            'pixel', 'beacon', 'tag-manager', 'disclaimer', 'newsletter', 
            'subscribe', 'signup', 'mailing-list', 'search', 'login', 
            'register', 'sign-in', 'cookie', 'gdpr', 'consent', 'privacy', 
            'terms', 'copyright', 'hidden', 'display-none', 'invisible', 
            'spacer', 'gap', 'background', 'decoration', 'ornament', 
            'pattern', 'gradient', 'carousel', 'slider', 'lightbox', 
            'tooltip', 'dropdown', 'skeleton', 'placeholder', 'loading', 
            'shimmer', 'spinner'
        }
        
        self.check_patterns = True

    def _is_empty(self, markdown):
        return not markdown.strip()

    def _clean_html(self, html_body):
        if not self.clean:
            return html_body
        elements_to_remove = html_body.select('nav, header, footer, form, button, input, script, label, style, select, textarea, option, meta, canvas, [aria-hidden="true"]')
        for element in elements_to_remove:
            element.decompose()
        if self.check_patterns and self.patterns:
            pattern_str = '|'.join(self.patterns)
            for element in html_body.find_all(class_=re.compile(pattern_str)):
                element.decompose()
            for element in html_body.find_all(id=re.compile(pattern_str)):
                element.decompose()
        for figure in html_body.find_all('figure'):
            img = figure.find('img')
            if img:
                figcaption = figure.find('figcaption')
                if figcaption:
                    img['alt'] = figcaption.get_text(strip=True)
                figure.replace_with(img)                
        return html_body

    def _convert_to_markdown(self, html_content, url=None):
        if url:
            html = BeautifulSoup(html_content, 'lxml')
            for img in html.find_all('img'):
                if 'src' in img.attrs:
                    img['src'] = urljoin(url, img['src'])
                if 'data-src' in img.attrs:
                    img['data-src'] = urljoin(url, img['data-src'])
            for link in html.find_all('a', href=True):
                link['href'] = urljoin(url, link['href'])
            html_content = str(html)
        convert = html2text.HTML2Text()
        convert.ignore_links = self.ignore_links
        convert.ignore_images = self.ignore_img
        convert.ignore_emphasis = True
        convert.protect_links = True
        convert.skip_internal_links = True
        convert.use_automatic_links = True
        convert.body_width = 0
        markdown = convert.handle(html_content)
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        markdown = re.sub(r'^\s+|\s+$', '', markdown)
        if self._is_empty(markdown):
            raise ValueError("No content found")
        return markdown
    
        
    def add_pattern(self, pattern):
        """Add a new pattern to the unnecessary_patterns."""
        self.patterns.add(pattern)
        self.check_patterns = True 

    def remove_pattern(self, pattern):
        """Remove a pattern from the unnecessary_patterns."""
        self.patterns.discard(pattern)
    
    def get_patterns(self):
        """Get the current list of patterns."""
        return list(self.patterns)
    
    def clear_patterns(self):
        """Clear the list of patterns."""
        self.patterns.clear()
        self.check_patterns = False

    def parse_class(self, content, class_name, url):
        """
        Extracts and converts elements by class name to markdown.

        Args:
            content (str): The HTML content.
            class_name (str): The class name to search for.
            url (str): The base URL.

        Returns:
            str: Converted markdown or an empty string.
        """
        html = BeautifulSoup(content, 'lxml')
        html_body = self._clean_html(html)
        elements = html_body.find_all(class_=class_name)
        if not elements:
            raise ValueError("No Element found")
        combined_html = BeautifulSoup("", 'lxml')
        for i, element in enumerate(elements):
            if i > 0:
                combined_html.append(combined_html.new_tag('hr'))
            combined_html.append(element)
            
        return self._convert_to_markdown(str(combined_html), url)

    def parse_id(self, content, element_id, url):
        """
        Extracts and converts an element by ID to markdown.

        Args:
            content (str): The HTML content.
            element_id (str): The ID to search for.
            url (str): The base URL.

        Returns:
            str: Converted markdown or an empty string.
        """
        html = BeautifulSoup(content, 'lxml')
        html_body = self._clean_html(html)
        element = html_body.find(id=element_id)
        if not element:
            raise ValueError("No Element found")
        return self._convert_to_markdown(str(element), url) 


    def parse_(self, content, url):
        """
        Converts the main content of a page to markdown.

        Args:
            content (str): The HTML content.
            url (str): The base URL.

        Returns:
            str: Converted markdown.
        """
        html = BeautifulSoup(content, 'lxml')
        html_body = html.find('main') or html.find('article') or html.find('body') or html
        html_body = self._clean_html(html_body)
        return self._convert_to_markdown(str(html_body), url)

    async def get_head(self, url):
            """
            Gets the head data of a webpage.

            Args:
                url (str): The webpage URL.

            Raises:
                ValueError: If the URL is invalid.

            Returns:
                dict: Headers and head data.
            """
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError("Invalid URL") 
            response = requests.get(url)
            response.raise_for_status()
            html = BeautifulSoup(response.text, 'lxml')
            head = html.find('head')        
            if not head:
                raise ValueError("No <head> tag found in the HTML")
            head_data = {
                tag_name: [str(tag) for tag in head.find_all(tag_name)]
                for tag_name in ['title', 'meta', 'link', 'script', 'style']
            }
            result = {
                'headers': dict(response.headers),
                'head_data': head_data
            }
            return json.dumps(result, indent=4)