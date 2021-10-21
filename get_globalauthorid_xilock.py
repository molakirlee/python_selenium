#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xilock 2021.08.23
"""
使用说明
1. 安装 python 3；
2. 安装selenium (python包,pip install selenium) 与 chromedriver (驱动,http://chromedriver.storage.googleapis.com/index.html)；
3. 调用该脚本；
4. 注意：CNKI有更新和反爬，及时更新脚本中的“XPATH”，建议使用chrome插件Xpath finder。
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
#    driver.get("https://www.cnki.net")
    driver.get("http://www.globalauthorid.com/WebPortal/EliteOrder")
    # 传入关键字
#    WebDriverWait( driver, 100 ).until( EC.presence_of_element_located( (By.XPATH ,'''//*[@id="txt_SearchText"]''') ) ).send_keys(theme)
    WebDriverWait( driver, 100 ).until( EC.presence_of_element_located( (By.XPATH ,'''//input[@id='ContentPlaceHolder1_txtSearchText4']''') ) ).send_keys(theme)
    # 点击搜索
#    WebDriverWait( driver, 100 ).until( EC.presence_of_element_located( (By.XPATH ,"/html/body/div[2]/div[2]/div/div[1]/input[2]") ) ).click()
    WebDriverWait( driver, 100 ).until( EC.presence_of_element_located( (By.XPATH ,"//span[@class='glyphicon glyphicon-search']") ) ).click()
    time.sleep(3)
    # 点击切换中文文献
#    WebDriverWait( driver, 100 ).until( EC.presence_of_element_located( (By.XPATH ,"/html/body/div[3]/div[1]/div/div/div/a[1]") ) ).click()
#    WebDriverWait( driver, 100 ).until( EC.presence_of_element_located( (By.XPATH ,"/html/body/div[3]/div[1]/div/ul[1]/li[1]/a") ) ).click()
    time.sleep(1)
    # 获取总文献数和页数
#    res_unm = WebDriverWait( driver, 100 ).until( EC.presence_of_element_located( (By.XPATH ,"/html/body/div[3]/div[2]/div[2]/div[2]/form/div/div[1]/div[1]/span[1]/em") ) ).text
    res_unm = WebDriverWait( driver, 100 ).until( EC.presence_of_element_located( (By.XPATH ,"//span[@id='ContentPlaceHolder1_LabelCount']") ) ).text
    res_unm = int(res_unm)
    # 去除千分位里的逗号
#    res_unm = int(res_unm.replace(",",''))
#    page_unm = int(res_unm/20) + 1
    page_unm = int(res_unm/100) + 1
    print(f"共找到 {res_unm} 条结果, {page_unm} 页。")
    return res_unm

def crawl(driver, papers_need, theme):
# 写入文件题头
    res = f"序号\t名字\t国家\t组织\t学科\tH因子\t论文数\t论文总评分\t论文篇均评分".replace("\n","")+"\n"
    print(res)
    with open(f'get_CNKI_{theme}.tsv', 'a', encoding='gbk') as f:
        f.write(res)
    
    count = 1
    while count < papers_need:
#        time.sleep(1)
#        title_list = WebDriverWait( driver, 10 ).until( EC.presence_of_all_elements_located( (By.CLASS_NAME  ,"fz14") ) )
        # 循环网页一页中的条目   
        length = 101
        for i in range(1, length):
#            time.sleep(1)
            try:
                term = count%100   # 本页的第几个条目
                print(term)
                if term == 0:
                    term = 100
                
                ii =i-1
                name_xpath = f"//span[@id='ContentPlaceHolder1_gvList_LabelValue2_{ii}']"    
                name = WebDriverWait( driver, 10 ).until( EC.presence_of_element_located((By.XPATH ,name_xpath) ) ).text
                country_xpath = f"//span[@id='ContentPlaceHolder1_gvList_LabelValue3_{ii}']"    
                country = WebDriverWait( driver, 10 ).until( EC.presence_of_element_located((By.XPATH ,country_xpath) ) ).text
                company_xpath = f"//span[@id='ContentPlaceHolder1_gvList_LabelValue4_{ii}']"    
                company = WebDriverWait( driver, 10 ).until( EC.presence_of_element_located((By.XPATH ,company_xpath) ) ).text
                major_xpath = f"/html[1]/body[1]/form[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/div[3]/div[1]/div[1]/table[1]/tbody[1]/tr[{ii+2}]/td[5]/span[1]"    
                major = WebDriverWait( driver, 10 ).until( EC.presence_of_element_located((By.XPATH ,major_xpath) ) ).text
                Hindex_xpath = f"//span[@id='ContentPlaceHolder1_gvList_LabelValue8_{ii}']"    
                Hindex = WebDriverWait( driver, 10 ).until( EC.presence_of_element_located((By.XPATH ,Hindex_xpath) ) ).text
                paper_xpath = f"//span[@id='ContentPlaceHolder1_gvList_LabelValue10_{ii}']"    
                paper = WebDriverWait( driver, 10 ).until( EC.presence_of_element_located((By.XPATH ,paper_xpath) ) ).text                
                
                scoreT_xpath = f"/html[1]/body[1]/form[1]/table[1]/tbody[1]/tr[2]/td[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/div[3]/div[1]/div[1]/table[1]/tbody[1]/tr[{i+1}]/td[6]/span[1]"    
                scoreT = WebDriverWait( driver, 10 ).until( EC.presence_of_element_located((By.XPATH ,scoreT_xpath) ) ).text
                scoreE_xpath = f"//span[@id='ContentPlaceHolder1_gvList_LabelValue7_{ii}']"    
                scoreE = WebDriverWait( driver, 10 ).until( EC.presence_of_element_located((By.XPATH ,scoreE_xpath) ) ).text     
                
                # 写入文件
                res = f"{count}\t{name}\t{country}\t{company}\t{major}\t{Hindex}\t{paper}\t{scoreT}\t{scoreE}".replace("\n","")+"\n"
                print(res)
                with open(f'get_CNKI_{theme}.tsv', 'a', encoding='gbk') as f:
                    f.write(res)

            except:
                print(f" 第{count} 条爬取失败\n")
                # 跳过本条，接着下一个
                continue
            finally:
                # 如果有多个窗口，关闭第二个窗口， 切换回主页
#                n2 = driver.window_handles
#                if len(n2) > 1:
#                    driver.close()
#                    driver.switch_to_window(n2[0])
                # 计数,判断需求是否足够
#                count += 1
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
    theme = "化学"
    # 设置所需篇数
#    papers_need = 200
    res_unm =  int(open_page(driver, theme))
    # 判断所需是否大于总篇数
#    papers_need = papers_need if (papers_need <= res_unm) else res_unm
    papers_need =  res_unm
    crawl(driver, papers_need, theme)
    # 关闭浏览器
#    driver.close()

main()
