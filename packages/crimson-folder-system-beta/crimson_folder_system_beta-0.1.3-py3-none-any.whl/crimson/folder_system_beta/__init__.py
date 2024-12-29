"""
---
```
Filter:
    - summary: Filter path to search
    - description: Use `FnFilter` or `ReFilter` as predefined `Filter`,
    or define your own `Filter`.
search:
    - summary: search folder or path
```
---
"""
from crimson.folder_system_beta.filter import Filter, FnFilter, ReFilter
from crimson.folder_system_beta.search import search
from crimson.folder_system_beta.delete import delete_files
