import ollama

"""
# Chat
response1 = ollama.chat(model="llama3.3:latest", messages=[
    {
        'role': 'user',
        'content': 'What it the capital of Korea? (Only capital name)',
    },
])

response2 = ollama.chat(model="llama3.3:latest", messages=[
    {
        'role': 'user',
        'content': 'And what about Grance, Germany? (Only capital name)',
    },
])

print(response1['message']['content'])
print(response2['message']['content'])

# generate
response1 = ollama.generate(model='phi3', prompt='What is the capital of Korea? (Only capital name)')
response2 = ollama.generate(model='phi3', prompt='And what about Grance, Germany? (Only capital name)')

print(response1['response'])
print(response2['response'])

# REST API
import requests
import json

# curl -X POST "http://localhost:11434/api/generate" -d '{ "model": "llama3.3:latest", "prompt": "세종대왕에 대해서 간단하게 알려주세요.(한국어로)" }'
def generate_response(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3.3:latest",
        "prompt": prompt
    }
    response = requests.post(url, json=data)
    return json.loads(response.text)['response']

prompt = "세종대왕에 대해서 간단하게 알려주세요.(한국어로)"
response = generate_response(prompt)
print(response)
"""

# 간단한 챗봇
def chat_main():
    print("Ollama 챗봇에 오신 것을 환영합니다! 대화를 마치려면 'exit'을 입력해주세요.")

    while True:
        user_input = input("You: ")

        if user_input == "exit":
            print("안녕히 가세요!")
            break

        response = ollama.generate(model='llama3.3:latest', prompt=user_input)
        print("Ollama: ", response['response'])

if __name__ == "__main__":
    chat_main()