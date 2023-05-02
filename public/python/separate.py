import os
import pydub 
import numpy as np
import soundfile as sf
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter

if __name__ == '__main__':
    def write(f, sr, x, normalized=False):
        """numpy array to MP3"""
        channels = 2 if (x.ndim == 2 and x.shape[1] == 2) else 1
        if normalized:  # normalized array - each item should be a float in [-1, 1)
            y = np.int16(x * 2 ** 15)
        else:
            y = np.int16(x)
        song = pydub.AudioSegment(y.tobytes(), frame_rate=sr, sample_width=2, channels=channels)
        song.export(f, format="mp3", bitrate="320k")

    # Using embedded configuration.
    separator = Separator('spleeter:2stems')

    # Use audio loader explicitly for loading audio waveform
    audio_loader = AudioAdapter.default()
    sample_rate = 44100
    cwd = os.getcwd().replace('\\', '/')
    waveform, _ = audio_loader.load(cwd + '/public/audio/temp1.mp3', sample_rate=sample_rate)

    # Perform the separation :
    prediction = separator.separate(waveform)

    sf.write(cwd + '/public/audio/temp1_vocals.mp3', prediction['vocals'], sample_rate)
    sf.write(cwd + '/public/audio/temp1_accompaniment.mp3', prediction['accompaniment'], sample_rate)

    # Use audio loader explicitly for loading audio waveform
    audio_loader = AudioAdapter.default()
    sample_rate = 44100
    cwd = os.getcwd().replace('\\', '/')
    waveform, _ = audio_loader.load(cwd + '/public/audio/temp2.mp3', sample_rate=sample_rate)

    # Perform the separation :
    prediction = separator.separate(waveform)

    sf.write(cwd + '/public/audio/temp2_vocals.mp3', prediction['vocals'], sample_rate)
    sf.write(cwd + '/public/audio/temp2_accompaniment.mp3', prediction['accompaniment'], sample_rate)

    print('Done!')