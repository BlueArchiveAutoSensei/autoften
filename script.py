import threading
import time
from ppadb.client import Client as AdbClient
import copy
from OPAgent import OPAgent
from state import State


def judge1(state):
    return (
        state is not None and
        state.exPoint > 3 and
        state.characters["yoruNoNero"].pos[0] != 0
    )


def judge2(state):
    return (
        state is not None and
        state.exPoint > 5 and
        state.characters["maidAlice"].pos[0] != 0
    )

def judge3(state):
    return (
        state is not None and
        state.exPoint > 6 and
        state.characters["maidAlice"].pos[0] != 0
    )

def judge4(state):
    return (
        state is not None and
        state.exPoint > 6 and
        state.characters["maidAlice"].pos[0] != 0 and
        state.characters["yoruNoNero"].pos[0] != 0
    )

def judge5(state):
    return (
        state is not None and
        state.exPoint > 5 and
        state.characters["yoruNoNero"].pos[0] != 0
    )

def judge6(state):
    return (
        state is not None and
        state.exPoint > 5 and
        state.characters["maidAlice"].pos[0] != 0
    )

def judge7(state):
    return (
        state is not None and
        state.exPoint > 5 and
        state.characters["maidAlice"].pos[0] != 0
    )

def judge8(state):
    return (
        state is not None and
        state.exPoint > 3 and
        state.characters["maidAlice"].pos[0] != 0
    )




state = State(
    ['ui', 'maidAlice', 'akane', 'newYearKayoko', 'yoruNoNero']
)


# recv_lock = threading.Lock()


def recv_func(pipe_conn_1, pipe_conn_2):
    while True:
        result = pipe_conn_1.recv()
        ex = pipe_conn_2.recv()

        state.updateCharacter(result)
        state.updateEX(ex)


def script_exec(pipe_conn_1, pipe_conn_2):
    # 创建发送线程
    recv_thread = threading.Thread(target=recv_func, args=(pipe_conn_1,pipe_conn_2))
    recv_thread.start()

    opAgent = OPAgent()
    print("script rdy!")
    # while True:
    #         print(state.exPoint)
    while True:
        print(state.exPoint)
        if judge1(state):
            opAgent.castEX(state, "akane", "yoruNoNero")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("JUDGE 1 TRIGGERED")
            print("EXP:", state.exPoint, )
            print("target: ",
                    state.characters["yoruNoNero"].pos)
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            break

    time.sleep(0.2)

    while True:
        print(state.exPoint)
        if judge2(state):
            opAgent.castEX(state, "ui", "maidAlice")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("JUDGE 2 TRIGGERED")
            print("EXP:", state.exPoint, )
            print("target: ",
                    state.characters["maidAlice"].pos)
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            break

    time.sleep(0.2)

    while True:
        print(state.exPoint)
        if judge3(state):
            opAgent.castEX(state, "newYearKayoko", "maidAlice")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("JUDGE 3 TRIGGERED")
            print("EXP:", state.exPoint, )
            print("target: ",
                    state.characters["maidAlice"].pos)
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            break
        
    time.sleep(0.2)
        
    while True:
        print(state.exPoint)
        if judge4(state):
            opAgent.castEX(state, "himari", "maidAlice")
            opAgent.castEX(state, "maidAlice", "yoruNoNero")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("JUDGE 4 TRIGGERED")
            print("EXP:", state.exPoint, )
            print("target: ",
                    state.characters["yoruNoNero"].pos)
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            break

    time.sleep(0.2)
        
    while True:
        print(state.exPoint)
        if judge5(state):
            opAgent.castEX(state, "akane", "yoruNoNero")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("JUDGE 5 TRIGGERED")
            print("EXP:", state.exPoint, )
            print("target: ",
                    state.characters["yoruNoNero"].pos)
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            break
    
    time.sleep(0.2)
        
    while True:
        print(state.exPoint)
        if judge6(state):
            opAgent.castEX(state, "newYearKayoko", "maidAlice")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("JUDGE 6 TRIGGERED")
            print("EXP:", state.exPoint, )
            print("target: ",
                    state.characters["maidAlice"].pos)
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            break

    time.sleep(0.2)
        
    while True:
        print(state.exPoint)
        if judge7(state):
            opAgent.castEX(state, "himari", "maidAlice")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("JUDGE 7 TRIGGERED")
            print("EXP:", state.exPoint, )
            print("target: ",
                    state.characters["maidAlice"].pos)
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            break

    time.sleep(0.2)
        
    while True:
        print(state.exPoint)
        if judge8(state):
            opAgent.castEX(state, "maidAlice", "yoruNoNero")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("JUDGE 8 TRIGGERED")
            print("EXP:", state.exPoint, )
            print("target: ",
                    state.characters["maidAlice"].pos)
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            break
    
