import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from hashlib import md5

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

def search():
    driver.get('https://www.toutiao.com')
    input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#rightModule > div.search-wrapper > div > div > div.tt-input.tt-input-group.tt-input-group--append > input"))
    )
    submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#rightModule > div.search-wrapper > div > div > div.tt-input.tt-input-group.tt-input-group--append > div > button')))
    input.send_keys('街拍')
    submit.click()

def click(num):
    #driver.get('https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D')
        driver.switch_to_window(driver.window_handles[1])     #机制问题！！！！！
        selector = '#J_section_' + str(num) + ' > div > div > div > div > div.title-box > a > span'
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        submit.click()

def count(num):
    selector = '#J_section_' + str(num) + ' > div > div > div > div > div.img-list.y-box > span'
    total = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, selector))).text
    count = total[:1]
    print(count)
    return int(count)



def getlink(count):
    selector = 'body > div > div.bui-box.container > div.galleryBox > div > div > div.bui-left.image-box > div > div > ul > li:nth-child(' + str(count) + ') > div > a'
    driver.switch_to_window(driver.window_handles[2])      #机制问题！！！！！
    submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
    submit.click()
    driver.switch_to_window(driver.window_handles[3])     #机制问题！！！！！
    url = driver.current_url
    driver.close()
    return url


def download_image(url):
    response=requests.get(url)
    try:
        if response.status_code==200:
            return response.content
        return None
    except RequestException:
        return None

def save_image(content):
    path_name='{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    if not os.path.exists(path_name):
        with open(path_name,'wb') as f:
            f.write(content)
            f.close()


def main():
    search()
    for num in range(0,5):
        click(num)
        countnum =count(num)
        for i in range(1,countnum+1):
                url = getlink(i)
                content = download_image(url)
                save_image(content)
        driver.switch_to_window(driver.window_handles[2])    #机制问题！！！！！
        driver.close()
    driver.quit()




if __name__ == '__main__':
    main()
