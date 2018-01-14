#encoding:utf-8
import requests
import re
import sys,time
from bs4 import BeautifulSoup
import csv

with open('melon.html',encoding='utf8') as f:
    data = f.read()
soup = BeautifulSoup(data,"lxml")
books = soup.find_all("p", class_="name")
circles = soup.find_all("p", class_="circle")
prices = soup.find_all("td", class_="price2")

nms = []
dts = []
crs = []
prs = []

for book in books:
    tt = book.find("a")["title"]
    nms.append(tt[tt.find(" ")+1:])
    print(tt[tt.find(" ")+1:])
    url = "https://www.melonbooks.co.jp" + book.find("a")["href"] + "&adult_view=1"
    page = requests.get(url).text
    soupB = BeautifulSoup(page,"lxml")
    try:
        date = soupB.find("em").text.replace("発売日：","")
        dts.append(date)
    except:
        dts.append("不明")
    
for circle in circles:
    cr = circle.find("a")["title"]
    crs.append(cr)

i = 0
for price in prices:
    i+=1
    if i == 2:
        hontai = int(price.text[1:].replace(",",""))
        print(hontai)
    elif i == 3:
        pr = hontai + int(price.text[1:].replace(",",""))
        prs.append(pr)
        i = 0
    
with open('test.csv','a',newline='') as f:
    writer = csv.writer(f)
    for i in range(0,len(nms)):
        writer.writerow([nms[i],crs[i],prs[i],dts[i]])
