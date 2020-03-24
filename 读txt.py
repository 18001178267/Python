with open(r'C:\Users\YZW\Desktop\magnetic_sensor\python\monitorS (2)\readme.txt','r',encoding='UTF-8') as f:
    #用with as 就不用写close（）了
    while True:
        line = f.readline()
        if not line:
            break;

        print(line.rstrip())
