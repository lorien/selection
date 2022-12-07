# Selection Documenation

[![Travis CI](https://travis-ci.org/lorien/selection.png?branch=master)](https://travis-ci.org/lorien/selection)

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


## Dependencies

* lxml
* tools
