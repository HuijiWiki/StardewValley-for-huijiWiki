import os
import os.path
import json

unpackPath = 'H:\\xinglugu\\StardewValley-for-huijiWiki\\unpack\\JSON'  # unpacked file path
path = 'H:\\xinglugu\\StardewValley-for-huijiWiki\\unpack'  # unpacked file path
list = []
schemaPath = path + '\\' + 'schema_2.json'  # const schema path
categoryDic = {"uncategory": [], "-25": [], "-260": []}

# Object Information
objectFilePath = path + '\\' + 'ObjectInformation.json'
objFile = open(objectFilePath, mode='r', encoding='utf8')
obj = json.load(objFile)
objData = obj['content']

# NPC Gifttastes
tasteFilePath = path + '\\' + 'NPCGiftTastes.json'
tasteFile = open(tasteFilePath, mode='r', encoding='utf8')
taste = json.load(tasteFile)
tasteData = taste['content']

universalLove = set()
universalLike = set()
universalNeutral = set()
universalDislike = set()
universalHate = set()

universal = {
    "love": universalLove,
    "like": universalLike,
    "neutral": universalNeutral,
    "dislike": universalDislike,
    "hate": universalHate
}

for v in tasteData["Universal_Love"].split(' '):
    universalLove.update({v})
for v in tasteData["Universal_Like"].split(' '):
    universalLike.update({v})
for v in tasteData["Universal_Neutral"].split(' '):
    universalNeutral.update({v})
for v in tasteData["Universal_Dislike"].split(' '):
    universalDislike.update({v})
for v in tasteData["Universal_Hate"].split(' '):
    universalHate.update({v})

    # create categoryDictionary
    if objData is not None:
        it = iter(objData)
        # start iterator
        for k in it:
            # split string to list
            resList = objData[k].split('/')
            categoryString = resList[3].split(' ')
            if len(categoryString) > 1:
                categoryIndex = categoryString[1]

                # insert current index into category Dictionary
                if str(categoryIndex) in categoryDic:
                    categoryDic[str(categoryIndex)].append(k)
                else:
                    categoryDic[str(categoryIndex)] = [k]
            else:
                categoryDic["uncategory"].append(k)


def getUpackFile(path, list):  # get all unpacked files (JSON)
    fileList = os.listdir(path)
    try:
        for file in fileList:
            filePath = os.path.join(path, file)
            if True == os.path.isdir(filePath):
                getUpackFile(filePath, list)
            elif filePath[filePath.rfind('.') + 1:].upper() == 'JSON':
                list.append(filePath)
    except PermissionError:
        pass


