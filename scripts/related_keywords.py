import requests
import bs4

kwd = "메이플"

url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=" + kwd

http = requests.get(url)

html = bs4.BeautifulSoup(http.text, 'html.parser')

result = html.find_all("div", {"class":"tit"})

for i in result:
    print(i.text)