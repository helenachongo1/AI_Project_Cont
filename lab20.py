import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
import IPython.display as ipd

# Load audio file
audio, sample_rate = sf.read("C:/Users/Acer/Downloads/senya.wav")
audio_1, sample_rate_1 = sf.read("C:/Users/Acer/Downloads/Audio_2_Audio Denoise.wav")
#Similarly, we can use the same library to write an audio file as follows:
#import soundfile as sf

# Write audio file
sf.write('new_audio_file.wav', audio, sample_rate)
sf.write('new_audio_file.wav', audio_1, sample_rate_1)

time = np.arange(0, len(audio))/sample_rate
time_1 = np.arange(0,len(audio_1) )/sample_rate_1

linear_conv = np.convolve(time, time_1)
print("Linear convolution:",linear_conv)

'''plt.plot(time,audio)
plt.xlabel('Time(s')
plt.ylabel('Amplitude')
ipd.Audio("C:/Users/Acer/Downloads/senya.wav")

#Example 2

audio= AudioSegment.from_file("C:/Users/Acer/Downloads/senya.wav")
audio_fade_in = audio.fade_in(2000)

audio_fade_in.export('audio_file_fade_in.wav',format='wav')

plt.show()'''