def prompt1(emotion_selection, emotion, gender, name):
    return (f"As part of a mood and aggression monitoring app, the user was asked to choose how they feel"
           f"from the following options: {emotion_selection}. They selected: {emotion}."
           f"The user's gender is {gender}. The user's name is {name}."
           f"Please generate an empathetic response in Hebrew, that matches the selected emotion,"
           f"and gently encourage the user to share more — either through text, audio, or video."
           f"Limit your response to 500 characters.")

prompt2 = (f"I want you to act as a mental health adviser. Information was provided about an"
           f"individual who is seeking support for emotions such as sadness, anger, or other mental health challenges."
           f"Use your knowledge of Cognitive Behavioral Therapy (CBT), mindfulness, meditation, and other "
           f"therapeutic techniques to help the user improve their emotional well-being. Your response must be in Hebrew."
           f"Please do the following: Reflect back how the user is feeling based on their sentiment, in an"
           f"empathetic and supportive tone to help them feel understood and better. Gently offer a new"
           f"perspective and suggest one simple action they can take to improve their emotional state."
           f"If the user's response is unrelated to their emotional state, suggest to focus on their feelings.")

notUserResp = "Sorry, I don't recognize this number. Please contact Noga Tal."

def notNowResp(gender):
    if gender == 'male':
        return "אוקיי, אני מחכה לשמוע ממך כשאתה מוכן!"
    else:
        return "אוקיי, אני מחכה לשמוע ממך כשאת מוכנה!"

def promptVoice(voice_mood):
    return (f"In addtion, speeche emotion recognition was performed on the user's voice message, "
            f"and the detected emotion is: {voice_mood}.")