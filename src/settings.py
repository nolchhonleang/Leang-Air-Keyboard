"""Settings management for Leang-Air-Keyboard."""

from config import DEBOUNCE_TIME, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE, SOUND_ENABLED, THEME, SENSITIVITY, SOUND_FREQUENCY, HELP_OVERLAY

class Settings:
    def __init__(self):
        self.debounce_time = DEBOUNCE_TIME
        self.language = DEFAULT_LANGUAGE
        self.sound_enabled = SOUND_ENABLED
        self.theme = THEME
        self.sensitivity = SENSITIVITY
        self.sound_frequency = SOUND_FREQUENCY
        self.help_overlay = HELP_OVERLAY

    def show_menu(self):
        """Console-based settings menu with improved error handling."""
        while True:
            print("\nSettings Menu:")
            print(f"1. Debounce Time: {self.debounce_time}s")
            print(f"2. Language: {self.language} ({', '.join(SUPPORTED_LANGUAGES)})")
            print(f"3. Sound: {'Enabled' if self.sound_enabled else 'Disabled'} | Freq: {self.sound_frequency}Hz")
            print(f"4. Theme: {self.theme}")
            print(f"5. Sensitivity: {self.sensitivity}")
            print(f"6. Help Overlay: {'On' if self.help_overlay else 'Off'}")
            print("7. Exit Menu")
            try:
                choice = input("Enter choice (1-7): ").strip()
                if choice == '1':
                    try:
                        new_time = float(input("New debounce time (s): "))
                        self.debounce_time = max(0.1, new_time)
                        print(f"Updated debounce time to {self.debounce_time}s")
                    except ValueError:
                        print("Invalid number. Try again.")
                elif choice == '2':
                    lang = input(f"Enter language ({', '.join(SUPPORTED_LANGUAGES)}): ").lower().strip()
                    self.language = lang if lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
                    print(f"Updated language to {self.language}")
                elif choice == '3':
                    self.sound_enabled = not self.sound_enabled
                    print(f"Sound {'enabled' if self.sound_enabled else 'disabled'}")
                    if self.sound_enabled:
                        try:
                            freq_input = input(f"New frequency (Hz, current {self.sound_frequency}): ").strip()
                            self.sound_frequency = int(freq_input) if freq_input else SOUND_FREQUENCY
                            print(f"Updated frequency to {self.sound_frequency}Hz")
                        except ValueError:
                            print("Invalid number. Keeping current frequency.")
                elif choice == '4':
                    self.theme = 'dark' if self.theme == 'light' else 'light'
                    print(f"Updated theme to {self.theme}")
                elif choice == '5':
                    try:
                        new_sens = float(input("New sensitivity (0.5-2.0): "))
                        self.sensitivity = max(0.5, min(2.0, new_sens))
                        print(f"Updated sensitivity to {self.sensitivity}")
                    except ValueError:
                        print("Invalid number. Try again.")
                elif choice == '6':
                    self.help_overlay = not self.help_overlay
                    print(f"Help overlay {'on' if self.help_overlay else 'off'}")
                elif choice == '7':
                    print("Exiting settings menu. Changes applied.")
                    return True  # Signal to refresh layout
                else:
                    print("Invalid choice. Please enter 1-7.")
            except KeyboardInterrupt:
                print("\nMenu interrupted. Exiting.")
                return True
            except Exception as e:
                print(f"Unexpected error: {e}. Try again.")

    def get_settings(self):
        """Return dict of settings."""
        return {
            'debounce_time': self.debounce_time,
            'language': self.language,
            'sound_enabled': self.sound_enabled,
            'theme': self.theme,
            'sensitivity': self.sensitivity,
            'sound_frequency': self.sound_frequency,
            'help_overlay': self.help_overlay
        }