import re
import sys


class Elevator:
    def __init__(self, id):
        self.id = id
        self.lastFloor = 0  # 上次到达的楼层
        self.lastArrivedTime = -1  # 上次到达楼层的时间
        self.num = 0  # 电梯内的乘客人数
        self.receivedNum = 0  # 接收的请求数
        self.isClosed = True  # 电梯门是否关闭
        self.speed = 0.4  # 电梯速度
        self.scheSpeed = 0.4  # 电梯临时调度速度
        self.passengerList = []  # 乘客列表

        # 临时调度相关
        self.isSche = False  # 是否处于临时调度中
        self.isScheAccepted = False  # 是否接受临时调度
        self.shceTargetFloor = 0  # 临时调度的目标楼层
        self.moveNumFromSche = 0  # 临时调度从接受到开始所移动的层数
        self.isTStopReached = False  # 是否可以结束临时调度
        self.scheAcceptTime = 0  # 接收临时调度的时间

        self.lastOpenTime = 0

    def checkArrive(self, time, parts):
        if self.isClosed is False:
            return f"Elevator {self.id} cannot move because the door is open at [{time - 0.1}]"
        if self.isSche is False and self.receivedNum == 0:
            return f"Elevator {self.id} cannot move because it did not receive any passenger at [{time - 0.1}]"

        if parts[1] not in floorMap.keys():
            return f"There is no floor {parts[1]} at [{time - 0.1}]"
        nowFloor = floorMap[parts[1]]
        if nowFloor == self.lastFloor:
            return f"Elevator {self.id} cannot move because it is already at {self.lastFloor} at [{time - 0.1}]"
        if nowFloor - self.lastFloor > 1 or nowFloor - self.lastFloor < -1:
            return f"Elevator {self.id} cannot move more than 1 floor at [{time - 0.1}]"
        if (time - self.lastArrivedTime + 0.001) < self.speed:
            return f"Elevator {self.id} ' s spped is too fast at [{time - 0.1}]"
        if self.isScheAccepted and self.isSche is False and self.moveNumFromSche == 2:
            return f"Elevator {self.id} cannot move because it need to temporary schedule at [{time - 0.1}]"

        self.lastFloor = nowFloor
        self.lastArrivedTime = time

        if self.isScheAccepted and self.isSche is False:
            self.moveNumFromSche += 1
        return "VALID"

    def checkReceive(self, time, parts):
        passengerId = (int)(parts[1])
        if self.isSche:
            return f"Elevator {self.id} cannot receive passenger {passengerId} because it is in temporary scheduling at [{time - 0.1}]"
        if passengerId not in passengers.keys():
            return f"There is no passenger {passengerId} at [{time - 0.1}]"
        passenger = passengers[passengerId]
        if passenger.isReceived != 0:
            return f"Passenger {passengerId} has already been received by elevator {passenger.isReceived} at [{time - 0.1}]"

        passenger.isReceived = self.id
        self.receivedNum += 1
        return "VALID"

    def scheAccept(self, time, parts):
        if self.isScheAccepted is True:
            return f"Elevator {self.id} cannot accept a temporary schedule because it has already accepted a temporary schedule at [{time - 0.1}]"
        self.isScheAccepted = True
        self.isSche = False
        self.moveNumFromSche = 0
        self.shceTargetFloor = floorMap[parts[-1]]
        self.scheSpeed = float(parts[3])
        self.scheAcceptTime = time
        return "VALID"

    def checkScheBegin(self, time, parts):
        if self.isScheAccepted is False:
            return f"Elevator {self.id} cannot temporary schedule because it did not receive any SCHE request at [{time - 0.1}]"

        self.isSche = True
        self.speed = self.scheSpeed
        self.moveNumFromSche = 0
        return "VALID"

    def checkScheEnd(self, time, parts):
        if self.isScheAccepted is False:
            return f"Elevator {self.id} cannot temporary schedule because it did not receive any SCHE request at [{time - 0.1}]"
        if self.lastFloor != self.shceTargetFloor:
            return f"Elevator {self.id} cannot end temporary schedule because it is not at {self.shceTargetFloor} at [{time - 0.1}]"
        if self.isClosed is False:
            return f"Elevator {self.id} cannot end temporary schedule because the door is open at [{time - 0.1}]"
        if self.passengerList:
            return f"Elevator {self.id} cannot end temporary schedule because it still has passengers at [{time - 0.1}]"
        if self.isTStopReached is False:
            return f"Elevator {self.id} cannot end temporary schedule because the T-stop is not reached at [{time - 0.1}]"
        if time - self.scheAcceptTime > 6:
            return f"Elevator {self.id} ' s temporary schedule costs too much time"

        self.isScheAccepted = False
        self.isSche = False
        self.speed = 0.4
        self.shceTargetFloor = 0
        self.canEndSche = False
        self.receivedNum = 0
        self.isTStopReached = False
        for passenger in passengers.values():
            if passenger.isReceived == self.id:
                passenger.isReceived = 0
        return "VALID"

    def checkOpen(self, time, parts):
        if self.isClosed is False:
            return f"Elevator {self.id} cannot open the door because the door is already open at [{time - 0.1}]"
        if self.isSche is True and self.shceTargetFloor != self.lastFloor:
            return f"Elevator {self.id} cannot open the door because it is in temporary scheduling at [{time - 0.1}]"

        self.isClosed = False
        self.lastOpenTime = time
        return "VALID"

    def checkClose(self, time, parts):
        if self.isClosed is True:
            return f"Elevator {self.id} cannot close the door because the door is already closed at [{time - 0.1}]"
        if self.isSche is False and (time - self.lastOpenTime + 0.001) < 0.4:
            return f"Elevator {self.id} cannot close the door because the door is open for too short at [{time - 0.1}]"
        if self.isSche is True and (time - self.lastOpenTime + 0.001) < 1:
            return f"Elevator {self.id} cannot close the door because the T-stop is not reached at [{time - 0.1}]"

        self.isClosed = True
        if self.isSche is True:
            self.isTStopReached = True
        return "VALID"

    def checkIn(self, time, parts):
        if self.isClosed is True:
            return f"Elevator {self.id} cannot let passenger {parts[1]} in because the door is closed at [{time - 0.1}]"
        passengerId = (int)(parts[1])
        if passengerId not in passengers.keys():
            return f"There is no passenger {passengerId} at [{time - 0.1}]"
        passenger = passengers[passengerId]
        if passenger.isReceived == 0:
            return f"Passenger {passengerId} has not been received at [{time - 0.1}]"
        if passenger.isReceived != self.id:
            return f"Passenger {passengerId} has already been received by elevator {passenger.isReceived} at [{time - 0.1}]"
        if passenger.fromFloor != self.lastFloor:
            return f"Passenger {passengerId} cannot be in the elevator because it is not at {passenger.fromFloor} at [{time - 0.1}]"
        if self.num >= 6:
            return f"Elevator {self.id} cannot let passenger {passengerId} in because it is full at [{time - 0.1}]"

        self.num += 1
        self.passengerList.append(passengerId)
        return "VALID"

    def checkOutS(self, time, parts):
        if self.isClosed is True:
            return f"Elevator {self.id} cannot let passenger {parts[1]} out because the door is closed at [{time - 0.1}]"
        passengerId = (int)(parts[2])
        if passengerId not in passengers.keys():
            return f"There is no passenger {passengerId} at [{time - 0.1}]"
        if passengerId not in self.passengerList:
            return f"Passenger {passengerId} is not in the elevator {self.id} at [{time - 0.1}]"

        passenger = passengers[passengerId]
        if passenger.targetFloor != self.lastFloor:
            return f"Passenger {passengerId} cannot be out the elevator because it is not at {passenger.targetFloor} at [{time - 0.1}]"

        self.num -= 1
        self.receivedNum -= 1
        self.passengerList.remove(passengerId)
        passengers.pop(passengerId)
        return "VALID"

    def checkOutF(self, time, parts):
        if self.isClosed is True:
            return f"Elevator {self.id} cannot let passenger {parts[1]} out because the door is closed at [{time - 0.1}]"
        passengerId = (int)(parts[2])
        if passengerId not in passengers.keys():
            return f"There is no passenger {passengerId} at [{time - 0.1}]"
        if passengerId not in self.passengerList:
            return f"Passenger {passengerId} is not in the elevator {self.id} at [{time - 0.1}]"

        passenger = passengers[passengerId]
        self.num -= 1
        self.receivedNum -= 1
        self.passengerList.remove(passengerId)
        passenger.isReceived = 0
        passenger.fromFloor = self.lastFloor
        return "VALID"


