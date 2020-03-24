import threading
import time

def run(n):
    print("task", n)
    print(threading.active_count()) #输出当前活跃的线程数
    time.sleep(1)
    print('2s')
    time.sleep(1)
    print('1s')
    time.sleep(1)
    print('0s')
    time.sleep(1)

t1 = threading.Thread(target=run, args=("t1",))
t2 = threading.Thread(target=run, args=("t2",))
t1.start()
t2.start()
t1.join()
t2.join()