import speech_recognition as sr
from deep_translator import GoogleTranslator
from google.transliteration import transliterate_text
import pyttsx3
import logging

class AudioProcessor:
    def __init__(self, input_lang='auto', output_lang='en', transliteration_scheme=None):
        self.input_lang = input_lang
        self.output_lang = output_lang
        self.transliteration_scheme = transliteration_scheme
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        
        # Set up logging
        logging.basicConfig(filename='audio_processor.log', level=logging.ERROR)

    def capture_from_microphone(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
            return self.process_audio(audio)

    def process_audio_file(self, file_path):
        with sr.AudioFile(file_path) as source:
            audio = self.recognizer.record(source)
            return self.process_audio(audio)

    def process_audio(self, audio):
        try:
            # Recognize speech using Google's speech recognition
            recognized_text = self.recognizer.recognize_google(audio, language=self.input_lang)
            print(f"Recognized (original): {recognized_text}")

            # Translate to the desired output language
            translated_text = self.translate_text(recognized_text)

            # Transliterate if needed
            if self.transliteration_scheme:
                transliterated_text = transliterate_text(translated_text, self.transliteration_scheme)
                print(f"Transliterated: {transliterated_text}")
                return transliterated_text

            # Convert text to speech
            self.text_to_speech(translated_text)

            return translated_text

        except sr.UnknownValueError:
            logging.error("Could not understand the audio.")
            return "Could not understand the audio."
        except sr.RequestError as e:
            logging.error(f"Failed to request results; {e}")
            return "Failed to request results."

    def translate_text(self, text):
        try:
            translated_text = GoogleTranslator(source=self.input_lang, target=self.output_lang).translate(text=text)
            print(f"Translated: {translated_text}")
            return translated_text
        except Exception as e:
            logging.error(f"Translation error: {e}")
            return "Translation failed."

    def text_to_speech(self, text):
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            logging.error(f"TTS error: {e}")
            print("Failed to convert text to speech.")

# Example usage:
# processor = AudioProcessor(input_lang='auto', output_lang='en', transliteration_scheme='Latin')
# processor.capture_from_microphone()

# To process an audio file instead of using the microphone:
# processor.process_audio_file('path_to_audio_file.wav')
