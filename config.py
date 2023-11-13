from windowCapture import pos_window_win32
from ultralytics import YOLO
import win32api
from pydantic import BaseModel
import yaml
from typing import Tuple, Optional, Any


# 获取屏幕分辨率
def get_screen_resolution():
    width = win32api.GetSystemMetrics(0)
    height = win32api.GetSystemMetrics(1)
    return width, height


class Config(BaseModel):
    windowTitle: str = ""
    defaultRes: Tuple[int, int] = (0,0)
    currentRes: Tuple[int, int] = (0,0)
    scale: float = 1.0
    yoloModelPath: str = ""
    ex_template_path: str = ""
    ex_point_template_path: str = ""
    ex_slot_pos: Tuple[int, int, int, int] = (0,0,0,0)
    ex_bar_pos: Tuple[int, int, int, int] = (0,0,0,0)
    tempMatch_threshold: float = 1.0
    adb_server_ip: str = ""
    adb_server_port: int = 0
    adb_device_ip: str = ""
    adb_device_port: int = 0
    model: Optional[Any] = None
    hwnd: Optional[int] = None
    pos: Optional[Tuple[int, int]] = None
    size: Optional[Tuple[int, int]] = None

    def __str__(self):
        return (
            f"Config(\n"
            f"  windowTitle: {self.windowTitle},\n"
            f"  defaultRes: {self.defaultRes},\n"
            f"  currentRes: {self.currentRes},\n"
            f"  scale: {self.scale},\n"
            f"  yoloModelPath: {self.yoloModelPath},\n"
            f"  ex_template_path: {self.ex_template_path},\n"
            f"  ex_point_template_path: {self.ex_point_template_path},\n"
            f"  ex_slot_pos: {self.ex_slot_pos},\n"
            f"  ex_bar_pos: {self.ex_bar_pos},\n"
            f"  tempMatch_threshold: {self.tempMatch_threshold},\n"
            f"  adb_server_ip: {self.adb_server_ip},\n"
            f"  adb_server_port: {self.adb_server_port},\n"
            f"  adb_device_ip: {self.adb_device_ip},\n"
            f"  adb_device_port: {self.adb_device_port}\n"
            f"  hwnd: {self.hwnd}\n"
            f"  pos: {self.pos}\n"
            f"  size: {self.size}\n"
            f")"
        )


# 为什么不用__init__:
# 因为会破坏Pydantic的初始化逻辑。
# 要么用post init hook，要么额外写个func
# 但我觉得这样额外写func好看点
def init() -> Config:

    config_file_path = "config.yaml"
    with open(config_file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    # 使用Pydantic创建实例
    config = Config(**data)



    # For Debug use
    config.windowTitle = "Mumu模拟器12"
    # config.windowTitle = "任务管理器"
    # config.windowTitle = "Image34.png ‎- 照片"
    # config.windowTitle = "ブルアカ(17).mp4 - VLC Media Player"
    config.ex_slot_pos = (1660, 1020, 2280, 1250)  # 原始视频截图的坐标
    config.ex_slot_pos = (1640, 1110, 2300, 1340)  # 照片app全屏截图
    config.ex_slot_pos = (1660, 1110, 2310, 1340)  # win32带MuMu标题栏
    config.ex_slot_pos = (900, 615, 1255, 740)  # win32带MuMu标题栏720p
    config.ex_bar_pos = (1640, 1250, 2285, 1316)  # 原始视频截图的坐标
    config.ex_bar_pos = (1640, 1350, 2285, 1400)  # 照片app全屏win32
    config.ex_bar_pos = (1640, 1342, 2285, 1385)  # 照片app全屏截图
    config.ex_bar_pos = (1648, 1345, 2298, 1400)  # win32带MuMu标题栏
    config.ex_bar_pos = (895, 740, 1248, 770)  # win32带MuMu标题栏720p

    config.currentRes = get_screen_resolution()
    # TODO: 由于截图已经换用win32API，
    # 目前截图实现里貌似不依赖角点坐标
    # 因此可以删除
    # 且，win32实现不依赖于窗口和屏幕的相对位置
    # 因此移动窗口不会导致捕获偏移。
    # 但目前缩放依然会导致捕获不全，因此需要注意
    config.hwnd, config.pos, config.size, config.scale = pos_window_win32(
        config.windowTitle)
    # Load a model
    config.model = YOLO(config.yoloModelPath)

    print("capturing window:", config.windowTitle)
    print("yolo model path:", config.yoloModelPath)

    print()    
    print(config)    


    return config
