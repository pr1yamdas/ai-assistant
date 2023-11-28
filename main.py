import random
import speech_recognition as sr
import win32com.client
import webbrowser
import sys
import subprocess
import datetime
import openai
from config import apikey
import requests
from config import newsapi
import pywhatkit
import re
import pyautogui
import time
import pyttsx3


openai.api_key = apikey
chatStr=""
current_voice= 0




engine = pyttsx3.init()

def change_voice():
    voices = engine.getProperty('voices')
    current_voice = engine.getProperty('voice')

    # Find the index of the current voice
    current_index = next((i for i, v in enumerate(voices) if v.id == current_voice), None)

    if current_index is not None:
        # Increment the index to switch to the next voice
        current_index = (current_index + 1) % len(voices)

        # Set the new voice
        engine.setProperty('voice', voices[current_index].id)


def play_spotify_track(track_name):
    # Open the web browser and go to the Spotify website
    webbrowser.open("https://open.spotify.com/search/")

    # Give some time for the website to load
    time.sleep(8)

    # Use pyautogui to click on the search bar
    pyautogui.click(x=700, y=100)  # Replace with the actual coordinates of the search bar

    # Type the track name in the search bar
    pyautogui.write(track_name)

    # Press Enter to initiate the search
    pyautogui.press('enter')

    time.sleep(4)

    # Click on the first search result (adjust coordinates as needed)
    pyautogui.moveTo(x=811, y=439)

    pyautogui.click()

def play_video_on_youtube(video_title):
    try:
        # Use pywhatkit to search and play the video on YouTube
        pywhatkit.playonyt(video_title)
        say(f"Playing {video_title} on YouTube ")

    except Exception as e:
        print(f"Error playing video: {e}")

def extract_video_title(query):
    # Use a simple regex to extract text after "play"
    match = re.search(r'\bvideo of\b (.+)', query)
    if match:
        return match.group(1)
    else:
        return None


import requests

def get_news(newsapi):
    news_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": newsapi,
        "country": "in",  # Change the country code as needed
    }

    try:
        response = requests.get(news_url, params=params)
        news_data = response.json()

        # Extract and display news headlines with links
        for article in news_data.get("articles", []):
            title = article.get("title", "")
            url = article.get("url", "")
            print(f"- {title}: {url}")

        if not news_data.get("articles"):
            print("No news available.")

    except Exception as e:
        print(f"Error fetching news: {e}")

# Assuming you have the 'newsapi' variable defined with your API key



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
    engine.say(text)
    engine.runAndWait()



# ... (existing code)

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.8
        try:
            audio = r.listen(source, timeout=10)
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")



            return query.lower()

        except sr.WaitTimeoutError:
            print("Listening timed out. Please repeat your command.")
            return ""


        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return "error"

# ... (existing code)


say("Good morning")
while True:
    print("Listening..")
    query = take_command()


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
    if "news" in query:
        #news_headlines = get_news(newsapi)
        get_news(newsapi)
        #say(news_headlines)
        '''if news_headlines:
            for headline in news_headlines:
                say(headline)

        else:
            say("No news available.")'''

    elif "stop" in query:
            say("Quitting")
            sys.exit()
    elif "town" in query:
            file_path = r'C:\Users\priya\Downloads\Lil Nas X - Old Town Road (Official Video) ft. Billy Ray Cyrus_r7qovpFAGrQ.mp3'
            subprocess.Popen([file_path], shell=True)
            say("Opening Old Town Road")
    elif "time" in query and "now" in query:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"The time is {current_time}")

    elif any(site in query for site in sites):
            matching_sites = [site for site in sites if site in query]
            say(f"Opening {matching_sites[0]}..")
            webbrowser.open(sites[matching_sites[0]])
    elif any(app in query for app in apps):
            matching_apps = [app for app in apps if app in query]
            say(f"Opening {matching_apps[0]}..")
            subprocess.Popen([apps[matching_apps[0]]], shell=True)
    elif "play" in query and "video" in query:
            video_title = extract_video_title(query)
            if video_title:
                    play_video_on_youtube(video_title)
            else:
                    say("Please specify a video title after 'play'")
    elif "play" in query and "song" in query:
            track_name = query.split("song", 1)[1].strip()
            play_spotify_track(track_name)
    elif "change voice" in query:
        change_voice()
        say("Voice changed.")
    else:
        chat(query)
