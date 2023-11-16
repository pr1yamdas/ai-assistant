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
    try:
        speak = win32com.client.Dispatch("SAPI.SpVoice")
        speak.Speak(text)
    except Exception as e:
        print(f"Error in saying: {e}")

def ai(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        gpt_response = response["choices"][0]["text"]
        print(gpt_response)
        say(gpt_response)

    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        say("Error in OpenAI API call. Please try again.")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.8
        try:
            audio = r.listen(source, timeout=5)  # Set a timeout of 5 seconds for waiting user input
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return "error"

say("Good morning")
while True:
    print("Listening..")
    query = input()

    if "news" in query:
        get_news(newsapi)

    if "stop" in query:
        say("Quitting")
        sys.exit()

    if "town" in query:
        file_path = r'C:\Users\priya\Downloads\Lil Nas X - Old Town Road (Official Video) ft. Billy Ray Cyrus_r7qovpFAGrQ.mp3'
        subprocess.Popen([file_path], shell=True)
        say("Opening Old Town Road")

    if "time" in query:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        say(f"The time is {current_time}")

    if "gpt" in query:
        ai(prompt=query)

    sites = {"youtube": "https://youtube.com", "wikipedia": "https://wikipedia.com", "google": "https://google.com", "mail": "https://mail.google.com/mail/u/0/#inbox"}
    for site, url in sites.items():
        if site in query:
            say(f"Opening {site}..")
            webbrowser.open(url)
            break

    apps = {"whatsapp": r"C:\Users\priya\OneDrive\Desktop\WhatsApp.lnk", "spotify": r"C:\Users\priya\OneDrive\Desktop\Spotify.lnk", "telegram": r"C:\Users\priya\OneDrive\Desktop\Telegram.lnk", "chat": r"C:\Users\priya\OneDrive\Desktop\ChatGPT.lnk"}
    for app, app_path in apps.items():
        if app in query:
            say(f"Opening {app}..")
            subprocess.Popen([app_path], shell=True)
            break
    else :
        chat(query)
