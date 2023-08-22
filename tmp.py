import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Say something:")
    audio_data = recognizer.listen(source,timeout=60)

try:
    text = recognizer.recognize_google(audio_data)
    print("You said: " + text)
except sr.UnknownValueError:
    print("Speech Recognition could not understand audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")
