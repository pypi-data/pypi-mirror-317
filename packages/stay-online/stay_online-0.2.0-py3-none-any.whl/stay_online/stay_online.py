import os
import random
import time
from datetime import datetime

import pyautogui
from pyautogui import press
from pynput import mouse

from stay_online.constants import DEFAULT_MAX_DELAY_SECONDS, DEFAULT_MAX_NUM_WORDS, DEFAULT_MIN_DELAY_SECONDS, DEFAULT_MIN_NUM_WORDS, DEFAULT_SHOW_TIMESTAMP, DEFAULT_STOP_HHMM, HELP_MAX_DELAY_SECONDS, HELP_MAX_NUM_WORDS, HELP_MIN_DELAY_SECONDS, HELP_MIN_NUM_WORDS, HELP_SHOW_TIMESTAMP, HELP_STOP_HHMM


def simulate_typing(
        min_num_words:int=DEFAULT_MIN_NUM_WORDS, 
        max_num_words:int=DEFAULT_MAX_NUM_WORDS, 
        show_timestamp:bool=DEFAULT_SHOW_TIMESTAMP
        ):
    f"""
    Simulate typing words with random slight paused in between each characters and spaces.
    :param int min_num_words: {HELP_MIN_NUM_WORDS}
    :param int max_num_words: {HELP_MAX_NUM_WORDS}
    :param bool show_timestamp: {HELP_SHOW_TIMESTAMP}
    """
    file_path = os.path.join(os.path.dirname(__file__), 'word_file.txt')
    with open(file_path, 'r') as word_file:
        n_words = random.randrange(min_num_words, max_num_words)

        word_list = random.sample(word_file.read().splitlines(), n_words)
        if show_timestamp:
            word_list.insert(0, f"{datetime.now().time()}")
        print(f"Typing: {word_list}")
        for word in word_list:
            for letter in word:
                press(letter)
                time.sleep(random.randrange(50) / 100)
            press('space')
            time.sleep(random.randrange(100) / 100)
        time.sleep(random.randrange(50) / 100)
        press('enter')


class CursorUtils:
    def on_click(self, x, y, button, pressed):
        print('{0} at {1}'.format(
            'Pressed' if pressed else 'Released',
            (x, y)))
        if pressed:
            print(f"This is x, y: {(x, y)}")
            return (x, y)
        if not pressed:
            return False

    def get_cursor_location(self):
        print(f"Place cursor at clicking position and left click once.")
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()
        controller = mouse.Controller()
        print(f"Controller position: {controller.position}")
        return controller.position

    def random_cursor_movement(self, x, y, min_time=1):
        pyautogui_mouse_movement_type = [key for key in list(pyautogui.__dict__.keys()) if key.startswith('ease')]
        n_random_movements = random.randrange(10, 50)
        total_time = min_time + random.randrange(100) / 100
        interval_time = total_time / n_random_movements
        if x and y:
            for i in range(10):
                interval = interval_time + random.randrange(-100, 101) / 100
                if interval < 0:
                    continue
                selected_movement_type = random.choice(pyautogui_mouse_movement_type)
                selected_movement = getattr(pyautogui, selected_movement_type)
                pyautogui.moveTo(random.randrange(50) + x, random.randrange(50) + y, interval, selected_movement)
            pyautogui.leftClick()
            time.sleep(random.randrange(100) / 100)
        return


def stay_online(
        stop_hhmm:str=DEFAULT_STOP_HHMM, 
        min_delay_seconds:int=DEFAULT_MIN_DELAY_SECONDS, 
        max_delay_seconds:int=DEFAULT_MAX_DELAY_SECONDS, 
        min_num_words:int=DEFAULT_MIN_NUM_WORDS, 
        max_num_words:int=DEFAULT_MAX_NUM_WORDS,
        show_timestamp:bool=DEFAULT_SHOW_TIMESTAMP
        ):
    f"""
    Simulate fake movement and fake keyboard typing.

    :param str stop_hhmm: {HELP_STOP_HHMM}
    :param int min_delay_seconds: {HELP_MIN_DELAY_SECONDS}
    :param int max_delay_seconds: {HELP_MAX_DELAY_SECONDS}
    :param int min_num_words: {HELP_MIN_NUM_WORDS}
    :param int max_num_words: {HELP_MAX_NUM_WORDS}
    :param bool show_timestamp: {HELP_SHOW_TIMESTAMP}
    """
    print(f"""
Remeber to provide the optional parameters:
    :param str stop_hhmm: {HELP_STOP_HHMM}
    :param int min_delay_seconds: {HELP_MIN_DELAY_SECONDS}
    :param int max_delay_seconds: {HELP_MAX_DELAY_SECONDS}
    :param int min_num_words: {HELP_MIN_NUM_WORDS}
    :param int max_num_words: {HELP_MAX_NUM_WORDS}
    :param bool show_timestamp: {HELP_SHOW_TIMESTAMP}
""")
    
    print(f"""
Stay Online Stop: {stop_hhmm if stop_hhmm != '' else 'Never'}
Min Delay Seconds: {min_delay_seconds}
Max Delay Seconds: {max_delay_seconds}
Min Number of Words: {min_num_words}
Max Number of Words: {max_num_words}
Show Timestamp: {show_timestamp}
""")
    cursor_location_object = CursorUtils()
    cursor_location = cursor_location_object.get_cursor_location()
    time.sleep(3)
    while True:
        current_time = datetime.now().time()
        print(f"Current time is: {datetime.now().time()}")
        if stop_hhmm != '':
            try:
                if current_time > datetime.strptime(stop_hhmm, "%H%M").time():
                    break
            except Exception as e:
                raise Exception(f'Please provide the correct time value in hhmm format.')
        try:
            cursor_location_object.random_cursor_movement(*cursor_location)
            simulate_typing(min_num_words=min_num_words, max_num_words=max_num_words, show_timestamp=show_timestamp)
            time.sleep(random.randrange(min_delay_seconds, max_delay_seconds))
        except Exception as e:
            print(f"Something went wrong: {e}")
