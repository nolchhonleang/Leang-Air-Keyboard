"""Keyboard layout module for Leang-Air-Keyboard. Professional minimalist English QWERTY design optimized for full screen with added spacing."""

import cv2
import utils
from config import WINDOW_WIDTH, WINDOW_HEIGHT, SUPPORTED_LANGUAGES, THEME, HELP_OVERLAY

class Button:
    def __init__(self, pos, text, base_size=(60, 60)):
        self.pos = pos
        self.text = text
        text_length = max(1, len(text))
        self.size = (base_size[0] + (text_length - 1) * 12, base_size[1])  # Tight, pro spacing
        if text == 'Space':
            self.size = (200, base_size[1])  # Sleek, compact space bar
        elif text == 'Delete':
            self.size = (80, base_size[1])  # Slightly larger for visibility

    def draw(self, img, highlight=False, pressed=False):
        colors = utils.get_theme_colors(THEME)
        color = colors['press'] if pressed else (colors['highlight'] if highlight else colors['bg'])
        padding = 5  # Increased padding for space around buttons
        border_color = (160, 160, 160)  # Light gray border for professionalism
        cv2.rectangle(img, (self.pos[0] - padding, self.pos[1] - padding),
                     (self.pos[0] + self.size[0] + padding, self.pos[1] + self.size[1] + padding),
                     border_color, 1)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.size[0], self.pos[1] + self.size[1]), color, cv2.FILLED)
        text_size = cv2.getTextSize(self.text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]  # Smaller, crisp font
        text_x = self.pos[0] + (self.size[0] - text_size[0]) // 2
        text_y = self.pos[1] + (self.size[1] + text_size[1]) // 2
        cv2.putText(img, self.text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, colors['text'], 2)

    def is_over(self, x, y):
        return self.pos[0] <= x < self.pos[0] + self.size[0] and self.pos[1] <= y < self.pos[1] + self.size[1]

def get_keyboard_layout(lang='en', layer=None):
    """Get professional minimalist English QWERTY layout optimized for full 1280x720 screen with added spacing."""
    if lang not in SUPPORTED_LANGUAGES:
        lang = 'en'

    # Minimalist QWERTY layout designed to fit all keys across the screen
    layout = [
        ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Delete'],
        ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\'', ','],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '.', '/', 'Space']
    ]

    button_list = []
    start_x = (WINDOW_WIDTH - (len(layout[0]) * 70)) // 2  # Adjusted for 70px spacing
    start_y = 80  # Reduced top margin to fit with increased spacing
    button_width = 70  # Increased spacing between buttons
    button_height = 70  # Increased spacing between rows

    for i, row in enumerate(layout):
        for j, key in enumerate(row):
            pos = (start_x + j * button_width, start_y + i * button_height)
            button_list.append(Button(pos, key))

    return button_list

def draw_all_buttons(img, button_list, highlighted_button=None, pressed_button=None):
    """Draw buttons with professional alignment."""
    for button in button_list:
        highlight = button == highlighted_button
        pressed = button == pressed_button
        button.draw(img, highlight, pressed)
    return img

def display_typed_text(img, text):
    """Display text area with professional styling."""
    colors = utils.get_theme_colors(THEME)
    text_area_height = 80
    cv2.rectangle(img, (50, WINDOW_HEIGHT - text_area_height - 20), (WINDOW_WIDTH - 50, WINDOW_HEIGHT - 20), colors['bg'], cv2.FILLED)
    cv2.putText(img, text, (60, WINDOW_HEIGHT - text_area_height // 2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.85, colors['text'], 2)

def draw_help_overlay(img):
    """Draw help text if enabled."""
    if HELP_OVERLAY:
        help_text = "Point: Index finger | Press: Pinch | q: Quit"
        cv2.putText(img, help_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (80, 80, 200), 2)  # Subtle professional blue