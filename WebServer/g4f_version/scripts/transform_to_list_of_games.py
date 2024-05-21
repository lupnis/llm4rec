import json

with open('./data/game_db.json', 'r', encoding='utf-8') as f:
    doc = json.loads(f.read())
    
    
    doc_new = [item for item in doc.values()]
    
    with open('./data/game_db_list.json', 'w', encoding='utf-8') as f2:
        f2.write(json.dumps(doc_new, ensure_ascii=False, indent=4))
print('done.')