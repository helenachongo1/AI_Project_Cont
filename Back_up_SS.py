import speech_recognition as sr
from langdetect import detect
from googletrans import Translator
from gtts import gTTS
import os
import numpy as np
import noisereduce as nr
from scipy.signal import butter, lfilter
from kivy.app import App  
from kivy.uix.button import Button
from kivy.uix.label import Label 
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

# Noise Reduction Helper Functions
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut=300.0, highcut=3400.0, fs=16000, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def enhance_audio(data, rate):
    """Apply noise reduction and bandpass filter to enhance the audio signal."""
    # Apply bandpass filter
    filtered_data = bandpass_filter(data, lowcut=300.0, highcut=3400.0, fs=rate)
    
    # Reduce noise
    reduced_noise_data = nr.reduce_noise(y=filtered_data, sr=rate)
    
    return reduced_noise_data

# Main Functions
def detect_language(text):
    """Detect the language of the given text."""
    return detect(text)

def real_time_speech_to_text():
    """Capture audio from the microphone, apply noise reduction, and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for speech...")
        
        # Adjust recognizer sensitivity to ambient noise
        recognizer.adjust_for_ambient_noise(source)
        recognizer.energy_threshold = 2000
        
        audio = recognizer.listen(source)
        
        try:
            # Get raw audio data as a NumPy array
            raw_audio = np.frombuffer(audio.get_raw_data(), np.int16)
            sample_rate = audio.sample_rate
            
            # Apply noise reduction and speech enhancement
            enhanced_audio = enhance_audio(raw_audio, sample_rate)
            
            # Convert back to a format recognizable by speech recognition
            enhanced_audio_bytes = enhanced_audio.tobytes()
            audio_data_enhanced = sr.AudioData(enhanced_audio_bytes, sample_rate, audio.sample_width)

            # Recognize speech from the enhanced audio
            text = recognizer.recognize_google(audio_data_enhanced)
            print(f"Recognized Text: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Error with API: {e}")
            return None

def translate_to_english(text, source_lang):
    """Translate the text from the source language to English."""
    translator = Translator()
    translated = translator.translate(text, src=source_lang, dest='en')
    print(f"Translated to English: {translated.text}")
    return translated.text

def translate_to_target_language(text, target_lang):
    """Translate the text from English to the target language."""
    translator = Translator()
    translated = translator.translate(text, src='en', dest=target_lang)
    print(f"Translated to {target_lang}: {translated.text}")
    return translated.text

def text_to_speech(text, language):
    """Convert the translated text to speech in the specified language."""
    tts = gTTS(text=text, lang=language)
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")  # Use os.startfile on Windows

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
        spoken_text = real_time_speech_to_text()
        if spoken_text:
            self.mic_label.text = "Processing..."
            detected_lang = detect_language(spoken_text)
            text_in_english = translate_to_english(spoken_text, detected_lang)
            translated_text = translate_to_target_language(text_in_english, 'pt')
            text_to_speech(translated_text, 'fr')
            self.mic_label.text = "Text translated and spoken!"
        else:
            self.mic_label.text = "Sorry, I couldn't understand that."

if __name__ == "__main__":
    MyApp().run()

