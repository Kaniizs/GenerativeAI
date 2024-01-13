import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv
import openai

load_dotenv()
keys = os.getenv("OPENAI_API_KEY")
openai.api_key = keys

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# recognize speech
r = sr.Recognizer()

def text_recorder():
    # loop in case of error
    while True:
        try:
            with sr.Microphone() as source:
                # wait for a second to let the recognizer adjust the
                # energy threshold based on the surrounding noise level
                r.adjust_for_ambient_noise(source, duration=0.2)

                # listens for the user's input
                audio = r.listen(source)

                # Using Google to recognize audio
                my_text = r.recognize_google(audio)
                my_text = my_text.lower()

                return my_text

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")

def ai_response(text, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=text,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    texts = response['choices'][0]['message']['content']
    text.append(response['choices'][0]['message']['content'])
    return texts

text = []
while True:
    message = text_recorder()
    text.append({"role": "user", "content": message})
    response = ai_response(text)
    speak(response)
    print(response)
