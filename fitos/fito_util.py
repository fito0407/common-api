from datetime import datetime, timezone
import os
import json
import pandas as pd

def get_now_utc():
    utc_now = datetime.now(timezone.utc)
    answer= utc_now.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    return  answer

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