#!/bin/bash
######################################
# BlogExporter - 博客文章导出工具
# Usage:
#   ./run.sh --article_url <URL> [--to_pdf]
#   ./run.sh --category_url <URL> [--to_pdf]
######################################

set -e

ARTICLE_URL=""
CATEGORY_URL=""
TO_PDF=""
MARKDOWN_DIR="markdown"
PDF_DIR="pdf"
SITE="auto"
START_PAGE=1
PAGE_NUM=100

while [[ $# -gt 0 ]]; do
    case $1 in
        --article_url)
            ARTICLE_URL="$2"
            shift 2
            ;;
        --category_url)
            CATEGORY_URL="$2"
            shift 2
            ;;
        --to_pdf)
            TO_PDF="1"
            shift
            ;;
        --markdown_dir)
            MARKDOWN_DIR="$2"
            shift 2
            ;;
        --pdf_dir)
            PDF_DIR="$2"
            shift 2
            ;;
        --site)
            SITE="$2"
            shift 2
            ;;
        --start_page)
            START_PAGE="$2"
            shift 2
            ;;
        --page_num)
            PAGE_NUM="$2"
            shift 2
            ;;
        --help|-h)
            echo "BlogExporter - 博客文章导出工具"
            echo ""
            echo "Usage:"
            echo "  $0 --article_url <URL> [options]"
            echo "  $0 --category_url <URL> [options]"
            echo ""
            echo "Options:"
            echo "  --article_url    Article URL (博客文章地址)"
            echo "  --category_url   Category URL (博客分类地址)"
            echo "  --to_pdf         Convert to PDF (转换为PDF)"
            echo "  --markdown_dir   Output directory (默认: markdown)"
            echo "  --pdf_dir        PDF output directory (默认: pdf)"
            echo "  --site           Site parser (auto 自动检测)"
            echo ""
            echo "Examples:"
            echo "  $0 --article_url \"https://blog.csdn.net/xxx/article/details/xxx\""
            echo "  $0 --article_url \"https://www.cnblogs.com/xxx/p/xxx\" --to_pdf"
            echo "  $0 --category_url \"https://blog.csdn.net/xxx/category_xxx.html\""
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [[ -z "$ARTICLE_URL" && -z "$CATEGORY_URL" ]]; then
    echo "BlogExporter - 博客文章导出工具"
    echo ""
    echo "Usage:"
    echo "  $0 --article_url <URL> [options]"
    echo "  $0 --category_url <URL> [options]"
    echo ""
    echo "Options:"
    echo "  --article_url    Article URL (博客文章地址)"
    echo "  --category_url   Category URL (博客分类地址)"
    echo "  --to_pdf         Convert to PDF"
    echo "  --markdown_dir   Output directory (默认: markdown)"
    echo "  --site           Site parser (auto 自动检测)"
    echo ""
    echo "Examples:"
    echo "  $0 --article_url \"https://blog.csdn.net/xxx/article/details/xxx\""
    echo "  $0 --article_url \"https://www.cnblogs.com/xxx/p/xxx\" --to_pdf"
    echo "  $0 --category_url \"https://blog.csdn.net/xxx/category_xxx.html\""
    exit 1
fi

echo "========================================"
echo "BlogExporter - 博客文章导出工具"
echo "========================================"
echo ""

CMD=(python -u main.py)

if [[ -n "$ARTICLE_URL" ]]; then
    echo "Download article: $ARTICLE_URL"
    CMD+=(--article_url "$ARTICLE_URL")
elif [[ -n "$CATEGORY_URL" ]]; then
    echo "Download category: $CATEGORY_URL"
    CMD+=(--category_url "$CATEGORY_URL")
    CMD+=(--start_page $START_PAGE)
    CMD+=(--page_num $PAGE_NUM)
fi

CMD+=(--markdown_dir "$MARKDOWN_DIR")
CMD+=(--pdf_dir "$PDF_DIR")
CMD+=(--site "$SITE")

if [[ -n "$TO_PDF" ]]; then
    CMD+=(--to_pdf)
fi

echo "Running: ${CMD[@]}"
echo ""

start_time=$(date +%s)
"${CMD[@]}"
end_time=$(date +%s)

echo ""
echo "========================================"
echo "Done! Time: $((end_time - start_time))s"
echo "========================================"
