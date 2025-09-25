"""Gesture detection module for Leang-Air-Keyboard."""

import cv2
import mediapipe as mp
from utils import get_distance, logging
from config import PINCH_THRESHOLD, SENSITIVITY

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

class GestureDetector:
    def __init__(self, min_detection_confidence=0.7, min_tracking_confidence=0.7):
        self.hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2,
                                    min_detection_confidence=min_detection_confidence,
                                    min_tracking_confidence=min_tracking_confidence)

    def process_frame(self, img):
        """Process for landmarks."""
        try:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.hands.process(img_rgb)
            return results
        except Exception as e:
            logging.error(f"Frame process error: {e}")
            return None

    def draw_landmarks(self, img, results):
        """Draw landmarks for all hands."""
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        return img

    def get_landmarks(self, results, img_shape):
        """Get landmarks, support multi-hand (return dominant - right if both)."""
        lm_lists = []
        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                lm_list = []
                for lm in hand_landmarks.landmark:
                    h, w, _ = img_shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append((cx, cy))
                lm_lists.append((lm_list, handedness.classification[0].label))
        if not lm_lists:
            return []
        # Prefer right hand if detected
        right_hand = next((lm for lm, label in lm_lists if label == 'Right'), lm_lists[0][0])
        return right_hand

    def detect_pinch(self, lm_list):
        """Detect pinch, adjusted for sensitivity."""
        if len(lm_list) >= 21:
            index_tip = lm_list[8]
            thumb_tip = lm_list[4]
            pinch_dist = get_distance(index_tip, thumb_tip)
            return pinch_dist < (PINCH_THRESHOLD * SENSITIVITY), index_tip
        return False, None