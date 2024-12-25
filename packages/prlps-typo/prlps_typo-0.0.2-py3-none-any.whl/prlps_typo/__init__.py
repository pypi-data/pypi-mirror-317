from pathlib import Path
from re import DOTALL, MULTILINE, compile
from time import sleep

from mistune import html
from html2text import HTML2Text
from httpx import Client, Timeout
from py_mini_racer.py_mini_racer import MiniRacer

WORK_DIR = Path(__file__).parent

TYPOGRAF_URL = 'https://cdn.jsdelivr.net/npm/typograf/dist/typograf.min.js'
TYPOGRAF_PATH = WORK_DIR / 'typograf.js'

MARKDOWN_PATTERN = compile(r'(\*\*[^*]+\*\*)|(__[^_]+__)|(`[^`]+`)|(\|\|[^|]+\|\|)|(^#{1,6}\s[^#]+)', MULTILINE)
HTML_PATTERN = compile(r'<[^>]+>.*?</[^>]+>', DOTALL)


def fetch(url: str) -> str | None:
    max_retries = 3
    with Client(
            follow_redirects=True,
            timeout=Timeout(connect=15, read=30, write=15, pool=30)
    ) as client:
        for attempt in range(1, max_retries + 1):
            try:
                response = client.get(url)
                response.raise_for_status()
                return response.text
            except Exception as e:
                if attempt == max_retries:
                    print(f'{e}: ошибка скачивания {url} после {max_retries} попыток.')
                    return None
                sleep(5)


def get_typograf() -> str | None:
    if not TYPOGRAF_PATH.exists():
        code = fetch(TYPOGRAF_URL)
        if code:
            TYPOGRAF_PATH.write_text(code)
    return TYPOGRAF_PATH.read_text()


def typograf(text: str) -> str:
    return MiniRacer().eval(
        f"{get_typograf()}"
        "var tp = new Typograf({locale: ['ru', 'en-US']});"
        "tp.enableRule('ru/money/ruble');"
        "tp.enableRule('common/nbsp/replaceNbsp');"
        f"tp.execute({text!r});"
    )


def detect_markup_type(text: str) -> str:
    if MARKDOWN_PATTERN.search(text):
        return 'Markdown'
    elif HTML_PATTERN.search(text):
        return 'HTML'
    else:
        return 'Plain text'


def html_to_md(html_content: str) -> str:
    text_maker = HTML2Text()
    text_maker.ul_item_mark = '•'
    text_maker.bypass_tables = False
    text_maker.code = True
    text_maker.code_snippets = True
    text_maker.code_blocks = True
    text_maker.mark_code = True
    text_maker.body_width = 0
    text_maker.ignore_links = True
    if detect_markup_type(html_content) != 'Markdown':
        markdown_content = text_maker.handle(html_content)
        return markdown_content
    else:
        return html_content


def md_to_html(md_content: str) -> str:
    if detect_markup_type(md_content) != 'HTML':
        return html(md_content)
    else:
        return md_content


def to_markdown_typograf(text: str) -> str:
    return html_to_md(typograf(md_to_html(text))).strip()


def to_html_typograf(text: str) -> str:
    return md_to_html(typograf(md_to_html(text))).strip()


__all__ = ['to_markdown_typograf', 'to_html_typograf']
