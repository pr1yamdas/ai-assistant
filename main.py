import speech_recognition as sr
import win32com.client
import webbrowser

def say(text):
    speak = win32com.client.Dispatch("SAPI.SpVoice")
    speak.Speak(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"user said: {query}")
            return query
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return "error"
say("Hello i am jarvis")
while True:
    print("listening..")
    query = takeCommand()
    sites=[["youtube","https://youtube.com"] , ["wikipedia","https://wikipedia.com"],["google","https://google.com"]]
  
