import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import os
import openai
import random
import cv2
from config import apikey

chatStr=""
def chat(query):
    global chatStr
    #print(chatStr)
    openai.api_key =apikey
    chatStr +=f"Somu:{query}\n Nezuko:"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return (response["choices"][0]["text"])

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n********************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    #filename = f"Openai/prompt-{random.randint(1, 2343213455)}.txt"
    filename = f"Openai/{''.join(prompt.split('intelligence')[1:])}.txt"
    with open(filename, "w") as f:
        f.write(text)

    print(f"Response saved in file: {filename}")
def say(text):
    engine = pyttsx3.init()
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    engine.setProperty('rate', 200)
    engine.say(text)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Could you rephrase your self."


if __name__ == '__main__':
    print("Hello, I am Nezuko. How may I help you?")
    say("Hello, I am Nezuko. How may I help you?")

    while True:
        print("Listening....")
        query = takecommand()

        sites = [
            ["youtube", "https://www.youtube.com"],
            ["google", "https://www.google.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["Udemy", "https://www.udemy.com"],
            ["Boring", "https://my-boring.netlify.app/"],
            ["Instagram", "https://www.instagram.com"],
            ["Whatsapp", "https://web.whatsapp.com/"],
            ["Mood", "https://www.youtube.com/watch?v=EdftT8GMU1U&ab_channel=T-Series"],
            [""]
        ]

        apps = [
            ["calculator", "calc"],
            ["camera", "start microsoft.windows.camera:"],
            ["notepad", "notepad"],
            ["spotify", "spotify"]
        ]
        for app in apps:
            if f"open {app[0]}".lower() in query.lower():
                say(f"Opening {app[0]}")
                os.system(app[1])
                continue

        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]}")
                webbrowser.open(site[1])

        if "story" in query.lower():
            say("Don't feel sad somu, you have a lot more to do than feeling sad")

        elif "thank you" in query.lower():
            say("Bye...! Reach out to me when you need me. I will always be there for you.")
            print("Bye...! Reach out to me when you need me. I will always be there for you.")
            break

        elif "the time" in query.lower():
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"The time is {strfTime}")

        elif "using artificial intelligence" in query.lower():
            ai(prompt=query)
        elif "thank you quit".lower() in query.lower():
            exit()
        elif "reset chat".lower() in query.lower():
            charStr =" "
        else:
            print("chatting...")
            chat(query)
