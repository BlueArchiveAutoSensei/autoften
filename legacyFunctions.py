import pyautogui
import numpy as np
import mss


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
