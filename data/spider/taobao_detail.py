from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import pandas as pd
import re
data = pd.read_csv('taobao_drop.csv')
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
product = {}
#进入淘宝网，输入鞋子，返回页面
def search():
    for i in data[data['tmall']!="天猫"]['shop'].unique():
        try:
            browser.get('https://shopsearch.taobao.com/search?app=shopsearch&q={}&js=1&initiative_id=staobaoz_20180427&ie=utf8'.format(i))
            # input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
            # submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_SearchForm > button')))
            # input.send_keys(i)
            # submit.click()
            # total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
            get_products(i)
            # return total.text
        except TimeoutException:
            return search()

#得到淘宝商品信息
def get_products(i):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#list-container > li:nth-child(1)')))
    html = browser.page_source
    doc = pq(html)
    #pyquery （browser.page_source）就相当于requests.get获取的内容
    items = doc('#list-container > li:nth-child(1) > ul > li.list-info.icon-5zhe > h4').items()
    for item in items:
        product = {
            'shop':str(i),
            'rank':item.find('.rank').attr('class'),
            'name': item.find('.shop-name').text(),
        }
        try:
            save_to_csv(product)
        except:
            pass


def save_to_csv(product):

    with open('taobao_shop.csv','a') as f:
        s=product['shop']+','+product['name']+','+product['rank']+'\n'
        try:
            f.write(s)
            print('保存到csv成功！',product)
        except:
            pass

def main():
    search()


if __name__ == '__main__':
    main()