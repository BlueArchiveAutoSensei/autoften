from windowCapture import pos_window_win32
from ultralytics import YOLO


class Config:
    def __init__(self) -> None:
        self.windowTitle = "Mumu模拟器12"
        # self.windowTitle = "任务管理器"
        # self.windowTitle = "Image34.png ‎- 照片"
        # self.windowTitle = "ブルアカ(17).mp4 - VLC Media Player"
        self.yoloModelPath = r"C:\Users\Vickko\code\batrain\runs\detect\train32\weights\best.pt"
        self.ex_template_path = r"C:\Users\Vickko\Pictures\workspace"
        self.ex_point_template_path = r"C:\Users\Vickko\Pictures\line.png"
        self.ex_slot_pos = (1660, 1020, 2280, 1250) # 原始视频截图的坐标
        self.ex_slot_pos = (1660, 1110, 2310, 1340) # win32带Mumu标题栏
        self.ex_slot_pos = (1640, 1110, 2300, 1340) # 照片app全屏截图
        self.ex_bar_pos = (1640, 1250, 2285, 1316)  # 原始视频截图的坐标
        self.ex_bar_pos = (1640, 1342, 2285, 1385)  # win32带Mumu标题栏
        self.ex_bar_pos = (1648, 1345, 2298, 1400)  # 照片app全屏截图
        self.ex_bar_pos = (1640, 1350, 2285, 1400)  # 照片app全屏win32
        self.tempMatch_threshold = 0.6
        self.model = None
        self.hwnd = None
        self.pos = None
        self.size = None


def init(config: Config) -> None:
    print("capturing window:", config.windowTitle)
    print("yolo model path", config.yoloModelPath)
    # 启动时获取窗口位置，后续不再更新，因此目前不允许移动模拟器位置
    config.hwnd, config.pos, config.size = pos_window_win32(config.windowTitle)
    # Load a model
    config.model = YOLO(config.yoloModelPath)
