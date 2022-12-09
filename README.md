# Selection Documenation

[![Tests](https://github.com/lorien/selection/actions/workflows/test.yml/badge.svg)](https://github.com/lorien/selection/actions/workflows/test.yml)
[![Code Quality](https://github.com/lorien/selection/actions/workflows/code_quality.yml/badge.svg)](https://github.com/lorien/selection/actions/workflows/code_quality.yml)
[![Typing](https://github.com/lorien/selection/actions/workflows/mypy.yml/badge.svg)](https://github.com/lorien/selection/actions/workflows/mypy.yml)
[![Test coverage](https://coveralls.io/repos/lorien/selection/badge.svg?branch=master)](https://coveralls.io/r/lorien/selection?branch=master)

API to query DOM tree of HTML/XML document.


## Usage Example

```
from selection import XpathSelector
from lxml.html import fromstring

html = '<div><h1>test</h1><ul id="items"><li>1</li><li>2</li></ul></div>'
sel = XpathSelector(fromstring(html))
print(sel.select('//h1')).text()
print(sel.select('//li').text_list()
print(sel.select('//ul').attr('id')
```


## Installation

Run: `pip install -U selection`


## Community

Telegram English chat: [https://t.me/grablab](https://t.me/grablab)

Telegram Russian chat: [https://t.me/grablab\_ru](https://t.me/grablab_ru)
