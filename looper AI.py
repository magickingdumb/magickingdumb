import openai
import pyttsx3
import speech_recognition as sr
import time

#set api key
openai.api_key = "OPENAI_API_KEY"

#Iniialize speech engine
engine = pyttsx3.init()

def transcribe_audio_to_text():
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename):
        audio = recognition.record(source)
        try:
            return recongnizer.recognize_google(audio)
        except:
            return("Error")

def generate_reponse(prompt):
    response = openai.Completion.create(
        engine="text-divinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        #wait for user to say "looper"
        print("Say 'looper' to start recording your question.../n")
        with sr.Recognizer():
            audio = recongnizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio)
            if transcription.lower() == "looper":
                #record audio
                filename = "input.wav"
                with sr.Microphone() as source:
                    recognizer = sr.Recognizer()
                    source.pause_threshold = 1
                    audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                    with open(filename, "wb") as f:
                        f.write(audio.get_wav_data())
            
                #transcribe audio to text
                text = transcribe_audio_to_text(filename)
                if text:
                    print(f"You said: {text}")

                    #generate response
                    response = generate_response(text)
                    print(f"Response: {response}")

                    #Read response using text-to-speech
                    speak_text(response)
        except Exception as e:
                print("An error occured: {}".format(e))

if __name__ == "__main__":
    main()