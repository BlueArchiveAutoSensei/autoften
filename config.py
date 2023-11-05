from windowCapture import pos_window_win32
from ultralytics import YOLO


class Config:
    def __init__(self) -> None:
        self.windowTitle = "Mumu模拟器12"
        # self.windowTitle = "任务管理器"
        # self.windowTitle = "Image34.png ‎- 照片"
        # self.windowTitle = "ブルアカ(17).mp4 - VLC Media Player"
        self.yoloModelPath = r"C:\Users\Vickko\code\batrain\runs\detect\train32\weights\best.pt"
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
