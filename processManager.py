import multiprocessing


sender_conn, receiver_conn = multiprocessing.Pipe()


class ProcessManager:
    def __init__(self) -> None:
        self.pipeMap: dict[str, list] = {}
        self.processMap: dict[str, multiprocessing.Process] = {}
        self.startSeq: list[str] = []

    def appendProcess(self, target: callable, args: tuple) -> None:
        self.processMap[target.__name__] = multiprocessing.Process(
            target=target, args=args)

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

