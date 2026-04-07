@echo off
@title BlogExporter

set "article_url="
set "category_url="
set "to_pdf="
set "markdown_dir=markdown"
set "pdf_dir=pdf"

:parse_args
if "%~1"=="" goto done
if /i "%~1"=="--article_url" set "article_url=%~2" & shift & shift & goto parse_args
if /i "%~1"=="--category_url" set "category_url=%~2" & shift & shift & goto parse_args
if /i "%~1"=="--to_pdf" set "to_pdf=1" & shift & goto parse_args
if /i "%~1"=="--markdown_dir" set "markdown_dir=%~2" & shift & shift & goto parse_args
if /i "%~1"=="--pdf_dir" set "pdf_dir=%~2" & shift & shift & goto parse_args
if /i "%~1"=="--site" set "site=%~2" & shift & shift & goto parse_args
if /i "%~1"=="--help" goto help
shift
goto parse_args

:done
if "%article_url%"=="" if "%category_url%"==" goto help

echo ========================================
echo BlogExporter - 博客文章导出工具
echo ========================================
echo.

if not "%category_url%"=="" (
    echo Download category: %category_url%
    python -u main.py --category_url "%category_url%" --markdown_dir %markdown_dir% --pdf_dir %pdf_dir% --is_win 1 %to_pdf%
) else (
    echo Download article: %article_url%
    python -u main.py --article_url "%article_url%" --markdown_dir %markdown_dir% --pdf_dir %pdf_dir% --is_win 1 %to_pdf%
)
echo.
echo Done!
pause
exit /b

:help
echo ========================================
echo BlogExporter - 博客文章导出工具
echo ========================================
echo.
echo Usage:
echo   run.bat --article_url ^<URL^> [options]
echo   run.bat --category_url ^<URL^> [options]
echo.
echo Options:
echo   --article_url    Article URL (博客文章地址)
echo   --category_url  Category URL (博客分类地址)
echo   --to_pdf         Convert to PDF (转换为PDF)
echo   --markdown_dir   Output directory (默认: markdown)
echo   --pdf_dir        PDF output directory (默认: pdf)
echo   --site           Site parser (auto 自动检测)
echo   --help           Show this help
echo.
echo Examples:
echo   run.bat --article_url "https://blog.csdn.net/xxx/article/details/xxx"
echo   run.bat --article_url "https://www.cnblogs.com/xxx/p/xxx" --to_pdf
echo   run.bat --category_url "https://blog.csdn.net/xxx/category_xxx.html" --markdown_dir myblog
echo.
pause
