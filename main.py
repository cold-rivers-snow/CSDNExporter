#############################
# CopyRight ~~~~~~ ##########
# Author: allenmirac ########
# Date: 2023-06-18 ##########
#############################
import os
import sys
import shutil
from os.path import join, exists
import urllib.request
import requests
import httpx
import argparse
import glob
from bs4 import BeautifulSoup, NavigableString
import time as tm
import re
from download_img_queue import Download_img_queue
from queue import Queue
from parsers.factory import ParserFactory
from parsers.csdn import CSDNParser

parser = argparse.ArgumentParser('Blog Exporter: To Markdown or To PDF')
group = parser.add_mutually_exclusive_group()
group.add_argument('--category_url', type=str,
                    help='Blog Category Url, e.g., https://blog.csdn.net/xxx/category_xxx.html')
group.add_argument('--article_url', type=str,
                    help='Blog Article Url, e.g., https://blog.csdn.net/xxx/article/details/xxx')
parser.add_argument('--site', type=str, default='auto',
                    choices=['auto', 'csdn', 'jianshu', 'segmentfault', 'oschina', 'zhihu', 
                            'tencent', 'meituan', 'cloudflare', 'lofter', 'feishu', 'wechat',
                            'cnblogs', 'wordpress', 'hexo', 'hugo', 'vuepress'],
                    help='Site parser to use (auto-detect by default)')
parser.add_argument('--start_page', type=int, default=1,
                   help='Start Page of Blog Category')
parser.add_argument('--page_num', type=int, default=100,
                    help='Page Number of Blog Category')
parser.add_argument('--markdown_dir', type=str, default='markdown',
                   help='Markdown Directory')
parser.add_argument('--pdf_dir', type=str, default='pdf',
                   help='PDF Directory')
parser.add_argument('--with_title', action='store_true')
parser.add_argument('--to_pdf', action='store_true')
parser.add_argument('--rm_cache', action='store_true',
                   help='remove cached file')
parser.add_argument('--is_win', 
                    choices=[1, 0], default=0, type=int,
                   help='platform: windows-1, Linux-0')
parser.add_argument('--combine_together', action='store_true',
                   help='Combine all markdown files into a single file')
args = parser.parse_args()

download_img_queue = Queue()
num_workers = 5
img_queue_downloader = Download_img_queue(download_img_queue, True, num_workers)


def get_parser_class(site_name, url):
    """Get parser class based on site name or auto-detect from URL"""
    if site_name == 'auto':
        parser_name = ParserFactory.auto_detect(url)
    else:
        parser_name = site_name
    
    parser_map = {
        'csdn': CSDNParser,
    }
    
    if parser_name in parser_map:
        return parser_map[parser_name]
    
    from parsers import jianshu, segmentfault, oschina, zhihu, tencent, meituan
    from parsers import cloudflare, lofter, feishu, wechat, cnblogs, wordpress, hexo, hugo, vuepress
    
    parser_map.update({
        'jianshu': jianshu.JianShuParser,
        'segmentfault': segmentfault.SegmentFaultParser,
        'oschina': oschina.OSChinaParser,
        'zhihu': zhihu.ZhihuParser,
        'tencent': tencent.TencentCloudParser,
        'meituan': meituan.MeituanParser,
        'cloudflare': cloudflare.CloudFlareParser,
        'lofter': lofter.LofterParser,
        'feishu': feishu.FeishuParser,
        'wechat': wechat.WeChatParser,
        'cnblogs': cnblogs.CnBlogsParser,
        'wordpress': wordpress.WordPressParser,
        'hexo': hexo.HexoParser,
        'hugo': hugo.HugoParser,
        'vuepress': vuepress.VuePressParser,
    })
    
    return parser_map.get(parser_name, CSDNParser)


def html2md(url, md_file, with_title=False, is_win=True, parser_class=None):
    response = httpx.get(url)
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding="utf-8")
    
    if parser_class is None:
        parser_class = get_parser_class(args.site, url)
    
    parser_instance = parser_class(str(soup), url, img_queue_downloader, is_win)
    metadata = parser_instance.get_metadata()
    content_html = parser_instance.get_content()
    
    safe_title = parser_instance._sanitize_filename(metadata.title)
    md_filename = safe_title + '.md'
    md_path = join(md_dir, md_filename)
    
    md_content = parser_instance._convert_to_markdown(content_html, metadata)
    
    with open(md_file, 'w', encoding="utf-8") as f:
        f.write(md_content)
    
    return safe_title


