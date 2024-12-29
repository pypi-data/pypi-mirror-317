# HadithPy

HadithPy is a simple and powerful Python library for searching and managing Hadiths (Prophet Muhammad's sayings) in various collections like Sahih Bukhari and Sunan Abu Dawood. This library provides an easy-to-use interface to search Hadiths by keyword and get results from different books.

## Features

- Search for Hadiths by keyword (Arabic text).
- Supports popular Hadith books like Sahih Bukhari and Sunan Abu Dawood.
- Easily extendable for more Hadith books in the future.
- Simple and clear API for integrating into Python projects.

## Installation

You can install the library using pip:

```bash
pip install HadithPy
```

## Example

```python
from HadithPy import HadithSearcher

hadith_searcher = HadithSearcher(["abudawud"])
search_result = hadith_searcher.search("الأعمال بالنيات")
print(search_result)
```

## Updates

[![Telegram](https://raw.githubusercontent.com/CLorant/readme-social-icons/main/large/colored/telegram.svg)](https://t.me/i88y8)
