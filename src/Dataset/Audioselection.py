import os
import random
import librosa
import numpy as np
import librosa.effects
import shutil

class AudioPreprocessor:
    def __init__(self, directory, num_samples, target_duration=5, sample_rate=22050):
        """
        directory: Path to the directory containing audio files.
        num_samples: Number of audio files to select for preprocessing.
        target_duration: Target duration for audio clips in seconds.
        sample_rate: Sampling rate of the audio files.
        """
        self.directory = directory
        self.num_samples = num_samples
        self.target_duration = target_duration
        self.sample_rate = sample_rate

    def select_audio_files(self):
        
        all_files = [os.path.join(self.directory, f) for f in os.listdir(self.directory) if f.endswith('.mp3')]
       
        return random.sample(all_files, min(self.num_samples, len(all_files)))

    def preprocess_audio(self, audio_path):
        # Load the audio file
        audio, sr = librosa.load(audio_path, sr=self.sample_rate)

        # Remove silence
        non_silent_intervals = librosa.effects.split(audio, top_db=30)  # Silence threshold
        audio = np.concatenate([audio[start:end] for start, end in non_silent_intervals], axis=0)

        # Apply STFT and then inverse STFT (ISTFT)
        stft = librosa.stft(audio)
        audio = librosa.istft(stft)

        # Truncate or extend the audio to match the target length
        target_length = int(self.target_duration * sr)
        if len(audio) > target_length:
            audio = audio[:target_length]  # Truncate
        elif len(audio) < target_length:
            audio = np.pad(audio, (0, max(0, target_length - len(audio))), mode='constant')

        # Normalize the signal
        audio = librosa.util.normalize(audio)

        return audio

    def preprocess_all(self):
        selected_files = self.select_audio_files()
        return [self.preprocess_audio(audio_path) for audio_path in selected_files]


class AudioSplitter:
    def __init__(self, base_path, train_ratio=0.8):
        self.base_path = base_path
        self.train_ratio = train_ratio
        self.train_path = os.path.join(base_path, 'train_set')
        self.test_path = os.path.join(base_path, 'test_set')

    def split(self):
        # Create directories for train and test sets
        os.makedirs(self.train_path, exist_ok=True)
        os.makedirs(self.test_path, exist_ok=True)

        # Get a list of all audio files
        all_files = [f for f in os.listdir(self.base_path) if f.endswith('.mp3')]  # Adjust the extension if needed
        random.shuffle(all_files)

        # Calculate the number of files for the training set
        train_size = int(len(all_files) * self.train_ratio)

        # Separate and move the files
        for i, file in enumerate(all_files):
            if i < train_size:
                shutil.move(os.path.join(self.base_path, file), self.train_path)
            else:
                shutil.move(os.path.join(self.base_path, file), self.test_path)

