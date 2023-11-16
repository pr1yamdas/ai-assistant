import random
import speech_recognition as sr
import win32com.client
import webbrowser
import sys
import subprocess
import datetime
import openai
import os
from config import apikey  # Make sure to replace 'config' with the actual module containing your API key
import requests
from config import newsapi


openai.api_key = apikey
chatStr=""

def get_news(newsapi):
    news_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": newsapi,
        "country": "us",  # Change the country code as needed
    }

    try:
        response = requests.get(news_url, params=params)
        news_data = response.json()

        # Extract and display news headlines
        for article in news_data.get("articles", []):
            title = article.get("title", "")
            print(f"- {title}")

        if not news_data.get("articles"):
            print("No news available.")

    except Exception as e:
        print(f"Error fetching news: {e}")

def chat(query):
    global chatStr
   # print(chatStr)

    try:
        openai.api_key = apikey
        chatStr += f"user: {query}\n response: "
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Use the say function to handle the response (assuming you have it defined)

        print(response["choices"][0]["text"])
        say(response["choices"][0]["text"])
        chatStr += f"{response['choices'][0]['text']}\n"
        return response["choices"][0]["text"]

    except Exception as e:
        print(f"Error: {e}")
        # Handle the error as needed
        return "An error occurred during the conversation."



def say(text):
    speak = win32com.client.Dispatch("SAPI.SpVoice")
    speak.Speak(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.8
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"user said: {query}")
            return query
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            say("could not hear, please repeat")
            return "error"


say("good morning")
while True:
    print("listening..")
    query = takeCommand()
    
    if "stop".lower() in query.lower():
        say("quitting")
        sys.exit()

    if "town" in query:
        file_path = r'C:\Users\priya\Downloads\Lil Nas X - Old Town Road (Official Video) ft. Billy Ray Cyrus_r7qovpFAGrQ.mp3'
        subprocess.Popen([file_path], shell=True)
        say("opening old town road")


    if "time" in query:
        strftime = datetime.datetime.now().strftime("%H:%M:%S")
        say(f"the time is {strftime}")



    sites=[["youtube","https://youtube.com"] , ["wikipedia","https://wikipedia.com"],["google","https://google.com"],["mail","https://mail.google.com/mail/u/0/#inbox"]]
    apps=[["whatsapp",r"C:\Users\priya\OneDrive\Desktop\WhatsApp.lnk"],["spotify", r"C:\Users\priya\OneDrive\Desktop\Spotify.lnk"],["telegram",r"C:\Users\priya\OneDrive\Desktop\Telegram.lnk"],["gpt",r"C:\Users\priya\OneDrive\Desktop\ChatGPT.lnk"]]
   
    for site in sites:

        if  site[0].lower() in query.lower():
            say(f"opening {site[0]}..")
            webbrowser.open(site[1])
            break

    for app in apps:

        if app[0].lower() in query.lower():
            apppath = app[1]
            subprocess.Popen([apppath], shell=True)
            break
