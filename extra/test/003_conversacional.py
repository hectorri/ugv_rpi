import openai
import speech_recognition as sr
from ..secrets import OPENAI_API_LEY_ROVER
import sounddevice
import gtts
import os

client = client = openai.OpenAI(api_key=OPENAI_API_LEY_ROVER)

messages = [
    {'role': 'system', 'content': 'Eres un asistente infantil, responde de forma breve'}
]

def text_to_speech(text):
    tts = gtts.gTTS(text, lang='es')
    filename = 'temp.mp3'
    tts.save(filename)
    os.system('mpg321 temp.mp3')

def listen_and_respond():
    """
    Listen for audio input, recognize it and respond using OpenAI
    """
    # Create speech recognizer object
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=2)

    with mic as source: 
        r.adjust_for_ambient_noise(source)

    # Listen for input
    with mic as source:
        print("Listenning...")
        audio = r.listen(source)

    # Try to recognize the audio
    try:
        prompt = r.recognize_google(audio, language="es_ES", show_all=False)
        print("Has preguntado:", prompt)

        if prompt.lower() == 'salir':
            exit()

        messages.append({'role': 'user', 'content': prompt})

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )

        response_text = completion.choices[0].message.content
        print(f"AI: {response_text}")

        # Speak the response
        text_to_speech(response_text)
        print()

    # Catch if recognition fails
    except sr.UnknownValueError:
        response_text = "Sorry, I didn't understand what you said"
        print(response_text)
        engine.say(response_text)
        engine.runAndWait()
        print()
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def main():
    while True:
        listen_and_respond()

if __name__ == "__main__":
    main()