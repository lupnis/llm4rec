import json

import re

import collections

def build_inverted_index(documents, stop_words = []):
    """
    构建倒排索引
    :param documents: 文档列表
    :return: 倒排索引
    """
    inverted_index = collections.defaultdict(list)
    for doc_id, doc in enumerate(documents):
        words = doc.split()
        for word in words:
            # 使用正则表达式去除标点符号
            word = re.sub(r'[^\w]', '', word)
            if word.lower() in stop_words:
                continue
            inverted_index[word.lower()].append(doc_id)
    return inverted_index



with open('./data/game_db.json', 'r', encoding='utf-8') as f:
    games = json.loads(f.read())
    docs = [
        f"{item['game_id']} {item['game_name']} {' '.join(item['game_tags'])}" for item in games.values()
    ]
    rvi = build_inverted_index(docs)
    
    with open('./inverted_index_db.json', 'w', encoding='utf-8') as f2:
        f2.write(json.dumps(rvi, ensure_ascii=False, indent=4))
        
    print('done.')