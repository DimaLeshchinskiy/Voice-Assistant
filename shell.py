import core
import function as f

def listen():
    return core.Comunication.listen()

def load():
    core.Core.load()

def afterload():
    core.Comunication.talk("Вас приветствует голосовой ассистент. С чего начнем?")

def getCorePath():
    return core.Core.fullpath_to_core

def proccess(text):
    dictionary = core.Core.pars_command(text)
    #dictionary = core.Core.pars_command("Найди информацию о николе тесле")
    print(dictionary)

    event = dictionary["event"]
    attr = dictionary["attr"]

    if event == "":
        return

    document = core.DocumentSystem.getDocumentByName(event)

    if event == "выключение":
        f.Func.end(document)
    if event == "поиск":
        f.Func.findInfo(document, attr)
    if event == "открыть папку":
        f.Func.openFolder(document, attr)
    if event == "сохранить":
        f.Func.save(document, attr)
    if event == "перезагрузить":
        f.Func.reload(document)
    if event == "настроить":
        f.Func.setup(document,attr)
    if event == "читать":
        f.Func.read(document, attr)
