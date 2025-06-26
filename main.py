from flask import Flask, request, make_response
import os
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from openai import OpenAI
import requests

#from dotenv import load_dotenv
#load_dotenv()

gender = "female"
#receiver = "whatsapp:+972507715395"
receiver = "whatsapp:+972522736713"

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
    if (incoming_msg == "אוקיי קדימה!") or (incoming_msg == "לא עכשיו") or (incoming_msg in emotion_selection):
        if incoming_msg == "אוקיי קדימה!":
            twilioClient.messages.create(from_=sender, to=receiver, content_sid='HX36ceb85a37eb8429553621d86bd26d72')
            resp = None
        if incoming_msg == "לא עכשיו":
            resp = MessagingResponse()
            resp.message("אוקיי, אני מחכה לשמוע ממך כשאת מוכנה!")
        if incoming_msg in emotion_selection:
            emotion = incoming_msg
            instructions = (f"As part of a mood and aggression monitoring app, the user was asked to choose how they feel "
                            f"from the following options: {emotion_selection}. They selected: {emotion}. The user's gender is {gender}. "
                            f"Please generate an empathetic response in Hebrew, that matches the selected emotion, "
                            f"and gently encourage the user to share more — either through text, audio, or video. "
                            f"Limit your response to 500 characters.")
            chat_history.append({"role": "system", "content": instructions})
            stream = openAIclient.chat.completions.create(model="gpt-4o-2024-05-13", messages=chat_history)
            response = stream.choices[0].message.content
            chat_history.append({"role": "assistant", "content": response})
            instructions = (f"I want you to act as a mental health adviser. Information was provided about an "
                            f"individual who is seeking support for emotions such as sadness, anger, or other mental health challenges. "
                            f"Use your knowledge of Cognitive Behavioral Therapy (CBT), mindfulness, meditation, and other "
                            f"therapeutic techniques to help the user improve their emotional well-being. Your response must be in Hebrew. "
                            f"Please do the following: Reflect back how the user is feeling based on their sentiment, in an "
                            f"empathetic and supportive tone to help them feel understood and better. Gently offer a new "
                            f"perspective and suggest one simple action they can take to improve their emotional state."
                            f"If the user's response is unrelated to their emotional state, suggest to focus on their feelings.")
            chat_history.append({"role": "system", "content": instructions})
            resp = MessagingResponse()
            resp.message(response)
    else:
        if int(request.form.get('NumMedia', 0)) > 0:
            media_url = request.form['MediaUrl0']
            user_media = requests.get(media_url, auth=(account_sid, auth_token))
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
    print(f"Message from {incoming_sender}: {incoming_msg}")
    print(chat_history)
    return str(resp)
#def webhook():
#    incoming_msg = request.form.get("Body", "")
#    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
#<Response>
#    <Message>You said: {incoming_msg}</Message>
#</Response>"""
#    response = make_response(twiml_response)
#    response.headers["Content-Type"] = "application/xml"
#    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    message = twilioClient.messages.create(from_=sender, to=receiver, content_sid='HXee8c500e794d49f8a96abf68df67da8a')
    app.run(host="0.0.0.0", port=port)
