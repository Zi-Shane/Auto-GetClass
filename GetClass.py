from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
from PIL import Image
from Verify import getPixel, clearNoise, enhance, get_captcha
import pytesseract
import password
import config


# 指定 Chromedriver 路徑
chromedriver = './chromedriver'
url = 'https://isdna1.yzu.edu.tw/Cnstdsel/Index.aspx'
# Open Chrome
browser = webdriver.Chrome(chromedriver)
browser.get(url)
sleep(2)

# Login Page
while True:
    select = Select(browser.find_element_by_id('DPL_SelCosType'))
    select.select_by_index(1)

    browser.find_element_by_id('Txt_User').clear()
    browser.find_element_by_id('Txt_User').send_keys(password.Account)
    browser.find_element_by_id('Txt_Password').clear()
    browser.find_element_by_id('Txt_Password').send_keys(password.password)

    # Captcha crack
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


sleep(1)
# Select Page
runTimes = 0
maxTimes = len(config.ClassIdentification)
while runTimes < maxTimes:
    browser.switch_to_default_content()

    browser.switch_to.frame('LeftCosList')
    sleep(1)
    select = Select(browser.find_element_by_id('DPL_DeptName'))
    select.select_by_value(config.DepartmentId[runTimes])
    sleep(1)
    select = Select(browser.find_element_by_id('DPL_Degree'))
    select.select_by_value(config.Degree[runTimes])
    sleep(2)
    browser.find_element_by_id(config.ClassIdentification[runTimes]).click()
    sleep(1)
    a2 = browser.switch_to.alert
    sleep(1)
    a2.accept()
    browser.switch_to.default_content()
    sleep(1)
    a3 = browser.switch_to.alert
    sleep(1)
    a3.accept()

    # Check if Selected ?
    browser.switch_to_default_content()
    browser.switch_to.frame('frameright')
    sleep(1)
    Class = browser.find_element_by_id(config.ClassTime[runTimes])
    if Class.get_attribute('class') == 'cls_res_main_c_sel_l':
        print('Selected: ' + config.ClassIdentification[runTimes])
        break
        # cls_res_main_n_sel
    else:
        print('unselected' + str(runTimes + 1) + ': '  + config.ClassIdentification[runTimes])
        sleep(3)
        runTimes = runTimes + 1

sleep(3)
browser.close()
