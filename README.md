# BlogExporter - 多平台博客文章导出工具

将博客文章导出为 Markdown / PDF 格式的工具，支持多个博客平台。

## 功能特性

- ✅ 支持多个博客平台自动识别
- ✅ 支持图片下载和嵌入
- ✅ 转换为 PDF（支持中文和图片）
- ✅ 批量导出分类文章
- ✅ 单元测试覆盖

## 支持的博客平台

| 平台 | 域名 | 状态 |
|------|------|------|
| CSDN | csdn.net | ✅ |
| 简书 | jianshu.com | ✅ |
| SegmentFault | segmentfault.com | ✅ |
| 开源中国 | oschina.net | ✅ |
| 知乎 | zhihu.com | ✅ |
| 腾讯云 | cloud.tencent.com | ✅ |
| 美团技术 | tech.meituan.com | ✅ |
| CloudFlare Blog | blog.cloudflare.com | ✅ |
| Lofter | lofter.com | ✅ |
| 飞书文档 | feishu.cn | ✅ |
| 微信公众号 | mp.weixin.qq.com | ✅ |
| WordPress | wordpress.com | ✅ |
| Hexo | hexo.io | ✅ |
| Hugo | gohugo.io | ✅ |
| VuePress | vuejs.org | ✅ |

## 安装

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

## 快速开始

### 1. 使用 run.py / run.sh / run.bat（推荐）

```bash
# Windows
run.bat --article_url "https://blog.csdn.net/xxx/article/details/xxx"
run.bat --article_url "https://www.cnblogs.com/tangge/p/19620738" --to_pdf

# Linux/Mac
python run.py --article_url "URL"
./run.sh --article_url "URL"

# 下载整个分类
python run.py --category_url "https://blog.csdn.net/xxx/category_xxx.html"
```

### 2. 直接使用 main.py

```bash
# 自动检测博客平台并下载
python main.py --article_url https://blog.csdn.net/xxx/article/details/xxx

# 下载整个分类
python main.py --category_url https://blog.csdn.net/xxx/category_xxx.html --page_num 10
```

### 2. 指定平台下载

```bash
# 指定 CSDN
python main.py --article_url <url> --site csdn

# 指定简书
python main.py --article_url <url> --site jianshu

# 指定腾讯云
python main.py --article_url <url> --site tencent

# 指定 WordPress
python main.py --article_url <url> --site wordpress

# 指定 Hexo
python main.py --article_url <url> --site hexo

# 指定 Hugo
python main.py --article_url <url> --site hugo
```

### 3. 转换为 PDF

```bash
# Markdown 转 PDF
python md_to_pdf.py --input markdown/你的文章.md

# 指定输出文件
python md_to_pdf.py --input markdown/文章.md --output output.pdf
```

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--article_url` | 文章 URL | - |
| `--category_url` | 分类页 URL | - |
| `--site` | 指定博客平台 (auto 自动检测) | auto |
| `--start_page` | 分类起始页 | 1 |
| `--page_num` | 分类页数 | 100 |
| `--markdown_dir` | Markdown 输出目录 | markdown |
| `--pdf_dir` | PDF 输出目录 | pdf |
| `--with_title` | 包含标题栏 | False |
| `--to_pdf` | 转换为 PDF | False |
| `--rm_cache` | 清除缓存 | False |
| `--is_win` | Windows 平台 | 0 (Linux) |
| `--combine_together` | 合并所有 Markdown | False |

## 支持的 URL 示例

```bash
# CSDN
python main.py --article_url https://blog.csdn.net/xxx/article/details/xxx

# 简书
python main.py --article_url https://www.jianshu.com/p/xxx

# SegmentFault
python main.py --article_url https://segmentfault.com/a/xxx

# 开源中国
python main.py --article_url https://my.oschina.net/u/xxx/blog/xxx

# 知乎
python main.py --article_url https://zhuanlan.zhihu.com/p/xxx

# 腾讯云
python main.py --article_url https://cloud.tencent.com/developer/article/xxx

# 美团技术
python main.py --article_url https://tech.meituan.com/xxx

# CloudFlare
python main.py --article_url https://blog.cloudflare.com/xxx

# Lofter
python main.py --article_url https://xxx.lofter.com/post/xxx

# 飞书
python main.py --article_url https://feishu.cn/content/xxx

# 微信公众号 (需要使用 Playwright/Selenium 渲染 JS)
python main.py --article_url https://mp.weixin.qq.com/s/xxx --site wechat
```

## 输出目录

```
CSDNExporter/
├── markdown/          # 下载的 Markdown 文件
├── figures/           # 下载的图片
├── pdf/               # 生成的 PDF 文件
└── *.pdf             # 单独的 PDF 文件
```

## 架构说明

```
parsers/
├── __init__.py        # 包入口
├── base.py            # 抽象基类 SiteParser
├── factory.py         # 解析器工厂
├── csdn.py            # CSDN 解析器
├── jianshu.py         # 简书解析器
├── segmentfault.py    # SegmentFault 解析器
├── oschina.py         # 开源中国解析器
├── zhihu.py           # 知乎解析器
├── tencent.py         # 腾讯云解析器
├── meituan.py         # 美团技术解析器
├── cloudflare.py      # CloudFlare 解析器
├── lofter.py          # Lofter 解析器
├── feishu.py          # 飞书解析器
├── wechat.py          # 公众号解析器
├── wordpress.py       # WordPress 解析器
├── hexo.py            # Hexo 解析器
├── hugo.py            # Hugo 解析器
└── vuepress.py        # VuePress 解析器
```

### 添加新的博客平台

1. 在 `parsers/` 目录下创建新的解析器文件，如 `mysite.py`
2. 继承 `SiteParser` 基类
3. 实现 `get_metadata()` 和 `get_content()` 方法
4. 在 `factory.py` 中注册

示例：

```python
from parsers.base import SiteParser, ArticleMetadata

class MySiteParser(SiteParser):
    SITE_NAME = "我的博客"
    SITE_DOMAINS = ['mysite.com', 'blog.mysite.com']
    
    def get_metadata(self) -> ArticleMetadata:
        # 实现元数据提取
        pass
    
    def get_content(self) -> str:
        # 实现内容提取
        pass
```

## 运行测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试
python -m pytest tests/test_csdn.py -v

# 运行解析器工厂测试
python -m pytest tests/test_parser_factory.py -v
```

## 注意事项

1. **微信公众号**：由于微信文章使用 JS 渲染，需要使用 Playwright/Selenium 等工具先渲染再解析
2. **图片下载**：工具会自动下载文章中的图片并嵌入 Markdown
3. **PDF 转换**：需要安装 pandoc 和 xelatex

## 依赖

- Python 3.8+
- requests, beautifulsoup4, httpx, bs4
- markdown2, playwright

## License

MIT

## 参考

- [axzml-CSDNExporter](https://github.com/axzml/CSDNExporter)
