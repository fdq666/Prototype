from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import xml.etree.ElementTree as ET


def Profile(url_person):
    profile = []
    college = []
    describle = []
    html = urlopen(url_person).read()
    soup = BeautifulSoup(html, features='lxml')
    # name
    name = soup.find('h2', {"class": "title"}).find('span').get_text()
    profile.append(name)

    # college
    colleges = soup.find('ul', {"class": "relations organisations"}).find_all('span')
    # print(colleges)
    for s in colleges:
        college.append(s.get_text())
    profile.append(college)

    # profile
    text = soup.select('div.staff_profile div.textblock')
    for t in text:
        d = t.get_text()
        describle.append(d)

    profile.append(describle)
    return profile


def Project(url_project):
    first = []
    second = []

    project = []

    html = urlopen(url_project).read()
    soup = BeautifulSoup(html, features='lxml')

    ol = soup.find('ol', {"class": "portal_list"})
    # first:title
    titles = ol.find_all('h2', {"class": "title"})
    for t in titles:
        t = t.find('span').get_text()
        first.append(t)
    #     print(len(first))

    # second:period
    period = ol.find_all('p', {"class": "period"})
    date = []
    if period != []:
        for p in period:
            time = p.find_all('span')
            if len(time) == 2:
                for t in time:
                    date.append(t.get_text())
            else:
                for t in time:
                    date.append(t.get_text())
                    date.append('...')
        for i in range(len(date)):
            if (i + 1) % 2 != 0:
                str = date[i] + '->' + date[i + 1]
                second.append(str)
    else:
        for i in range(len(titles)):
            second.append('no time')

    i = 0
    for i in range(len(first)):
        project.append(first[i])
        project.append(second[i])
    return project


def Publication(url_pub):
    a = []
    b = []
    #     c = []
    publication = []
    html = urlopen(url_pub).read()
    soup = BeautifulSoup(html, features='lxml')

    ol = soup.find('ol', {"class": "portal_list"})

    # a: title
    titles = ol.select('h2.title > a > span')
    for t in titles:
        t = t.get_text()
        a.append(t)
    #     print(len(a))

    # b: time
    time = ol.find_all('span', {"class": "date"})
    for t in time:
        b.append(t.get_text())
    #         where = t.nextSibling.nextSibling
    #         print(type(where))
    #         if type(whereis None:
    #             continue
    #         c.append(where.get_text())

    for i in range(len(a)):
        list = []
        list.append(a[i])
        list.append(b[i])
        publication.append(list)
    return publication

researcher =[]
base_url = "https://www.research.ed.ac.uk/portal/en/persons"
person_path = 'person.txt'
with open (person_path,'r') as f:
    person_list = f.read().splitlines()
project = "/projects"
publications = "/publications"
end = ".html"
for i in range(len(person_list)):
    list = []
    describes = []
    url_base = base_url +  person_list[i] + end
    html = urlopen(url_base).read()
    soup = BeautifulSoup(html, features='lxml')
    contains= soup.select('ul.tabs span')
    for c in range(len(contains)):
        h = contains[c].get_text()
        describes.append(''.join(h.split()))
    for d in describes:
        if 'Overview' == d:
            list.append(Profile(url_base))
        elif 'Researchoutputs' == d:
            url_pub = base_url + person_list[i] + publications + end
            list.append(Publication(url_pub))
        elif 'Projects'== d:
            url_project = base_url + person_list[i] + project + end
            list.append(Project(url_project))
    researcher.append(list)
    if i % 2 == 0:
        print(i, end =" ")

import pickle
output = open('researchers.pkl', 'wb')
pickle.dump(researcher, output)
output.close()