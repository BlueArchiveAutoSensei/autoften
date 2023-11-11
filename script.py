import threading
import time
from ppadb.client import Client as AdbClient
import copy
from OPAgent import OPAgent


def judge1(situ):
    return (
        situ is not None and
        situ.exPoint > 3 and
        situ.characters["yoruNoNero"].pos[0] != 0
    )


def script(pipe_conn):

    # ---------------- #

    # 初始化共享数据和锁
    # situ = Situation([])
    shared_data = {
        "situ": None,
        "data_ready": False
    }

    data_lock = threading.Lock()

    def recv_data_thread():
        data = None
        while True:
            while not pipe_conn.poll():
                # print("no")
                pass
            while pipe_conn.poll():
                # print("yes")
                data = pipe_conn.recv()
            if shared_data["data_ready"] == False:
                with data_lock:
                    shared_data["situ"] = data
                    shared_data["data_ready"] = True
                    # print(shared_data["situ"].exPoint)

    # 创建发送线程
    thread = threading.Thread(target=recv_data_thread)
    thread.start()

    # ---------------- #

    state = None
    opAgent = OPAgent()

    print("script rdy!")
    while True:
        # while shared_data["data_ready"] == False:
        #     pass
        if shared_data["data_ready"] == True:
            with data_lock:
                state = copy.copy(shared_data["situ"])
                # time.sleep(0.1)
                shared_data["data_ready"] = False

        if state is not None:
            print("main:", state.exPoint, "??",
                  state.characters["yoruNoNero"].pos)
            print(state is not None,
                  state.exPoint > 3,
                  state.characters["yoruNoNero"].pos[0] != 0)

        if judge1(state):
            opAgent.castEX(state,"akane","yoruNoNero")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("main:", state.exPoint, "??",
                  state.characters["yoruNoNero"].pos)
            break


if __name__ == "__main__":
    script(None)
