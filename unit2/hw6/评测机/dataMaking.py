import random
from typing import List


def generate_simple_requests(
        requests_per_block: int = 8,
        sche_prob: float = 0.5,
        current_time: float = 0.1
) -> List[str]:
    """
    简化版电梯请求生成器
    :param current_time: 起始时间
    :param requests_per_block: 每个时间块的请求数(7-8条)
    :param sche_prob: 生成SCHE指令的概率
    :return: 请求列表
    """
    requests = []
    time_block_end = min(current_time + 0.3, 30.0)
    timestamp =[]
    for _ in range(requests_per_block):
        timestamp.append(round(random.uniform(current_time, time_block_end), 3))
    timestamp.sort()
    # 在当前时间块生成请求
    for _ in range(requests_per_block):
        if _ < 5:
            sche_prob = 0.3
        else:
            sche_prob = 0.7

        # 生成临时调度指令
        if (random.random() < sche_prob and
                any(timestamp[_] - sche_records[eid] >= 6 for eid in sche_records)):

            # 选择符合条件的电梯
            valid_elevators = [eid for eid in sche_records
                               if timestamp[_] - sche_records[eid] >= 6]
            elevator_id = random.choice(valid_elevators)
            speed = round(random.uniform(0.2, 0.5), 1)
            target_floor = random.choice(['B2', 'B1', 'F1', 'F2', 'F3', 'F4', 'F5'])

            requests.append(f"[{timestamp[_]:.3f}]SCHE-{elevator_id}-{speed}-{target_floor}")
            sche_records[elevator_id] = timestamp[_]
        # 生成乘客请求
        else:
            # 生成普通乘客请求
            request_id = random.randint(1, 1000)
            while request_id in used_ids:
                request_id = random.randint(1, 1000)
            used_ids.add(request_id)

            while True:
                from_floor, to_floor = random.choices(
                    ['B4', 'B3', 'B2', 'B1', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7'],
                    k=2
                )
                if from_floor != to_floor:
                    break

            requests.append(
                f"[{timestamp[_]:.3f}]{request_id}-PRI-{random.randint(1, 100)}-"
                f"FROM-{from_floor}-TO-{to_floor}"
            )

    # 按时间戳排序
    # return sorted(requests, key=lambda x: float(x.split(']')[0][1:]))
    return requests

used_ids = set()

if __name__ == "__main__":
    current_time = round(random.uniform(0.5, 4), 3)
    block_cnt = random.randint(3, 6)
    sche_records = {eid: -10.0 for eid in range(1, 7)}  # 记录电梯上次调度时间

    while block_cnt > 0 :
        block_cnt -= 1
        requests = generate_simple_requests(
            requests_per_block= random.randint(8, 16),
            current_time = current_time,
        )
        for req in requests:
            print(req)
        right = min(30.0, current_time + 15.0)
        current_time = round(random.uniform(current_time, right), 3)