import win32gui
import win32ui
import ctypes
import numpy as np
import os
import cv2
from datetime import datetime

# 获取Windows当前屏幕缩放等级
def get_window_dpi_scale(hwnd):
    DPI_AWARENESS_CONTEXT_UNAWARE = -1
    ctypes.windll.user32.SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_UNAWARE)
    dpi = ctypes.windll.user32.GetDpiForWindow(hwnd)
    scale = dpi / 96.0
    return scale

# 返回指定窗口的左上右下坐标(经过缩放修正)
def pos_window_win32(title):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd:
        left, top, right, bot = win32gui.GetClientRect(hwnd)
        scaling_factor = get_window_dpi_scale(hwnd)
        left = int(left*scaling_factor)
        top = int(top*scaling_factor)
        right = int(right*scaling_factor)
        bot = int(bot*scaling_factor)
        w = right - left
        h = bot - top
        return hwnd, (left, top, right, bot), (w, h)
    return None

# 截图指定窗口（左上右下坐标）
def screenshot_window_win32(hwnd, pos, size, save_dir):
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    left, top, right, bot = pos
    w, h = size

    # 创建位图保存截图
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)

    ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    height = bmpinfo['bmHeight']
    width = bmpinfo['bmWidth']
    bgrx_arr = np.frombuffer(bmpstr, dtype=np.uint8).reshape((height, width, 4))
    bgr_arr = np.ascontiguousarray(bgrx_arr)[..., :-1]

    # 生成文件名
    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")
    filename = os.path.join(save_dir, f"{current_time}.png")
    cv2.imwrite(filename, bgr_arr)
    cv2.imshow('Templates Matched', bgr_arr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    return filename

if __name__ == '__main__':
    # 预定义的窗口名称和保存目录
    window_name = "Image34.png ‎- 照片"
    window_name = "QQ"
    window_name = "MuMu模拟器12"
    save_dir = r"C:\Users\Vickko\Pictures"
    os.makedirs(save_dir, exist_ok=True)
    
    hwnd, pos, size = pos_window_win32(window_name)
    if hwnd:
        screenshot_path = screenshot_window_win32(hwnd, pos, size, save_dir)
        print(f"Screenshot saved at: {screenshot_path}")
    else:
        print(f"No window found with name: {window_name}")
