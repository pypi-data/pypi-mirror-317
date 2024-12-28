## BiEmoji

A simple Python library for accessing bilibili memes and dress-ups.

All APIs come from GitHub, and the APIs will become invalid with official updates.

If it fails, stop using it and wait for a later update.

## Installation

```bash
pip install dumb-menu
```

## Usage

This package is divided into two parts：

1. Emoji part

   ```python
   from biliemoji.emoji import Emoji
   
   # Create a Emoji object
   e = Emoji()
   # Use IDS to obtain emoji information
   res = e.certain_emoji(ids=53)
   # Returns a JSON object
   print(res)
   ```

2. Dress part

   ```python
   from biliemoji.dress import Dress
   
   # Create a Dress object
   d = Dress()
   # Search by keyword and temporarily the first piece of data
   res = d.search_dress(1,keyword="2233")
   # Returns a JSON object
   print(res)
   ```

For more information, please refer to GitHub

## GetHelp

Please to see github to understand the code structure, and if it is indeed a bug, please submit an issue

## Update log

`1.0,0` first release