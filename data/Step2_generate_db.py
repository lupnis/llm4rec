import json
import jsonlines


file_user_behaviors = open(
    "./data/transformed/steam_user_purchase_and_play_details.json",
    "r",
    encoding="utf-8",
)
file_game_details = open(
    "./data/transformed/steam_games_details.json", "r", encoding="utf-8"
)
qref_dict = {}  # quick ref dict for games
for i, li in enumerate(jsonlines.Reader(file_game_details)):
    if not li.get("id") or not li.get("app_name"):
        continue
    dict_game_details = {
        "id": li["id"],
        "name": li["app_name"],
        "cates": list(
            set(li.get("tags", []))
            | set(li.get("specs", []))
            | set(li.get("specs", []))
        ),
        "price": (
            0.0 if str(li.get("price", 0.0)).lower().find("free") != -1 else li.get("price", 0.0)
        ),
    }
    qref_dict[li["app_name"]] = dict_game_details
user_purchase_dict = {}
user_play_dict = {}
for i, li in enumerate(jsonlines.Reader(file_user_behaviors)):
    game_name = li["game_title"]
    user_id = li["user_id"]
    if qref_dict.get(game_name):
        if li["behavior"] == "purchase":
            if not user_purchase_dict.get(user_id):
                user_purchase_dict[user_id] = []
            user_purchase_dict[user_id].append({"game": qref_dict[game_name]})
        else:
            if not user_play_dict.get(user_id):
                user_play_dict[user_id] = []
            user_play_dict[user_id].append(
                {"game": qref_dict[game_name], "play_hours": li["play_hours"]}
            )
with open("./data/transformed/purchase.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(user_purchase_dict, ensure_ascii=False, indent=4))

with open("./data/transformed/play.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(user_play_dict, ensure_ascii=False, indent=4))
file_user_behaviors.close()
file_game_details.close()
print("done.")


"""
    
    instr_dict = {
            "input": "the user purchased games with following category and price info:(sample game 1:free,[c1,c2,c3]),(sammple game 2:10,[c2,c3,c4]), and played following games with time spent info:(sample game 1:1.0 hour),(sammple game 2:10.0 hours). conclude the preferences of the user in the format:([favorite cate1, favorite cate2, ...], preferred game price), rank from the most preferred. DO NOT RETURN ANYTHING OTHER THAN THE SPECIFIED FORMAT STRING."
        }
    """
