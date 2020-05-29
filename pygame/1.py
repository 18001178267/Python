import ctypes
player = ctypes.windll.kernel32
player.Beep(1000,2000)
                '''
                musicPath = r"C:\Users\YFZX\Desktop\1.mp3"
                pygame.mixer.init()#初始化
                track = pygame.mixer.music.load(musicPath)#加载音乐
                pygame.mixer.music.play()#播放
                userIn = input()#输入空格暂停
                if userIn == ' ':
                    pygame.mixer.music.pause()
                else:
                    time.sleep(207)#表示音频的长度
                pygame.mixer.music.stop()
                '''
