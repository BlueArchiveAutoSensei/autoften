import pyautogui
import cv2
import numpy as np
import mss
from windowCapture import pos_window_win32, screenshot_window_win32
import time
from config import Config, init
from processManager import ProcessManager

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
def screenshot_window_mss(pos, queue):
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

    screenshot = None
    start_time = None
    while True:
        while queue_in.empty():
            pass
        if start_time == None:
            start_time = time.time()
        # while not queue_in.empty():
        #     screenshot = queue_in.get()
        screenshot = queue_in.get()
        # predict on an image
        results = model(screenshot, stream=True, verbose=False)
        # results = model(r"C:\Users\Vickko\Documents\MuMu共享文件夹\VideoRecords\ブルアカ(17).mp4",stream=True,verbose=False)

        result = None
        for r in results:
            result = r
        # Visualize the results on the frame
        annotated_frame = result.plot()
        queue_out.put(annotated_frame)
        queue_act.put(result.cpu())
        frame_rate = 1/(time.time()-start_time)
        start_time = time.time()
        print("detection speed: ", frame_rate, "fps")


# 将截图用cv窗口显示出来
# TODO: 大约100ms延迟，考虑使用：
# 1. 硬件加速
# 2. 更高效的截图库（mss)
# 3. 使用共享内存(multiprocessing 的 shared_memory)
# 4. opencv -> pygame/pyqt
# 5. 线程
def show_image_cv2(queue, width, height):
    screenshot = None
    
    while True:
        while queue.empty():
            pass
        while not queue.empty():
            screenshot = queue.get()
        #screenshot = queue.get()
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
    # 创建两个队列来传递截图
    pm.appendQueue("queue1to2")
    pm.appendQueue("queue2to3")
    pm.appendQueue("queue_act")
    # 创建并启动两个子进程
    pm.appendProcess(screenshot_window_win32,
                     (config.hwnd, config.pos, config.size, pm.queueMap['queue1to2']))
    pm.appendProcess(detect_yolo,
                     (config.model,
                      pm.queueMap['queue1to2'], pm.queueMap['queue_act'], pm.queueMap['queue2to3']))
    pm.appendProcess(update_for_situ,
                     (pm.queueMap['queue_act'],))
    pm.appendProcess(show_image_cv2,
                     (pm.queueMap['queue2to3'], *config.size))

    # pm.startBySequence(['screenshot_window_win32',
    #                     'detect_yolo',
    #                     ])
    pm.startBySequence(['show_image_cv2',
                        'screenshot_window_win32',
                        'detect_yolo',
                        'update_for_situ'])

    pm.terminateProcesses(keyProcessName='show_image_cv2')
