import os
from PIL import Image
from MyQR import myqr

def genQrcode(wordOrUrl,name,path,**kwargs):
    #words, version=1, level='H', picture=None,
    # colorized=False, contrast=1.0, brightness=1.0, save_name=None, save_dir=os.getcwd()
    version = kwargs.get('version',1)
    level = kwargs.get('level','H')
    picture = kwargs.get('picture',None)
    colorized = kwargs.get('colorized',False)
    contrast = kwargs.get('contrast',1.0)
    brightness = kwargs.get('brightness',1.0)
    #生成并返回图片路径
    picture = myqr.run(wordOrUrl,version,level,picture,colorized,contrast,brightness,save_name=name,save_dir=path)
    return picture[2]

def openQrcode(fullPath):
    image = Image.open(fullPath)
    image.show()

if __name__ == '__main__':
    url = 'https://u.jd.com/5aRb5X'
    name = '拍子.png'
    dirName = 'D:\\ftp'
    openQrcode(genQrcode(url,name,dirName))