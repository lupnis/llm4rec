import jsonlines
import json
with open(r'I:\AAA\graduate_design\data\transformed\steam_games_details.json', 'r', encoding='utf-8') as f:
    ret = {}
    for i, li in enumerate(jsonlines.Reader(f)):
        if not li.get("id") or not li.get("app_name"):
            continue
        id, game_name = li["id"], li["app_name"]
        cates = list(
            set(li.get("tags", []))
            | set(li.get("specs", []))
            | set(li.get("specs", []))
        )
        price = (
            0.0 if str(li.get("price", 0.0)).lower().find(
                "free") != -1 else li.get("price", 0.0)
        )
        href = li["url"]
        ret[id] = {
            "game_id": id,
            "game_name": game_name,
            "game_img": f"https://media.st.dl.eccdnx.com/steam/apps/{id}/header.jpg",
            "game_tags": cates,
            "game_price": price,
            "game_href": href
        }
    with open('./data/game_db.json', 'w', encoding='utf-8') as f2:
        f2.write(json.dumps(ret, indent=4, ensure_ascii=False))
print('done.')