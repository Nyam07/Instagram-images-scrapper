from conf import MY_USERNAME, MY_PASSWORD
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import os
import wget




PATH = "C:\Program Files (x86)\chromedriver.exe"
browser = webdriver.Chrome(PATH)

url = "https://www.instagram.com"
browser.get(url)

username_el =WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password_el =WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

username_el.clear()
password_el.clear()

username_el.send_keys(MY_USERNAME)
password_el.send_keys(MY_PASSWORD)

login_btn_el = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))

login_btn_el.click()

bt_now = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
bt_now2 = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()

search_el = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder = 'Search']")))

search_el.clear()
keyword = "#piano"
search_el.send_keys(keyword)

#FIXING THE DOUBLE ENTER
time.sleep(5)  # Wait for 5 seconds
my_link = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
    (By.XPATH, "//a[contains(@href, '/" + keyword[1:] + "/')]")))
my_link.click()

#scroll down 2 times
n_scrolls = 2
for j in range(0, n_scrolls):
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(5)

#target all the links in the page
anchors = browser.find_elements_by_tag_name('a')
anchors = [a.get_attribute('href') for a in anchors]
#narrow down all links to image links only
anchors = [a for a in anchors if str(
    a).startswith("https://www.instagram.com/p/")]
#print('Found ' + str(len(anchors)) + ' links to images')
#print(anchors[:5])


images = []
# follow each image link and extract only the image atindex=1

for a in anchors:
    browser.get(a)
    time.sleep(5)
    img= browser.find_elements_by_tag_name('img')
    img = [i.get_attribute('src') for i in img]
    images.append(img[1])

#print(images[:5])


# create a new directory to save the images
path = os.getcwd()  # navigate to current directory
path = os.path.join(path, keyword[1:] + "s")    # create a new directory with the keyword as the name except the # and add an s in the end

os.mkdir(path)   # makes the directory



counter = 0
for image in images:
    # specify the names
    save_as = os.path.join(path, keyword[1:] + str(counter) + '.jpg')
    wget.download(image, save_as)
    counter +=1