def generate_pdf(input_md_file, pdf_dir, is_win=True):
    if not exists(pdf_dir):
        os.makedirs(pdf_dir)

    md_name = os.path.basename(input_md_file)
    pdf_name = md_name.replace('.md', '.pdf')
    pdf_file = join(pdf_dir, pdf_name)
    if is_win:
        cmd = ['pandoc',
            '--toc',
            '--pdf-engine=xelatex',
            '-V mainfont="Source Code Pro"',
            '-V monofont="Source Code Pro"',
            '-V documentclass="ctexbook"',
            '-V geometry:"top=2cm, bottom=1cm, left=1.5cm, right=1.5cm"',
            '-V pagestyle=plain',
            '-V fontsize=11pt',
            '-V colorlinks=blue',
            '-s {}'.format(input_md_file),
            '-o {}'.format(pdf_file),
        ]
    else:
        cmd = ["pandoc",
            "--toc",
            "--pdf-engine=xelatex",
            "-V mainfont='Source Code Pro'",
            "-V monofont='Source Code Pro'",
            "-V documentclass='ctexart'",
            "-V geometry:'top=2cm, bottom=1cm, left=1.5cm, right=1.5cm'",
            "-V pagestyle=plain",
            "-V fontsize=11pt",
            "-V colorlinks=blue",
            "-s {}".format(input_md_file),
            "-o {}".format(pdf_file),
        ]
    cmd = ' '.join(cmd)
    print('Generate PDF File: {}'.format(pdf_file))
    os.system(cmd)


def get_category_article_info(soup):
    url = soup.find_all('a')[0].attrs['href']
    h2_tag = soup.find_all('h2', {'class': 'title'})[0]
    for child in h2_tag.children:
        if isinstance(child, NavigableString):
            title = '_'.join(child.replace('*', '').strip().split())
            break
    return url, title


def download_category_url(category_url, md_dir, start_page=1, page_num=100, pdf_dir='pdf', to_pdf=False, is_win=True):
    parser_class = get_parser_class(args.site, category_url)
    
    if not exists(md_dir):
        os.makedirs(md_dir)

    article_url = []
    article_title = []
    for page in range(start_page, page_num + 1):
        suffix = '.html' if page == 1 else '_{}.html'.format(page)
        category_url_new = category_url.rstrip('.html') + suffix
        print('Getting Response From {}'.format(category_url_new))
        try:
            response = httpx.get(category_url_new, timeout=10)
        except:
            break
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding="utf-8")
        article_list = soup.find_all('ul', {'class': 'column_article_list'})
        if not article_list:
            print('No article list found in {}, I Will Skip It!'.format(category_url_new))
            break
        article_list = article_list[0]
        p = article_list.find_all('p')
        if p and p[0].string == '空空如也':
            print('No Content in {}, I Will Skip It!'.format(category_url_new))
            break
        for child in article_list.children:
            if child.name == 'li':
                url, title = get_category_article_info(child)
                title = re.compile(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])").sub('', title)
                article_url.append(url)
                article_title.append(title)

    for idx, (url, title) in enumerate(zip(article_url, article_title), 1):
        md_file = join(md_dir, title + '.md')
        print('BlogNum: {}, Exporting Markdown File To {}'.format(idx, md_file))
        if not exists(md_file):
            html2md(url, md_file, is_win=is_win, parser_class=parser_class)
            if to_pdf:
                generate_pdf(md_file, pdf_dir, is_win)


def download_single_page(details_url, md_dir, with_title=True, pdf_dir='pdf', to_pdf=False, is_win=True):
    parser_class = get_parser_class(args.site, details_url)
    
    print(md_dir)
    if not exists(md_dir):
        os.makedirs(md_dir)
    response = httpx.get(details_url)
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding="utf-8")
    
    parser_instance = parser_class(str(soup), details_url, img_queue_downloader, is_win)
    metadata = parser_instance.get_metadata()
    
    safe_title = parser_instance._sanitize_filename(metadata.title)
    md_file = join(md_dir, safe_title + '.md')
    print('Export Markdown File To {}'.format(md_file))
    
    content_html = parser_instance.get_content()
    md_content = parser_instance._convert_to_markdown(content_html, metadata)
    
    with open(md_file, 'w', encoding="utf-8") as f:
        f.write(md_content)
    
    if to_pdf:
        generate_pdf(md_file, pdf_dir, is_win)


if __name__ == '__main__':
    time_start = tm.time()
    if not args.category_url and not args.article_url:
        raise Exception('Option category_url or article_url is not specified!')

    if exists(args.markdown_dir) and args.rm_cache:
        shutil.rmtree(args.markdown_dir)

    if exists('./figures') and args.rm_cache:
        shutil.rmtree('./figures')

    if exists(args.pdf_dir) and args.rm_cache:
        shutil.rmtree(args.pdf_dir)

    is_win = args.is_win == 1
    md_dir = args.markdown_dir

    if args.category_url:
        download_category_url(args.category_url,
                               md_dir,
                               start_page=args.start_page,
                               page_num=args.page_num)
    else:
        download_single_page(args.article_url,
                              md_dir,
                              with_title=args.with_title)
    
    if args.combine_together:
        source_files = join(args.markdown_dir, '*.md')
        md_file = 'my_together_all_file.md'
        if is_win:
            cmd_line = f"type {source_files} > {md_file}"
        else:
            cmd_line = 'cat {} > {}'.format(source_files, md_file)
        os.system(cmd_line)
        if args.to_pdf:
            generate_pdf(md_file, args.pdf_dir, is_win)

    print("开始多线程下载文件.....")
    img_queue_downloader.start()
    img_queue_downloader.task_queue.join()
    img_queue_downloader.stop()
    print("下载文件结束!!!")
    time_end = tm.time()
    print("Time consume: ", time_end-time_start)
