from flask import request
from twilio.twiml.messaging_response import MessagingResponse
import requests
from users import users
from prompts import prompt1, prompt2, notUserResp, notNowResp, promptVoice
from setup import openAIclient, twilioClient, sender, emotion_selection, chat_history, port, app, voiceAuth, demoSid, forwardSid
import voice

@app.route("/", methods=["POST"])
def whatsapp_reply():
    resp = MessagingResponse()
    incoming_msg = request.form.get('Body')
    incoming_sender = request.form.get('From')
    user = next((u for u in users if u['phone'] == incoming_sender), None)
    if not user:
        resp.message(notUserResp)
        return str(resp)
    gender = user['gender']
    name = user['name']
    match incoming_msg.lower():
        case "demo":
            twilioClient.messages.create(from_= sender, to = incoming_sender, content_sid = demoSid)
            resp = None
        case "אוקיי קדימה!":
            twilioClient.messages.create(from_= sender, to = incoming_sender, content_sid = forwardSid(gender))
            resp = None
        case "לא עכשיו":
            resp.message(notNowResp)
        case c if c in emotion_selection:
            instructions = prompt1(emotion_selection, incoming_msg, gender, name)
            chat_history.append({"role": "system", "content": instructions})
            stream = openAIclient.chat.completions.create(model="gpt-4o-2024-05-13", messages=chat_history)
            response = stream.choices[0].message.content
            chat_history.append({"role": "assistant", "content": response})
            chat_history.append({"role": "system", "content": prompt2})
            resp.message(response)
        case _:
            if int(request.form.get('NumMedia', 0)) > 0:
                media_url = request.form['MediaUrl0']
                user_media = requests.get(media_url, auth = voiceAuth)
                content_type = user_media.headers.get("Content-Type", "")
                if "ogg" in content_type.lower():
                    voice_mood, incoming_msg = voice.analyze_speech(user_media.content)
                    chat_history.append({"role": "system", "content": promptVoice(voice_mood)})
            chat_history.append({"role": "user", "content": incoming_msg})
            stream = openAIclient.chat.completions.create(model="gpt-4o-2024-05-13", messages=chat_history)
            response = stream.choices[0].message.content
            chat_history.append({"role": "assistant", "content": response})
            resp.message(response)
    return str(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
