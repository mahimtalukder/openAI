import config
import open_ai_model
from flask import Flask, jsonify, request, send_from_directory
from fpdf import FPDF
import time
import requests

app = Flask(__name__)

# messages = []

@app.route('/file/<filename>')
def send_file(filename):
    return send_from_directory('file', filename)

@app.route("/", methods=['GET'])
def fbverify():
    # global messages
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token")== "chatbot": # Replace "chatbot" with your verify token
            return "Verification token missmatch", 403
        return request.args['hub.challenge'], 200
    return "Hello world", 200

@app.route("/", methods=['POST'])
def fbwebhook():
    data = request.get_json()
    api_key = config.open_ai_key
    file_name = config.dataset 
    file_contents = open_ai_model.load_file_contents(file_name)
    print(data)
    try:
        message = data['entry'][0]['messaging'][0]['message']
        sender_id = data['entry'][0]['messaging'][0]['sender']['id']
        # chatbot_response = open_ai_model.openai_chatbot(api_key, file_contents, message['text'].lower(), messages)
        chatbot_response = open_ai_model.openai_chatbot(api_key, file_contents, message['text'].lower())
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size = 12)
        pdf.cell(0, 10, "KT Informatik", ln=True, align='C')  # Title
        pdf.ln(10)  # Line break

        # Use multi_cell for multi-line text
        pdf.multi_cell(0, 10, chatbot_response)

        tm = round(time.time())
        name = "file/"+ str(tm) + "_estimation.pdf"
        pdf.output(name)
        link = 'http://localhost:5000/' + name
        chatbot_response =chatbot_response + "\n\n Please check the estimation file: " + link
        request_body = {
            "recipient": {
             "id": sender_id
            },
            "message": {
                "text": chatbot_response
             }
         }
        # if print.entry[0].id == messages[0].id:
        #     if len(messages) < 3:
        #         new_message = {
        #             "id": print.entry[0].id,
        #             "question": message,
        #             "message": response
        #         }
        #         messages.append(new_message)
        #     else:
        #         messages.pop(0)
        #         new_message = {
        #             "id": print.entry[0].id,
        #             "question": message,
        #             "message": response
        #         }
        #         messages.append(new_message)
        # else:
        #     new_message = [{
        #         "id": print.entry[0].id,
        #         "question": message,
        #         "message": response
        #     }]
        #     messages = new_message
        
        response = requests.post(config.API, json=request_body).json()
        return jsonify(response), 200
    except requests.exceptions.RequestException:
        return "not ok", 500 

    return "Unhandled request", 400 

if __name__ =='__main__':
    app.run()

