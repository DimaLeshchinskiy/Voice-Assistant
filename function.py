import core
import sys
from bs4 import BeautifulSoup
import requests
import os

class Func:
    @staticmethod
    def reload(document):
        core.Comunication.talk(document[0])
        core.Core.load()
        core.Comunication.talk(document[1])

    @staticmethod
    def end(document):
        core.Comunication.talk(document[0])
        sys.exit()

    @staticmethod
    def setup(document, attr):

        core.Comunication.talk(document[0])
        res = core.Core.setup(attr)

        if res is 1:
            core.Comunication.talk(document[1])
        elif res is -1:
            core.Comunication.talk(document[2])

    @staticmethod
    def read(document, attr):
        if attr == "":
            attr = "memory"

        file = open(core.Core.fullpath_to_core + "data_core\\memory\\" + attr + ".dim", "r", encoding='utf-8')
        for item in core.DocumentSystem.getAbsoluteWord(file.readlines()):
            core.Comunication.talk(item)

    @staticmethod
    def save(document, attr):
        if attr == "":
            core.Comunication.talk(document[1])
            return

        fileTo = open(core.Core.fullpath_to_core + "data_core\\memory\\" + attr + ".dim", "w", encoding='utf-8')
        fileFrom = open(core.Core.fullpath_to_core + "data_core\\memory\\memory.dim", "r", encoding='utf-8')

        for item in core.DocumentSystem.getAbsoluteWord(fileFrom.readlines()):
            fileTo.write(item + "\n")

        core.Comunication.talk(document[0] + " " + attr)

    @staticmethod
    def findInfo(document, attr):
        if attr == "":
            core.Comunication.talk(document[1])
            return

        url = 'http://www.google.com/search?hl=ru&q=' + attr + '&btnI'
        r = requests.get(url)
        soup = BeautifulSoup(r.text.encode('utf8'), features="html.parser")
        file = open(core.Core.fullpath_to_core + "data_core\\memory\\memory.dim", "w", encoding='utf-8')

        for item in soup.find_all('a', href=True):
            print(item['href'] + " ==" + item.getText())
            if item['href'] == item.getText():
                r = requests.get(item['href'])
                soup = BeautifulSoup(r.text.encode('utf8'), features="html.parser")

                for item in soup.find_all('p'):
                    file.write(item.getText() + "\n")

                core.Comunication.talk(document[0])


    @staticmethod
    def openFolder(document, attr):
        if attr == "":
            core.Comunication.talk(document[0])
            return

        folder = core.DocumentSystem.getFolderByName(attr)
        print(folder)
        if folder == -1:
            core.Comunication.talk(document[1])
        else:
            os.startfile(folder.get("path"))
            core.Comunication.talk(document[2])
