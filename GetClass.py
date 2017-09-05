from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
from PIL import Image
from Verify import getPixel, clearNoise, enhance
import pytesseract
import myPassword

def get_captcha(driver, element, path):
    # now that we have the preliminary stuff out of the way time to get that image :D
    location = element.location
    size = element.size
    # saves screenshot of entire page
    driver.save_screenshot(path)

    # uses PIL library to open image in memory
    image = Image.open(path)

    left = location['x'] + 58
    top = location['y'] + 282
    right = location['x'] + size['width'] + 120
    bottom = location['y'] + size['height'] + 302

    image = image.crop((left, top, right, bottom))  # defines crop points
    image.save(path, 'png')  # saves new cropped image

# 指定 Chromedriver 路徑
chromedriver = './chromedriver'
url = 'https://isdna1.yzu.edu.tw/Cnstdsel/Index.aspx'
# Open Chrome
browser = webdriver.Chrome(chromedriver)
browser.get(url)

while True:
    select = Select(browser.find_element_by_id('DPL_SelCosType'))
    select.select_by_index(1)

    browser.find_element_by_id('Txt_User').clear()
    browser.find_element_by_id('Txt_User').send_keys(myPassword.Account)
    browser.find_element_by_id('Txt_Password').clear()
    browser.find_element_by_id('Txt_Password').send_keys(myPassword.password)


    img = browser.find_element_by_xpath('//*[@id="Panel2"]/table/tbody/tr[2]/td[1]/table[1]/tbody/tr[2]/td[2]/img')
    get_captcha(browser, img, "captcha.png")
    #打開圖片  
    image = Image.open("captcha.png")
    #將圖片轉換成灰度圖片  
    image = image.convert("L")
    #第一次 Enhance
    image = enhance(image)
    #第一次去噪,G = 50,N = 4,Z = 4  
    clearNoise(image, 50 , 4 , 4)  
    #第二次 Enhance
    image = enhance(image)
    #第二次去噪,G = 50,N = 4,Z = 4  
    clearNoise(image, 50 , 3 , 3)  
    #保存圖片  
    # image.save( "./result/result.png" )  
    #顯示圖片
    # image.show()


    captcha = pytesseract.image_to_string(image).replace(" ", "")

    browser.find_element_by_id('Txt_CheckCode').send_keys(captcha)

    sleep(2)

    browser.find_element_by_id('btnOK').click()

    a1 = browser.switch_to.alert
    sleep(1)
    a1.accept()

    html = browser.page_source
    if html.find('Txt_CheckCode') == -1:
        break


sleep(2)

runTimes = 0
while runTimes < 3:
    browser.switch_to_default_content()
    browser.switch_to.frame('LeftCosList')
    sleep(1)
    select = Select(browser.find_element_by_id('DPL_DeptName'))
    select.select_by_value('901')
    sleep(1)
    select = Select(browser.find_element_by_id('DPL_Degree'))
    select.select_by_value('1')
    sleep(1)
    browser.find_element_by_id('SelCos,LS209,A,1,E,2,Y,Chinese,LS209,A,2 生物科技概論').click()

    a2 = browser.switch_to.alert
    sleep(1)
    a2.accept()
    a3 = browser.switch_to.alert
    sleep(1)
    a3.accept()

    browser.switch_to_default_content()
    browser.switch_to.frame('frameright')
    Class = browser.find_element_by_id('111')
    if Class.get_attribute('class') == 'cls_res_main_c_sel_l':
        print('Selected')
        break
        # cls_res_main_n_sel
    else:
        print('unselected')
        runTimes = runTimes + 1

browser.close()
