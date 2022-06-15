import json 
import pyttsx3
import speech_recognition as sr
import pyjokes
import wikipedia
import pywhatkit
import datetime
import requests 
import pyaudio
from datetime import date
import plyer
import ctypes

engine = pyttsx3.init()
engine.setProperty('rate', 150)

def talk(text):
    engine.say(text)
    engine.runAndWait()
    return

def okno(ime, besedilo):
    return ctypes.windll.user32.MessageBoxW(
        0, 
        besedilo, 
        ime, 
        0, 
        0x00001000)
    
def getCommand(tekst):
    if tekst != None:
        tekst = tekst.lower()
        datum = str(date.today())
        if 'alex' in tekst:
            tekst = tekst.replace('alex', '')
            if 'play' in tekst:
                tekst = tekst.replace('play', '')
                talk('playing' + tekst)
                pywhatkit.playonyt(tekst)
            elif 'date' in tekst:
                talk('current date is ' + str(datum.replace('-', ' ')))
            elif 'who is' in tekst:
                tekst = tekst.replace('who is', '')
                talk('searching wikipedia for' + tekst)
                talk(wikipedia.summary(tekst))
            elif 'who was' in tekst:
                tekst = tekst.replace('who was', '')
                talk('searching wikipedia for' + tekst)
                talk(wikipedia.summary(tekst))
            elif 'menu' in tekst:
                tekst = tekst.replace('menu', '')
                m = requests.get('https://api.gimvicurnik.filips.si/menus/date/' + datum)
                meni = m.json()
                if 'lunch' in tekst:
                    okno('Današnji jedilnik', str('Danes bo za kosilo: \n' + ' \n' + (meni['lunch']['normal'])))
                elif 'snack' in tekst:
                    okno('Današnji jedilnik', str('Danes bo za malico: \n' + ' \n' +(meni['snack']['normal'])))
                else:
                    okno('Današnji jedilnik', str('Danes je na jedilniku: \n' + ' \n' + 'Malica: \n' + (meni['snack']['normal']) + '\n \n' + 'Kosilo: \n' + (meni['lunch']['normal'])))
            elif 'substitutions' in tekst:
                m = requests.get('https://api.gimvicurnik.filips.si/substitutions/date/' + datum + '/teachers/Bajec')
                m = m.json()
                if len(m) == 0:
                    talk('you have no substitutions today. Have a nice day')
                else:
                    nad = ''
                    for nadomescanje in m:
                        nad = str(nad) + str('Lesson: ' + str(nadomescanje['time']) + '., Class: ' + str(nadomescanje['class']) + ', Classroom: ' + str(nadomescanje['classroom']) + ' ') + '\n'
                    okno('Nadomeščanja danes', str(nad))
        return
    else:
        return

def glas():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Spregovorite")
        audio = r.listen(source)
    try:
        return(r.recognize_google(audio))
    except sr.UnknownValueError:
        print('napaka 1')
    except sr.RequestError as e:
        print('napaka 2')
    return    

def alex():
    ukaz = glas()
    getCommand(ukaz)

while True:
    alex()
