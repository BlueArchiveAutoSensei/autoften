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
        state.characters["yoruNoNero"].pos[0] != 0
    )

def judge9(state):
    return (
        state is not None and
        state.exPoint > 5 and
        state.characters["yoruNoNero"].pos[0] != 0
    )

def judge10(state):
    return (
        state is not None and
        state.exPoint > 4 and
        state.characters["maidAlice"].pos[0] != 0
    )

def judge11(state):
    return (
        state is not None and
        state.exPoint > 4 and
        state.characters["maidAlice"].pos[0] != 0
    )

def judge12(state):
    return (
        state is not None and
        state.exPoint > 9 and
        state.characters["yoruNoNero"].pos[0] != 0
    )

def judge13(state):
    return (
        state is not None and
        state.exPoint > 8 and
        state.characters["yoruNoNero"].pos[0] != 0
    )

def judge14(state):
    return (
        state is not None and
        state.exPoint > 6 and
        state.characters["maidAlice"].pos[0] != 0
    )

def judge15(state):
    return (
        state is not None and
        state.exPoint > 8 and
        state.characters["maidAlice"].pos[0] != 0
    )

def judge16(state):
    return (
        state is not None and
        state.exPoint > 2 and
        state.characters["yoruNoNero"].pos[0] != 0
    )

def judge17(state):
    return (
        state is not None and
        state.exPoint > 8 and
        state.characters["yoruNoNero"].pos[0] != 0
    )

