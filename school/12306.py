import os
from datetime import datetime
from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture( scope="function" )
def driver():
    # 提交最终代码脚本时，请将驱动路径换回官方路径"C:\\Users\\86153\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe"
    service = Service(
       # executable_path="C:\\Users\\86153\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe" )
        executable_path=r"D:\ChromeDriver\chromedriver.exe")
    driver = webdriver.Chrome( service=service )
    driver.get( "https://www.12306.cn/index" )
    driver.maximize_window()
    driver.implicitly_wait( 10 )
    yield driver
    driver.quit()


class Test12306:

    # test-code-start

    # 请在此处插入Selenium+Pytest代码
    #工具函数
    def hover_click(self, driver,by_menu,menu_elem,by_click,click_elem):
        hover_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by_menu, menu_elem)))
        ActionChains(driver).move_to_element(hover_menu).perform()
        click_goback = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((by_click,click_elem)))
        ActionChains(driver).click(click_goback).perform()
        sleep(1)
    def input_city(self,driver,by_method,city_input,by,city_list,city_name):
        city_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by_method, city_input)))
        ActionChains(driver).click(city_element).perform()
        sleep(1.2)
        city_element.send_keys(city_name)
        city_opt = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, city_list)))
        ActionChains(driver).click(city_opt).perform()
        sleep(1)
    def depart_date(self,driver,by_method,date_xpath,date):
        date_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by_method, date_xpath)))
        ActionChains(driver).click(date_input).perform()
        sleep(1)
        date_input.clear()
        date_input.send_keys(date)
        sleep(1.2)
    def common_click(self,driver,by,xpath):
        elem = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((by,xpath)))
        ActionChains(driver).click(elem).perform()

        sleep(1)
    # 模块一单程车票查询
    @pytest.mark.parametrize("start_city,end_city,date,file_name",[
        ("北京","广州","2025-11-16","12306_R001_001.png"),
        ("北京", "成都", "2025-11-16", "12306_R001_002.png"),
        ("上海","广州","2025-11-16","12306_R001_003.png"),
        ("上海","成都","2025-11-16","12306_R001_004.png"),
    ])
    def test_12306_R001(self,driver,start_city,end_city,date,file_name):
    # 悬浮菜单，点击单程
        self.hover_click(driver,By.XPATH,"//a[@class='nav-hd item'][contains(text(),'车票')]",By.XPATH,"//a[contains(text(),'单程')]")
    #输入出发地
        self.input_city(driver,By.XPATH,"//input[@id='fromStationText']",By.XPATH,f"//div[@id='panel_cities']//span[text()='{start_city}']",start_city)
    #输入目的地
        self.input_city(driver,By.XPATH,"//input[@id='toStationText']",By.XPATH,f"//div[@id='panel_cities']//span[text()='{end_city}']",end_city)
    #输入出发日期
        self.depart_date(driver,By.XPATH,"//input[@id='train_date']",date)
    #点击搜索
        self.common_click(driver,By.XPATH,"//a[@id='query_ticket']")
    # 截图
        self.take_screenshot(driver,file_name)

    @pytest.mark.parametrize("start_city,end_city,date,file_name", [
        ("北京", "广州", "2025-11-10", "12306_R002_001.png"),
        ("北京", "成都", "2025-11-30", "12306_R002_002.png"),
    ])
    def test_12306_R002(self,driver,start_city,end_city,date,file_name):
        self.hover_click(driver, By.XPATH, "//a[@class='nav-hd item'][contains(text(),'车票')]", By.XPATH,
                         "//a[contains(text(),'单程')]")
        # 输入出发地
        self.input_city(driver, By.XPATH, "//input[@id='fromStationText']", By.XPATH,
                        f"//div[@id='panel_cities']//span[text()='{start_city}']", start_city)
        # 输入目的地
        self.input_city(driver, By.XPATH, "//input[@id='toStationText']", By.XPATH,
                        f"//div[@id='panel_cities']//span[text()='{end_city}']", end_city)
        # 输入出发日期
        self.depart_date(driver, By.XPATH, "//input[@id='train_date']", date)
        # 点击搜索
        self.common_click(driver, By.XPATH, "//a[@id='query_ticket']")
        # 截图
        self.take_screenshot(driver, file_name)
    def test_12306_R003(self,driver):
        self.hover_click(driver, By.XPATH, "//a[@class='nav-hd item'][contains(text(),'车票')]", By.XPATH,
                         "//a[contains(text(),'单程')]")
        # 输入出发地
        self.input_city(driver, By.XPATH, "//input[@id='fromStationText']", By.XPATH,
                        f"//div[@id='panel_cities']//span[text()='北京']", '北京')
        # 输入目的地
        self.input_city(driver, By.XPATH, "//input[@id='toStationText']", By.XPATH,
                        f"//div[@id='panel_cities']//span[text()='上海']", '上海')
        # 输入出发日期
        self.depart_date(driver, By.XPATH, "//input[@id='train_date']", '2025-11-17')
        # 点击搜索
        self.common_click(driver, By.XPATH, "//a[@id='query_ticket']")
        #点击每排第一个
    def click_first(self,driver):
        self.common_click(driver,By.XPATH, "//ul[@id='_ul_station_train_code']//label[text()='GC-高铁/城际']")
        self.common_click(driver, By.XPATH, '//ul[@id="from_station_ul"]/li[1]')
        self.common_click(driver, By.XPATH, '//ul[@id="to_station_ul"]/li[1]')
        self.common_click(driver, By.XPATH, '//ul[@id="seat_type_new_ul"]/li[1]')
        self.take_screenshot(driver, "12306_R003_001.png")
        #取消点击
        self.click_first(driver)
        self.take_screenshot(driver, "12306_R003_002.png")
    @pytest.mark.parametrize("start_city,end_city,godate,backdate,file_name", [
        ("北京", "南京","2025-11-15","2025-11-18", "12306_R004_001.png"),
        ("北京", "上海","2025-11-15","2025-11-21", "12306_R004_002.png"),
        ("重庆", "成都", "2025-11-15","2025-11-15","12306_R004_003.png"),
        ("重庆", "上海","2025-11-15","2025-11-24", "12306_R004_004.png"),
    ])
    def test_12306_R004(self,driver,start_city,end_city,godate,backdate,file_name):
        #进入往返页面
        self.hover_click(driver,By.XPATH, "//a[@class='nav-hd item'][contains(text(),'车票')]", By.XPATH,"//a[contains(text(),'往返')]")
        #点击输入出发地
        self.input_city(driver,By.XPATH, "//input[@id='fromStationText']", By.XPATH,f"//div[@id='panel_cities']//span[text()='{start_city}']", start_city)
        #点击输入目的地
        self.input_city(driver,By.XPATH, "//input[@id='toStationText']", By.XPATH,f"//div[@id='panel_cities']//span[text()='{end_city}']",end_city)
        #点击输入出发日
        self.depart_date(driver,By.XPATH, "//input[@id='train_date']", godate)
        #点击输入返程日
        self.depart_date(driver,By.XPATH, "//input[@id='back_train_date']", backdate)
        #点击搜索
        self.common_click(driver, By.XPATH, "//a[@id='query_ticket']")

    @pytest.mark.parametrize("start_city,end_city,godate,backdate,file_name", [
        ("北京", "南京", "2025-11-15", "2025-11-32", "12306_R005_001.png"),
        ("北京", "上海", "2025-11-15", "2025-11-27", "12306_R005_002.png"),
        ("重庆", "成都", "2025-11-15", "2025-11-14", "12306_R005_003.png"),
    ])
    def test_12306_R005(self, driver, start_city, end_city, godate, backdate, file_name):
        # 进入往返页面
        self.hover_click(driver, By.XPATH, "//a[@class='nav-hd item'][contains(text(),'车票')]", By.XPATH,
                         "//a[contains(text(),'往返')]")
        # 点击输入出发地
        self.input_city(driver, By.XPATH, "//input[@id='fromStationText']", By.XPATH,
                        f"//div[@id='panel_cities']//span[text()='{start_city}']", start_city)
        # 点击输入目的地
        self.input_city(driver, By.XPATH, "//input[@id='toStationText']", By.XPATH,
                        f"//div[@id='panel_cities']//span[text()='{end_city}']", end_city)
        # 点击输入出发日
        self.depart_date(driver, By.XPATH, "//input[@id='train_date']", godate)
        # 点击输入返程日
        self.depart_date(driver, By.XPATH, "//input[@id='back_train_date']", backdate)
        # 点击搜索
        self.common_click(driver, By.XPATH, "//a[@id='query_ticket']")
    def test_12306_R006(self,driver):
        # 进入往返页面
        self.hover_click(driver, By.XPATH, "//a[@class='nav-hd item'][contains(text(),'车票')]", By.XPATH,
                         "//a[contains(text(),'往返')]")
        #控件选择出发地
        self.common_click(driver, By.XPATH, "//input[@id='fromStationText']")
        self.common_click(driver, By.XPATH, "//li[@id='nav_list3']")
        self.common_click(driver, By.XPATH, "//li[@title='福州南']")
        #控件选择目的地
        self.common_click(driver,By.XPATH,"//input[@id='toStationText']")
        self.common_click(driver, By.XPATH, "//li[@title='厦门']")
        # 点击输入出发日返程日
        self.depart_date(driver, By.XPATH, "//input[@id='train_date']", "2025-11-15")
        self.depart_date(driver, By.XPATH, "//input[@id='back_train_date']", "2025-11-20")
        #选择学生
        self.common_click(driver, By.XPATH, "//label[@id='sf2_label']")
        # 点击搜索
        self.common_click(driver, By.XPATH, "//a[@id='query_ticket']")
        # 使用tab切换日期到11-19
        self.common_click(driver,By.XPATH, "//span[contains(text(),'11-19')]")
        # 选择车次类型最后的一个复选框
        self.common_click(driver, By.XPATH, '//*[@id="_ul_station_train_code"]/li[8]/label')
        # 出发车站和到达车站选择全部
        self.common_click(driver, By.XPATH, "//span[@id='from_station_name_all']")
        self.common_click(driver, By.XPATH, "//span[@id='to_station_name_all']")
        # 选择折扣车次
        self.common_click(driver, By.XPATH, "//label[@for='avail_zk']")
        # 截图
        self.take_screenshot(driver, "12306_R006_001.png")

    @pytest.mark.parametrize("departure_city,arrival_city,departure_day,file_name", [
        ("哈尔滨", "济南", "2025-11-15", "12306_R007_001.png"),
        ("长春", "西安", "2025-11-15", "12306_R007_002.png"),
        ("安吉", "拉萨", "2025-11-15", "12306_R007_003.png"),
    ])
    def test_12306_R007(self, driver, departure_city, arrival_city, departure_day, file_name):
        # 进入中转页面
        self.hover_click(driver, By.XPATH, "//a[@class='nav-hd item'][contains(text(),'车票')]", By.XPATH,
                         "//a[@name='g_href'][contains(text(),'中转换乘')]")
        # 点击输入出发地
        self.input_city(driver, By.XPATH, "//input[@id='fromStationText']", By.XPATH,
                        f"//div[@id='panel_cities']//span[text()='{departure_city}']", departure_city)
        # 点击输入目的地
        self.input_city(driver, By.XPATH, "//input[@id='toStationText']", By.XPATH,
                        f"//div[@id='panel_cities']//span[text()='{arrival_city}']", arrival_city)
        #选择出发日
        self.depart_date(driver, By.XPATH, "//input[@id='train_date']", departure_day)
        #点击搜索
        self.common_click(driver,By.XPATH,"//a[@id='query_ticket']")
        #截图
        self.take_screenshot(driver, file_name)
    @pytest.mark.parametrize("departure_city,arrival_city,departure_day,file_name", [
        ("哈尔滨", "@@s", "2025-11-11", "12306_R008_001.png"),
        ("长春", "132165", "2025-11-15", "12306_R008_002.png"),
    ])
    def test_12306_R008(self, driver, departure_city, arrival_city, departure_day, file_name):
        # 进入中转页面
        self.hover_click(driver, By.XPATH, "//a[@class='nav-hd item'][contains(text(),'车票')]", By.XPATH,
                         "//a[@name='g_href'][contains(text(),'中转换乘')]")
        # 点击输入出发地
        self.input_city(driver, By.XPATH, "//input[@id='fromStationText']", By.XPATH,
                        f"//div[@id='panel_cities']//span[text()='{departure_city}']", departure_city)
        # 点击输入目的地
        input_error=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='toStationText']")))
        ActionChains(driver).click(input_error).perform()
        sleep(1)
        input_error.send_keys(arrival_city)
       #断言
        notice = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@id='form_cities']//div[@id='top_cities' and contains(text(),'无法匹配')]"))
        )
        assert "无法匹配" in notice.text, f"Expected '无法匹配' but got {notice.text}"
        print(f"Success: '{notice.text}' contains '无法匹配'")
        #截图
        self.take_screenshot(driver, file_name)
    @pytest.mark.parametrize("departure_city,arrival_city,transfer_city,departure_day,file_name", [
        ("哈尔滨", "南京","济南", "2025-11-15", "12306_R009_001.png"),
        ("哈尔滨", "南京","安阳", "2025-11-15", "12306_R009_002.png"),
    ])
    def test_12306_R009(self, driver, departure_city, arrival_city, transfer_city,departure_day, file_name):
        # 进入中转页面
        self.hover_click(driver, By.XPATH, "//a[@class='nav-hd item'][contains(text(),'车票')]", By.XPATH,
                         "//a[@name='g_href'][contains(text(),'中转换乘')]")
        # 点击输入出发地
        self.input_city(driver, By.XPATH, "//input[@id='fromStationText']", By.XPATH,
                        f"//div[@id='panel_cities']//span[text()='{departure_city}']", departure_city)
        # 点击输入目的地
        self.input_city(driver, By.XPATH, "//input[@id='toStationText']", By.XPATH,
                        f"//div[@id='panel_cities']//span[text()='{arrival_city}']", arrival_city)
        # 点击换乘复选框
        self.common_click(driver,By.XPATH,"//input[@id='radio_input_search']")
        # 输入换乘站
        self.input_city(driver,By.XPATH, "//input[@id='changeStationText']", By.XPATH,f"//div[@id='panel_cities']//span[text()='{transfer_city}']", transfer_city)
        # 选择出发日
        self.depart_date(driver, By.XPATH, "//input[@id='train_start_date']", departure_day)
        #点击搜索
        self.common_click(driver,By.XPATH,"//a[@id='_a_search_btn']")
        #截图
        self.take_screenshot(driver, file_name)
    @pytest.mark.parametrize("start_city,end_city,file_name", [
        ("北京", "大厂", "12306_R010_001.png"),
        ("北京", "唐山", "12306_R010_002.png"),
    ])
    def test_12306_R010(self,driver,start_city,end_city,file_name):
        # 进入济慈票页面
        self.hover_click(driver,By.XPATH, "//a[@class='nav-hd item'][contains(text(),'车票')]", By.XPATH,"//li[@role='menuitemradio']//a[@name='g_href'][contains(text(),'计次•定期票')]")
        self.common_click(driver,By.LINK_TEXT,"扫码登录")
       #成功进入登录页面再次跳转
        login_cache = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.LINK_TEXT,"个人中心")))
        sleep(1)
        self.hover_click(driver, By.XPATH, "//a[@class='nav-hd item'][contains(text(),'车票')]", By.XPATH,
                         "//li[@role='menuitemradio']//a[@name='g_href'][contains(text(),'计次•定期票')]")
        sleep(1.5)
        #输入出发地
        self.common_click(driver,By.ID,'city-start')
        opt = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,f'//ul[@id="start-box"]//li[text()="{start_city}"]')))
        opt.click()
        sleep(1)
        #输入目的地
        self.common_click(driver,By.ID,'city-end')
        opt_end = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,f"//ul[@id='end-box']//li[text()='{end_city}']")))
        ActionChains(driver).click(opt_end).perform()
        sleep(1)
        #点击搜索
        self.common_click(driver,By.XPATH,"//a[@class='btn btn-primary w140 go-search']")
        #截图
        self.take_screenshot(driver, file_name)

    @pytest.mark.parametrize("start_city,file_name", [
        ("北京", "12306_R010_001.png"),
        ("北京",  "12306_R010_002.png"),
    ])
    def test_12306_R011(self, driver, start_city, file_name):
        # 进入济慈票页面
        self.hover_click(driver, By.XPATH, "//a[@class='nav-hd item'][contains(text(),'车票')]", By.XPATH,
                         "//li[@role='menuitemradio']//a[@name='g_href'][contains(text(),'计次•定期票')]")
        self.common_click(driver, By.LINK_TEXT, "扫码登录")
        # 成功进入登录页面再次跳转
        login_cache = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.LINK_TEXT, "个人中心")))
        sleep(1)
        self.hover_click(driver, By.XPATH, "//a[@class='nav-hd item'][contains(text(),'车票')]", By.XPATH,
                         "//li[@role='menuitemradio']//a[@name='g_href'][contains(text(),'计次•定期票')]")
        sleep(1.5)
        # 输入出发地
        self.common_click(driver, By.ID, 'city-start')
        opt = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//ul[@id="start-box"]//li[text()="{start_city}"]')))
        opt.click()
        sleep(1)
        # 点击搜索
        self.common_click(driver, By.XPATH, "//a[@class='btn btn-primary w140 go-search']")
        # 截图
        self.take_screenshot(driver, file_name)
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
