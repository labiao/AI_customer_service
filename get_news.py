import requests
from bs4 import BeautifulSoup   # Beautiful Soup是一个可以从HTML或XML文件中提取结构化数据的Python库

#要爬的网页
url = "https://news.baidu.com/mil"
# 构造头文件，模拟浏览器访问,否则访问个别网页会出现403错误，headers可以随便复制一个即可我的前第一篇爬虫文章中有些如何获取headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
#用requests库中的gete方法向网页发送请求
page = requests.get(url)
#获取html
html=page.text
#print(html)
# 将获取到的内容转换成BeautifulSoup格式，并将html.parser作为解析器
soup = BeautifulSoup(html, 'html.parser')
# 查找html中所有a标签中class='title'的语句，所查找到的内容返回到变量a_labels中
a_labels = soup.find_all('a', 'title')
#获取所有<a>标签中的href对应的值，即超链接
for a in a_labels:
    print(a.string)
    print(a.get('href'))