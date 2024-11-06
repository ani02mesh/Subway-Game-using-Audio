# here we are creating our own audio data , so for every word in ['left','right','up','down','start'], the below code record 0.8sec audio of us saying that respective word for N times.
# press ctrl+C to stop recording audio of that specific word. 
# Update File path for every word.

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import time
import os

def play_beep(frequency=440, duration=0.5, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # Generate a sine wave (smooth tone)
    waveform = 0.5 * np.sin(2 * np.pi * frequency * t)
    # Apply a fade-in and fade-out envelope
    fade_in = np.linspace(0, 1, int(sample_rate * duration / 10))
    fade_out = np.linspace(1, 0, int(sample_rate * duration / 10))
    envelope = np.concatenate([fade_in, np.ones(int(sample_rate * duration) - 2 * len(fade_in)), fade_out])
    waveform *= envelope
    # Play the waveform
    sd.play(waveform, samplerate=sample_rate)
    sd.wait()


# Parameters
sample_rate = 44100  # Hz
duration = 0.8  # seconds
output_dir = 'File Path to store audio'               # PATH + ['left','right','up','down','start']
count = 1

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def record_audio(filename):
    print(f"Recording to {filename}...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    write(filename, sample_rate, audio_data)
    print("Saved")

try:
    while True:
        # timestamp = int(time.time())
        filename = os.path.join(output_dir, f'down{count}.wav')
        play_beep(frequency=440, duration=0.3)
        record_audio(filename)
        count = count + 1
        time.sleep(1)  # Wait 1 second before starting the next recording

except KeyboardInterrupt:
    print("Recording stopped by user.")
