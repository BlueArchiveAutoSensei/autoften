import win32gui
import win32ui
import ctypes
import numpy as np
import time as time
import threading
import copy
import cv2


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
        # left, top, right, bot = win32gui.GetWindowRect(hwnd)
        left, top, right, bot = win32gui.GetClientRect(hwnd)

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
        return hwnd, (left, top, right, bot), (w, h), scaling_factor
    return None


# 截图指定窗口（左上右下坐标）
# 当前状态下，1440p全屏裸截图性能大约30-45fps
# 根据cProfile+snakeviz,
# windll PrintWindow大约占此函数80%耗时
# saveBitMap.GetBitmapBits占14%
# saveDC.SelectObject占3%
# 可继续使用线程分摊函数主线压力以优化性能
def screenshot_window_win32(hwnd, pos, size, pipe_conn1, pipe_conn2):

    # ---------------- #

    # 初始化共享数据和锁
    shared_data = {
        "bgr_arr": None,
        "data_ready": False,
    }
    data_lock = threading.Lock()

    # 检测data_ready标志位，
    # 当rdy=True时加锁，把共享区域的信息拷贝至data准备发送
    # 拷贝完成即开锁，共享区域立刻可以更新为新数据
    # data负责发送刚刚拷贝完成的信息
    def send_data_thread():
        while True:
            # data = None
            if shared_data["data_ready"]:
                with data_lock:
                    data = shared_data["bgr_arr"].copy()

                    shared_data["data_ready"] = False
                pipe_conn1.send(data)
                pipe_conn2.send(data)
                # cv2.imshow("1", data)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()

    # 创建发送线程
    thread = threading.Thread(target=send_data_thread)
    thread.start()

    # ---------------- #

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

        # StretchBlt可能导致一些窗口黑屏
        # # 截图
        # saveDC.StretchBlt((0, 0), (w, h), mfcDC, (0, 0),
        #                   (w, h), win32con.SRCCOPY)
        ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        height = bmpinfo['bmHeight']
        width = bmpinfo['bmWidth']
        bgrx_arr = np.frombuffer(bmpstr, dtype=np.uint8).reshape(
            (height, width, 4))  # 4 for BGRX channels
        # bgr_arr = bgrx_arr[:, :, :3]
        # make image C_CONTIGUOUS and drop alpha channel
        bgr_arr = np.ascontiguousarray(bgrx_arr)[..., :-1]

        # 转为PIL Image
        # img = Image.frombuffer(
        #     'RGB',
        #     (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        #     bmpstr, 'raw', 'BGRX', 0, 1
        # )

        # pipe_conn.send(bgr_arr)

        with data_lock:
            # 更新共享数据
            shared_data["bgr_arr"] = bgr_arr
            shared_data["data_ready"] = True

        # 释放位图资源
        win32gui.DeleteObject(saveBitMap.GetHandle())

        end_time = time.time()
        if end_time - start_time == 0:
            frame_rate = 114514
        else:
            frame_rate = 1/(end_time-start_time)
        start_time = time.time()
        # print("capture speed: ", frame_rate, "fps")

    # 释放设备上下文资源
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
