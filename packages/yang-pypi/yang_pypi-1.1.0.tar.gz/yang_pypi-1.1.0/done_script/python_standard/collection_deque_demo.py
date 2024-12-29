"""
collections.deque 与 queue.Queue对比
    1.collections.deque不是线程安全队列，需要格外加锁, 不支持阻塞操作。两端操作时效率高
    2.queue.Queue是线程安全队列，自带锁且支持阻塞操作，但是性能比前者差(因为频繁的加锁)
"""
import collections
from queue import Queue

if __name__ == '__main__':
    Queue()
    my_queue = collections.deque(maxlen=100)
    print(bool(my_queue))  # 空队列的布尔值为False
    my_queue.append("a")
    # print(bool(my_queue))  # 非空队列的布尔值为True
    my_queue.append("b")
    my_queue.append("c")
    print(my_queue[0])
    # print(my_queue, len(my_queue))
    # my_queue.append("d")
    # my_queue.append("e")
    # my_queue.clear()
    # print(my_queue)

    # for item in my_queue:
    #     print(item)
    pass