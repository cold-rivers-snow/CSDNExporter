import os
import sys
import argparse
import re
import asyncio
import base64
from playwright.async_api import async_playwright
import markdown2

async def md_to_pdf_async(input_md, output_pdf):
    with open(input_md, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    md_content = re.sub(r'^---.*?---', '', md_content, flags=re.DOTALL)
    md_content = re.sub(r'^<meta[^>]*>', '', md_content, flags=re.MULTILINE)
    
    figures_dir = os.listdir('figures')[0]
    figures_path = os.path.join('figures', figures_dir)
    
    def replace_image(match):
        alt = match.group(1)
        path = match.group(2)
        path = path.replace('./figures/', '')
        path_parts = path.split('/')
        filename = path_parts[-1]
        full_path = os.path.join(figures_path, filename)
        if os.path.exists(full_path):
            with open(full_path, 'rb') as img_file:
                b64 = base64.b64encode(img_file.read()).decode('utf-8')
                ext = os.path.splitext(filename)[1][1:]
                return f'![{alt}](data:image/{ext};base64,{b64})'
        return match.group(0)
    
    md_content = re.sub(r'!\[([^\]]+)\]\(([^)]+)\)', replace_image, md_content)
    
    html_content = markdown2.markdown(md_content, extras=['code-friendly', 'Tables', 'fenced-code-blocks'])
    
    html_template = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Document</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: "SimSun", "Microsoft YaHei", "PingFang SC", "Noto Sans SC", sans-serif;
            font-size: 14px;
            line-height: 1.8;
            padding: 40px;
            max-width: 800px;
            margin: 0 auto;
            color: #333;
        }}
        h1 {{ font-size: 24px; font-weight: bold; margin: 30px 0 20px; color: #1a1a1a; }}
        h2 {{ font-size: 20px; font-weight: bold; margin: 25px 0 15px; color: #2a2a2a; border-bottom: 1px solid #eee; padding-bottom: 8px; }}
        h3 {{ font-size: 16px; font-weight: bold; margin: 20px 0 12px; color: #3a3a3a; }}
        h4, h5, h6 {{ font-size: 14px; font-weight: bold; margin: 15px 0 10px; }}
        pre {{
            background-color: #f6f8fa;
            padding: 16px;
            border-radius: 6px;
            font-family: "Consolas", "Courier New", monospace;
            font-size: 13px;
            overflow-x: auto;
            border: 1px solid #e1e4e8;
            line-height: 1.5;
        }}
        code {{
            font-family: "Consolas", "Courier New", monospace;
            background-color: #f6f8fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 13px;
        }}
        pre code {{
            padding: 0;
            background: none;
        }}
        blockquote {{
            border-left: 4px solid #007acc;
            margin: 16px 0;
            padding: 10px 16px;
            background-color: #f6f8fa;
            color: #6a737d;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 16px 0;
        }}
        ul, ol {{
            margin: 12px 0;
            padding-left: 24px;
        }}
        li {{
            margin: 6px 0;
        }}
        a {{
            color: #007acc;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 16px 0;
        }}
        th, td {{
            border: 1px solid #dfe2e5;
            padding: 10px 14px;
            text-align: left;
        }}
        th {{
            background-color: #f6f8fa;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #fafbfc;
        }}
        hr {{
            border: none;
            border-top: 1px solid #e1e4e8;
            margin: 24px 0;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>'''

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--allow-file-access-from-files',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process'
            ]
        )
        page = await browser.new_page()
        await page.set_content(html_template, wait_until='domcontentloaded', timeout=60000)
        
        await page.pdf(
            path=output_pdf,
            format='A4',
            margin={'top': '20mm', 'bottom': '20mm', 'left': '20mm', 'right': '20mm'},
            print_background=True,
            display_header_footer=False
        )
        
        await browser.close()
    
    print(f'PDF saved: {output_pdf}')

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown to PDF using Playwright')
    parser.add_argument('--input', '-i', required=True, help='Input markdown file')
    parser.add_argument('--output', '-o', help='Output PDF file (default: same name with .pdf)')
    args = parser.parse_args()

    input_file = args.input
    if not os.path.exists(input_file):
        print(f'Error: File {input_file} not found')
        sys.exit(1)

    if args.output:
        output_file = args.output
    else:
        output_file = os.path.splitext(input_file)[0] + '.pdf'

    asyncio.run(md_to_pdf_async(input_file, output_file))

if __name__ == '__main__':
    main()
