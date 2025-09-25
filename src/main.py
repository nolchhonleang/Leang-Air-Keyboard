"""Main entry for Leang-Air-Keyboard."""
import cv2
import sys
import time
from pynput.keyboard import Controller
from keyboard_layout import get_keyboard_layout, draw_all_buttons, display_typed_text, draw_help_overlay, Button
from gesture_detector import GestureDetector
from utils import debounce_press, save_text_to_file, load_text_from_file, play_sound, logging
from config import WINDOW_WIDTH, WINDOW_HEIGHT, TEXT_OUTPUT_FILE

def calibrate(gesture_detector, cap):
    """Simple calibration: Detect hand for 5 seconds to adjust."""
    logging.info("Calibrating... Show your hand.")
    start = time.time()
    while time.time() - start < 5:
        success, img = cap.read()
        if not success:
            logging.error("Calibration failed: No frame captured.")
            break
        img = cv2.flip(img, 1)
        results = gesture_detector.process_frame(img)
        gesture_detector.draw_landmarks(img, results)
        cv2.putText(img, "Calibrating...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Calibration", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sys.exit()
    cv2.destroyWindow("Calibration")
    logging.info("Calibration complete.")

# Init
keyboard_controller = Controller()
gesture_detector = GestureDetector()
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    logging.error("Webcam error. Exiting.")
    sys.exit(1)
cap.set(3, WINDOW_WIDTH)
cap.set(4, WINDOW_HEIGHT)

# State
typed_text = load_text_from_file(TEXT_OUTPUT_FILE)
last_press_time = 0

# Calibrate
calibrate(gesture_detector, cap)

logging.info("Leang-Air-Keyboard started.")

try:
    button_list = get_keyboard_layout()
    while True:
        success, img = cap.read()
        if not success:
            logging.error("Frame capture failed.")
            break

        img = cv2.flip(img, 1)
        results = gesture_detector.process_frame(img)
        img = gesture_detector.draw_landmarks(img, results)
        lm_list = gesture_detector.get_landmarks(results, img.shape)

        is_pinching, index_tip = gesture_detector.detect_pinch(lm_list)

        highlighted_button = None
        if index_tip:
            cv2.circle(img, index_tip, 10, (200, 100, 200), cv2.FILLED)  # Subtle highlight circle
            for button in button_list:
                if button.is_over(index_tip[0], index_tip[1]):
                    highlighted_button = button
                    break

        pressed_button = None
        if is_pinching and highlighted_button:
            can_press, last_press_time = debounce_press(last_press_time, 0.5)  # Fixed debounce
            if can_press:
                key = highlighted_button.text
                logging.info(f"Pressed: {key}")
                pressed_button = highlighted_button
                play_sound()

                if key == 'Space':
                    typed_text += ' '
                    keyboard_controller.press(' ')
                    keyboard_controller.release(' ')
                elif key == 'Delete':
                    if typed_text:
                        typed_text = typed_text[:-1]
                    keyboard_controller.press('\b')
                    keyboard_controller.release('\b')
                else:
                    typed_text += key.lower()  # No shift/caps, all lowercase
                    keyboard_controller.press(key.lower())
                    keyboard_controller.release(key.lower())

        img = draw_all_buttons(img, button_list, highlighted_button, pressed_button)
        display_typed_text(img, typed_text)
        draw_help_overlay(img)

        cv2.imshow("Leang-Air-Keyboard", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    save_text_to_file(typed_text, TEXT_OUTPUT_FILE)  # Auto-save
    cap.release()
    cv2.destroyAllWindows()
    logging.info("Application closed.")