import os
import time
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import platform

def get_default_directory() -> str:
    """Returns the default directory based on the operating system."""
    system = platform.system().lower()
    user_name = os.getlogin()  # Get the current user's name

    if system == 'windows':  # Windows
        return os.path.join("C:\\Users", user_name, "SOUNDS", "spectrograms")
    elif system == 'darwin':  # macOS
        return os.path.join("/Users", user_name, "SOUNDS", "spectrograms")
    elif system == 'linux':  # Linux
        return os.path.join("/home", user_name, "SOUNDS", "spectrograms")
    else:
        raise OSError("Unsupported operating system")


def create_session_folder(directory=None) -> str:
    """Creates a new session folder inside the provided directory."""

    if directory is None:
        directory = get_default_directory()

    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Determine the next session number
    session_number = len(os.listdir(directory)) + 1

    # Create the session folder with a unique name
    session_folder = os.path.join(directory, f'session_{session_number}')
    os.makedirs(session_folder)

    # Print confirmation and return the path to the session folder
    print(f"Created new session: {session_folder}")
    return session_folder


def get_latest_session_folder(directory=None) -> None | str:
    """Finds the session folder with the highest number and returns its path."""

    if directory is None:
        directory = get_default_directory()

    # If the directory doesn't exist, return None
    if not os.path.exists(directory):
        return None

    # List all session folders starting with 'session_'
    sessions = [d for d in os.listdir(directory) if d.startswith('session_')]
    if not sessions:
        return None

    # Find the latest session folder based on the session number
    latest_session = max(sessions, key=lambda x: int(x.split('_')[1]))
    return os.path.join(directory, latest_session)


def plot_spectrogram(audio_data, rate=44100):
    """Plots the spectrogram of the given audio data."""
    fig, ax = plt.subplots()
    ax.set_title('Spectrogram')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')

    # Generate the spectrogram
    ax.specgram(audio_data, NFFT=256, Fs=rate, noverlap=128)
    return fig, ax


def save_spectrogram(fig, session_folder) -> str:
    """Saves the generated spectrogram plot to the session folder."""
    # Generate a timestamp for the file name
    timestamp = time.ctime().replace(' ', '_').replace(':', '-')
    filename = os.path.join(session_folder, f'spectrogram_{timestamp}.png')

    # Save the figure as a PNG file
    fig.savefig(filename)
    plt.close(fig)  # Close the figure to free up memory

    return filename


def record_audio(duration=3, rate=44100, channels=1):
    """Records audio data and returns it."""
    print("Starting recording...")

    # Record the audio data
    audio_data = sd.rec(int(rate * duration), samplerate=rate, channels=channels)
    sd.wait()  # Wait for the recording to finish

    print("Recording finished.")
    return audio_data.flatten()  # Flatten the audio data to a 1D array