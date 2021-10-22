#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xilock 2021.10.22
"""
使用说明
1. 安装 python 3；
2. 安装selenium (python包,pip install selenium) 与 chromedriver (驱动,http://chromedriver.storage.googleapis.com/index.html)；
3. 调用该脚本；
4. 注意：及时更新脚本中的“XPATH”，建议使用chrome插件Xpath finder。
"""

import time 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib.parse import urljoin


def open_page(driver , theme):
    # 打开页面
    driver.get("http://www.globalauthorid.com/WebPortal/EliteOrder")
    # 传入关键字
    WebDriverWait( driver, 100 ).until( EC.presence_of_element_located( (By.XPATH ,'''//input[@id='ContentPlaceHolder1_txtSearchText4']''') ) ).send_keys(theme)
    # 点击搜索
    WebDriverWait( driver, 100 ).until( EC.presence_of_element_located( (By.XPATH ,"//span[@class='glyphicon glyphicon-search']") ) ).click()
    time.sleep(3)
    # 获取总文献数和页数
    res_unm = WebDriverWait( driver, 100 ).until( EC.presence_of_element_located( (By.XPATH ,"//span[@id='ContentPlaceHolder1_LabelCount']") ) ).text
    res_unm = int(res_unm)
    page_unm = int(res_unm/100) + 1
    print(f"共找到 {res_unm} 条结果, {page_unm} 页。")
    return res_unm

def crawl(driver, papers_need, theme):
# 写入文件题头
    res = f"序号\t名字\t国家\t组织\t学科\t论文总评分\t论文篇均评分\tH因子\t论文数".replace("\n","")+"\n"
    print(res)
    with open(f'get_globalauthorid_{theme}.tsv', 'a', encoding='gbk') as f:
        f.write(res)
    
    count = 1
    while count < papers_need:
#        time.sleep(0.5)
        # 循环网页一页中的条目   
        length = 101
        for i in range(1, length):
#            time.sleep(0.5)
            try:
                term = count%100   # 本页的第几个条目
                print(term)
                if term == 0:
                    term = 100
                
                name_xpath    = f"/html[1]/body[1]/form[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/div[3]/div[1]/div[1]/table[1]/tbody[1]/tr[{i+1}]/td[2]/span[1]"    
                country_xpath = f"/html[1]/body[1]/form[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/div[3]/div[1]/div[1]/table[1]/tbody[1]/tr[{i+1}]/td[3]/span[1]"    
                company_xpath = f"/html[1]/body[1]/form[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/div[3]/div[1]/div[1]/table[1]/tbody[1]/tr[{i+1}]/td[4]/span[1]"    
                major_xpath   = f"/html[1]/body[1]/form[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/div[3]/div[1]/div[1]/table[1]/tbody[1]/tr[{i+1}]/td[5]/span[1]"    
                scoreT_xpath  = f"/html[1]/body[1]/form[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/div[3]/div[1]/div[1]/table[1]/tbody[1]/tr[{i+1}]/td[6]/span[1]"    
                scoreE_xpath  = f"/html[1]/body[1]/form[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/div[3]/div[1]/div[1]/table[1]/tbody[1]/tr[{i+1}]/td[7]/span[1]"    
                Hindex_xpath  = f"/html[1]/body[1]/form[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/div[3]/div[1]/div[1]/table[1]/tbody[1]/tr[{i+1}]/td[8]"    
                paper_xpath   = f"/html[1]/body[1]/form[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/div[3]/div[1]/div[1]/table[1]/tbody[1]/tr[{i+1}]/td[9]"    



                name = WebDriverWait( driver, 10 ).until( EC.presence_of_element_located((By.XPATH ,name_xpath) ) ).text
                country = WebDriverWait( driver, 10 ).until( EC.presence_of_element_located((By.XPATH ,country_xpath) ) ).text
                company = WebDriverWait( driver, 10 ).until( EC.presence_of_element_located((By.XPATH ,company_xpath) ) ).text
                major = WebDriverWait( driver, 10 ).until( EC.presence_of_element_located((By.XPATH ,major_xpath) ) ).text
                Hindex = WebDriverWait( driver, 10 ).until( EC.presence_of_element_located((By.XPATH ,Hindex_xpath) ) ).text
                paper = WebDriverWait( driver, 10 ).until( EC.presence_of_element_located((By.XPATH ,paper_xpath) ) ).text                
                scoreT = WebDriverWait( driver, 10 ).until( EC.presence_of_element_located((By.XPATH ,scoreT_xpath) ) ).text
                scoreE = WebDriverWait( driver, 10 ).until( EC.presence_of_element_located((By.XPATH ,scoreE_xpath) ) ).text     
                
                # 写入文件
                res = f"{count}\t{name}\t{country}\t{company}\t{major}\t{Hindex}\t{paper}\t{scoreT}\t{scoreE}".replace("\n","")+"\n"
                print(res)
                with open(f'get_globalauthorid_{theme}.tsv', 'a', encoding='gbk') as f:
                    f.write(res)

            except:
                print(f" 第{count} 条爬取失败\n")
                # 跳过本条，接着下一个
                continue
            finally:
                # 计数,判断需求是否足够
                if count == papers_need:break
                count += 1
        
        # 切换到下一页
        if count == papers_need:break
        WebDriverWait( driver, 10 ).until( EC.presence_of_element_located( (By.XPATH ,"//a[contains(text(),'下一页')]") ) ).click()
        
def main():
    #get直接返回，不再等待界面加载完成
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    # 设置谷歌驱动器的环境
    options = webdriver.ChromeOptions()
    # 设置chrome不加载图片，提高速度
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    # 设置不显示窗口
#    options.add_argument('--headless')
    # 创建一个谷歌驱动器
    driver = webdriver.Chrome(options=options)
    # 设置搜索主题
#    theme = "丁二酸丁二酯"
    theme = "石油"
    # 判断所需总篇数
    res_unm =  int(open_page(driver, theme))
    papers_need =  res_unm
    crawl(driver, papers_need, theme)
    # 关闭浏览器
#    driver.close()

main()
