from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

format_url = "https://www.time.ir/fa/event/list/0/{}/{}/{}"
# 1399 kabise

years = [i+1395 for i in range(10)]
months = [i+1 for i in range(12)]
days = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30]


def kabise(x):
    return (1399-x) % 4 == 0

events_file=open('events.db','wb')

i=1

for year in years:
    if (kabise(year)):
        days.append(30)
    else:
        days.append(29)
    for month in months:
        for day in range(1, days[month-1]+1):

            opened_url = urlopen(format_url.format(year, month, day))
            html_page = opened_url.read()
            opened_url.close()

            soup = BeautifulSoup(html_page, 'html.parser')

            events_pre = soup.find('ul', {'class': 'list-unstyled'})
            try:
                events = soup.find_all("span", text=re.compile(events_pre.span.text))
            except:
                events=""
            events_file.write('{},{},{}'.format(year, month, day).encode(encoding="utf-8"))

            for event in events:
                events_file.write((',"'+str(event.next_sibling.strip())+'"').encode(encoding="utf-8"))
            events_file.write("\n".encode("utf-8"))
            print(f"{i}/3653")
            i+=1
        events_file.close()
        events_file=open('events.db','ab')
    days.pop()
