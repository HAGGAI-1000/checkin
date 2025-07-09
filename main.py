from flask import Flask, request
import os
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from openai import OpenAI
import requests
from users import users
from prompts import prompt1, prompt2

#uncommnet for running locally:
#from dotenv import load_dotenv
#load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_token = os.getenv("TWILIO_AUTH_TOKEN")

openAIclient = OpenAI(api_key = openai_api_key)
chat_history = []
app = Flask(__name__)
sender = "whatsapp:+19707804331"
twilioClient = Client(twilio_sid, twilio_token)
emotion = "unspecified"
emotion_selection = ["I'm really okay", "Great", "Don't know", "Sad", "Edgy", "Scared", "Helpless", "Angry"]

@app.route("/", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get('Body')
    incoming_sender = request.form.get('From')
    user = next((u for u in users if u['phone'] == incoming_sender), None)
    if not user:
        resp = MessagingResponse()
        resp.message("Sorry, I don't recognize this number. Please contact Noga Tal.")
        return str(resp)
    gender = user['gender']
    name = user['name']
    match incoming_msg:
        case "demo":
            twilioClient.messages.create(from_= sender, to = incoming_sender, content_sid = 'HXee8c500e794d49f8a96abf68df67da8a')
            resp = None
        case "אוקיי קדימה!":
            if gender == 'male':
                twilioClient.messages.create(from_= sender, to = incoming_sender, content_sid = 'HX36ceb85a37eb8429553621d86bd26d72')
            else:
                twilioClient.messages.create(from_= sender, to = incoming_sender, content_sid = 'HX36ceb85a37eb8429553621d86bd26d72')
            resp = None
        case "לא עכשיו":
            resp = MessagingResponse()
            if gender == 'male':
                resp.message("אוקיי, אני מחכה לשמוע ממך כשאתה מוכן!")
            else:
                resp.message("אוקיי, אני מחכה לשמוע ממך כשאת מוכנה!")
        case c if c in emotion_selection:
            emotion = incoming_msg
            instructions = prompt1(emotion_selection, emotion, gender, name)
            chat_history.append({"role": "system", "content": instructions})
            stream = openAIclient.chat.completions.create(model="gpt-4o-2024-05-13", messages=chat_history)
            response = stream.choices[0].message.content
            chat_history.append({"role": "assistant", "content": response})
            instructions = prompt2
            chat_history.append({"role": "system", "content": instructions})
            resp = MessagingResponse()
            resp.message(response)
        case _:
            if int(request.form.get('NumMedia', 0)) > 0:
                media_url = request.form['MediaUrl0']
                user_media = requests.get(media_url, auth=(twilio_sid, twilio_token))
                with open("C:\\Temp\\temp_audio.ogg", 'wb') as f:
                    f.write(user_media.content)
                transcript = openAIclient.audio.transcriptions.create(
                    model="whisper-1",
                    file=open("C:\\Temp\\temp_audio.ogg", "rb"),
                    language="he")
                incoming_msg = transcript.text
            chat_history.append({"role": "user", "content": incoming_msg})
            stream = openAIclient.chat.completions.create(model="gpt-4o-2024-05-13", messages=chat_history)
            response = stream.choices[0].message.content
            chat_history.append({"role": "assistant", "content": response})
            resp = MessagingResponse()
            resp.message(response)
    return str(resp)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