def checkFileList(list):  # check unpacked files one by one
    schemaFile = open(schemaPath, mode='r', encoding='utf8')
    schema = json.load(schemaFile)

    logPath = unpackPath + '\\' + 'log.json'
    logFile = open(logPath, mode='w', encoding='utf8')

    objIndexPath = unpackPath + '\\' + 'objIndex.json'
    objFile = open(objIndexPath, mode='w', encoding='utf8')

    cookingTVIndexPath = unpackPath + '\\' + 'cookingTV.json'
    cookingFile = open(cookingTVIndexPath, mode='w', encoding='utf8')

    characterIndexPath = unpackPath + '\\' + 'characters.json'
    characterFile = open(characterIndexPath, mode='w', encoding='utf8')

    cookingTVIndexDic = {}
    characterDic = {}
    objIndexDic = {}
    log = {}
    tempList = ["0"]

    for file in list:
        # root name
        fileFullName = file.split('\\')[-1]
        # name
        fileName = fileFullName.split('.')[0]
        # localization name (zh-CN/...)
        fileLocal = fileFullName.split('.')[1]
        print(fileFullName, fileName, fileLocal)

        log[fileName] = {
            "unresolved_entities": [],
        }

        # discard other languages
        if (fileName.lower() in schema) and (fileLocal == 'zh-CN') or fileName.lower() == "locations":
            log[fileName]["processed"] = "true"

            # open file
            fileRaw = open(file, mode='r', encoding='utf8')

            # load JSON
            data = json.load(fileRaw)['content']

            if data is not None:
                # create folder
                if not os.path.exists(unpackPath + '\\' + fileName):
                    os.mkdir(unpackPath + '\\' + fileName)

                # initialize content (empty dictionary)
                resDic = {}

                it = iter(data)
                # start iterator
                for k in it:

                    if fileName.lower() == "objectinformation":
                        objIndexDic[k] = {}
                    if fileName.lower() == "cookingchannel":
                        cookingTVIndexDic[k] = {}
                    if fileName.lower() == "npcdispositions":
                        characterDic[k] = {}

                    # split string to list
                    resList = data[k].split('/')

                    # insert [key] as a new index
                    resDic["index"] = k

                    # insert [fileName] as main_category
                    resDic["main_category"] = fileName

                    # new JSON file's path
                    json_file_name = k.replace(":", "_")
                    json_file_name = json_file_name.replace("/", "_")
                    newPath = unpackPath + '\\' + fileName + '\\' + fileName + '_' + json_file_name + '.json'

                    # open new file
                    newFile = open(newPath, mode='w', encoding='utf8')

                    # start write
                    for item in resList:
                        # log
                        log[fileName][k] = len(resList)

                        if str(len(resList)) in schema[fileName.lower()]:
                            schemaData = schema[fileName.lower()][str(len(resList))]
                            # get new key
                            dicKey = schemaData[resList.index(item)]
                            # pair new value
                            resDic[dicKey] = item
                            # object information
                            if fileName.lower() == "objectinformation":
                                objIndexDic[k][dicKey] = item
                            if fileName.lower() == "cookingchannel":
                                cookingTVIndexDic[k][dicKey] = item
                            if fileName.lower() == "npcdispositions":
                                characterDic[k][dicKey] = item

                            # finish iterator
                        else:
                            maxNum = 1
                            for keys in schema[fileName.lower()]:
                                if maxNum < int(keys):
                                    maxNum = int(keys)  # capacity of current
                            if len(resList) < maxNum:
                                # get default key from biggest schema
                                schemaData = schema[fileName.lower()][str(maxNum)]
                                dicKey = schemaData[resList.index(item)]
                                # pair new value
                                resDic[dicKey] = item
                                # finish iterator
                            elif resList.index(item) < maxNum:
                                # get default key from biggest schema
                                schemaData = schema[fileName.lower()][str(maxNum)]
                                dicKey = schemaData[resList.index(item)]
                                # pair new value
                                resDic[dicKey] = item
                            else:
                                log[fileName]["unresolved_entities"].append(k)
                                # get default key
                                temp_index = resList.index(item) - maxNum
                                dicKey = "unresolved_" + str(temp_index)
                                # pair new value
                                resDic[dicKey] = item

                        # add Object data
                        if fileName.lower() == "objectinformation":  # object information
                            categoryString = resList[3].split(' ')
                            if len(categoryString) > 1:
                                categoryIndex = categoryString[1]
                                categoryName = schema["Enums"]["objectCategory"][str(categoryIndex)]
                                # add [subCategory]
                                resDic["sub_category"] = categoryName

                        # add CraftingRecipes data
                        if fileName.lower() == "craftingrecipes" :
                            craftItemString = resList[2].split(' ')
                            if len(craftItemString) > 0:
                                craftIndex = craftItemString[0]
                                if craftIndex in objData:
                                    craftCategoryString = objData[craftIndex].split('/')
                                    craftCategory = craftCategoryString[3].split(' ')
                                    craftCategory = craftCategory[0]
                                else:
                                    craftCategory = '999'
                                # add [craftCategory]
                                resDic["craft_category"] = craftCategory

                        # add cookingRecipe data
                        if fileName.lower() == "cookingrecipes":  # craft information
                            tempList.append(k)
                            resDic["sort_key"] = len(tempList)

                        # add cookingRecipe data
                        if fileName.lower() == "cookingchannel":  # craft information
                            resDic["sort_key"] = int(k)

                        # add GiftTaste data
                        if fileName.lower() == "npcgifttastes":  # NPC Gift Tastes
                            # is NPC data
                            if len(resList) > 1:
                                # create personal tastes dictionary
                                pLove = set()
                                pLike = set()
                                pNeutral = set()
                                pDislike = set()
                                pHate = set()
                                personal = {"love": pLove,
                                            "like": pLike,
                                            "neutral": pNeutral,
                                            "dislike": pDislike,
                                            "hate": pHate
                                            }
                                for v in resList[1].split(' '):
                                    pLove.update({v})
                                for v in resList[3].split(' '):
                                    pLike.update({v})
                                for v in resList[9].split(' '):
                                    pNeutral.update({v})
                                for v in resList[5].split(' '):
                                    pDislike.update({v})
                                for v in resList[7].split(' '):
                                    pHate.update({v})

                                resDic["love"] = _giftTaste("love", personal, universal)
                                resDic["like"] = _giftTaste("like", personal, universal)
                                resDic["neutral"] = _giftTaste("neutral", personal, universal)
                                resDic["dislike"] = _giftTaste("dislike", personal, universal)
                                resDic["hate"] = _giftTaste("hate", personal, universal)

                        # add Weapon data
                        if fileName.lower() == "weapons":  # NPC Gift Tastes
                            weaponTypeIndex = resList[8]
                            weaponTypeName = schema["Enums"]["weapon"][str(weaponTypeIndex)]
                            # add [subCategory]
                            resDic["sub_category"] = weaponTypeName

                        # add Monster data
                        if fileName.lower() == "monsters":  # Monster
                            resDic["monsterFamily"] = _monster(k)

                    newFile.write(json.dumps(resDic, ensure_ascii=False))
                    # finish
                    print(k)

            fileRaw.close()

    # write
    logFile.write(json.dumps(log, ensure_ascii=False))
    objFile.write(json.dumps(objIndexDic, ensure_ascii=False))
    cookingFile.write(json.dumps(cookingTVIndexDic, ensure_ascii=False))
    characterFile.write(json.dumps(characterDic, ensure_ascii=False))
    #close
    cookingFile.close()
    logFile.close()
    objFile.close()
    schemaFile.close()


