import speech_recognition as sr
from langdetect import detect
from googletrans import Translator
from gtts import gTTS
import os
import numpy as np
import noisereduce as nr
from scipy.signal import butter, lfilter

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

if __name__ == "__main__":
    #1: Capture and recognize speech
    spoken_text = real_time_speech_to_text()

    if spoken_text:
        #2: Detect the language of the spoken text
        detected_lang = detect_language(spoken_text)

        #3: Translate spoken text to English
        text_in_english = translate_to_english(spoken_text, detected_lang)

        #4: Translate English text to target language (e.g., French)
        target_language = 'fr'  # Example: French
        translated_text = translate_to_target_language(text_in_english, target_language)

        #5: Convert translated text to speech
        text_to_speech(translated_text, target_language)

