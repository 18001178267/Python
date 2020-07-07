# def foo(num):
#     print("starting...")
#     while num<10:
#         num=num+1
#         yield num
#
# # g=foo(0)
# for n in foo(0):
#     print(n)
# # print(foo(0))
#!/usr/bin/python
# -*- coding: UTF-8 -*-


import time,datetime
def fab(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b      # 使用 yield
        # print b
        a, b = b, a + b
        n = n + 1
# print(datetime.datetime.now(),time.time())
for n in fab(100):
    print(n)