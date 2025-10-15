# Keyboard key to morse audio output

This script generates a sine wave audio signal that can be controlled by pressing and releasing specific keys.
It uses the sounddevice library for audio output and pynput for keyboard input.

It allows the user to select an audio output device and generates a continuous tone while the specified keys are pressed.
When the keys are released, it smoothly ends the sound by playing the remaining wave period.

Original script by discord user @sgvsbg8k
Translated and modified by github user @MxPerrot

# Installation

## Dependencies

1. Install Dependencies

    ```shell
    pip install -r requirements.txt
    ```

2. Install VBCable in order to create a virtual sound device (Required for use in Discord voice chat)

    Follow instructions at [https://vb-audio.com/Cable/](https://vb-audio.com/Cable/)

3. Run help command 

    ```shell
    python3 main.py -h
    ```

4. Run default program (prompts for audio device to output to)

    ```shell
    python3 main.py
    ```