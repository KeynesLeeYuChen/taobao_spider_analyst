from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import pandas as pd
from multiprocessing import Pool
data = pd.read_csv('data_url_normall.csv')
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
product = {}
#进入淘宝网，输入鞋子，返回页面
def search(url):
    try:
        browser.get('https:{}'.format(url))
            # input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
            # submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_SearchForm > button')))
            # input.send_keys(i)
            # submit.click()
            # total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        get_products(url)
            # return total.text
    except TimeoutException:
        pass

#得到淘宝商品信息
def get_products(url):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#attributes')))
    html = browser.page_source
    doc = pq(html)
    #pyquery （browser.page_source）就相当于requests.get获取的内容
    item = doc('#attributes')
    product = {
        'url': str(url),
        'detail': item.text().replace('\n',' '),
    }
    try:
        save_to_csv(product)
    except:
        pass

def save_to_csv(product):

    with open('product_details_normall.csv','a') as f:
        s=product['url']+','+product['detail']+'\n'
        try:
            f.write(s)
            print('保存到csv成功！',product)
        except:
            pass

def main():
    for i in data['url']:
        search(i)


if __name__ == '__main__':
    main()