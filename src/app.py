import speech_recognition as sr
import pyttsx3
import requests
import os
from flask import Flask, render_template


app = Flask(__name__, static_folder='static')

recog = sr.Recognizer()
last_news = False

def SpeakText(comand):
    out = pyttsx3.init()
    out.setProperty('voice', 'pt-br')
    if(comand != "desligar"):
        out.say(comand)
    else:
        out.say("Ok! Estou desligando...")
    out.runAndWait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/news', methods=['POST'])
def news():
    global last_news
    try:
        with sr.Microphone() as mic:
            recog.adjust_for_ambient_noise(mic)
            print("IA: ouvindo...")
            audio = recog.listen(mic)
            text = recog.recognize_google(audio, language='pt-BR')
            text = text.lower()
            print("IA: Você disse " + text + "")
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": text,
                "sortBy": "publishedAt",
                "pageSize": 10,
                "apiKey": "40ea1ab64d014d479780b1d50b14ee15"
            }
            response = requests.get(url, params=params)
            data = response.json()
            articles = data["articles"]
            for article in articles[:5]:
                title = article["title"]
                print("IA: Título da notícia: " + title)
                if not last_news:
                    SpeakText('Notícias de ultima hora')
                    last_news = True
                SpeakText(title)
            if last_news:
                SpeakText('Aqui estão as outras notícias')
            return render_template('news.html', articles=articles)
    except sr.RequestError as e:
        print("Não foi possível requisitar o pedido; {0}".format(e))
    except sr.UnknownValueError:
        print("Um erro desconhecido ocorreu")

if __name__ == '__main__':
    port = int(os.getenv('PORT'), '5000')
    app.run(host='0.0.0.0', port = port)
