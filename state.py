class Status:
    def __init__(self) -> None:
        self.count_costdown_half = 0


class Character:
    def __init__(self, name, pos, lastSeen):
        self.name = name
        # center (x,y,w,h)
        self.pos = pos
        # (pos, n_frame_ago)
        self.lastSeen = lastSeen
        self.stat = Status()
    # def __init__(self, stu, enemy):
    #     self.stu = stu
    #     self.enemy = enemy


class State:
    def __init__(self, chara_names):
        self.characters = {}
        self.namedic = {}
        for name in chara_names:
            self.characters[name] = Character(
                name, [0, 0, 0, 0], [[0, 0, 0, 0], 0])
            self.namedic[name] = False
        self.exSlot = {}
        self.exPoint = 0

    def updateCharacter(self, result):
        # 识别对象的数字id的集合
        cls_num = result.boxes.cls.numpy().astype(int)
        for i in range(len(cls_num)):
            cls_name = result.names[cls_num[i]]
            self.characters[cls_name].pos = result.boxes.xywh[i]
            self.characters[cls_name].lastSeen = [result.boxes.xywh[i], 0]
            self.namedic[cls_name] = True

        for name in self.namedic:
            if self.namedic[name] == False:
                self.characters[name].lastSeen[0] = self.characters[name].pos
                self.characters[name].lastSeen[1] += 1
                self.characters[name].pos = [0, 0, 0, 0]
                # print("no ", name, ", ")
            else:
                self.namedic[name] = False
                # print(name, "at ", self.characters[name].pos, ", ")

        # print("---------")

    def updateEX(self, result):
        self.exSlot = result[0]
        self.exPoint = result[1]
