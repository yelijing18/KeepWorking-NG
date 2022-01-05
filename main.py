from gui.gui import main_window
from pynput.keyboard import Key, Listener
from collections import deque

if __name__ == '__main__':
    queue = deque([], maxlen=1)


    def on_release(key):
        if key == Key.esc:
            queue.append('')


    Listener(on_release=on_release).start()
    main_window(queue)
