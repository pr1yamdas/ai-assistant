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
say("Good morning")
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
