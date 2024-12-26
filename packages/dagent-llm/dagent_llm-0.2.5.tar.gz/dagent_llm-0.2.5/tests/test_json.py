import os
import csv
import subprocess
import pandas as pd
from tqdm import tqdm
from datetime import datetime
import argparse
import time

from rich.console import Console
from rich.table import Table

console = Console()

# Importing relevant classes
from dspeech import STT
from dagent_llm import LLM
from dguard import DguardModel as dm

# Initialize LLM
dagent = LLM("ollama")

fields = [
    {
        "name": "专利名称",
        "type": "str",
        "description": "专利名称",
        "example": "一种用于检测和诊断白血病的方法",
    },
    {
        "name": "专利简介",
        "type": "str",
        "description": "专利简介",
        "example": "本发明公开了一种用于检测和诊断白血病的方法",
    },
]

# json_result = dagent.generate_json("请提供专利名称和专利简介", fields)
# print(json_result)
# print(json_result["专利名称"])


# json_result = dagent.generate_jsons("请提供3个专利名称和专利简介", fields)
# print(json_result)


text = """
```python
print(a)```
xxxxx
```abc
adsf
```
yyy
```
你好
```
"""

code_list = dagent.get_code(text, code_type=["python", ""])
print(code_list)
