import pyautogui
import numpy as np
import mss
from state import State
import threading
import time


# 从窗口名获得左上角坐标和长宽
def get_window_position_and_size(title):
    try:
        window = pyautogui.getWindowsWithTitle(title)[0]
        return window.left, window.top, window.width, window.height
    except IndexError:
        print(f"No window with title '{title}' found.")
        return None


# 截图指定窗口（左上坐标和长宽）
def screenshot_window(pos, queue):
    while True:
        if pos:
            left, top, width, height = pos
            screenshot = pyautogui.screenshot(
                region=(left, top, width, height))
            # Convert the screenshot to a NumPy array
            frame_bgr = np.array(screenshot)
            queue.put(frame_bgr)
        else:
            print("No screenshots taken as the window was not found.")


# 使用mss截图的代码，目前好像输出格式不对，yolo会报错不能用
def screenshot_window_mss(pos, queue):
    with mss.mss() as sct:
        left, top, width, height = pos
        monitor = {"top": top, "left": left, "width": width, "height": height}
        screenshot = sct.grab(monitor)
        # Convert the screenshot to a NumPy array
        frame_bgr = np.array(screenshot)
        queue.put(frame_bgr)


tempSitu = State(
    ['ui', 'maidAlice', 'akane', 'newYearKayoko', 'yoruNoNero'])


def update_for_situ(pipe_conn_1, pipe_conn_2, pipe_conn_out):

    data_lock = threading.Lock()
    def send_data_thread():
        while True:
            with data_lock:
                if tempSitu.exPoint != 0:
                    pipe_conn_out.send(tempSitu)
                    # print("update", tempSitu.exPoint)
            time.sleep(0.05)


    # 创建发送线程
    thread = threading.Thread(target=send_data_thread)
    thread.start()

    while True:
        results = pipe_conn_1.recv()
        ex = pipe_conn_2.recv()
        with data_lock:
            tempSitu.updateCharacter(results)
            tempSitu.updateEX(ex)
        #print("update", tempSitu.exPoint)

        # ex = ex_positioning()
        # pipe_conn_out.send(tempSitu)