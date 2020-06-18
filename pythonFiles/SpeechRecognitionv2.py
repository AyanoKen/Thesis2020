import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
  print("Speak now: ")
  audio = r.listen(source)

  try:
    text = r.recognize_google(audio)
  except:
    text = "Could not recognize"

print(text)