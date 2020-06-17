import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import pyowm
import webbrowser
import datetime
import re
from yandex_music.client import Client
import tkinter as tk
import threading
import easygui
import locale


win = tk.Tk()
win["bg"]='gray22'
win.title("Помощник")
win.geometry("150x300")
res = tk.Label(win, text = "",background="gray22",foreground= "#ffffff",font= ("Helvetica", 10))
res.place(x=0 ,y=85)


def onclick():

# настройки
    opts = {
        "alias": ('бездарь',''),
        "tbr": ('скажи','расскажи','покажи','сколько','произнеси','открой','сделай','включи'),
        "cmds": {
            "ctime": ('текущее время','сейчас времени','который час'),
            "weather": ('погоду','какая погода сегодня','погода'),
            "browsing": ('страницу','сайт'),
            "organiser": ('органайзер','календарь'),
            "alert": ('напоминание','уведомление'),
            "music": ('музыку'),
            "video": ('видео')
        }
    }

        # функции
    def speak(what):
        res.configure(text = what)
        speak_engine.say(what)
        speak_engine.runAndWait()
        speak_engine.stop()

    def callback(recognizer, audio):
        try:
            voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
            res.configure(text="Вы сказали: " + voice)

            if voice.startswith(opts["alias"]):
                # обращение
                cmd = voice

                for x in opts['alias']:
                    cmd = cmd.replace(x, "").strip()

                for x in opts['tbr']:
                    cmd = cmd.replace(x, "").strip()

                # распознаем и выполняем команду
                cmd = recognize_cmd(cmd)
                execute_cmd(cmd['cmd'])


        except sr.UnknownValueError:
            res.configure(text = "Голос не распознан!")
        except sr.RequestError as e:
            res.configure(text ="Неизвестная ошибка, проверьте интернет!")

    def recognize_cmd(cmd):
        RC = {'cmd': '', 'percent': 0}
        for c,v in opts['cmds'].items():

            for x in v:
                vrt = fuzz.ratio(cmd, x)
                if vrt > RC['percent']:
                    RC['cmd'] = c
                    RC['percent'] = vrt

        return RC

    def execute_cmd(cmd):
        if cmd == 'ctime':
            # сказать текущее время
            locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
            now = datetime.datetime.now()
            speak("Сегодня "+str(now.day)+" "+ str(now.strftime('%B'))+" " + str(now.hour) + ":" + str(now.minute))


        elif cmd == 'weather':
            gorod = 'Оренбург'
            owm = pyowm.OWM('165f33386df06f97d19787e3d780273a')
            observation = owm.weather_at_place(gorod)
            w = observation.get_weather()
            temperature = w.get_temperature('celsius')['temp']
            speak("В городе " + gorod + " сейчас " + str(temperature) + "°С")


        elif cmd == 'browsing':
            text = r.recognize_google(audio, language='ru-RU')
            f_text = ('https://yandex.ru/search/?text=' + text())
            webbrowser.open(f_text)


        elif cmd == 'organiser':
            url = 'https://calendar.yandex.ru/'
            webbrowser.open(url)


        elif cmd == 'alert':

            if re.search(r'\минут\b', r.recognize_google(audio, language='ru-RU')):
                dur = int(''.join(filter(str.isdigit, r.recognize_google(audio, language='ru-RU'))))
                dur *= 60
                for i in range(dur, 0, -1):
                    time.sleep(1)
                easygui.msgbox(r.recognize_google(audio,language='ru-RU'));

            if re.search(r'\секунд\b', r.recognize_google(audio, language='ru-RU')):
                dur = int(''.join(filter(str.isdigit, r.recognize_google(audio, language='ru-RU'))))
                for i in range(dur, 0, -1):
                    time.sleep(1)
                easygui.msgbox(r.recognize_google(audio, language='ru-RU'));

            else:
                dur = int(''.join(filter(str.isdigit, r.recognize_google(audio, language='ru-RU'))))
                dur *= 3600
                for i in range(dur, 0, -1):
                    time.sleep(1)
                easygui.msgbox(r.recognize_google(audio, language='ru-RU'));



        elif cmd == 'music':
            mus = r.recognize_google(audio, language='ru-RU').lower()
            mus = mus.replace("включи музыку", "")
            mus = mus.replace("включи песню", "")
            mus = mus.replace("включи трек  ", "")
            client = Client.from_credentials('borzwow@yandex.com', 'roguedeal100ki11')
            client.search(mus).best.result.download('audio.mp3')
            os.system('audio.mp3')

        elif cmd =='video':
            url = r.recognize_google(audio, language= 'ru-RU').lower()
            url = url.replace("включи видео","")
            url = url.replace("открой видео", "")
            url = url.replace("поставь видео", "")
            webbrowser.open("www.youtube.com/results?search_query="+url)


        else:
            res.configure(text='Команда не распознана, повторите!')

    speak_engine = pyttsx3.init()

    speak('Скажи,чего ты хочешь')

    #Запуск программы
    r = sr.Recognizer()
    m = sr.Microphone(device_index = 1)	# active microphone index

    while True:
      with m as source:
        audio = r.listen(source)
      callback(r, audio)


def start(event):
    button.config(state='disabled')
    t1 = threading.Thread(target=onclick)
    t1.start()

def quit():
    win.destroy()


button=tk.Button (win, text = "нажми меня", command = onclick, background="#555", foreground="#ccc",pady='2',padx= '2',  font="16")
button.bind('<Button-1>', start)
button.place(x=25 ,y=2 )
btn = tk.Button(win, text = "Выйти", command = quit, background="#555", foreground="#ccc",pady='5',padx= '2',  font="16")
btn.place(x=75, y=250)

win.mainloop()
