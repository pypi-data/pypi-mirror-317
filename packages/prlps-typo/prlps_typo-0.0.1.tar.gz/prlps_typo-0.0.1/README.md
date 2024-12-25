`pip install prlps_typo`

```python

from prlps_typo import to_html_typograf
from prlps_typo import to_markdown_typograf

bad_md_text = """
# (с) заголовок из маркдауна

## это - подзаголовок

* [ссылка](https://github.com/gniloyprolaps/prlps_typo)

> "цитата" на 1000000руб.

- это - пункт 1
- тут,пункт 2

"""

bad_html_text = """
<h1>заголовок из хтмл(tm)</h1>
<h2>это - подзаголовок!!?</h2>
<ul>
<li><a href="https://github.com/gniloyprolaps/prlps_typo">мда.... ссылка</a></li>
</ul>
<blockquote>
<p>"цитата" на 1000000руб.</p>
</blockquote>
<ul>
<li>это - пункт 1....</li>
<li>тут,пункт №№2</li>
</ul>
"""

typo = to_markdown_typograf(bad_html_text)
print(typo)
print('\n---\n')
typo = to_markdown_typograf(bad_md_text)
print(typo)
print('\n---\n')
typo = to_html_typograf(bad_html_text)
print(typo)
print('\n---\n')
typo = to_html_typograf(bad_md_text)
print(typo)
print('\n---\n')

```