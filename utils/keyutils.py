# coding: utf-8

"""
This script provides utility functions for handling keyboard keys using the pynput library.

It includes a mapping of special keys to their corresponding pynput Key objects and functions to convert key names to key objects.
"""

from pynput import keyboard

SPECIAL_KEYS = {
    'alt': keyboard.Key.alt,
    'alt_gr': keyboard.Key.alt_gr,
    'alt_l': keyboard.Key.alt_l,
    'alt_r': keyboard.Key.alt_r,
    'backspace': keyboard.Key.backspace,
    'caps_lock': keyboard.Key.caps_lock,
    'cmd': keyboard.Key.cmd,
    'cmd_l': keyboard.Key.cmd_l,
    'cmd_r': keyboard.Key.cmd_r,
    'ctrl': keyboard.Key.ctrl,
    'ctrl_l': keyboard.Key.ctrl_l,
    'ctrl_r': keyboard.Key.ctrl_r,
    'delete': keyboard.Key.delete,
    'down': keyboard.Key.down,
    'end': keyboard.Key.end,
    'enter': keyboard.Key.enter,
    'esc': keyboard.Key.esc,
    'f1': keyboard.Key.f1,
    'f2': keyboard.Key.f2,
    'f3': keyboard.Key.f3,
    'f4': keyboard.Key.f4,
    'f5': keyboard.Key.f5,
    'f6': keyboard.Key.f6,
    'f7': keyboard.Key.f7,
    'f8': keyboard.Key.f8,
    'f9': keyboard.Key.f9,
    'f10': keyboard.Key.f10,
    'f11': keyboard.Key.f11,
    'f12': keyboard.Key.f12,
    'f13': keyboard.Key.f13,
    'f14': keyboard.Key.f14,
    'f15': keyboard.Key.f15,
    'f16': keyboard.Key.f16,
    'f17': keyboard.Key.f17,
    'f18': keyboard.Key.f18,
    'f19': keyboard.Key.f19,
    'f20': keyboard.Key.f20,
    'home': keyboard.Key.home,
    'insert': keyboard.Key.insert,
    'left': keyboard.Key.left,
    'media_next': keyboard.Key.media_next,
    'media_play_pause': keyboard.Key.media_play_pause,
    'media_previous': keyboard.Key.media_previous,
    'media_volume_down': keyboard.Key.media_volume_down,
    'media_volume_mute': keyboard.Key.media_volume_mute,
    'media_volume_up': keyboard.Key.media_volume_up,
    'menu': keyboard.Key.menu,
    'num_lock': keyboard.Key.num_lock,
    'page_down': keyboard.Key.page_down,
    'page_up': keyboard.Key.page_up,
    'pause': keyboard.Key.pause,
    'print_screen': keyboard.Key.print_screen,
    'right': keyboard.Key.right,
    'scroll_lock': keyboard.Key.scroll_lock,
    'shift': keyboard.Key.shift,
    'shift_l': keyboard.Key.shift_l,
    'shift_r': keyboard.Key.shift_r,
    'space': keyboard.Key.space,
    'tab': keyboard.Key.tab,
    'up': keyboard.Key.up,
}

def key_object(name):
    """Convert a key name to a pynput keyboard Key or KeyCode object.
    Args:
        name (str): The name of the key.
    Returns:
        keyboard.Key or keyboard.KeyCode: The corresponding key object.
    Raises:
        ValueError: If the key name is unknown.
    """
    name = name.lower()
    if name in SPECIAL_KEYS:
        return SPECIAL_KEYS[name]
    elif len(name) == 1:
        return keyboard.KeyCode(char=name)
    else:
        raise ValueError(f"Unknown key: {name}")

def keys_dict(key_names):
    """Create a dictionary mapping key names to their corresponding key objects.
    Args:
        key_names (list): A list of key names.
    Returns:
        dict: A dictionary mapping key names to key objects, with all values set to False.
    """
    return {key_object(name): False for name in key_names}