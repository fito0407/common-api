from datetime import datetime, timezone, timedelta
import os
import json
import pandas as pd
from html.parser import HTMLParser
import re

def get_now_utc():
    utc_now = datetime.now(timezone.utc)
    answer = convert_date_to_utc_iso86001string(utc_now)
    return answer

def get_now_utc_x_days_back(days: int):
    target_date = datetime.now(timezone.utc) - timedelta(days=days)
    answer= convert_date_to_utc_iso86001string(target_date)
    return answer

def convert_date_to_utc_iso86001string(target_date):
    return target_date.isoformat(timespec='milliseconds').replace('+00:00', 'Z')

def get_now_utcfilenamesafe():
    answer = get_now_utc().replace(":", "_").replace(".", "_")
    return  answer

def get_dataframe_from_jsons(directory_path):
    all_data = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_data.append(data)
    answer = pd.DataFrame(all_data)
    return answer

def get_date_from_utc_iso86001string(value):
    answer= datetime.fromisoformat(value.replace('Z', '+00:00'))
    return answer

def get_elapsed_milliseconds(dt_end, dt_init):
    answer= (dt_end - dt_init).total_seconds() * 1000
    return answer

def save_list_of_dicts_by_index(data_list, folder_name):
    os.makedirs(folder_name, exist_ok=True)
    for index, data_dict in enumerate(data_list):
        filename = f"{index}.json"
        filepath = os.path.join(folder_name, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=4)

def chunk(items, size):
    return [items[i:i + size] for i in range(0, len(items), size)]

class HTMLToText(HTMLParser):
    # Block-level tags become a line break so words either side don't run
    # together (e.g. "<p>Java</p><p>SQL</p>" -> "Java\nSQL", not "JavaSQL").
    _BLOCK_TAGS = {
        'p', 'br', 'div', 'li', 'ul', 'ol', 'tr', 'table', 'section',
        'article', 'header', 'footer', 'blockquote',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)  # decodes &amp; &nbsp; etc.
        self._parts = []

    def handle_data(self, data):
        self._parts.append(data)

    def handle_starttag(self, tag, attrs):
        if tag in self._BLOCK_TAGS:
            self._parts.append('\n')

    def handle_endtag(self, tag):
        if tag in self._BLOCK_TAGS:
            self._parts.append('\n')

    def get_text(self):
        return ''.join(self._parts)

def clean_html(text):
    # Strip HTML tags and decode entities from a document's text. Returns the
    # input unchanged when it is empty/None so missing descriptions stay missing.
    if not text:
        return text
    parser = HTMLToText()
    parser.feed(text)
    parser.close()
    cleaned = parser.get_text()
    cleaned = re.sub(r'[^\S\n]+', ' ', cleaned)   # collapse spaces/tabs, keep \n
    cleaned = re.sub(r' *\n *', '\n', cleaned)     # trim spaces around newlines
    cleaned = re.sub(r'\n{2,}', '\n', cleaned)     # collapse blank lines
    return cleaned.strip()