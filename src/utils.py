"""Utility functions for Leang-Air-Keyboard."""

import math
import logging
import time
import numpy as np
import sounddevice as sd
from config import LOG_LEVEL, LOG_FILE, SOUND_ENABLED, SOUND_FREQUENCY, SOUND_DURATION

# Setup logging to file and console
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()])

def get_distance(p1, p2):
    """Calculate Euclidean distance."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def debounce_press(last_press_time, debounce_time):
    """Debounce key presses."""
    current_time = time.time()
    if current_time - last_press_time > debounce_time:
        return True, current_time
    return False, last_press_time

def save_text_to_file(text, filename):
    """Save text to file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        logging.info(f"Saved to {filename}")
    except Exception as e:
        logging.error(f"Save error: {e}")

def load_text_from_file(filename):
    """Load text from file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logging.error(f"Load error: {e}")
        return ""

def play_sound():
    """Play beep sound if enabled."""
    if not SOUND_ENABLED:
        return
    sample_rate = 44100
    t = np.linspace(0, SOUND_DURATION, int(sample_rate * SOUND_DURATION), False)
    note = np.sin(SOUND_FREQUENCY * t * 2 * np.pi)
    sd.play(note, sample_rate)
    time.sleep(SOUND_DURATION)
    sd.stop()

def get_theme_colors(theme):
    """Get colors based on theme."""
    if theme == 'dark':
        return {
            'bg': (50, 50, 50),
            'text': (255, 255, 255),
            'highlight': (0, 150, 0),
            'press': (0, 0, 150)
        }
    return {
        'bg': (255, 255, 255),
        'text': (0, 0, 0),
        'highlight': (0, 255, 0),
        'press': (0, 0, 255)
    }