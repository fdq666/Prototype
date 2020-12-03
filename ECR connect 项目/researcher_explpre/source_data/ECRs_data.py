from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import xml.etree.ElementTree as ET

# 1. Determine whether they are ECRs, not have "Prof."  5841  person_ECRs.pkl
# 2. Determine whether the "describe" is empty  1370   person_describe.pkl
# 3. Determine whether there is "output"  1279    person_describe_output.pkl
# 4. Is there interest in describe 517 right_person.pkl
# 5. Is there "Reader" in the title 103 person_choose_final.pkl

right_person = []
i = 0
for url in all_person:
    try:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features='lxml')

        # Judgment condition 1 2: are ECRs
        name = soup.find('h2', {"class": "title"}).find('span').get_text()

        # Judgment condition 3: have output
        output = []
        tabs = soup.find('ul', {"class": "tabs"}).find_all('span')
        for t in tabs:
            output.append(''.join(t.get_text().split()))

        # Judgment condition 4: have interest
        describe = []
        text = soup.find('div', {"class": "rendering rendering_person rendering_edinburghpersonportal rendering_person_edinburghpersonportal"})
        h3 = text.find_all('h3')
        div = text.find_all(['div','table'],{"class":"textblock"})
        for w in range(len(h3)):
            h = h3[w].get_text()
            describe.append(''.join(h.split()))
        i = i+1
        if i % 10 == 0:
            print(i, end=" ")
        if ('Researchoutputs' in output) and ('ResearchInterests' in describe) and (('Mrs'or'Dr'or 'Mr' or 'Ms') in name):
            right_person.append(url)
    except:
        continue

person_final = []
i = 0
for url in person_choose:
    try:
        i = i + 1
        if i % 10 == 0:
            print(i, end=" ")
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features='lxml')

        # Judgment condition 5: readers not in title
        name = soup.find('h2', {"class": "title"})
        title = name.nextSibling.get_text()
        if 'Reader' not in title:
            print(url)
            person_final.append(url)
    except:
        continue

