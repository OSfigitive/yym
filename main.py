from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import selenium
import cv2
import requests
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from PIL import Image
from selenium.webdriver.chrome.options import Options #（这个需要前提引入的，就想时间等待一样）
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import random


options = webdriver.ChromeOptions()
wb = webdriver.Chrome(options=options)

#放检验的打开浏览器
# opt = Options()
# opt.add_experimental_option('excludeSwitches',['enable-automation'])
# wb = webdriver.Chrome(options=opt)

#运行正在打开的浏览器
# opt = Options()
# opt.add_experimental_option('debuggerAddress','127.0.0.1:9527')
# wb = webdriver.Chrome(options=opt)

#打开无头浏览器
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# wb = webdriver.Chrome(options=chrome_options)

time_start = time.time()#开始计时
def get_url():
    wb.get('https://www.douyin.com/discover')
    WebDriverWait(wb, 5, 0.5).until(ec.visibility_of_element_located(
        (By.XPATH, '//*[@id="login-pannel"]/div[3]/div/article/article/article/div[1]/ul[1]/li[2]')),'失败')#等待 直到登录按钮出现
    # time.sleep(1)
    try:
        wb.find_element(By.XPATH,'//*[@id="login-pannel"]/div[3]/div/article/article/article/div[1]/ul[1]/li[2]').click()
    except:
        print(WebDriverWait(wb, 2, 0.5).until(ec.visibility_of_element_located(
            (By.XPATH, '//*[@id="verify-bar-close"]')), '失败'))#关闭点选验证界面

        # time.sleep(1.5)
        wb.find_element(By.XPATH, '//*[@id="verify-bar-close"]').click()
        print(WebDriverWait(wb, 2, 0.5).until(ec.visibility_of_element_located(
            (By.XPATH, '//*[@id="verify-bar-close"]')), '失败'))#等待 直到点选验证界面出现
        # time.sleep(1)
        wb.find_element(By.XPATH, '//*[@id="verify-bar-close"]').click()
        # time.sleep(0.5)
        WebDriverWait(wb, 2, 0.5).until(ec.visibility_of_element_located(
            (By.XPATH, '//*[@id="login-pannel"]/div[3]/div/article/article/article/div[1]/ul[1]/li[2]')), '失败')
        wb.find_element(By.XPATH,'//*[@id="login-pannel"]/div[3]/div/article/article/article/div[1]/ul[1]/li[2]').click()
        pass

    time.sleep(1)
    try:  #要输入就要下面这三行
        wb.find_element(By.XPATH, '//*[@id="login-pannel"]/div[3]/div/article/article/article/form/div[1]/div/input').click()
        wb.find_element(By.XPATH, '//*[@id="login-pannel"]/div[3]/div/article/article/article/form/div[1]/div/input').clear()
        wb.find_element(By.XPATH, '//*[@id="login-pannel"]/div[3]/div/article/article/article/form/div[1]/div/input').send_keys(18948233333)
    except: #预防点选验证码弹出
        # time.sleep(2)
        print(WebDriverWait(wb, 2, 0.5).until(ec.visibility_of_element_located(
            (By.XPATH, '//*[@id="verify-bar-close"]')), '失败'))  # 等待 直到点选验证界面出现
        wb.find_element(By.XPATH, '//*[@id="verify-bar-close"]').click()
        time.sleep(1)
        wb.find_element(By.XPATH, '//*[@id="verify-bar-close"]').click()
        time.sleep(0.5)
        wb.find_element(By.XPATH, '//*[@id="login-pannel"]/div[3]/div/article/article/article/form/div[1]/div/input').click()
        wb.find_element(By.XPATH, '//*[@id="login-pannel"]/div[3]/div/article/article/article/form/div[1]/div/input').clear()
        wb.find_element(By.XPATH, '//*[@id="login-pannel"]/div[3]/div/article/article/article/form/div[1]/div/input').send_keys(18948233333)
        pass
    # wb.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[3]/div[2]/div[2]/div[1]/input').send_keys(122)
    time.sleep(0.5)
    wb.find_element(By.XPATH, '//*[@id="login-pannel"]/div[3]/div/article/article/article/form/div[2]/div/span').click() #点击获取验证码
    # time.sleep(1)

    time_end1 = time.time()  # 结束计时
    time_c1 = time_end1 - time_start  # 运行所花时间
    print('time cost', time_c1, 's')
    return

