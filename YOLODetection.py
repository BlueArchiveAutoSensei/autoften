import cv2
import time
import threading
import copy
from ultralytics import YOLO

# yolo会在此函数外预先启动，从pipe_conn_in得到原始截图，
# 预测并打上标记后递交给pipe_conn_out以备后续显示
# 此外，预测结果会从pipe_conn_act送给后续处理
# 当前状态下，裸yolo性能大约50fps
# recv 线程 1440下性能大约15fps（IPC瓶颈）
# 720下（默认窗口大小）性能大约35-40fps
# TODO: IPC优化可以暂缓，但仍不能忽略
def detect_yolo(model: YOLO, pipe_conn_in: Pipe, pipe_conn_act: Pipe, pipe_conn_out: Pipe) -> None:
    # model = YOLO(
    # r"C:\Users\Vickko\code\batrain\runs\detect\train32\weights\best.pt")
    # sys.stderr = open(os.devnull, 'w')
    # sys.stdout = open(os.devnull, 'w')

    # ---------------- #

    # 初始化共享数据和锁
    shared_data = {
        "screenshot": None,
        "data_ready": False,
    }
    data_lock = threading.Lock()

    def read_data_thread() -> None:
        # video_path = r"C:\Users\Vickko\Documents\MuMu共享文件夹\VideoRecords\ブルアカ(17).mp4"
        # cap = cv2.VideoCapture(video_path)
        data = None
        start_time = None
        while True:
            if start_time == None:
                start_time = time.time()
            # time.sleep(0.005)
            # print("while")
            # success, data = cap.read()
            data = pipe_conn_in.recv()
            # print("recv")
            if shared_data["data_ready"] == False:
                # print("child get false")
                # print("false")
                with data_lock:
                    # print("child get lock")
                    shared_data["screenshot"] = data
                    # time.sleep(0.02)
                    shared_data["data_ready"] = True
                    # print("child set true")
                    # cv2.imshow("1", shared_data["screenshot"])
                    # cv2.waitKey(0)
                    # cv2.destroyAllWindows()
                # print("child release lock")
            # frame_rate = 1/(time.time()-start_time)
            # start_time = time.time()
            # print("detect recv speed: ", frame_rate, "fps")

    # 创建读取线程
    thread = threading.Thread(target=read_data_thread)
    thread.start()

    # ---------------- #

    # while True:
    #     pass

    screenshot = None
    # screenshot = cv2.imread(r"C:\Users\Vickko\Pictures\Image34.png")
    start_time = None
    while True:
        if start_time == None:
            start_time = time.time()
        # while not pipe_conn_in.poll():
        #     pass
        # screenshot = pipe_conn_in.recv()

        results = None
        # print(111111)
        # while shared_data["data_ready"] == False:
        #     pass
        # print(222222)
        # print("parent get true")
        if shared_data["data_ready"] == True:
            with data_lock:
                # print("parent get lock")
                # screenshot = copy.deepcopy(shared_data["screenshot"])
                screenshot = shared_data["screenshot"]
                # results = model(screenshot, stream=True, verbose=False)
                shared_data["data_ready"] = False
                # print("parent set false")
            # print("parent release lock")

        if screenshot is not None:
            # predict on an image
            results = model(screenshot, stream=True, verbose=False)
            # print(444444)

            result = None
            for r in results:
                result = r
            # Visualize the results on the frame
            annotated_frame = result.plot()
            # pipe_conn_out.send(annotated_frame)
            pipe_conn_act.send(result.cpu())

            # cv2.imshow("1", annotated_frame)
            # if cv2.waitKey(1) & 0xFF == ord("q"):
            #     cv2.destroyAllWindows()
            #     break

            frame_rate = 1/(time.time()-start_time)
            start_time = time.time()
            # print("detection speed: ", frame_rate, "fps")