def judge18(state):
    return (
        state is not None and
        state.exPoint > 8 and
        state.characters["yoruNoNero"].pos[0] != 0
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
    recv_thread = threading.Thread(
        target=recv_func, args=(pipe_conn_1, pipe_conn_2))
    recv_thread.start()

    opAgent = OPAgent()
    print("script rdy!")
    # while True:
    #         #print(state.exPoint)

    # boss stage 1
    # akane 挂破甲
    while True:
        #print(state.exPoint)
        time.sleep(0.001)
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

    # boss stage 1
    # ui 给 maidAlice 上减费
    while True:
        #print(state.exPoint)
        time.sleep(0.001)
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

    # boss stage 1
    # newYearKayoko 增伤 maidAlice
    while True:
        #print(state.exPoint)
        time.sleep(0.001)
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

    # boss stage 1
    # himari 单拐 maidAlice 攻击
    while True:
        #print(state.exPoint)
        time.sleep(0.001)
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

    # boss stage 2
    # akane 挂破甲
    while True:
        #print(state.exPoint)
        time.sleep(0.001)
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

    # boss stage 2
    # newYearKayoko 增伤 maidAlice
    while True:
        #print(state.exPoint)
        time.sleep(0.001)
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

    # boss stage 2
    # himari 单拐 maidAlice
    while True:
        #print(state.exPoint)
        time.sleep(0.001)
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

    # boss stage 2
    # maidAlice攻击
    while True:
        #print(state.exPoint)
        time.sleep(0.001)
        if judge8(state):
            opAgent.castEX(state, "maidAlice", "yoruNoNero")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("JUDGE 8 TRIGGERED")
            print("EXP:", state.exPoint, )
            print("target: ",
                  state.characters["yoruNoNero"].pos)
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            break

    time.sleep(0.2)

    # boss stage 3
    # akane 挂破甲
    while True:
        #print(state.exPoint)
        time.sleep(0.001)
        if judge9(state):
            opAgent.castEX(state, "akane", "yoruNoNero")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("JUDGE 9 TRIGGERED")
            print("EXP:", state.exPoint, )
            print("target: ",
                  state.characters["yoruNoNero"].pos)
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            break

    
    time.sleep(0.2)

    # boss stage 3
    # ui 给 maidAlice 上减费
    while True:
        #print(state.exPoint)
        time.sleep(0.001)
        if judge10(state):
            opAgent.castEX(state, "ui", "maidAlice")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("JUDGE 10 TRIGGERED")
            print("EXP:", state.exPoint, )
            print("target: ",
                  state.characters["maidAlice"].pos)
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            break

    
    time.sleep(0.2)

    # boss stage 3
    # newYearKayoko 增伤 maidAlice
    while True:
        #print(state.exPoint)
        time.sleep(0.001)
        if judge11(state):
            opAgent.castEX(state, "newYearKayoko", "maidAlice")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("JUDGE 11 TRIGGERED")
            print("EXP:", state.exPoint, )
            print("target: ",
                  state.characters["maidAlice"].pos)
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            break

    time.sleep(0.2)

    # boss stage 3
    # himari 单拐 maidAlice 攻击
    while True:
        #print(state.exPoint)
        time.sleep(0.001)
        if judge12(state):
            opAgent.castEX(state, "himari", "maidAlice")
            opAgent.castEX(state, "maidAlice", "yoruNoNero")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("JUDGE 12 TRIGGERED")
            print("EXP:", state.exPoint, )
            print("target: ",
                  state.characters["yoruNoNero"].pos)
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            break

    
    time.sleep(0.2)

    # boss stage 4
    # akane挂破甲
    while True:
        #print(state.exPoint)
        time.sleep(0.001)
        if judge13(state):
            opAgent.castEX(state, "akane", "yoruNoNero")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("JUDGE 13 TRIGGERED")
            print("EXP:", state.exPoint, )
            print("target: ",
                  state.characters["yoruNoNero"].pos)
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            break

    
    time.sleep(0.2)

    # boss stage 4
    # newYearKayoko 增伤 maidAlice
    while True:
        #print(state.exPoint)
        time.sleep(0.001)
        if judge14(state):
            opAgent.castEX(state, "newYearKayoko", "maidAlice")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("JUDGE 14 TRIGGERED")
            print("EXP:", state.exPoint, )
            print("target: ",
                  state.characters["maidAlice"].pos)
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            break

    
    time.sleep(0.2)

    # boss stage 4
    # 双拐 maidAlice
    while True:
        #print(state.exPoint)
        time.sleep(0.001)
        if judge15(state):
            opAgent.castEX(state, "himari", "maidAlice")
            opAgent.castEX(state, "ako", "maidAlice")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("JUDGE 15 TRIGGERED")
            print("EXP:", state.exPoint, )
            print("target: ",
                  state.characters["maidAlice"].pos)
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            break
    
    time.sleep(0.2)

    # boss stage 4
    # maidAlice 攻击
    while True:
        #print(state.exPoint)
        time.sleep(0.001)
        if judge16(state):
            opAgent.castEX(state, "maidAlice", "yoruNoNero")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("JUDGE 16 TRIGGERED")
            print("EXP:", state.exPoint, )
            print("target: ",
                  state.characters["yoruNoNero"].pos)
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            break
    
    time.sleep(0.2)

    # boss stage 5
    # 垫三buff
    while True:
        #print(state.exPoint)
        time.sleep(0.001)
        if judge17(state):
            opAgent.castEX(state, "akane", "yoruNoNero")
            opAgent.castEX(state, "ui", "maidAlice")
            opAgent.castEX(state, "newYearKayoko", "maidAlice")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("JUDGE 17 TRIGGERED")
            print("EXP:", state.exPoint, )
            print("target: ",
                  state.characters["yoruNoNero"].pos)
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            break
    
    time.sleep(0.2)

    # boss stage 5
    # 反手拐maidAlice
    while True:
        #print(state.exPoint)
        time.sleep(0.001)
        if judge18(state):
            opAgent.castEX(state, "maidAlice", "yoruNoNero")
            opAgent.castEX(state, "himari", "maidAlice")
            opAgent.castEX(state, "ako", "maidAlice")
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            print("JUDGE 18 TRIGGERED")
            print("EXP:", state.exPoint, )
            print("target: ",
                  state.characters["yoruNoNero"].pos)
            print("[][][][][][][]]][][][][][][][][][]][][][][][]")
            break
