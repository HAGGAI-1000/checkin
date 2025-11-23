import os
from twilio.rest import Client
from openai import OpenAI
from flask import Flask

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
# Notice emotion list must match twilio predefined options
emotion_selection = ["I'm really okay", "Great", "Don't know", "Sad", "Edgy", "Scared", "Helpless", "Angry"]
port = int(os.environ.get("PORT", 10000))
voiceAuth = (twilio_sid, twilio_token)
demoSid = 'HXbcdb929723b9e8f0c0e5f1d3ebdd7460'
def forwardSid(gender):
    if gender == 'male':
        return 'HX61bf0f509d4168b68dcd38fc2c10fb93'
    else:
        return 'HXb563ed8bc142dbceec74fc23b6bf90e9'