import pyautogui
import cv2
import numpy as np
import multiprocessing
from ultralytics import YOLO
import mss
import os
import sys

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

    def update(self, result):
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
                print("no ", name, ", ")
            else:
                self.namedic[name] = False
                print(name, "at ", self.characters[name].pos, ", ")

        print("---------")


tempSitu = Situation(
    ['ui', 'maidAlice', 'akane', 'newYearKayoko', 'yoruNoNero'])


def update_for_situ(queue):
    while True:
        results = queue.get()
        tempSitu.update(results)


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
def screenshot_window_new(pos, queue):
    with mss.mss() as sct:
        left, top, width, height = pos
        monitor = {"top": top, "left": left, "width": width, "height": height}
        screenshot = sct.grab(monitor)
        # Convert the screenshot to a NumPy array
        frame_bgr = np.array(screenshot)
        queue.put(frame_bgr)


# yolo会在此函数外预先启动，从queue_in得到原始截图，
# 预测并打上标记后递交给queue_out以备后续显示
def detect_yolo(model, queue_in, queue_act, queue_out):
    # sys.stderr = open(os.devnull, 'w')
    # sys.stdout = open(os.devnull, 'w')
    while True:
        screenshot = queue_in.get()
        # predict on an image
        results = model(screenshot, verbose=False)
        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        queue_out.put(annotated_frame)
        queue_act.put(results[0].cpu())


# 将截图用cv窗口显示出来
# TODO: 大约100ms延迟，考虑使用：
# 1. 硬件加速
# 2. 更高效的截图库（mss)
# 3. 使用共享内存(multiprocessing 的 shared_memory)
# 4. opencv -> pygame/pyqt
# 5. 线程
def show_image_cv2(queue, width, height):
    while True:
        screenshot = queue.get()
        if screenshot is None:
            break  # 结束进程
        # Convert RGB to BGR (OpenCV uses BGR by default, but pyautogui.screenshot returns RGB)
        frame_rgb = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        # Resize the image to 1/2 of its original dimensions
        resized_frame = cv2.resize(frame_rgb, (width // 2, height // 2))
        # Display the image using OpenCV
        cv2.imshow('BAAS', resized_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":

    # sys.stderr = open(os.devnull, 'w')
    # sys.stdout = open(os.devnull, 'w')

    title = "Mumu模拟器12"
    model_path = r"C:\Users\Vickko\code\batrain\runs\detect\train34\weights\best.pt"
    # 启动时获取窗口位置，后续不再更新，因此目前不允许移动模拟器位置
    pos = get_window_position_and_size(title)
    # Load a model
    model = YOLO(model_path)

    # 创建两个队列来传递截图
    queue1to2 = multiprocessing.Queue()
    queue2to3 = multiprocessing.Queue()
    queue_act = multiprocessing.Queue()
    # 创建并启动两个子进程
    p4 = multiprocessing.Process(
        target=show_image_cv2, args=(queue2to3, pos[2], pos[3]))
    p1 = multiprocessing.Process(
        target=screenshot_window, args=(pos, queue1to2))
    p2 = multiprocessing.Process(
        target=detect_yolo, args=(model, queue1to2, queue_act, queue2to3))
    p3 = multiprocessing.Process(
        target=update_for_situ, args=(queue_act,))
    p1.start()
    p2.start()
    p3.start()
    p4.start()

    while True:
        if not p4.is_alive():
            # 如果 p4 已停止，终止 p1p2
            p1.terminate()
            p2.terminate()
            p3.terminate()
            break

    # 等待所有子进程结束
    p1.join()
    p2.join()
    p3.join()
    p4.join()
