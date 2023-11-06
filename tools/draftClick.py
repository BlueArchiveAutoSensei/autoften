import win32con
import win32api
import win32gui


def click_at(hwnd, x, y):
    # 转换坐标为窗口客户区坐标
    client_rect = win32gui.GetClientRect(hwnd)
    screen_rect = win32gui.ClientToScreen(
        hwnd, (client_rect[0], client_rect[1]))
    # x += screen_rect[0]
    # y += screen_rect[1]

    # 将坐标转换为LPARAM
    lparam = win32api.MAKELONG(x, y)

    # 发送鼠标点击消息
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN,
                         win32con.MK_LBUTTON, lparam)
    win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP,
                         win32con.MK_LBUTTON, lparam)


# 窗口名称
window_name = "QQ"
# 目标坐标（相对于窗口客户区的左上角）
target_x, target_y = int(40/1.5), int(150/1.5)

# 找到窗口句柄
hwnd = win32gui.FindWindow(None, window_name)
if hwnd == 0:
    raise Exception("Window not found: " + window_name)

# 在指定位置点击鼠标左键
click_at(hwnd, target_x, target_y)
