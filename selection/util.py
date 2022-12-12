"""Helpful things used in multiple modules of selection package.

Most of this module contents is a copy-paste from weblib package. It is done to
drop outdated weblib dependency.
"""
from __future__ import annotations

import re
from html.entities import name2codepoint
from re import Match
from typing import List, cast

import lxml.html
from lxml.etree import _Element

RE_NUMBER = re.compile(r"\d+")
RE_NUMBER_WITH_SPACES = re.compile(r"\d[\s\d]*")
RE_SPACE = re.compile(r"\s+")
RE_NAMED_ENTITY = re.compile(r"(&[a-z]+;)")
RE_NUM_ENTITY = re.compile(r"(&#[0-9]+;)")
RE_HEX_ENTITY = re.compile(r"(&#x[a-f0-9]+;)", re.I)


def normalize_spaces(val: str) -> str:
    return re.sub(r"\s+", " ", val).strip()


def drop_spaces(val: str) -> str:
    """Drop all space-chars in the `text`."""
    return RE_SPACE.sub("", val)


def find_number(
    text: str,
    ignore_spaces: bool = False,
    make_int: bool = True,
    ignore_chars: None | str | list[str] = None,
) -> str | int:
    """Find the number in the `text`.

    :param text: str
    :param ignore_spaces: if True then consider groups of digits delimited
        by spaces as a single number

    Raises IndexError if number was not found.
    """
    if ignore_chars:
        for char in ignore_chars:
            text = text.replace(char, "")
    rex = RE_NUMBER_WITH_SPACES if ignore_spaces else RE_NUMBER
    match = rex.search(text)
    if match:
        val = match.group(0)
        if ignore_spaces:
            val = drop_spaces(val)
        if make_int:
            return int(val)
        return val
    raise IndexError("Could not find a number in given text")


def process_named_entity(match: Match[str]) -> str:
    entity = match.group(1)
    name = entity[1:-1]
    if name in name2codepoint:
        return chr(name2codepoint[name])
    return entity


def process_num_entity(match: Match[str]) -> str:
    entity = match.group(1)
    num = entity[2:-1]
    try:
        return chr(int(num))
    except ValueError:
        return entity


def process_hex_entity(match: Match[str]) -> str:
    entity = match.group(1)
    code = entity[3:-1]
    try:
        return chr(int(code, 16))
    except ValueError:
        return entity


def decode_entities(html: str) -> str:
    """Convert all HTML entities into their unicode representations.

    This functions processes following entities:
     * &XXX;
     * &#XXX;

    Example::

        >>> print html.decode_entities('&rarr;ABC&nbsp;&#82;&copy;')
        →ABC R©
    """
    html = RE_NUM_ENTITY.sub(process_num_entity, html)
    html = RE_HEX_ENTITY.sub(process_hex_entity, html)
    return RE_NAMED_ENTITY.sub(process_named_entity, html)


def render_html(node: _Element) -> str:
    """Render Element node."""
    return lxml.html.tostring(
        cast(lxml.html.HtmlElement, node), encoding="utf-8"
    ).decode("utf-8")


def get_node_text(
    node: _Element, smart: bool = False, normalize_space: bool = True
) -> str:
    """Extract text content of the `node` and all its descendants.

    In smart mode `get_node_text` insert spaces between <tag><another tag>
    and also ignores content of the script and style tags.

    In non-smart mode this func just return text_content() of node
    with normalized spaces
    """
    if isinstance(node, str):
        value = str(node)
    elif smart:
        # pylint: disable=deprecated-typing-alias
        value = " ".join(
            cast(
                List[str],
                node.xpath(
                    './descendant-or-self::*[name() != "script" and '
                    'name() != "style"]/text()[normalize-space()]'
                ),
            )
        )
    elif isinstance(node, lxml.html.HtmlElement):
        value = node.text_content()
    else:
        # If DOM tree was built with lxml.etree.fromstring
        # then tree nodes do not have text_content() method
        value = "".join(map(str, node.xpath(".//text()")))
    if normalize_space:
        return normalize_spaces(value)
    return value
