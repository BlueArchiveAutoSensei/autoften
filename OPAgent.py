import win32con
import win32api
import win32gui
import time
from ppadb.client import Client as AdbClient
import subprocess


ex_slot_pos = (1660, 1020, 2280, 1250)  # 原始视频截图的坐标
ex_slot_pos = (1640, 1110, 2300, 1340)  # 照片app全屏截图
ex_slot_pos = (1660, 1110, 2310, 1340)  # win32带MuMu标题栏
ex_slot_pos = (900, 615, 1255, 740)  # win32带MuMu标题栏720p


ex_slot_0 = (int(ex_slot_pos[0]+(ex_slot_pos[2]-ex_slot_pos[0]) * 1/6),
             int((ex_slot_pos[1]+ex_slot_pos[3])/2))
ex_slot_1 = (int(ex_slot_pos[0]+(ex_slot_pos[2]-ex_slot_pos[0]) * 3/6),
             int((ex_slot_pos[1]+ex_slot_pos[3])/2))
ex_slot_2 = (int(ex_slot_pos[0]+(ex_slot_pos[2]-ex_slot_pos[0]) * 5/6),
             int((ex_slot_pos[1]+ex_slot_pos[3])/2))


def which_slot(name, exSlots):
    for slot in exSlots:
        if exSlots[slot] == name:
            return slot

    return -1


def slot_pos(slotNum):
    if slotNum == 0:
        return ex_slot_0
    elif slotNum == 1:
        return ex_slot_1
    elif slotNum == 2:
        return ex_slot_2

    return (0, 0)


def chara_center(pos):
    return (
        int(pos[0]),
        int(pos[1])
    )


class OPAgent:
    def __init__(self) -> None:
        self.client = None
        self.device = None
        self.deviceRes = (0, 0)
        self.windowRes = (0, 0)
        self.resRatio = 1
        self.headerCorrection = 0

        deviceAddr = ('localhost', 16384)
        # TODO：54是MuMu header绝对值，
        # 当全屏时，页眉会有额外12px黑边
        # 此外还有因窗口区域宽于16：9时模拟器画面会有额外灰边需要计算
        # 1440p是 12+54+17 = 83px
        self.headerCorrection = 54
        # TODO:后续采用实际计算
        self.resRatio = 1.831
        c, d = self.connect(deviceAddr)
        self.client = c
        self.device = d
        self.deviceRes = self.getResolution()

    def getResolution(self):
        # 获取屏幕分辨率
        resolution_output = self.device.shell("wm size")
        resolution_line = resolution_output.strip().splitlines()[-1]
        resolution_parts = resolution_line.split()[-1].split('x')
        width, height = map(int, resolution_parts)

        # 获取屏幕方向
        rotation_output = self.device.shell(
            "dumpsys input | grep 'SurfaceOrientation'")
        rotation_line = rotation_output.strip()
        rotation = int(rotation_line.split(':')[-1].strip())

        # 根据屏幕方向调整分辨率顺序
        if rotation == 0 or rotation == 2:
            # Portrait
            return min(width, height), max(width, height)
        else:
            # Landscape
            return max(width, height), min(width, height)

    def connect(self, deviceAddr, serverAddr=('localhost', 5037)):
        # 通过shell启动ADB server
        subprocess.run(["adb", "start-server"], check=True)

        HOST, PORT = serverAddr
        DEVICE_IP, DEVICE_PORT = deviceAddr

        # 初始化adb客户端
        client = AdbClient(host=HOST, port=PORT)

        # 连接到远程设备
        device = client.remote_connect(DEVICE_IP, DEVICE_PORT)

        # 获取设备对象
        device = client.device(f"{DEVICE_IP}:{DEVICE_PORT}")

        return client, device

    def coordCorrection(self, x, y):
        # x -= self.headerCorrection
        y -= self.headerCorrection
        x = int(x*self.resRatio)
        y = int(y*self.resRatio)
        return x, y

    def click(self, x, y):
        x, y = self.coordCorrection(x, y)
        # 发送鼠标点击消息
        self.device.shell(f"input tap {x} {y}")

    def drag(self, x_start, y_start, x_end, y_end, duration=100):
        x_start, y_start = self.coordCorrection(x_start, y_start)
        x_end, y_end = self.coordCorrection(x_end, y_end)
        self.device.shell(
            f"input swipe {x_start} {y_start} {x_end} {y_end} {duration}")

    def disconnect(self, deviceAddr):
        DEVICE_IP, DEVICE_PORT = deviceAddr
        # 断开连接
        self.client.remote_disconnect(DEVICE_IP, DEVICE_PORT)

    def castEX(self, state, character, target):
        slotNum = which_slot(character, state.exSlot)
        START_X, START_Y = slot_pos(slotNum)
        END_X, END_Y = chara_center(state.characters[target].pos)
        print(START_X, START_Y, END_X, END_Y)
        self.drag(START_X, START_Y, END_X, END_Y)

if __name__ == "__main__":
    opa = OPAgent()
    opa.click(1224,719)
    # opa.drag(959,677,1114,329)
