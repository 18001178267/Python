import os

class ImageRename():
    def __init__(self):
        self.path = 'C:\\Users\\YFZX\\Desktop\\13_institute\\Image_input\\original' #需要将图片命名的文件夹路径

    def rename(self):
        filelist = os.listdir(self.path)
        totalnum = len(filelist)

        i = 1

        for item in filelist:
            if item.endswith('.JPG'):
                src = os.path.join(os.path.abspath(self.path),item)
                dst = os.path.join(os.path.abspath(
                    self.path),('SOIL'+format(str(i),'0>4s') + '.JPG')) #4为位数，如0001.
                os.rename(src,dst)
                i = i + 1


if __name__ == '__main__':
    newname = ImageRename()
    newname.rename()
