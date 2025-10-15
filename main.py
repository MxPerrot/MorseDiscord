# coding: utf-8

"""
This script generates a sine wave audio signal that can be controlled by pressing and releasing specific keys.
It uses the sounddevice library for audio output and pynput for keyboard input.

It allows the user to select an audio output device and generates a continuous tone while the specified keys are pressed.
When the keys are released, it smoothly ends the sound by playing the remaining wave period.

Original script by discord user @sgvsbg8k
Translated and modified by github user @MxPerrot
"""

###############################################################################
#                                   IMPORTS                                   #
###############################################################################


import argparse
import sounddevice as sd
import numpy as np
from time import sleep
from utils.keyutils import keys_dict, keyboard


###############################################################################
#                                  FUNCTIONS                                  #
###############################################################################

def get_readable_keys(keys) -> list[str]:
    """Convert keys to a readable format.
    Args:
        keys: Dictionary of keys.
    Returns:
        List of readable key names.
    """
    return [k.name if hasattr(k, 'name') else str(k.char) for k in keys]


def choose_device(devices) -> int:
    """Display available audio devices and allow the user to select one.
    Returns:
        int: The index of the selected audio device.
    """
    print("Available audio devices:")
    for index, device in enumerate(devices):
        print(f"{(str(index) + ':'): <4} {device['name']}")
    max_retries = 5  # Maximum number of retries
    retries = 0
    while retries < max_retries:
        try:
            output_device = int(input("Please enter chosen audio device number: "))
            if output_device < 0 or output_device >= len(devices):
                raise ValueError("Invalid device number")
            return output_device
        except ValueError as e:
            retries += 1
            print(f"Error: {e}. Please enter a valid device number. ({retries}/{max_retries} retries)")
    print("Maximum retries reached. Exiting.")
    exit(1)

def on_press(key: str) -> None:
    """Handle key press events to enable audio generation.
    Args:
        key: The key that was pressed.
    """
    if key in keys:
        keys[key] = True

def on_release(key: str) -> None:
    """Handle key release events to disable audio generation.
    Args:
        key: The key that was released.
    """
    if key in keys:
        keys[key] = False

def generate_audio(num_samples: int, offset: float = 0) -> tuple[np.ndarray, float]:
    """Generate a sine wave audio signal.
    Args:
        num_samples: Number of samples to generate.
        offset: Offset in seconds for the sine wave.
    Returns:
        A tuple containing the generated audio signal and the updated offset.
    """
    t = np.linspace(offset, num_samples / SAMPLERATE + offset, num_samples, endpoint=False)
    offset += num_samples / SAMPLERATE
    while offset >= 1 / FREQUENCY:
        offset -= 1 / FREQUENCY
    audio = np.sin(2 * np.pi * FREQUENCY * t) * VOLUME
    audio = np.tile(audio[:, np.newaxis], (1, CHANNELS))
    return audio, offset

def audio_callback(outdata: np.ndarray, frames: int, time: float, status: sd.CallbackFlags) -> None:
    """Callback function for audio output.
    Args:
        outdata: Output buffer for audio data.
        frames: Number of frames to write.
        time: Timestamp of the audio callback.
        status: Status of the audio stream.
    """

    global offset
    if status:
        print(status)

    if all(keys.values()):  # Key pressed → Normal tone
        audio, offset = generate_audio(frames, offset)
        outdata[:] = audio
    else:  # Key released → Clean ending with last wave period
        outdata[:] = np.zeros((frames, CHANNELS), dtype=np.float32)  # Default: silence
        if offset != 0:
            num = int(((1 / FREQUENCY) - offset) * SAMPLERATE)  # Calculate remaining samples
            
            if num == 0:
                offset = 0
                return
            if num > frames:
                num = frames  # Limit if num is greater than frames
            audio, new_offset = generate_audio(num, offset)  # Only take audio, ignore offset
            outdata[:num] = audio  # Write signal at the start 
            offset = max(0, new_offset)  # Reset offset

###############################################################################
#                                MAIN FUNCTION                                #
###############################################################################

if __name__ == "__main__":

    # Default parameters
    FREQUENCY = 440.0  # Frequency of the sine wave in Hz
    VOLUME = 0.5  # Volume of the sine wave
    KEYS = ['shift_r']  # Default keys to control audio
    SAMPLERATE = 44100  # Sample rate for audio output
    CHANNELS = 2  # Number of audio channels
    output_device = None  # Audio output device index, None for auto-select
    DEVICES = sd.query_devices()

    # Argument parsing
    parser = argparse.ArgumentParser(description="Generate a sine wave audio signal controlled by keyboard input.")
    parser.add_argument('-l', '--list-devices', action='store_true', help='List available audio devices and exit')
    parser.add_argument('-d', '--device', type=int, help='Audio output device index (default: auto-select)')
    parser.add_argument('-k', '--keys', nargs='+', default=KEYS, help='Keys to simultaneously press to generate sound (default: shift_r)')
    parser.add_argument('-f', '--frequency', type=float, default=FREQUENCY, help='Frequency of the sine wave in Hz (default: 440.0)')
    parser.add_argument('-v', '--volume', type=float, default=VOLUME, help='Volume of the sine wave (default: 0.5)')
    parser.add_argument('-s', '--samplerate', type=int, default=44100, help='Sample rate for audio output (default: 44100)')
    parser.add_argument('-c', '--channels', type=int, default=2, help='Number of audio channels (default: 2)')
    args = parser.parse_args()

    # Parameters
    OUTPUT_DEVICE = args.device
    KEYS = args.keys
    FREQUENCY = args.frequency
    VOLUME = args.volume
    SAMPLERATE = args.samplerate
    CHANNELS = args.channels
    
    keys = keys_dict(KEYS)  # Dictionary to track key states
    offset = 0.0  # Offset for the sine wave generation

    # List available audio devices if requested
    if args.list_devices:
        print("Available audio devices:")
        for i, device in enumerate(DEVICES):
            print(f"  {i}: {device['name']}")
        exit(0)

    # Choose audio output device if not specified
    if OUTPUT_DEVICE is None:
        OUTPUT_DEVICE = choose_device(DEVICES)
    elif OUTPUT_DEVICE < 0 or OUTPUT_DEVICE >= len(DEVICES):
        raise ValueError("Invalid device number")

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    finished_callback = lambda: listener.stop() if listener.running else None

    try:
        with sd.OutputStream(
            callback    = audio_callback,
            device      = output_device,
            samplerate  = SAMPLERATE,
            channels    = CHANNELS,
            dtype       = np.float32,
            finished_callback = finished_callback,
            blocksize   = 256,
            latency     = 'low',
        ):

            readable_keys = get_readable_keys(keys)
            print(f"Hold {' & '.join(readable_keys)} to beep")

            try:
                while True:
                    sleep(1)  # Keep the program running without hogging CPU
            except KeyboardInterrupt:
                print("\nProgram ended")
                listener.stop()
    except Exception as e:
        print(f"Could not start audio stream: {e}. Parameters: device={OUTPUT_DEVICE}, samplerate={SAMPLERATE}, channels={CHANNELS}, dtype=np.float32, blocksize=256, latency='low'")
        listener.stop()
    finally:
        listener.stop()
        print("Listener stopped")