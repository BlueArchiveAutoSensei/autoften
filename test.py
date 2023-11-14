import cv2
from windowCapture import screenshot_window_win32
from YOLODetection import detect_yolo
from config import init
from processManager import ProcessManager
from UIPositioning import ui_positioning_pipe
from script import script_exec



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


def main():
    # sys.stderr = open(os.devnull, 'w')
    # sys.stdout = open(os.devnull, 'w')

    config = init()

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
    pm.appendProcess(script_exec,
                     (pm.pipeMap['pipe_act'][1], pm.pipeMap['pipe4toact'][1]))
    pm.appendProcess(show_image_cv2,
                     (pm.pipeMap['pipe2to3'][1], *config.size))



    startSequence = ['show_image_cv2',
                     'screenshot_window_win32',
                     'ui_positioning_pipe',
                     'detect_yolo',
                     'script_exec',
                     ]
    startSequence = [
                     'screenshot_window_win32',
                     'ui_positioning_pipe',
                     'detect_yolo',
                     'script_exec',
                     ]

    pm.startBySequence(startSequence)

    pm.terminateProcesses(keyProcessName='show_image_cv2')


###############################################################
#                         screenshot_window_win32             #
#                         ↓                       ↘          #
#               detect_yolo                 ui_positioning    #
#               ↓         ↘             ↙                   #
#  show_image_cv2            script_exec                      #
###############################################################

if __name__ == "__main__":
    main()