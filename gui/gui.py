import PySimpleGUI

from gui.countdown import countdown_window


def main_window(queue):
    layout = [[PySimpleGUI.Text('轻点鼠标，保持工作!')],
              [PySimpleGUI.Button('开始工作', key='keep_working')]]
    window = PySimpleGUI.Window('Keep Working', layout, size=(255, 75), location=(100, 100), icon='icon.ico')
    while True:
        event, values = window.read(timeout=100)
        if event == PySimpleGUI.WIN_CLOSED:
            break
        if event == 'keep_working':
            window.Hide()
            countdown_window(5, window, queue)
    window.close()