def _monster(monster_id):
    monster_family = {
        "Lava Bat": "bat",
        "Iridium Bat": "bat",
        "Frost Bat": "bat",
        "Bat": "bat",
        "Green Slime": "slime",
        "Frost Jelly": "slime",
        "Sludge": "slime",
    }
    if monster_id in monster_family:
        return monster_family[monster_id]


def _giftTaste(tasteType, personal, universal):
    # start process personal tastes
    # expand all negative values in universal dictionary and remove duplicates
    universal = expandCategory(categoryDic, universal)
    # expand all negative values in personal dictionary and remove duplicates
    personal = expandCategory(categoryDic, personal)
    res = personal[tasteType].union(universal[tasteType])
    objFile.close()
    tasteFile.close()
    return str(res)


def expandCategory(categoryDic, dic):
    if dic is not None:
        enums = set()

        # start iterator
        for sets in iter(dic):
            for item in iter(dic[sets]):
                if len(item) > 0:
                    if int(item) > 0:
                        enums.update({item})

        # start iterator again
        for sets in iter(dic):
            pending = set()
            removing = set()
            for item in iter(dic[sets]):
                if len(item) > 0:
                    if int(item) < 0:
                        removing.update({item})
                        for v in categoryDic[str(item)]:
                            pending.update({v})
                        pending = pending.difference(enums)
                        pending = pending.difference(removing)
            dic[sets].union(pending)

    return dic


def main():
    getUpackFile(path, list)
    checkFileList(list)
    print(list)
    print(len(list))


main()
