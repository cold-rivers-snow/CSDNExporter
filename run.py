#!/usr/bin/env python
"""
BlogExporter - Simple runner script
Usage:
    python run.py --article_url <URL> [--to_pdf] [--markdown_dir DIR] [--site SITE]
    python run.py --category_url <URL> [--to_pdf] [--markdown_dir DIR]
"""
import os
import sys
import subprocess
import argparse
import time


def main():
    parser = argparse.ArgumentParser(description='BlogExporter - 博客文章导出工具')
    parser.add_argument('--article_url', type=str, help='Article URL (博客文章地址)')
    parser.add_argument('--category_url', type=str, help='Category URL (博客分类地址)')
    parser.add_argument('--to_pdf', action='store_true', help='Convert to PDF (转换为PDF)')
    parser.add_argument('--markdown_dir', type=str, default='markdown', help='Output directory')
    parser.add_argument('--pdf_dir', type=str, default='pdf', help='PDF output directory')
    parser.add_argument('--site', type=str, default='auto', help='Site parser (auto 自动检测)')
    parser.add_argument('--start_page', type=int, default=1, help='Start page')
    parser.add_argument('--page_num', type=int, default=100, help='Page number')
    parser.add_argument('--is_win', action='store_true', help='Windows platform')
    
    args = parser.parse_args()
    
    if not args.article_url and not args.category_url:
        print("""
BlogExporter - 博客文章导出工具
================================

Usage:
    python run.py --article_url <URL> [options]
    python run.py --category_url <URL> [options]

Options:
    --article_url    Article URL (博客文章地址)
    --category_url  Category URL (博客分类地址)
    --to_pdf         Convert to PDF (转换为PDF)
    --markdown_dir   Output directory (默认: markdown)
    --pdf_dir        PDF output directory (默认: pdf)
    --site           Site parser (auto 自动检测)
    --start_page     Start page (分类下载时)
    --page_num       Page number (分类下载时)

Examples:
    python run.py --article_url "https://blog.csdn.net/xxx/article/details/xxx"
    python run.py --article_url "https://www.cnblogs.com/xxx/p/xxx" --to_pdf
    python run.py --category_url "https://blog.csdn.net/xxx/category_xxx.html"
""")
        sys.exit(1)
    
    print("========================================")
    print("BlogExporter - 博客文章导出工具")
    print("========================================")
    print()
    
    cmd = ['python', '-u', 'main.py']
    
    if args.article_url:
        cmd.extend(['--article_url', args.article_url])
    if args.category_url:
        cmd.extend(['--category_url', args.category_url])
        cmd.extend(['--start_page', str(args.start_page)])
        cmd.extend(['--page_num', str(args.page_num)])
    
    cmd.extend(['--markdown_dir', args.markdown_dir])
    cmd.extend(['--pdf_dir', args.pdf_dir])
    cmd.extend(['--site', args.site])
    
    if args.to_pdf:
        cmd.append('--to_pdf')
    if args.is_win:
        cmd.append('--is_win')
        cmd.append('1')
    
    print(f"Running: {' '.join(cmd)}")
    print()
    
    start_time = time.time()
    subprocess.call(cmd)
    end_time = time.time()
    
    print()
    print("========================================")
    print(f"Done! Time: {end_time - start_time:.2f}s")
    print("========================================")


if __name__ == '__main__':
    main()
