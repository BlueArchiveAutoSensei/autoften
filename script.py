import threading
import time
from ppadb.client import Client as AdbClient
import copy


# 默认的adb服务器主机和端口
HOST = '127.0.0.1'
PORT = 5037

# 设备的IP地址和端口（需要根据你的设备进行替换）
DEVICE_IP = 'localhost'
DEVICE_PORT = 16384

# 初始化adb客户端
client = AdbClient(host=HOST, port=PORT)

# 连接到远程设备
device = client.remote_connect(DEVICE_IP, DEVICE_PORT)

# 获取设备对象
device = client.device(f"{DEVICE_IP}:{DEVICE_PORT}")

ex_slot_pos = (1660, 1020, 2280, 1250)  # 原始视频截图的坐标
ex_slot_pos = (1640, 1110, 2300, 1340)  # 照片app全屏截图
ex_slot_pos = (1660, 1110, 2310, 1340)  # win32带Mumu标题栏

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


def judge1(situ):
    return (
        situ is not None and
        situ.exPoint > 4 and
        situ.characters["yoruNoNero"].pos[0] != 0
    )


def script(pipe_conn):

    # ---------------- #

    # 初始化共享数据和锁
    # situ = Situation([])
    shared_data = {
        "situ": None,
        "data_ready": False
    }

    data_lock = threading.Lock()

    def recv_data_thread():
        data = None
        while True:
            while not pipe_conn.poll():
                # print("no")
                pass
            while pipe_conn.poll():
                # print("yes")
                data = pipe_conn.recv()
            if shared_data["data_ready"] == False:
                with data_lock:
                    shared_data["situ"] = data
                    shared_data["data_ready"] = True
                    # print(shared_data["situ"].exPoint)

    # 创建发送线程
    thread = threading.Thread(target=recv_data_thread)
    thread.start()

    # ---------------- #

    situ = None

    print("script rdy!")
    while True:
        # while shared_data["data_ready"] == False:
        #     pass
        if shared_data["data_ready"] == True:
            with data_lock:
                situ = copy.copy(shared_data["situ"])
                # time.sleep(0.1)
                shared_data["data_ready"] = False

        if situ is not None:
            print("main:", situ.exPoint, "??",
                  situ.characters["yoruNoNero"].pos)
            print(situ is not None,
                  situ.exPoint > 2,
                  situ.characters["yoruNoNero"].pos[0] != 0)

        if judge1(situ):
            slotNum = which_slot("akane", situ.exSlot)
            print("slot", slotNum)
            # # drag(hwnd, slot_pos(slotNum), chara_center(situ.characters["yoruNoNero"].pos))
            START_X, START_Y = slot_pos(slotNum)
            END_X, END_Y = chara_center(situ.characters["yoruNoNero"].pos)
            print(START_X, START_Y, END_X, END_Y)
            if START_X != 0 and START_Y != 0:
                pass
            # 83是1440p的修正值，54是720p的修正值
            # END_X -= 83
            # END_Y -= 83
            END_X -= 54
            END_Y -= 54
            END_X *=2
            END_Y *=2
            # 执行滑动操作
            device.shell(f"input swipe {START_X} {START_Y} {END_X} {END_Y}")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("main:", situ.exPoint, "??",
                  situ.characters["yoruNoNero"].pos)
            break


if __name__ == "__main__":
    script(None)
