import speech_recognition as sr
import numpy as np
from scipy.signal import butter, lfilter
from scipy.io.wavfile import write
import io
from googletrans import Translator
from langdetect import detect
import pyttsx3
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock


# Bandpass filter
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order)
    return lfilter(b, a, data)

# To recognize speech 
def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Listening for speech...")

    # Adjust for ambient noise before recording
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  
        try:
            audio = recognizer.listen(source)
            print("Recognizing speech...")

            # Convert the audio to a numpy array and apply the bandpass filter
            raw_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)

            # If stereo , convert to mono by averaging
            if len(raw_data) % 2 == 0:
                raw_data = raw_data[::2]  # Reduce to mono by keeping every second sample (if stereo)

            fs = 16000  # Sample rate for audio

            # Apply the bandpass filter (300 Hz to 3400 Hz is typical for speech)
            filtered_audio = bandpass_filter(raw_data, 300, 3400, fs)

            # Save filtered audio to a byte buffer to pass to the recognizer
            byte_io = io.BytesIO()
            write(byte_io, fs, filtered_audio.astype(np.int16))  # Writing back as 16-bit PCM format
            byte_io.seek(0)

            # Recognize the filtered speech
            audio = sr.AudioData(byte_io.read(), fs, 2)  # 2 is the number of bytes per sample (16-bit PCM)
            detected_text = recognizer.recognize_google(audio)

            return detected_text
        except sr.UnknownValueError:
            print("Speech was unclear.")
        except sr.RequestError:
            print("Service is unavailable. Please try again.")
        return None


# To detect language
def detect_language(text):
    try:
        return detect(text)
    except Exception as e:
        print(f"Language detection error: {e}")
        return None

# To translate text
def translate_text(text, src_lang, target_lang):
    translator = Translator()
    print(f"Translating text from {src_lang} to {target_lang}...")
    try:
        translation = translator.translate(text, src=src_lang, dest=target_lang)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return None

# To synthesize speech
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
        Clock.schedule_once(self.record_speech, 0.5)  #Delay to allow recording to start

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
                text_in_english = translate_text(spoken_text, detected_lang, 'en')
                if text_in_english:
                    print(f"Translated to English: {text_in_english}")
                    target_lang = 'pt'  
                    final_translation = translate_text(text_in_english, 'en', target_lang)

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
