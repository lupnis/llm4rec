import json

with open(r"I:\AAA\graduate_design\data\final_for_sft.json", 'r', encoding='utf-8') as f:
    doc = json.loads(f.read())
    outd = {
        "00000000": {
            "user_id": "00000000",
            "user_name": "user",
            "password": "eb5637cef0d0ba8a35a8091116d07561",
            "saved_pref": []
        }
    }
    inc = 0
    for i, item in enumerate(doc):
        pref = eval(item["output"])
        uname = str((inc+1)).rjust(8, '0')

        item_data = {
            "user_id": uname,
            "user_name": "user_"+uname,
            "password": "eb5637cef0d0ba8a35a8091116d07561",
            "saved_pref": pref
        }
        if len(pref[0]) == 0 or ''.join(pref[0]) == '':
            continue
        outd[uname] = item_data
        inc += 1

    with open('./data/user_db.json', 'w', encoding='utf-8') as f2:
        f2.write(json.dumps(outd, indent=4, ensure_ascii=False))
