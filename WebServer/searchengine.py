import re
import json


class SearchEngine:
    def __init__(self, doc_path):
        with open(doc_path, 'r', encoding='utf-8') as f:
            self.db = json.loads(f.read())

    def search(self, query):
        query_words = query.split()
        relevant_docs = []
        for word in query_words:
            word = re.sub(r'[^\w]', '', word)
            relevant_docs.append(set(self.db[word.lower()]))
        if not relevant_docs:
            return []
        return list(set.intersection(*relevant_docs))

