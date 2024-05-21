import json
import numpy as np

from searchengine import SearchEngine


class GameManager:
    def __init__(self, db_path, inverted_index_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            self.db = json.loads(f.read())
        self.search_engine = SearchEngine(inverted_index_path)

    def search_game(self,
                    query=None,
                    game_tags=None,
                    game_price_range=None,
                    top_k = 10):

        ret_list = []
        if top_k >= len(list(self.db.keys())):top_k = len(list(self.db.keys()))
        q2filter = self.search_engine.search(query) if (query and len(query)) else range(len(list(self.db.keys())))
        for game in q2filter:
            matched_game = self.db[list(self.db.keys())[game]]
            if ((not game_tags or len(
                    set.intersection(set(matched_game["game_tags"]), set(game_tags)))) and
                (not game_price_range or (
                    float(game_price_range[0]) <= matched_game["game_price"] <= float(game_price_range[1])))):
                ret_list.append(matched_game)
            if len(ret_list) >= top_k: return ret_list
        return ret_list
