import speech_recognition as sr
from difflib import SequenceMatcher
from tkinter import messagebox as tk
import time

def speechtest():
    sampleSentence = "this is a sample sentence"

    ratios = [-1.0, -1.0, -1.0]
    r = sr.Recognizer()
    unintcounter = 0

    for i in range (3):
        with sr.Microphone() as source:
            tk.showinfo('Information', "Please say the following Sentence after pressing 'OK': \n"+sampleSentence)
            audio = r.listen(source)
        try:
            said = r.recognize_google(audio)
            tk.showinfo('Information', "You said " + said)
            ratios[i] = SequenceMatcher(None, sampleSentence, said).ratio()

        except LookupError:
            tk.showwarning('Warning', "Could not understand audio")
            unintcounter += 1


        #tk.showinfo('Result', '"You imitated the sentence with "+str(int(ratios[i]*100))+" Accuracy.")

    average = (ratios[0] + ratios[1] + ratios[2]) / 3
    tk.showinfo('Result', "You imitated the sentence with "+str(int(average*100))+" percent accuracy.")
    tk.showinfo('Result', "You have spoken unintelligibly " +str(unintcounter)+" times")
    result = False
    exp1 = average < 0.6
    exp2 = unintcounter > 1
    if exp1 or exp2:
        result = True

    return result