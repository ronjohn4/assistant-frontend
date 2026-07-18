import pyttsx3


def speak(text):
    # print(f"Saying: {text}")
    engine = pyttsx3.init('speechd')
    engine.say(text)
    engine.runAndWait()
    del engine


def speak_dummy(text):
    # print(f"Saying: {text}")
    engine = pyttsx3.init('dummy')
    engine.say(text)
    engine.runAndWait()
    del engine


def dummy_espeak(text):
    # print(f"Saying: {text}")
    engine = pyttsx3.init(driverName='espeak')
    engine.say(text)
    engine.runAndWait()
    del engine

# speak("Text to speech module initialized.")
# speak("Ready to receive text.")
