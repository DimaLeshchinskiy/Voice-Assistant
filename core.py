import pyttsx3
import speech_recognition as sr
import pyaudio
import os
import sys
import webbrowser
import importlib.util
import time
import codecs

class Comunication:
    @staticmethod
    def talk(phrase):
        engine = pyttsx3.init()

        rate = engine.getProperty('rate')
        engine.setProperty('rate', Setup.setup_data["voice rate"])

        volume = engine.getProperty('volume')
        engine.setProperty('volume', Setup.setup_data["voice volume"])

        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[Setup.setup_data["voice id"]].id)

        engine.say(phrase)
        engine.runAndWait()
        engine.stop()

    @classmethod
    def listen(cls):
        r = sr.Recognizer()
        m = sr.Microphone()
        with m as source:
            r.energy_threshold = 3000
            r.dynamic_energy_threshold = True
            audio = r.listen(source)
        return Core.recognizeAudio(r, audio)


class Setup:
    setup_data = {
    "voice volume" : 1,
    "voice id": 0,
    "voice rate":250,
    "listen language":"ru-RU",
    "name":"dave",
    "connection": False
    }


    @staticmethod
    def setup(map):
        if map.get("key") in Setup.setup_data:
            Setup.setup_data[map.get("key")] = map.get("val")
            return 1
        else:
            return -1

class DocumentSystem:

    fileSystem = []

    @staticmethod
    def getFolderByName(name):

        for item in DocumentSystem.fileSystem:
            if item.get("name") == name:
                return item

        return -1

    @staticmethod
    def addFolder(obj):
        DocumentSystem.fileSystem.append(obj)

    @staticmethod
    def getDocumentByName(name):
        file_name = name + ".dim"
        file = open(Core.fullpath_to_core + "data_core\\bin\\" + file_name, "r", encoding='utf-8')
        return DocumentSystem.getAbsoluteWord(file.readlines())

    @staticmethod
    def getAbsoluteWord(list):
        new_list = []

        for word in list:
            new_list.append(word.rstrip())
        return new_list


class Core:
    fullpath_to_core = ""
    dictionary_core_data = {}
    dictionary_core_data_synonyms = {}

    @staticmethod
    def recognizeAudio(recognizer, audio):
        try:
            cmd = recognizer.recognize_google(audio, language=Setup.setup_data["listen language"])
            return cmd
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return ""

    @staticmethod
    def pars_command(str):
        str = str.lower()
        print(str)

        dictionary_query = {"event": "", "attr":""}

        for val in Core.dictionary_core_data.get("key_list"):
            if str.startswith(val.lower()):
                dictionary_query["event"] = val.lower()
                attr = str.replace(val.lower(), "")
                dictionary_query["attr"] = attr.rstrip().lower()
                return dictionary_query

        if dictionary_query["event"] == "":
            for key, val in Core.dictionary_core_data_synonyms.items():
                for item in val:
                    if str.startswith(item.lower()):
                        dictionary_query["event"] = key.lower()
                        attr = str.replace(item.lower(), "")
                        dictionary_query["attr"] = attr.strip().lower()
                        return dictionary_query

        return dictionary_query



    @staticmethod
    def load():
        Core.fullpath_to_core = os.path.abspath(os.path.dirname(sys.argv[0])) + "\\"

        for file_name in os.listdir(Core.fullpath_to_core + "data_core"):
            try:
                file = open(Core.fullpath_to_core + "data_core\\" + file_name, "r", encoding='utf-8')
                Core.dictionary_core_data[file_name.split(".")[0]] = DocumentSystem.getAbsoluteWord(file.readlines())
            except:
                continue

        for file_name in os.listdir(Core.fullpath_to_core + "data_core\\synonyms"):
            file = open(Core.fullpath_to_core + "data_core\\synonyms\\" + file_name, "r", encoding='utf-8')
            Core.dictionary_core_data_synonyms[file_name.split(".")[0]] = DocumentSystem.getAbsoluteWord(file.readlines())

        for path in Core.dictionary_core_data.get("folderRoot"):
            name = os.path.basename(path)
            if os.path.exists(path + '\\jarvisFolderName.dim'):
                file = open(path + '\\jarvisFolderName.dim', "r", encoding='utf-8')
                name = file.readlines()[0]
            DocumentSystem.addFolder({"name":name, "path":path})

    @staticmethod
    def setup(str):
        words = str.lower().split(" ")

        if len(words) < 2:
            return -1

        last_word = words[len(words) - 1]
        map = {"key" : str.replace(" " + last_word, ""), "val" : last_word}

        res = Setup.setup(map)
        return res
