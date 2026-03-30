import os
from datetime import datetime
from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture( scope="function" )
def driver():
    # 提交最终代码脚本时，请将驱动路径换回官方路径"C:\\Users\\86153\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe"
    service = Service(
        # executable_path="C:\\Users\\86153\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe" )
        "D:\ChromeDriver\chromedriver.exe")
    driver = webdriver.Chrome( service=service )
    driver.get( "https://ctrip.com/ " )
    driver.maximize_window()
    driver.implicitly_wait( 10 )
    yield driver
    driver.quit()


class TestCtrip:

    # test-code-start

    # 请在此处插入Selenium+Pytest代码
    # 工具函数
    def common_click(self,driver,method,road_way):
        elem = WebDriverWait( driver, 10).until(EC.presence_of_element_located((method,road_way)))
        ActionChains(driver).click( elem ).perform()
        sleep(1)
    def hover_click(self, driver,by_menu,menu_elem,by_click,click_elem):
        hover_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by_menu, menu_elem)))
        ActionChains(driver).move_to_element(hover_menu).perform()
        click_goback = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((by_click,click_elem)))
        ActionChains(driver).click(click_goback).perform()
        sleep(1)
    def input_city(self, driver, by_method, city_input, by,xpath,city_name):
        # 等输入框可点击
        city_input_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((by_method, city_input))
        )
        ActionChains(driver).move_to_element(city_input_box).click().perform()
        sleep(0.3)
        # 选中 + 删除旧值（通过键盘）
        city_input_box.send_keys(Keys.CONTROL, 'a')
        city_input_box.send_keys(Keys.BACKSPACE)
        sleep(0.5)
        city_input_box.send_keys(city_name)
        # 查找城市候选（先精确再模糊）
        exact_xpath = f'//ul[@class="widget-search-bd"]//div[normalize-space(.)="{city_name}"]'
        fuzzy_xpath = f'//ul[@class="widget-search-bd"]//div[contains(normalize-space(.),"{city_name}")]'
        try:
            city_elem = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, exact_xpath))
            )
        except:
            city_elem = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, fuzzy_xpath))
            )
        # 再用 ActionChains 去点（原生事件流）
        ActionChains(driver).move_to_element(city_elem).click().perform()
        sleep(0.5)
    def js_click(self, driver, by, value):
        elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
        driver.execute_script("arguments[0].click();", elem)
        sleep(1)

    def open_depart_date(self, driver):
        # 1️⃣ 找到 label 元素或父 div，而不是 input
        date_wrapper = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='date'][label[@for='label-departDate']]"))
        )
        # 2️⃣ 滚动到视图中（防遮挡）
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", date_wrapper)

        # 3️⃣ 模拟用户点击
        ActionChains(driver).move_to_element(date_wrapper).click().perform()
        sleep(1)

    def choose_return_date(self, driver):
        return_wrapper = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='date'][label[@for='label-returnDate']]"))
        )
        ActionChains(driver).move_to_element(return_wrapper).click().perform()
        sleep(1)

    def choose_date(self, driver,target_day="2025-11-17"):
        input_year,input_month,input_day = target_day.split("-")
        input_month = str(int(input_month))
        input_day = str(int(input_day))
        date_wrapper = driver.find_elements(By.XPATH,'//ul[@class="widget-calendar-hd"]/li/h3')
        panel_index = 0
        for i,m in enumerate(date_wrapper):
            title = m.text
            year, month = title.split("年")
            month = month.replace("月", "").strip()
            if year == input_year and month == input_month:
                panel_index = i
                break
        date_choose = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,f'//ul[@class="date-bd"][{panel_index+1}]/li/strong[text()="{input_day}"]')))
        ActionChains(driver).move_to_element(date_choose).click().perform()
        sleep(1)

    #模块一
    @pytest.mark.parametrize("start_city,end_city,file_name",[
        ("济南","西安","Ctrip_R005_001.png"),
        ("济南", "杭州","Ctrip_R005_002.png"),
        ("天津", "西安", "Ctrip_R005_003.png"),
        ("天津", "杭州", "Ctrip_R005_004.png"),
    ])
    def test_Ctirp_R005(self,driver,start_city,end_city,file_name):
        #悬浮在菜单上
        hover_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='pc_home-tabbtnIcon lsn_ico_9C9TD']")))
        ActionChains(driver).move_to_element(hover_menu).perform()
        sleep(1)
        #悬浮并且点击火车
        self.hover_click(driver,By.XPATH,"//span[@class='lsn_top_nav_font_4h1KU lsn_top_nav_font_line_0iVuu'][contains(text(),'火车票')]",By.XPATH,"//a[@class='lsn_menu_son_nav_HoNwa']//span[@class='lsn_font_data_rSNIK'][contains(text(),'国内火车票')]")
        #点击往返
        self.js_click(driver,By.XPATH,"//ul[@class='search-select']//li[button[text()='往返']] ")
        #输入出发城市
        self.input_city(driver,By.XPATH,"//input[@id='label-departStation']",By.XPATH,f'//ul[@class="widget-search-bd"]//div[contains(normalize-space(.), "{start_city}")]',start_city)
        #输入目的地
        self.input_city(driver,By.XPATH,"//input[@id='label-arriveStation']",By.XPATH,f'//ul[@class="widget-search-bd"]//div[contains(normalize-space(.), "{end_city}")]',end_city)
        #选择出发日期
        self.open_depart_date(driver)
        # self.common_click(driver,By.XPATH,"//div[@class='date-fade-enter-done']//div[1]//ul[2]//li[23]//strong[1]")
        self.choose_date(driver)
        #点击搜索
        self.common_click(driver,By.XPATH,"//button[@class='btn-blue btn-search']")
        #车型，【坐席】、【出发车站】点击第一个
        self.common_click(driver,By.XPATH,"//body/div[@id='hp_container']/div[@id='content']/div[@id='main']/div[@id='__next']/div/div[@class='train-wrapper return-view']/div[@class='return-box']/div[1]/div[2]/div[3]/div[1]")
        self.common_click(driver,By.XPATH,"//div[@class='return-box']//div[1]//div[2]//div[3]//ul[1]//li[1]//div[1]//i[1]")
        self.common_click(driver,By.XPATH,"//ul[@class='screen-list open']//li[4]//div[1]//i[1]")
        self.common_click(driver,By.XPATH,"//ul[@class='screen-list open']//li[5]//div[1]//i[1]")
        #【出发时间】、【到达时间】、选中第二个复选框
        self.common_click(driver,By.XPATH,"//ul[@class='screen-list open']//li[2]//div[2]//i[1]")
        self.common_click(driver,By.XPATH,"//ul[@class='screen-list open']//li[3]//div[2]//i[1]")
        #截图
        self.take_screenshot(driver,file_name)

    @pytest.mark.parametrize("start_city,end_city,file_name", [
        ("兰州", "郑州", "Ctrip_R006_001.png"),
        ("兰州", "厦门", "Ctrip_R006_002.png"),
        ("兰州", "郑州", "Ctrip_R006_003.png"),
        ("兰州", "厦门", "Ctrip_R006_004.png"),
    ])
    def test_Ctirp_R006(self, driver, start_city, end_city, file_name):
        # 悬浮在菜单上
        hover_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='pc_home-tabbtnIcon lsn_ico_9C9TD']")))
        ActionChains(driver).move_to_element(hover_menu).perform()
        sleep(1)
        # 悬浮并且点击火车
        self.hover_click(driver, By.XPATH,
                         "//span[@class='lsn_top_nav_font_4h1KU lsn_top_nav_font_line_0iVuu'][contains(text(),'火车票')]",
                         By.XPATH,
                         "//a[@class='lsn_menu_son_nav_HoNwa']//span[@class='lsn_font_data_rSNIK'][contains(text(),'国内火车票')]")
        # 点击往返
        self.js_click(driver, By.XPATH, "//ul[@class='search-select']//li[button[text()='往返']] ")
        # 输入出发城市
        self.input_city(driver, By.XPATH, "//input[@id='label-departStation']", By.XPATH,
                        f'//ul[@class="widget-search-bd"]//div[contains(normalize-space(.), "{start_city}")]',
                        start_city)
        # 输入目的地
        self.input_city(driver, By.XPATH, "//input[@id='label-arriveStation']", By.XPATH,
                        f'//ul[@class="widget-search-bd"]//div[contains(normalize-space(.), "{end_city}")]', end_city)
        # 选择出发日期
        self.open_depart_date(driver)
        self.choose_date(driver, "2025-11-18")
        # 点击搜索
        self.common_click(driver, By.XPATH, "//button[@class='btn-blue btn-search']")
        # 车型，【坐席】、【出发车站】点击第一个
        self.common_click(driver, By.XPATH,
                          "//body/div[@id='hp_container']/div[@id='content']/div[@id='main']/div[@id='__next']/div/div[@class='train-wrapper return-view']/div[@class='return-box']/div[1]/div[2]/div[3]/div[1]")
        self.common_click(driver, By.XPATH,
                          "//div[@class='return-box']//div[1]//div[2]//div[3]//ul[1]//li[1]//div[1]//i[1]")
        self.common_click(driver, By.XPATH, "//ul[@class='screen-list open']//li[4]//div[1]//i[1]")
        self.common_click(driver, By.XPATH, "//ul[@class='screen-list open']//li[5]//div[1]//i[1]")
        # 【出发时间】、【到达时间】、选中第二个复选框
        self.common_click(driver, By.XPATH, "//ul[@class='screen-list open']//li[2]//div[2]//i[1]")
        self.common_click(driver, By.XPATH, "//ul[@class='screen-list open']//li[3]//div[2]//i[1]")
        # 截图
        self.take_screenshot(driver, file_name)

    @pytest.mark.parametrize("start_city,end_city,file_name", [
        ("123", "海南", "Ctrip_R007_001.png"),
        ("&*", "海南", "Ctrip_R007_002.png"),
        ("东方男", "海南", "Ctrip_R007_003.png"),
    ])
    def test_Ctirp_R007(self, driver, start_city, end_city, file_name):
        # 悬浮在菜单上
        hover_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='pc_home-tabbtnIcon lsn_ico_9C9TD']")))
        ActionChains(driver).move_to_element(hover_menu).perform()
        sleep(1)
        # 悬浮并且点击火车
        self.hover_click(driver, By.XPATH,
                         "//span[@class='lsn_top_nav_font_4h1KU lsn_top_nav_font_line_0iVuu'][contains(text(),'火车票')]",
                         By.XPATH,
                         "//a[@class='lsn_menu_son_nav_HoNwa']//span[@class='lsn_font_data_rSNIK'][contains(text(),'国内火车票')]")
        # 点击往返
        self.js_click(driver, By.XPATH, "//ul[@class='search-select']//li[button[text()='往返']] ")
        # 输入出发城市
        self.input_city(driver, By.XPATH, "//input[@id='label-departStation']", By.XPATH,
                        f'//ul[@class="widget-search-bd"]//div[contains(normalize-space(.), "{start_city}")]',
                        start_city)
        error_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//body/div[@id='hp_container']/div[@id='content']/div[@id='main']/div[@id='__next']/div[1]")))
        assert "对不起" in error_text.text
        # 截图
        self.take_screenshot(driver, file_name)
    def test_Ctirp_R008(self, driver):
        # 悬浮在菜单上
        hover_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='pc_home-tabbtnIcon lsn_ico_9C9TD']")))
        ActionChains(driver).move_to_element(hover_menu).perform()
        sleep(1)
        # 悬浮并且点击火车
        self.hover_click(driver, By.XPATH,
                         "//span[@class='lsn_top_nav_font_4h1KU lsn_top_nav_font_line_0iVuu'][contains(text(),'火车票')]",
                         By.XPATH,
                         "//a[@class='lsn_menu_son_nav_HoNwa']//span[@class='lsn_font_data_rSNIK'][contains(text(),'国内火车票')]")
        # 点击往返
        self.js_click(driver, By.XPATH, "//ul[@class='search-select']//li[button[text()='往返']] ")
        #点击出发地
        self.common_click(driver, By.XPATH,"//input[@id='label-departStation']")
        self.common_click(driver, By.XPATH,"//li[normalize-space()='NPQRS']")
        self.common_click(driver,By.XPATH,"//ul[@class='widget-city-bd']//li[contains(text(),'上海')]")
        #点击目的地
        self.common_click(driver,By.XPATH,"//input[@id='label-arriveStation']")
        self.common_click(driver,By.XPATH,"//li[contains(text(),'热门选择')]")
        self.common_click(driver,By.XPATH,"//ul[@class='widget-city-bd']//li[contains(text(),'北京')]")
        #选择出发日期
        self.open_depart_date(driver)
        self.choose_date(driver, "2025-11-18")
        #选择返程日期
        self.choose_return_date(driver)
        self.choose_date(driver,"2025-11-20")
        #只搜动车
        self.common_click(driver,By.XPATH,"//span[contains(text(),'只搜高铁动车')]")
        #点击搜索
        self.common_click(driver, By.XPATH, "//button[@class='btn-blue btn-search']")
        #在【去程】Tab中日期选择11-19周二
        self.common_click(driver,By.XPATH,"/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/ul[1]/li[3]")
        #然后【出发时间】全部勾选，【到达时间】、【坐席】、【出发车站】、【到达车站】选中第一个复选框
        self.common_click(driver, By.XPATH,
                          "//body/div[@id='hp_container']/div[@id='content']/div[@id='main']/div[@id='__next']/div/div[@class='train-wrapper return-view']/div[@class='return-box']/div[1]/div[2]/div[3]/div[1]")
        self.common_click(driver,By.XPATH,"//ul[@class='screen-list open']//li[2]//div[1]//i[1]")
        self.common_click(driver, By.XPATH, "//ul[@class='screen-list open']//li[2]//div[2]//i[1]")
        self.common_click(driver, By.XPATH, "//ul[@class='screen-list open']//li[2]//div[3]//i[1]")
        self.common_click(driver, By.XPATH, "//ul[@class='screen-list open']//li[2]//div[4]//i[1]")
        self.common_click(driver,By.XPATH,"//ul[@class='screen-list open']//li[3]//div[1]//i[1]")
        self.common_click(driver, By.XPATH, "//ul[@class='screen-list open']//li[4]//div[1]//i[1]")
        self.common_click(driver, By.XPATH, "//ul[@class='screen-list open']//li[5]//div[1]//i[1]")
        #截图
        self.take_screenshot(driver, "Ctrip_R008_001.png")
    # test-code-start
    @staticmethod
    def take_screenshot(driver, file_name):
        timestamp = datetime.now().strftime( "%H%M%S%d%f" )[:-3]
        timestamped_file_name = f"{timestamp}_{file_name}"
        screenshots_dir = "screenshots"
        if not os.path.exists( screenshots_dir ):
            os.makedirs( screenshots_dir )
        screenshot_file_path = os.path.join( screenshots_dir, timestamped_file_name )
        driver.save_screenshot( screenshot_file_path )
