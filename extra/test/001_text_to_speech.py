from time import sleep
import gtts
import os

while True:
    texto = input("Introduzca un texto: ")
    if(texto == "salir"):
        break
    tts = gtts.gTTS(texto, lang='es')
    filename = 'temp.mp3'
    tts.save(filename)
    os.system('mpg321 temp.mp3')
    os.remove(filename)