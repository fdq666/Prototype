import xml.etree.ElementTree as ET
import pickle
import xml.dom.minidom
from bs4 import BeautifulSoup
from urllib.request import urlopen

doc = xml.dom.minidom.Document()
root = doc.createElement('Researchers')
doc.appendChild(root)

pkl_file = open('researchers.pkl', 'rb')
researcher = pickle.load(pkl_file)
pkl_file.close()
# print(len(researcher))
base_url = "https://www.research.ed.ac.uk/portal/en/persons"
person_path = 'person.txt'
with open(person_path, 'r') as f:
    person_list = f.read().splitlines()
project = "/projects"
publications = "/publications"
end = ".html"

for i in range(len(researcher)):
    try:
        nodeResearcher = doc.createElement('Researcher')
        root.appendChild(nodeResearcher)

        nodeDocNo = doc.createElement('ResearcherNo')
        nodeDocNo.appendChild(doc.createTextNode(str(i + 1)))
        nodeResearcher.appendChild(nodeDocNo)

        describes = []
        url_base = base_url + person_list[i] + end
        html = urlopen(url_base).read()
        soup = BeautifulSoup(html, features='lxml')
        contains = soup.select('ul.tabs span')
        for c in range(len(contains)):
            h = contains[c].get_text()
            describes.append(''.join(h.split()))
        if len(describes) > 3:
            describes = describes[0:3]

        for d in range(len(describes)):
            if 'Overview' == describes[d]:
                profile = researcher[i][d]
                nodeName = doc.createElement('Name')
                nodeName.appendChild(doc.createTextNode(str(profile[0])))
                nodeCollege = doc.createElement("College")
                nodeCollege.appendChild(doc.createTextNode(str(profile[1])))
                nodeDescrible = doc.createElement("Describle")
                nodeDescrible.appendChild(doc.createTextNode(str(profile[2])))
                nodeResearcher.appendChild(nodeName)
                nodeResearcher.appendChild(nodeCollege)
                nodeResearcher.appendChild(nodeDescrible)

            elif 'Researchoutputs' == describes[d]:
                publication = researcher[i][d]
                nodePublication = doc.createElement('Publication')
                for i in range(len(publication)):
                    #     print(project[i])
                    nodeTitle = doc.createElement('title')
                    nodeTitle.appendChild(doc.createTextNode(str(publication[i][0])))
                    nodePublication.appendChild(nodeTitle)
                    nodeTime = doc.createElement("time")
                    nodeTime.appendChild(doc.createTextNode(str(publication[i][1])))
                    nodePublication.appendChild(nodeTime)
                nodeResearcher.appendChild(nodePublication)

            elif 'Projects' == describes[d]:
                project = researcher[i][d]
                nodeProject = doc.createElement('Project')
                for l in range(len(project)):
                    if (l + 1) % 2 != 0:
                        #         print(project[i])
                        nodeTerm = doc.createElement('term')
                        nodeTerm.appendChild(doc.createTextNode(str(project[l])))
                        nodeProject.appendChild(nodeTerm)
                    else:
                        #         print(project[i])
                        nodePeriod = doc.createElement("period")
                        nodePeriod.appendChild(doc.createTextNode(str(project[l])))
                        nodeProject.appendChild(nodePeriod)
                nodeResearcher.appendChild(nodeProject)
    except Exception as e:
        print(i, end=" ")
        print(e)
        continue

fp = open('Researchers_1.xml', 'w')
doc.writexml(fp, indent='\t', addindent='\t', newl='\n')