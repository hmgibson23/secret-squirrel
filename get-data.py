from html.parser import HTMLParser
from time import sleep
import requests, json


API_KEY=""
CAPI="http://content.guardianapis.com/search"
DUMP_FILE="capi-dump"
TOTAL_PAGES=None

class Stripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = Stripper()
    s.feed(html)
    return s.get_data()


def fetchContent(page):
    params = {'api-key': API_KEY, 'page-size': '50',
              'page': page, 'show-fields': 'body',
              'type': 'article'}
    response = requests.get(CAPI, params=params)
    json_data = json.loads(response.text)['response']

    print(json_data['pages'])

    stripped = ""
    for content in json_data['results']:
        if 'fields' in content:
            stripped += strip_tags(content['fields']['body'])


    return stripped

def getTotalPages():
    params = {'api-key': API_KEY, 'page-size': '50',
              'type': 'article'}
    response = requests.get(CAPI, params=params)
    json_data = json.loads(response.text)['response']
    return json_data['pages']


def writeToFile(contents):
    with open(DUMP_FILE, "a", encoding='utf-8') as myfile:
        myfile.write(contents)


if __name__ == "__main__":
    totalPages = getTotalPages()
    currentPage = 904
    print("Fetching total: " + str(totalPages))
    while currentPage <= totalPages:
        data = fetchContent(currentPage)
        print ("Writing page " + str(currentPage) + " to " + DUMP_FILE)
        currentPage += 1
        writeToFile(data)
        if currentPage % 10 == 0:
            sleep(1)

    print ("Done...")
