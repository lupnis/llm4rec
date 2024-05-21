import json


file_purchase = open("./data/transformed/purchase.json", "r", encoding="utf-8")
json_purchase = json.loads(file_purchase.read())
file_play = open("./data/transformed/play.json", "r", encoding="utf-8")
json_play = json.loads(file_play.read())

all_users = list(set(json_purchase.keys()) | set(json_play.keys()))

str_input_pre = "the user "
str_purchase_pre = "purchased following games with price and category info: "
str_play_pre = "played following games with hours spent and category info: "
instruction_str = "Conclude preferences of the user ONLY in the format: ([favorite cate1, favorite cate2, ...], preferred game price), rank from the most preferred to the least. Leave the price to 0.0 if there is no purchase info. DO NOT RETURN ANYTHING OTHER THAN THE SPECIFIED FORMAT STRING: "

all_data = []
for user_id in all_users:
    dict_data = {"instruction": instruction_str, "input": str_input_pre, "output": ""}
    connecting_str = ""
    if json_purchase.get(user_id) and len(json_purchase.get(user_id, [])):
        dict_data["input"] += str_purchase_pre
        connecting_str = ", and "
        for item in json_purchase[user_id]:
            dict_data[
                "input"
            ] += f"({item['game']['name']}:{item['game']['price']}, {item['game']['cates']}), "
    dict_data["input"] = dict_data["input"][:-2]
    if json_play.get(user_id) and len(json_play.get(user_id, [])):
        dict_data["input"] += connecting_str + str_play_pre
        for item in json_play[user_id]:
            dict_data[
                "input"
            ] += f"({item['game']['name']}:{item['play_hours']}, {item['game']['cates']}), "
            dict_data["input"] = dict_data["input"][:-2]
    dict_data["input"] += "."    
    all_data.append(dict_data)
with open("./data/dataset/sft_no_groundtruth.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(all_data, ensure_ascii=False, indent=4))
file_purchase.close()
file_play.close()
print("done.")
