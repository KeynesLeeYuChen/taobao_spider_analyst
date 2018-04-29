from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import re

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
product = {}
#进入淘宝网，输入鞋子，返回页面
def search():
    try:
        browser.get('https://www.taobao.com/')
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
        input.send_keys(u'口红')
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        get_products()
        return total.text
    except TimeoutException:
        return search()
#跳转到下一页
def next_page(page_number):
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)
#得到淘宝商品信息
def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    #pyquery （browser.page_source）就相当于requests.get获取的内容
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            # 'image':item.find('.pic .img').attr('src'),
            'url':item.find('.J_ClickStat').attr('href'),
            'price':item.find('.price').text().replace('\n',''),
            'deal':item.find('.deal-cnt').text()[:-3],
            'title':item.find('.title').text().replace('\n','').replace(',',''),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text(),
        }
        save_to_csv(product)

def save_to_csv(product):

    with open('taobao.csv','a') as f:
        s=product['title']+','+product['price']+','+product['deal']+','+product['location']+','+product['shop']+','+product['url']+'\n'
        try:
            f.write(s)
            print('保存到csv成功！',product)
        except:
            pass

def main():
    total = search()
    total = int(re.compile('(\d+)').search(total).group(1))
    #爬取所有的数据用total+1
    for i in range(2,total+1):
        next_page(i)


if __name__ == '__main__':
    main()