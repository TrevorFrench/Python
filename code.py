import requests
from bs4 import BeautifulSoup, SoupStrainer
import bs4, csv
search_link = "https://www.census.gov/programs-surveys/popest.html"

r = requests.get(search_link)
raw_html = r.text
soup = BeautifulSoup(raw_html, 'html.parser')
all_links = soup.find_all("a")
r.content

i = []

for link in all_links:
    i.append(link.get('href'))

finalList = set()

index = 0

while index < len(i):
    if str(i[index]).endswith('.pdf'):
        index += 1
    elif str(i[index]).endswith('.xlsx'):
        index += 1
    elif str(i[index]).startswith('http', 0):
        finalList.add(i[index])
        index += 1
    elif str(i[index]).startswith('/', 0):
        finalList.add("https://www.census.gov/programs-surveys" + i[index])
        index += 1
    else:
        index += 1
    
uniqueList = list(finalList)
    
with open("output.csv","w",newline="") as f:
    cw =csv.writer(f)
    for item in uniqueList:
        cw.writerow([item])
    
f.close()

print("Successfully Executed Script!")

# print(r.content)