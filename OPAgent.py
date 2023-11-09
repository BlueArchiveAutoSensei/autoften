import win32con
import win32api
import win32gui
import time
from ppadb.client import Client as AdbClient


def connect(server, device):
    HOST, PORT = server
    DEVICE_IP, DEVICE_PORT = device

    # 初始化adb客户端
    client = AdbClient(host=HOST, port=PORT)

    # 连接到远程设备
    device = client.remote_connect(DEVICE_IP, DEVICE_PORT)

    # 获取设备对象
    device = client.device(f"{DEVICE_IP}:{DEVICE_PORT}")

    return device


def click(device, x, y):
    # 发送鼠标点击消息
    device.shell(f"input tap {x} {y}")


def drag(device, x_start, y_start, x_end, y_end, duration=50):
    device.shell(f"input swipe {x_start} {y_start} {x_end} {y_end} {duration}")