def verify():
    #保存验证码
    verify_img = wb.find_element(By.XPATH, '//*[@id="captcha-verify-image"]')#读取要拼图的图片
    point_img = wb.find_element(By.XPATH,'//*[@id="captcha_container"]/div/div[2]/img[2]')#读取拼图的图片
    img_url = verify_img.get_attribute('src')
    img_url2 = point_img.get_attribute('src')
    print('成功获取图片url')
    time.sleep(0.5)
    content = requests.get(img_url).content
    content2 = requests.get(img_url2).content
    print('成功写入content')
    with open('verift_img.jpg','wb')as f:#要写入本地
        f.write(content)
    verify_img = cv2.imread('verift_img.jpg')
    with open('point_img.jpg','wb')as f:
        f.write(content2)
    point_img = cv2.imread('point_img.jpg')#变成BRG格式来OpenCV处理

    bg_edge = cv2.Canny(verify_img, 100, 200)#获取图像的边缘，Canny（图，阈值，阈值）
    tp_edge = cv2.Canny(point_img, 100, 200)

    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)#颜色空间转换函数，cvtColor（图，要变成的格式）
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
    # 缺口匹配
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)#模板匹配函数，mathTemplate(图，图，匹配类型【一般用cv2.TM_CCOEFF_NORMED】）
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # 寻找最优匹配
    X = max_loc[0]*340/552 #根据图片真实与表面大小的比例进行缩放
    '''
    # # 绘制方框
    # th, tw = tp_pic.shape[:2]
    # tl = max_loc # 左上角点的坐标
    # br = (tl[0]+tw,tl[1]+th) # 右下角点的坐标
    # cv2.rectangle(verify_img, tl, br, (0, 0, 255), 2) # 绘制矩形
    # cv2.imwrite('out.jpg', verify_img) # 保存在本地
    '''
    return(X)


def check():
    #用于验证码输入，几乎没有用
    wb.find_element(By.XPATH,
                    '//*[@id="login-pannel"]/div[3]/div/article/article/article/form/div[2]/div/div/input').click()
    wb.find_element(By.XPATH,
                    '//*[@id="login-pannel"]/div[3]/div/article/article/article/form/div[2]/div/div/input').clear()
    wb.find_element(By.XPATH,
                    '//*[@id="login-pannel"]/div[3]/div/article/article/article/form/div[2]/div/div/input').send_keys(111111)
    return

# 移动滑块
def start_move(distance):
    element = wb.find_element(By.XPATH,('//*[@id="secsdk-captcha-drag-wrapper"]/div[2]'))
    # 使用滑块的一半进行偏移设置
    # distance -= element.size.get('width') / 2
    # distance += 30

    # 按下鼠标左键
    ActionChains(wb).click_and_hold(element).perform()#点并按住elemnet，操作
    time.sleep(0.5)
    while distance > 0:
        if distance > 20:
            # 如果距离大于20，就让他移动快一点
            span = random.randint(60, 70)#
        else:
            # 快到缺口了，就移动慢一点
            span = random.randint(45, 50)
        ActionChains(wb).move_by_offset(span, 0).perform()
        distance -= span
        time.sleep(random.randint(10, 50) / 100)

    ActionChains(wb).move_by_offset(distance, 1).perform()
    ActionChains(wb).release(on_element=element).perform()



if __name__ == '__main__':
    get_url()
    WebDriverWait(wb, 5,0.5).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="captcha-verify-image"]')), '失败')
    while ec.visibility_of_element_located((By.XPATH, '//*[@id="captcha-verify-image"]')):
        X = verify()
        print('图片获取完成')
        time.sleep(1)
        WebDriverWait(wb, 5, 0.5).until(ec.element_to_be_clickable(
            (By.XPATH, '//*[@id="secsdk-captcha-drag-wrapper"]/div[2]')),'失败')
        print('开始滑块验证')
        start_move(X)
        print('滑块验证完成')
        time.sleep(1)
    # try:
    #     time.sleep(1)
    #     check()
    # except:
    #     X = verify()
    #     start_move(X)
    # time.sleep(0.5)
    # X = verify()
    # start_move(X)
    # time.sleep(0.5)
    # print('第二次滑块验证完成')
    time_end = time.time()  # 结束计时
    time_c = time_end - time_start  # 运行所花时间
    print('time cost', time_c, 's')
    #
    # # wb.get_screenshot_as_file("d:\\bing.png")
    # wb.save_screenshot('img0.png')


    print('****完成啦****')