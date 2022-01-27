from re import S
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
import wolframalpha
import json
import requests
import urllib.request
import re
from googletrans import Translator

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice','voices[0].id')
wikipedia.set_lang("pl")
translator = Translator()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    timestamp = time.strftime('%H:%M:%S')
    hour = int(timestamp.split(':')[0])
    if hour>=0 and hour<18:
        if (hour % 2 == 0):
            speak("Dzień dobry")
        else:
            speak("Witaj")
    else:
        speak("Dobry wieczór")

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Słucham...")
        audio=r.listen(source)
        try:
            statement=r.recognize_google(audio,language='pl-PL')
            print(f"user said:{statement}\n")
        except Exception as e:
            speak("Przepraszam, proszę powtórz jeszcze raz")
        return statement


closeStatements = ['żegnaj', 'ok pa', 'stop', 'zamknij', 'wyjdź']
wikiStatements = ['wikipedia', 'otwórz wikipedię', 'przeszukaj wikipedię', 'znajdź w wikipedii']
youtubeSearchStatements = ['wyszukaj w youtube', 'przeszukaj youtube', 'szukaj w youtube']
youtubeFirstSearchStatement = ['youtube znajdź', 'znajdź w youtube']
googleStatements = ['google', 'otwórz google']
mailStatements = ['otwórz gmail', 'otwórz pocztę', 'poczta email', 'email']
weatherStatements = ['pogoda', 'jaka jest pogoda', 'powiedz mi jaka jest pogoda']
timeStatements = ['czas', 'jaka jest godzina', 'jaka jest teraz godzina', 'jaką mamy godzinę', 'która teraz jest godzina', 'obecna godzina']
whoStatements = ['kim jesteś', 'co potrafisz', 'co umiesz', 'przedstaw się', 'powiedz coś o sobie']
buildStatements = ['kto cię stworzył', 'kto cię zbudował', 'kto cię wynalazł']
stackStatements = ['otwórz stack overflow', 'otwórz stackoverflow', 'stackoverflow', 'stack overflow']
newsStatements = ['news', 'newsy', 'informacje', 'wiadomości']
searchStatements = ['wyszukaj', 'znajdź']
logoutStatements = ['wyloguj']


def greet():
    speak("Ładowanie twojego personalnego asystenta głosowego")
    print('Ładowanie twojego personalnego asystenta głosowego')
    wishMe()

def voice_assistant():
    speak("Jak mogę Ci pomóc?")
    statement = takeCommand().lower()
    if statement==0:
        return

    if any(text in statement for text in closeStatements):
        speak('Do usłyszenia!')
        print('Do usłyszenia!')
        return

    elif text := next((text for text in wikiStatements if text in statement), None):
        try:
            speak('Przeszukuję Wikipedię...')
            statement = statement.replace(text, "")
            results = wikipedia.summary(statement, sentences=3)
            if (len(results) < 90):
                results = wikipedia.summary(statement, sentences=4)
            speak("Według wikipedii")
            print(results)
            speak(results)
        except Exception as e:
            speak("Nie znaleziono wyniku")

    elif statement == 'otwórz youtube' or statement == 'youtube':
        webbrowser.open_new_tab("https://www.youtube.com")
        speak("Otworzono youtube")

    elif text := next((text for text in youtubeSearchStatements if text in statement), None):
        statement = statement.replace(text, "").strip()
        if (len(statement) != 0):
            webbrowser.open_new_tab(f"https://www.youtube.com/results?search_query={statement}")
            speak(f"Wyniki dla: {statement}")

    elif text := next((text for text in youtubeFirstSearchStatement if text in statement), None):
        statement = statement.replace(text, "").strip().replace(' ', '+')
        if (len(statement) != 0):
            html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={statement}")
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            webbrowser.open_new_tab(f"https://www.youtube.com/watch?v={video_ids[0]}")
            speak(f"Youtube, otworzono: {statement}")

    elif any(text in statement for text in googleStatements):
        webbrowser.open_new_tab("https://www.google.com")
        speak("Otwieram stronę google.com")
        time.sleep(3)

    elif any(text in statement for text in mailStatements):
        webbrowser.open_new_tab("gmail.com")
        speak("Otworzono gmail")
        time.sleep(3)

    elif any(text in statement for text in weatherStatements):
        api_key="8ef61edcf1c576d65d836254e11ea420"
        base_url="https://api.openweathermap.org/data/2.5/weather?"
        speak("W jakim mieście?")
        city_name=takeCommand()
        complete_url=base_url+"appid="+api_key+"&q="+city_name
        response = requests.get(complete_url)
        x=response.json()
        if x["cod"]!="404":
            y=x["main"]
            current_temperature = y["temp"]
            current_humidiy = y["humidity"]
            z = x["weather"]
            description_translated = None
            # if z[0]["description"] is not None:
            #     print(z[0]["description"])
            #     description_translated = translator.translate(z[0]["description"], src='en', dest='pl')
            speak(f'Temperatura wynosi: {int(current_temperature - 273.15)}')
            speak(f'Procentowa wilgotność wynosi: {current_humidiy}')
            speak(f'Opis: {z[0]["description"]}')
            # if description_translated is not None:
            #     speak(f'Opis: {description_translated}')

        else:
            speak(" Nie znaleziono miasta")

    elif any(text in statement for text in timeStatements):
        strTime=datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Obecna godzina: {strTime}")

    elif any(text in statement for text in whoStatements):
        speak('Jestem asystentem głosowym, potrafiącym wykonywać takie czynności jak'
                'otworzyć youtube, google, gmail czy stack overflow, zwracać czas, przeszukiwać wikipedię i zwracać aktualną pogodę w danym mieście' 
                'zwracam newsy z kraju oraz radzę sobie z obliczeniami i pytaniami geograficznymi')

    elif any(text in statement for text in buildStatements):
        speak("Zostałam zbudowana przez Huberta, Marcina i Mateusza")

    elif any(text in statement for text in stackStatements):
        webbrowser.open_new_tab("https://stackoverflow.com")
        speak("Otworzono stack overflow")

    elif any(text in statement for text in newsStatements):
        news = webbrowser.open_new_tab("https://news.google.com/topstories?hl=pl&gl=PL&ceid=PL:pl")
        speak('Oto kilka newsów zaproponowanych przez Google. Miłego czytania')
        time.sleep(3)

    elif text := next((text for text in searchStatements if text in statement), None):
        statement = statement.replace(text, "").strip().replace(" ","%20")
        webbrowser.open_new(f"http://google.com/search?q={statement}")

    elif 'zapytaj' in statement:
        speak('Potrafię odpowiedzieć na pytania obliczeniowe i geograficzne. Co chcesz wiedzieć?')
        question=takeCommand()
        app_id="R2K75H-7ELALHR35X"
        client = wolframalpha.Client('R2K75H-7ELALHR35X')
        res = client.query(question)
        answer = next(res.results).text
        speak(answer)
        print(answer)

    elif any(text in statement for text in logoutStatements):
        speak("Ok, twój komputer wyłączy się za 10 sekund, upewnij się, że zamknąłeś i zapisałeś stan we wszystkich aplikacjach")
        subprocess.call(["shutdown", "/l"])

    else:
        speak("Nie rozumiem polecenia")