#! -*- coding:utf-8 -*-
import datetime
import time

import pymysql
import requests
from lxml import etree
from selenium import webdriver

driver = webdriver.Chrome()

def get_one_page(url):

    driver.get(url)
    html = driver.page_source
    return html

def next_page():
    for i in range(1,101):  # selenium 循环翻页成功！
        driver.find_element_by_xpath('//*[@id="js-pjax-container"]/div/div[3]/div/div[3]/div/a[last()]').click()
        time.sleep(3)
        html = driver.page_source
        return html

def parse_page(html):
    selector = etree.HTML(html)
    title = selector.xpath('//*[@id="js-pjax-container"]/div/div[3]/div/ul/li/div[1]/h3/a/text()')
    links = selector.xpath('//*[@id="js-pjax-container"]/div/div[3]/div/ul/li/div[1]/h3/a/@href')
    desc = selector.xpath('//*[@id="js-pjax-container"]/div/div[3]/div/ul/li/div[1]/p/text()')
    f_desc = []
    for item in desc:

        str_f = "".join(item)
        f_desc.append(str_f)
    stars = selector.xpath('//*[@id="js-pjax-container"]/div/div[3]/div/ul/li/div[2]/div[2]/a/text()')
    f_stars = []
    # 需要去列表中的奇数索引值的值
    for item in stars:

        str_f = "".join(item.split())
        f_stars.append(str_f)

    for i1,i2,i3,i4 in zip(title,links,f_stars[1::2],f_desc[1::2]):
        big_list.append((i1,"https://github.com"+i2,i3,i4))
    return big_list





def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='Github',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    # 这里是判断big_list的长度，不是content字符的长度
    try:
        cursor.executemany('insert into cPlus (title,links,stars,sh_desc) values (%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except :
        print('出列啦')



if __name__ == "__main__":
    big_list = []
    url = 'https://github.com/search?l=C%2B%2B&o=desc&q=c%2B%2B&s=stars&type=Repositories'

    html = get_one_page(url)
    content = parse_page(html)
    time.sleep(5)
    insertDB(content)
    while True:
        html = next_page()
        time.sleep(10)

        content = parse_page(html)
        insertDB(content)
        print(datetime.datetime.now())

#
# create table cPlus(
# id int not null primary key auto_increment,
# title text,
# links text,
# stars varchar(10),
# sh_desc text
# ) engine=InnoDB  charset=utf8;


# drop  table cPlus;