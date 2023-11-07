from windowCapture import pos_window_win32
from ultralytics import YOLO
import win32api

# 获取屏幕分辨率
def get_screen_resolution():
    width = win32api.GetSystemMetrics(0)
    height = win32api.GetSystemMetrics(1)
    return width, height

class Config:
    def __init__(self) -> None:
        self.windowTitle = "Mumu模拟器12"
        # self.windowTitle = "任务管理器"
        # self.windowTitle = "Image34.png ‎- 照片"
        # self.windowTitle = "ブルアカ(17).mp4 - VLC Media Player"
        self.defaultRes = (2560,1600)
        self.currentRes = get_screen_resolution()
        self.scale = 1
        self.yoloModelPath = r"C:\Users\Vickko\code\batrain\runs\detect\train32\weights\best.pt"
        self.ex_template_path = r"C:\Users\Vickko\Pictures\workspace"
        self.ex_point_template_path = r"C:\Users\Vickko\Pictures\line.png"
        self.ex_slot_pos = (1660, 1020, 2280, 1250) # 原始视频截图的坐标
        self.ex_slot_pos = (1640, 1110, 2300, 1340) # 照片app全屏截图
        self.ex_slot_pos = (1660, 1110, 2310, 1340) # win32带Mumu标题栏
        self.ex_bar_pos = (1640, 1250, 2285, 1316)  # 原始视频截图的坐标
        self.ex_bar_pos = (1640, 1350, 2285, 1400)  # 照片app全屏win32
        self.ex_bar_pos = (1640, 1342, 2285, 1385)  # 照片app全屏截图
        self.ex_bar_pos = (1648, 1345, 2298, 1400)  # win32带Mumu标题栏
        self.tempMatch_threshold = 0.6
        self.model = None
        self.hwnd = None
        self.pos = None
        self.size = None


def init(config: Config) -> None:
    print("capturing window:", config.windowTitle)
    print("yolo model path", config.yoloModelPath)
    # TODO: 由于截图已经换用win32API，
    # 目前截图实现里貌似不依赖角点坐标
    # 因此可以删除
    # 且，win32实现不依赖于窗口和屏幕的相对位置
    # 因此移动窗口不会导致捕获偏移。
    # 但目前缩放依然会导致捕获不全，因此需要注意
    config.hwnd, config.pos, config.size, config.scale = pos_window_win32(config.windowTitle)
    # Load a model
    config.model = YOLO(config.yoloModelPath)
