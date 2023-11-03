import win32gui
import win32ui
import win32con
import ctypes
import numpy as np
import time as time


# 获取Windows当前屏幕缩放等级
def get_window_dpi_scale(hwnd):
    DPI_AWARENESS_CONTEXT_UNAWARE = -1
    ctypes.windll.user32.SetProcessDpiAwarenessContext(
        DPI_AWARENESS_CONTEXT_UNAWARE)
    dpi = ctypes.windll.user32.GetDpiForWindow(hwnd)
    scale = dpi / 96.0
    return scale


# 返回指定窗口的左上右下坐标(经过缩放修正)
def pos_window_win32(title):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd:
        # 获取窗口的坐标
        left, top, right, bot = win32gui.GetWindowRect(hwnd)

        # 获取窗口的DPI缩放
        scaling_factor = get_window_dpi_scale(hwnd)
        # print(scaling_factor)

        # # 根据DPI缩放调整尺寸
        # w = int((right - left) * scaling_factor)
        # h = int((bot - top) * scaling_factor)

        # 根据DPI缩放调整尺寸
        left = int(left*scaling_factor)
        top = int(top*scaling_factor)
        right = int(right*scaling_factor)
        bot = int(bot*scaling_factor)
        w = right - left
        h = bot - top

        # left, top, right, bot = int(left * scaling_factor), int(
        #     top * scaling_factor), int(right * scaling_factor), int(bot * scaling_factor)

        print("window position:", (left, top, right, bot), (w, h), scaling_factor)
        return hwnd, (left, top, right, bot), (w, h)
    return None


# 截图指定窗口（左上右下坐标）
# 当前状态下，裸截图性能大约100fps
def screenshot_window_win32(hwnd, pos, size, pipe_conn):
    # 获取窗口的DC
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    left, top, right, bot = pos
    w, h = size

    start_time = None
    while True:
        if start_time == None:
            start_time = time.time()

        # 创建位图保存截图
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        saveDC.SelectObject(saveBitMap)

        # 截图
        saveDC.StretchBlt((0, 0), (w, h), mfcDC, (0, 0),
                          (w, h), win32con.SRCCOPY)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        height = bmpinfo['bmHeight']
        width = bmpinfo['bmWidth']
        bgrx_arr = np.frombuffer(bmpstr, dtype=np.uint8).reshape(
            (height, width, 4))  # 4 for BGRX channels
        bgr_arr = bgrx_arr[:, :, :3]

        # 转为PIL Image
        # img = Image.frombuffer(
        #     'RGB',
        #     (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        #     bmpstr, 'raw', 'BGRX', 0, 1
        # )

        pipe_conn.send(bgr_arr)

        # 释放位图资源
        win32gui.DeleteObject(saveBitMap.GetHandle())

        end_time = time.time()
        if end_time - start_time == 0:
            frame_rate = 114514
        else:
            frame_rate = 1/(end_time-start_time)
        start_time = time.time()
        print("capture speed: ", frame_rate, "fps")

    # 释放设备上下文资源
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
