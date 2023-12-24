from sklearn.decomposition import MiniBatchDictionaryLearning
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Audio, display
import time


class DictionaryLearner:
    def __init__(self, n_components, alpha, max_iter, batch_size=3):
        """
        n_components: Number of atoms in the dictionary.
        alpha: Sparsity controlling parameter.
        max_iter: Number of iterations to run the algorithm.
        batch_size: Size of the mini-batches.
        """
        self.model = MiniBatchDictionaryLearning(n_components=n_components, alpha=alpha, max_iter=max_iter, batch_size=batch_size)

    def fit(self, data):
        """
        data: Preprocessed audio data as a list of NumPy arrays.
        """
        # Flatten the data and stack them as a 2D array
        data_flattened = np.vstack([d.flatten() for d in data])
        
        # Start timing
        start_time = time.time()

        # Fit the model
        self.model.fit(data_flattened)

        # End timing
        end_time = time.time()

        # Calculate and print the training time
        training_time = end_time - start_time
        print(f"Training Time: {training_time} seconds")

        return self.model.components_



class DictionaryVisualizer:
    def __init__(self, dictionary, sample_rate):
        """
        dictionary: The learned dictionary (atoms).
        sample_rate: Sampling rate of the audio data.
        """
        self.dictionary = dictionary
        self.sample_rate = sample_rate

    def visualize_atom(self, atom_index):
        plt.figure(figsize=(12, 4))
        plt.plot(self.dictionary[atom_index])
        plt.title(f"Atom {atom_index}")
        plt.xlabel("Samples")
        plt.ylabel("Amplitude")
        plt.show()

    def play_atom(self, atom_index):
        display(Audio(self.dictionary[atom_index], rate=self.sample_rate))

    def show_atom(self, atom_index):
        self.visualize_atom(atom_index)
        self.play_atom(atom_index)

    def show_all_atoms(self):
        for i in range(len(self.dictionary)):
            self.show_atom(i)