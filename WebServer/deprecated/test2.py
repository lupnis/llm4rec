from g4f.client import Client

proxies = {
    "all": "http://127.0.0.1:7890"
}

client = Client(proxies=proxies)

chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "请在响应时带上用户名：用户名为aaa。"},
              {"role": "user", "content": "Hi!"}],

)

print(chat_completion.choices[0].message.content or "")
