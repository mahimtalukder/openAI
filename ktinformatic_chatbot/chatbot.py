from flask import Flask, jsonify, request
import requests
import os
import openai

app = Flask(__name__)

def load_file_contents(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return f.read()

def openai_chatbot(api_key, file_contents, user_input):
    openai.api_key = api_key
    prompt = f"Based on the following information:\n{file_contents}\n\nUser: {user_input}\nChatbot:"

    response = openai.Completion.create(
        engine="text-davinci-003", 
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
     )

    generated_text = response.choices[0].text.strip()
    return generated_text
    
PAGE_ACCESS_TOKEN = "APP_Token" # Paste your page access token here 
API = f"https://graph.facebook.com/v13.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"


@app.route("/", methods=['GET'])
def fbverify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token")== "chatbot": # Replace "chatbot" with your verify token
            return "Verification token missmatch", 403
        return request.args['hub.challenge'], 200
    return "Hello world", 200

@app.route("/", methods=['POST'])
def fbwebhook():
    data = request.get_json()
    api_key = "Open_AI_API_Key" # Paste your OpenAI API key here
    file_name = "output.txt" # Paste your data file name here
    file_contents = load_file_contents(file_name)
    print(data)
    try:
        message = data['entry'][0]['messaging'][0]['message']
        sender_id = data['entry'][0]['messaging'][0]['sender']['id']
        chatbot_response = openai_chatbot(api_key, file_contents, message['text'].lower())
        request_body = {
            "recipient": {
             "id": sender_id
            },
            "message": {
                "text": chatbot_response
             }
         }
        response = requests.post(API, json=request_body).json()
        return jsonify(response), 200
    except requests.exceptions.RequestException:
        return "not ok", 500 

    return "Unhandled request", 400 
if __name__ =='__main__':
    app.run()