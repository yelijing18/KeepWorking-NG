import PySimpleGUI
import time
import threading
import keyboard
import random
from collections import deque

COUNTDOWN_EVENT = '-COUNTDOWN-'
COUNTDOWN_FINISH_EVENT = '-COUNTDOWN-FINISH-'
KEYBOARD_INTERRUPT_EVENT = '-KEYBOARD-INTERRUPT-'
WORKING_EVENT = '-WORKING-'

I18N = {'up': '上', 'down': '下'}


def countdown(window, seconds):
    try:
        for i in range(seconds):
            window.write_event_value(COUNTDOWN_EVENT, (i,))
            time.sleep(1)
        window.write_event_value(COUNTDOWN_FINISH_EVENT, ())
    except AttributeError:
        pass


def working(window, now_working):
    while True:
        if not now_working():
            break
        key = random.choice(['up', 'down'])
        keyboard.press_and_release(key)
        window.write_event_value(WORKING_EVENT, (key,))
        time.sleep(1)


def countdown_window(seconds: int, main_window, queue):
    layout = [[PySimpleGUI.Text('倒计时：', key='label'), PySimpleGUI.Text('', key='label_value')],
              [PySimpleGUI.ProgressBar(1000, orientation='h', size=(25, 10), key='progressbar')],
              [PySimpleGUI.Button('停止', key='cancel')]]
    window = PySimpleGUI.Window('Counting down...', layout, location=(100, 100), icon='icon.ico')
    label = window['label']
    label_value = window['label_value']
    progress_bar = window['progressbar']
    history = deque([], maxlen=5)
    init = True
    now_working = False

    while True:
        event, values = window.read(timeout=10)
        if init:
            init = False
            label_value.update(seconds)
            threading.Thread(target=countdown, args=(window, seconds,), daemon=True).start()
        if now_working and len(queue) > 0:
            window.write_event_value(KEYBOARD_INTERRUPT_EVENT, ())
        if event == COUNTDOWN_EVENT:
            label_value.update(seconds - values[COUNTDOWN_EVENT][0])
            progress_bar.UpdateBar(values[COUNTDOWN_EVENT][0] * 1000 // seconds)
        if event == COUNTDOWN_FINISH_EVENT:
            progress_bar.UpdateBar(1000)
            window.set_title('Working...')
            label.update('近五次按键为：')
            label_value.update('')
            now_working = True
            queue.clear()
            threading.Thread(target=working, args=(window, lambda: now_working,), daemon=True).start()
        if event == WORKING_EVENT:
            history.append(I18N[values[WORKING_EVENT][0]])
            label_value.update(', '.join(history))
        if event == 'cancel' or event == PySimpleGUI.WIN_CLOSED or (event == KEYBOARD_INTERRUPT_EVENT and now_working):
            now_working = False
            main_window.UnHide()
            window.close()
            break