class PassengerState:
    def __init__(self, id, priority, fromFloor, targetFloor):
        self.id = int(id)  # 乘客id
        self.priority = int(priority)  # 乘客优先级
        self.targetFloor = floorMap[targetFloor]  # 乘客目标楼层
        self.fromFloor = floorMap[fromFloor]  # 乘客起始楼层
        self.isReceived = 0  # 乘客被哪部电梯接受


Elevators = [Elevator(i) for i in range(0, 7)]
passengers = {}
floorMap = {
    "B4": -4, "B3": -3, "B2": -2, "B1": -1,
    "F1": 0, "F2": 1, "F3": 2, "F4": 3,
    "F5": 4, "F6": 5, "F7": 6
}

def parse_and_merge_files(input_file: str, output_file: str):
    """
    合并输入和输出文件并按时间戳排序
    :param input_file: 输入文件路径
    :param output_file: 输出文件路径
    :return: 按时间戳排序后的合并列表
    """
    # 读取并解析输入文件
    input_entries = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # 解析时间戳
            match = re.match(r'^\[(\d+\.\d+)]', line)
            if not match:
                continue
            timestamp = float(match.group(1))
            input_entries.append((timestamp, line))

    # 读取并解析输出文件
    output_entries = []
    with open(output_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # 解析时间戳（处理可能的前导空格）
            match = re.match(r'^\[\s*(\d+\.\d+)]', line)
            if not match:
                continue
            timestamp = float(match.group(1))
            timestamp += 0.1
            # 规范化输出行的格式（去除多余空格）
            normalized_line = re.sub(r'\[\s+(\d+\.\d+)]', r'[\1]', line)
            output_entries.append((timestamp, normalized_line))

    # 合并并排序
    all_entries = input_entries + output_entries
    all_entries.sort(key=lambda x: x[0])
    all_entries = [list(entry) for entry in all_entries]
    # 删除 entry[1]中的[]及中间的内容
    for entry in all_entries:
        entry[1] = re.sub(r'\[\d+\.\d+]', '', entry[1])
    return all_entries

def main():
    i = sys.argv[1]
    input_file = f'Input{i}.txt'
    output_file = f'Output{i}.txt'
    all_entries = parse_and_merge_files(input_file, output_file)
    for entry in all_entries:
        # print(entry)
        parts = entry[1].split('-')
        # 如果 parts[0] 是数字，则说明是乘客请求
        if parts[0].isdigit():
            passengers[int(parts[0])] = PassengerState(parts[0], parts[2], parts[4], parts[6])
            continue
        elif parts[0] == 'SCHE' and parts[1].isdigit():
            continue
        elif parts[0] == 'SCHE' and parts[1] == 'ACCEPT':
            elevatorId = int(parts[2])
            Elevators[elevatorId].scheAccept(entry[0], parts)
            continue

        elevatorId = int(parts[-1])
        if parts[0] == 'ARRIVE':
            isValid = Elevators[elevatorId].checkArrive(entry[0], parts)
        elif parts[0] == 'RECEIVE':
            isValid = Elevators[elevatorId].checkReceive(entry[0], parts)
        elif parts[0] == 'SCHE' and parts[1] == 'BEGIN':
            isValid = Elevators[elevatorId].checkScheBegin(entry[0], parts)
        elif parts[0] == 'SCHE' and parts[1] == 'END':
            isValid = Elevators[elevatorId].checkScheEnd(entry[0], parts)
        elif parts[0] == 'OPEN':
            isValid = Elevators[elevatorId].checkOpen(entry[0], parts)
        elif parts[0] == 'CLOSE':
            isValid = Elevators[elevatorId].checkClose(entry[0], parts)
        elif parts[0] == 'IN':
            isValid = Elevators[elevatorId].checkIn(entry[0], parts)
        elif parts[0] == 'OUT' and parts[1] == 'S':
            isValid = Elevators[elevatorId].checkOutS(entry[0], parts)
        elif parts[0] == 'OUT' and parts[1] == 'F':
            isValid = Elevators[elevatorId].checkOutF(entry[0], parts)
        else:
            isValid = "Invalid command:"

        if isValid != "VALID":
            print(isValid)
            return

    for elevator in Elevators:
        if elevator.isClosed is False:
            print(f"Elevator {elevator.id} is still open at the end")
            return
        if elevator.num != 0:
            print(f"Elevator {elevator.id} still has {elevator.num} passengers at the end")
            return
        if elevator.isSche:
            print(f"Elevator {elevator.id} is still scheduling at the end")
            return

    for passengerId in passengers.keys():
        print(f"Passenger {passengerId} is still waiting at the end")
        return

    print("Accepted")


if __name__ == '__main__':
    main()

