import fitos.fito_processor as fp
import os
import json
from pathlib import Path

NUMBER_WORKERS= 5


def _process_entity(entity):
    answer = {
        'success': True,
    }
    try:
        with open(entity['filepath'], 'r', encoding='utf-8') as f:
            entity['text'] = json.load(f)
    except Exception as ex:
        answer['success']= False
        answer['message'] = str(ex)

    return answer

directory_path='test_json'
entities= []
for filename in os.listdir(directory_path):
    filepath= None
    entities.append({
                'filepath': str(Path(directory_path)/ filename),
              })
processor = fp.Processor(NUMBER_WORKERS)
response= processor.run(entities,_process_entity)
print(response['message'])
a=1
