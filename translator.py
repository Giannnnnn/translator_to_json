import os
import googletrans
import json
import sys
from termcolor import colored, cprint
from os import walk
from googletrans import Translator
os.system('color')
translator = Translator()

pt_br = []
en_us = []
es_es = []
fr_fr = []
fr_ca = []

trialsToFixErrors = 5


def formatLine(unformattedLine, index, isAValidLine, isAColumnDescriptionName):
    unspaced_line = unformattedLine.strip()
    translationSuggestion = " "
    stringItems = unformattedLine.partition(":")
    keys = stringItems[0]
    translation = stringItems[2]
    jsonLine = [keys, translation, unspaced_line, index,
                stringItems, isAValidLine, isAColumnDescriptionName, translationSuggestion]
    return jsonLine


def markDirtiedLines(lines):
    for item in lines:
        if item[0].strip() == '{' or item[0].strip() == ',{' or item[0].strip() == '},' or item[0].strip() == '}':
            item[5] = False
        elif item[1].strip() == '{':
            item[6] = True
    return lines


def compareLists(listA, listB):
    filteredListA = []
    filteredListB = []
    errorList = []
    errorListLength = 0
    count = len(listA)
    rowCount = 0
    indexA = 0
    indexB = 0

    while count >= rowCount and (indexA <= len(listB)):

        if(listA[indexA][0] != listB[indexB][0]):
            step = 0
            trials = 5
            cprint((listA[indexA][0] + " != " +
                   listB[indexB][0]), 'white', 'on_red')

            log = [[listA[indexA][0]], ["!="], [listB[indexB][0]], [rowCount]]

            errorList.extend(log)
            while(trials >= 0):
                step = step + 1
                trials = trials - 1

                if(listA[indexA + step][0] == listB[indexB][0]):
                    print(listA[indexA + step][0] + "  " + listB[indexB][0])
                    trials = 0
                    step = 0
                    break
                elif(listA[indexA][0] == listB[indexB + step][0]):
                    print(listA[indexA][0] + "  " + listB[indexB+step][0])
                    trials = 0
                    step = 0
                    break
                else:
                    break
            errorListLength = errorListLength + 1
            indexA = indexA+1

        elif(listA[indexA][0] == listB[indexB][0]):
            if(listA[indexA][5] == False):
                print(listA[indexA][0] + "  " + listA[indexA][1])
            elif(listA[indexA][6] == True):
                print(listA[indexA][0] + " : " + listA[indexA][1])
            else:
                print(listA[indexA][0] + " : " + listA[indexA][1])

            filteredLineA = [listA[indexA][0], listA[indexA][1]]
            filteredLineB = [listB[indexB][0], listB[indexB][1]]

            filteredListA.extend(filteredLineA)
            filteredListB.extend(filteredLineB)

            indexA = indexA + 1
            indexB = indexB + 1
            rowCount = rowCount + 1

    if(errorListLength > 0):
        cprint((" #{0}".format(errorListLength) + " errors found!"),
               'white', 'on_red', attrs=['bold'])


# def returnTranslatedLines(lines, languageFrom, languageTo):
#     for toTranslate in lines:
#         translatted = translator.translate(toTranslate[1])
#         print(translatted)
#         toTranslate[7] = translatted.text
#     return lines

def returnFilteredLines(lines):
    translatableItems = []
    for item in lines:
        if item[5] == True and item[6] == False:
            translatableItems.append(item)
    return translatableItems


def printLines(itemList):
    for item in itemList:
        print("")
        cprint(("                                     LINE: #{0}".format(
            item[3])), 'white', attrs=['bold'])
        print("")
        cprint(("                                        KEY:        " +
                item[0].strip()), 'blue')
        print("----------------------------------------------------------------------------------------------------------------------------------------------------------")
        cprint(
            ("                                           VALUE:     "+item[1]), 'yellow')
        print("")
        cprint(("############################################################################################################################################################"), 'white', 'on_white')


def printToTranslateColumn(itemList):
    for item in itemList:
        cprint(("" + item[0].strip() + " : " + item[1]), 'yellow')


def initialize():
    dir = input("Enter the translation path: \n")
    onlyfiles = next(os.walk(dir))[2]
    counter = len(onlyfiles)

    while counter > 0:
        f = []
        for (dirpath, dirnames, filenames) in walk(dir):
            f.extend(filenames)
            counter -= 1

    for file in filenames:
        if(file.endswith(".json")):
            match file:
                case "pt-br.json":
                    with open(file) as f:
                        portugueseCounter = 0
                        for json_obj in f:
                            try:
                                a_dict = json.loads(json_obj)
                            except:
                                portugueseCounter = portugueseCounter+1
                                counter = counter+1
                                pt_br.append(formatLine(
                                    json_obj, portugueseCounter, True, False))
                case "fr-ca.json":
                    with open(file) as f:
                        canadianCounter = 0
                        for json_obj in f:
                            try:
                                a_dict = json.loads(json_obj)
                            except:
                                canadianCounter = canadianCounter+1
                                counter = counter+1
                                fr_ca.append(formatLine(
                                    json_obj, canadianCounter, True, False))
                case  "fr-fr.json":
                    with open(file) as f:
                        frenchCounter = 0
                        for json_obj in f:
                            try:
                                a_dict = json.loads(json_obj)
                            except:
                                frenchCounter = frenchCounter+1
                                counter = counter+1
                                fr_fr.append(formatLine(
                                    json_obj, frenchCounter, True, False))
                case "en-us.json":
                    with open(file) as f:
                        northAmericanCounter = 0
                        for json_obj in f:
                            try:
                                a_dict = json.loads(json_obj)
                            except:
                                northAmericanCounter = northAmericanCounter+1
                                counter = counter+1
                                en_us.append(formatLine(
                                    json_obj, northAmericanCounter, True, False))
                case "es-es.json":
                    with open(file) as f:
                        spanishCounter = 0
                        for json_obj in f:
                            try:
                                a_dict = json.loads(json_obj)
                            except:
                                spanishCounter = spanishCounter+1
                                counter = counter+1
                                es_es.append(formatLine(
                                    json_obj, spanishCounter, True, False))


initialize()


pt_br = markDirtiedLines(pt_br)
en_us = markDirtiedLines(en_us)
es_es = markDirtiedLines(es_es)
fr_ca = markDirtiedLines(fr_ca)
fr_fr = markDirtiedLines(fr_fr)

compareLists(pt_br, en_us)

# remove extra lines that arent "key" : "value" type
# formattedListPTBR = returnFilteredLines(pt_br)
# formattedListENUS = returnFilteredLines(en_us)
# formattedListESES = returnFilteredLines(es_es)
# formattedListFRCA = returnFilteredLines(fr_ca)
# formattedListFRFR = returnFilteredLines(fr_fr)
