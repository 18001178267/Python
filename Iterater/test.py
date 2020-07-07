# def generator_1(titles):
#     yield titles
# def generator_2(titles):
#     yield from titles
#
# titles = ['Python','Java','C++']
# g=generator_2(titles)
# for title in generator_1(titles):
#     print(type(title))
#     print('生成器1:',title)
# # for title in generator_2(titles):
# #     print(type(title),generator_1(titles))
# #     print('生成器2:',title)
# print(next(g))
# print(next(g))

def foo(num):
    print("starting...")
    while num<10:
        num=num+1
        yield num
print(foo(0))
for n in foo(0):
    print(n)