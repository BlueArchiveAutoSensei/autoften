import multiprocessing


sender_conn, receiver_conn = multiprocessing.Pipe()


class ProcessManager:
    def __init__(self) -> None:
        self.queueMap: dict[str, multiprocessing.Queue] = {}
        self.pipeMap: dict[str, list] = {}
        self.processMap: dict[str, multiprocessing.Process] = {}
        self.startSeq: list[str] = []

    def appendProcess(self, target: callable, args: tuple) -> None:
        self.processMap[target.__name__] = multiprocessing.Process(
            target=target, args=args)

    def appendQueue(self, name: str) -> None:
        self.queueMap[name] = multiprocessing.Queue()

    def appendPipe(self, name: str) -> None:
        x, y = multiprocessing.Pipe()
        self.pipeMap[name] = [x, y]

    def startBySequence(self, seq: list[str]):
        self.startSeq = seq
        for s in seq:
            self.processMap[s].start()
            print("start", s)

    # 按以下逻辑结束所有进程：
    # 当指定进程名且存在此进程时，关键进程为此指定进程
    # 当未指定或指定错误进程名时， 关键进程为启动顺序的最后一个
    # 无限等待关键进程结束，达成时，关闭其他所有进程。
    def terminateProcesses(self, keyProcessName: str = "") -> None:

        if keyProcessName == '' or keyProcessName not in self.startSeq:
            keyProcess = self.processMap[self.startSeq[-1]]
            keyProcessName = self.startSeq[-1]
        else:
            keyProcess = self.processMap[keyProcessName]

        while True:
            if not keyProcess.is_alive():
                for s in self.startSeq:
                    if s != keyProcessName:
                        self.processMap[s].terminate()
                break

        # 等待所有子进程结束
        for s in self.startSeq:
            self.processMap[s].join()


# processManager前的原始逻辑：

    # # 创建两个队列来传递截图
    # queue1to2 = multiprocessing.Queue()
    # queue2to3 = multiprocessing.Queue()
    # queue_act = multiprocessing.Queue()
    # # 创建并启动两个子进程
    # p4 = multiprocessing.Process(
    #     target=show_image_cv2, args=(queue2to3, *config.size))
    # p1 = multiprocessing.Process(
    #     target=screenshot_window_win32, args=(config.hwnd, config.pos, config.size, queue1to2))
    # p2 = multiprocessing.Process(
    #     target=detect_yolo, args=(config.model, queue1to2, queue_act, queue2to3))
    # p3 = multiprocessing.Process(
    #     target=update_for_situ, args=(queue_act,))
    # p4.start()
    # print("p4 start")
    # p1.start()
    # print("p1 start")
    # p2.start()
    # print("p2 start")
    # p3.start()
    # print("p3 start")

    # while True:
    #     if not p4.is_alive():
    #         # 如果 p4 已停止，终止 p1p2
    #         p1.terminate()
    #         p2.terminate()
    #         p3.terminate()
    #         break

    # # 等待所有子进程结束
    # p1.join()
    # p2.join()
    # p3.join()
    # p4.join()
