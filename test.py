import cv2
from windowCapture import screenshot_window_win32
from YOLODetection import detect_yolo
from config import Config, init
from processManager import ProcessManager
from UIPositioning import ui_positioning_pipe
import time
import threading
from OPAgent import click, drag
from ppadb.client import Client as AdbClient
from script import script

# class Stu:


class Status:
    def __init__(self) -> None:
        self.count_costdown_half = 0


class Character:
    def __init__(self, name, pos, lastSeen):
        self.name = name
        # center (x,y,w,h)
        self.pos = pos
        # (pos, n_frame_ago)
        self.lastSeen = lastSeen
        self.stat = Status()
    # def __init__(self, stu, enemy):
    #     self.stu = stu
    #     self.enemy = enemy


class Situation:
    def __init__(self, chara_names):
        self.characters = {}
        self.namedic = {}
        for name in chara_names:
            self.characters[name] = Character(
                name, [0, 0, 0, 0], [[0, 0, 0, 0], 0])
            self.namedic[name] = False
        self.exSlot = {}
        self.exPoint = 0

    def updateCharacter(self, result):
        # 识别对象的数字id的集合
        cls_num = result.boxes.cls.numpy().astype(int)
        for i in range(len(cls_num)):
            cls_name = result.names[cls_num[i]]
            self.characters[cls_name].pos = result.boxes.xywh[i]
            self.characters[cls_name].lastSeen = [result.boxes.xywh[i], 0]
            self.namedic[cls_name] = True

        for name in self.namedic:
            if self.namedic[name] == False:
                self.characters[name].lastSeen[0] = self.characters[name].pos
                self.characters[name].lastSeen[1] += 1
                self.characters[name].pos = [0, 0, 0, 0]
                # print("no ", name, ", ")
            else:
                self.namedic[name] = False
                # print(name, "at ", self.characters[name].pos, ", ")

        # print("---------")

    def updateEX(self, result):
        self.exSlot = result[0]
        self.exPoint = result[1]


tempSitu = Situation(
    ['ui', 'maidAlice', 'akane', 'newYearKayoko', 'yoruNoNero'])


def update_for_situ(pipe_conn_1, pipe_conn_2, pipe_conn_out):
    while True:
        results = pipe_conn_1.recv()
        tempSitu.updateCharacter(results)
        ex = pipe_conn_2.recv()
        tempSitu.updateEX(ex)
        # print("update", tempSitu.exPoint)

        # ex = ex_positioning()
        pipe_conn_out.send(tempSitu)


# 将截图用cv窗口显示出来
# TODO: 大约100ms延迟，考虑使用：
# 1. 硬件加速
# 2. 更高效的截图库（mss)
# 3. 使用共享内存(multiprocessing 的 shared_memory)
# 4. opencv -> pygame/pyqt
# 5. 线程
def show_image_cv2(pipe_conn, width, height):

    screenshot = None
    while True:
        while not pipe_conn.poll():
            pass
        while pipe_conn.poll():
            screenshot = pipe_conn.recv()
        if screenshot is None:
            break  # 结束进程
        # # Convert RGB to BGR (OpenCV uses BGR by default, but pyautogui.screenshot returns RGB)
        # frame_rgb = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        # Resize the image to 1/2 of its original dimensions
        resized_frame = cv2.resize(screenshot, (width // 2, height // 2))
        # Display the image using OpenCV
        cv2.imshow('BAAS', resized_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # sys.stderr = open(os.devnull, 'w')
    # sys.stdout = open(os.devnull, 'w')

    config = Config()
    init(config)

    pm = ProcessManager()
    # 创建管道来传递截图
    pm.appendPipe("pipe1to2")
    pm.appendPipe("pipe2to3")
    pm.appendPipe("pipe1to4")
    pm.appendPipe("pipe4toact")
    pm.appendPipe("pipe_act")
    pm.appendPipe("pipe_script")

    # 创建并启动两个子进程
    pm.appendProcess(screenshot_window_win32,
                     (config.hwnd, config.pos, config.size,
                      pm.pipeMap['pipe1to2'][0], pm.pipeMap['pipe1to4'][0]))
    pm.appendProcess(ui_positioning_pipe,
                     (pm.pipeMap['pipe1to4'][1], pm.pipeMap['pipe4toact'][0],
                      config.ex_template_path, config.ex_point_template_path,
                      config.ex_slot_pos, config.ex_bar_pos,
                      config.tempMatch_threshold))
    pm.appendProcess(detect_yolo,
                     (config.model,
                      pm.pipeMap['pipe1to2'][1], pm.pipeMap['pipe_act'][0], pm.pipeMap['pipe2to3'][0]))
    pm.appendProcess(update_for_situ,
                     (pm.pipeMap['pipe_act'][1], pm.pipeMap['pipe4toact'][1], pm.pipeMap['pipe_script'][0]))
    pm.appendProcess(show_image_cv2,
                     (pm.pipeMap['pipe2to3'][1], *config.size))
    pm.appendProcess(script, (pm.pipeMap['pipe_script'][1],))

    startSequence = ['show_image_cv2',
                     'screenshot_window_win32',
                     'ui_positioning_pipe',
                     'detect_yolo',
                     'update_for_situ',
                     'script'
                     ]
    startSequence = [
                     'screenshot_window_win32',
                     'ui_positioning_pipe',
                     'detect_yolo',
                     'update_for_situ',
                     'script'
                     ]

    pm.startBySequence(startSequence)

    pm.terminateProcesses(keyProcessName='show_image_cv2')


###############################################################
#                         screenshot_window_win32             #
#                         ↓                       ↘          #
#               detect_yolo                 ui_positioning    #
#               ↓         ↘             ↙                   #
#  show_image_cv2          update_for_situ                    #
###############################################################
