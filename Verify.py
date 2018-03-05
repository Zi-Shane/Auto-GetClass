#coding:utf-8  
import sys,os  
from PIL import Image, ImageDraw ,ImageEnhance
import pytesseract
  
#二值判斷,如果確認是噪聲,用改點的上面一個點的灰度進行替換  
#該函數也可以改成RGB判斷的,具體看需求如何  
def getPixel(image, x, y, G, N):  
    L = image.getpixel((x, y))  
    if  L > G:
        L = True  
    else:  
        L = False  
  
    nearDots = 0  
    if  L == (image.getpixel((x - 1, y - 1)) > G):  
        nearDots +=  1  
    if  L == (image.getpixel((x - 1, y)) > G):  
        nearDots +=  1  
    if  L == (image.getpixel((x - 1, y + 1)) > G):  
        nearDots +=  1  
    if  L == (image.getpixel((x, y - 1)) > G):  
        nearDots +=  1  
    if  L == (image.getpixel((x, y + 1)) > G):  
        nearDots +=  1  
    if  L == (image.getpixel((x + 1, y - 1)) > G):  
        nearDots +=  1  
    if  L == (image.getpixel((x + 1, y)) > G):  
        nearDots +=  1  
    if  L == (image.getpixel((x + 1, y + 1)) > G):  
        nearDots +=  1  
  
    if  nearDots < N:  
        return image.getpixel((x,y - 1))  
    else:  
        return None   
  
# 降噪   
# 根據一個點A的RGB值，與周圍的8個點的RBG值比較，設定一個值N（0 <N <8），當A的RGB值與周圍8個點的RGB相等數小於N時，此點為噪點   
# G: Integer 圖像二值化閥值   
# N: Integer 降噪率 0 <N <8   
# Z: Integer 降噪次數   
# 輸出   
# 0：降噪成功   
# 1：降噪失敗   
def clearNoise(image, G, N, Z):  
    draw = ImageDraw.Draw(image)  
  
    for i in range(0, Z):  
        for x in range(1, image.size[0] - 1):  
            for y in range(1, image.size[1] - 1):  
                color = getPixel(image, x, y, G, N)  
                if  color !=  None :  
                    draw.point((x, y), color)  

# Enhance
def enhance(image):
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(5)
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(10.0)
    return image

def get_captcha(driver, element, path):
    # now that we have the preliminary stuff out of the way time to get that image :D
    location = element.location
    size = element.size
    # saves screenshot of entire page
    driver.save_screenshot(path)

    # uses PIL library to open image in memory
    image = Image.open(path)

    left = location['x'] + 61
    top = location['y'] + 272
    right = location['x'] + size['width'] + 114
    bottom = location['y'] + size['height'] + 286

    image = image.crop((left, top, right, bottom))  # defines crop points
    image.save(path, 'png')  # saves new cropped image
