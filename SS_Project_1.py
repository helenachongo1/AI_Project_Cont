import speech_recognition as sr
from googletrans import Translator
from langdetect import detect
import pyttsx3
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock


#To recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Listening for speech...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            print("Recognizing speech...")
            detected_text = recognizer.recognize_google(audio)
            return detected_text
        except sr.UnknownValueError:
            print("Speech was unclear.")
        except sr.RequestError:
            print("Service is unavailable. Please try again.")
        return None

#To detect language
def detect_language(text):
    try:
        return detect(text)
    except Exception as e:
        print(f"Language detection error: {e}")
        return None

#To translate text
def translate_text(text, src_lang, target_lang):
    translator = Translator()
    print(f"Translating text from {src_lang} to {target_lang}...")
    try:
        translation = translator.translate(text, src=src_lang, dest=target_lang)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return None

#To synthesize speech
def synthesize_speech(text, language_code):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)

    voices = engine.getProperty('voices')
    voice = None
    for v in voices:
        if language_code in v.languages:
            voice = v
            break
    if voice:
        engine.setProperty('voice', voice.id)
    else:
        print("Language code not found, using default voice.")

    print("Speaking translated text...")
    engine.say(text)
    engine.runAndWait()


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.mic_label = Label(text='Press button to start recording...')
        layout.add_widget(self.mic_label)

        self.record_button = Button(text="Start Recording")
        self.record_button.bind(on_press=self.toggle_recording)
        layout.add_widget(self.record_button)

        self.is_recording = False
        return layout

    def toggle_recording(self, instance):
        """Toggle between start/stop recording."""
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

        # Toggle the button text based on recording state
        self.is_recording = not self.is_recording
        self.record_button.text = "Stop Recording" if self.is_recording else "Start Recording"

    def start_recording(self):
        """Start the recording and process the speech-to-text."""
        self.mic_label.text = "Recording started..."
        Clock.schedule_once(self.record_speech, 0.5)  # Small delay to allow recording to start

    def stop_recording(self):
        """Stop the recording."""
        self.mic_label.text = "Recording stopped."

    def record_speech(self, dt):
        """Capture and process speech to text."""
        spoken_text = recognize_speech()
        if spoken_text:
            self.mic_label.text = "Processing..."
            detected_lang = detect_language(spoken_text)
            print(f"Detected language: {detected_lang}")
            if detected_lang:
                text_in_english = translate_text(spoken_text, detected_lang, 'pt')
                if text_in_english:
                    print(f"Translated to English: {text_in_english}")
                    target_lang = 'pt'
                      # We can change this to any target language code
                    final_translation = translate_text(text_in_english, 'fr', target_lang)

                    if final_translation:
                        print(f"Final Translation ({target_lang}): {final_translation}")
                        synthesize_speech(final_translation, target_lang)
                        self.mic_label.text = "Text translated and spoken!"
                    else:
                        self.mic_label.text = "Error in final translation."
                else:
                    self.mic_label.text = "Error in translation to English."
            else:
                self.mic_label.text = "Error in language detection."
        else:
            self.mic_label.text = "Sorry, I couldn't understand that."


if __name__ == "__main__":
    MyApp().run()


