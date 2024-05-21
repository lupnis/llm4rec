import json
import pandas


# transform game details
file_game_details_input = open(
    "./data/original/steam_games_details.json", "r", encoding="utf-8"
)
file_game_details_jsonl_output = open(
    "./data/transformed/steam_games_details.json", "w", encoding="utf-8"
)
line_data = file_game_details_input.readline()
while line_data:
    file_game_details_jsonl_output.write(
        json.dumps(eval(line_data), ensure_ascii=False) + "\n"
    )
    line_data = file_game_details_input.readline()
file_game_details_jsonl_output.close()
file_game_details_input.close()
print("done 1.")

# transform game reviews
file_game_reviews_input = open("./data/original/steam_reviews.json", "r", encoding="utf-8")
file_game_reviews_jsonl_output = open(
    "./data/transformed/steam_reviews.json", "w", encoding="utf-8"
)
line_data = file_game_reviews_input.readline()
while line_data:
    file_game_reviews_jsonl_output.write(
        json.dumps(eval(line_data), ensure_ascii=False) + "\n"
    )
    line_data = file_game_reviews_input.readline()
file_game_reviews_jsonl_output.close()
file_game_reviews_input.close()
print("done 2.")

# transform game play statistics
df_user_behaviors = pandas.read_csv(
    "./data/original/steam_user_purchase_and_play_details.csv"
)
file_user_behaviors_jsonl_output = open(
    "./data/transformed/steam_user_purchase_and_play_details.json", "w", encoding="utf-8"
)
for i, item in df_user_behaviors.iterrows():
    flush_dict = {
        "user_id": item["user-id"],
        "game_title": item["game-title"],
        "behavior": item["behavior-name(purchase/play)"],
        "play_hours": item["play-hours(1.0-if-purchase)"],
    }
    file_user_behaviors_jsonl_output.write(
        json.dumps(flush_dict, ensure_ascii=False) + "\n"
    )
file_user_behaviors_jsonl_output.close()
print("done 3.")
