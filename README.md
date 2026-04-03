# CSDNExporter

将 CSDN 博客导出为 Markdown / PDF 格式的工具。

## 功能特性

- ✅ 下载 CSDN 单篇文章或整个分类
- ✅ 支持图片下载和嵌入
- ✅ 转换为 PDF（支持中文和图片）
- ✅ 批量导出

## 安装

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

## 快速开始

### 1. 下载 CSDN 文章

```bash
# 下载单篇文章
python main.py --article_url https://blog.csdn.net/weixin_43980547/article/details/137085690

# 下载整个分类
python main.py --category_url https://blog.csdn.net/xxx/category_xxx.html --page_num 10
```

### 2. 转换为 PDF

```bash
# Markdown 转 PDF（推荐，带图片）
python md_to_pdf.py --input markdown/你的文章.md

# 指定输出文件
python md_to_pdf.py --input markdown/文章.md --output output.pdf
```

## 输出目录

```
CSDNExporter/
├── markdown/          # 下载的 Markdown 文件
├── figures/           # 下载的图片
└── *.pdf             # 生成的 PDF 文件
```

## 依赖

- Python 3.8+
- requests, beautifulsoup4, httpx, bs4
- markdown2, playwright

## License

MIT

# Reference

- [axzml-CSDNExporter](https://github.com/axzml/CSDNExporter)