import speech_recognition as sr
import json
import sys

r = sr.Recognizer()

with sr.Microphone() as source:
  audio = r.listen(source)

  try:
    text = r.recognize_google(audio)
  except:
    text = "Could not recognize"


resp = {
    "Response":200,
    "text": text
}

print(json.dumps(resp))

sys.stdout.flush()
