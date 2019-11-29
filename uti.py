import os
import os.path
import json

path = 'H:\\xinglugu\\unpack'
list = []
schemaPath = path + '\\' + 'schema.json'


def getUpackFile(path, list):
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


def checkFileList(list):
    for file in list:
        fileFullName = file.split('\\')[-1]
        fileName = fileFullName.split('.')[0]
        fileLocal = fileFullName.split('.')[1]
        if fileName.lower() != 'schema' and fileLocal == 'zh-CN':
            fileRaw = open(file, mode='r', encoding='utf8')
            data = json.load(fileRaw)['content']
            if data is not None:

                if not os.path.exists(path + '\\' + fileName):
                    os.mkdir(path + '\\' + fileName)

                resDic = {}
                it = iter(data)
                for k in it:
                    resList = data[k].split('/')  # split string to list
                    resDic["index"] = k
                    resDic["main_category"] = fileName
                    newPath = path + '\\' + fileName + '\\' + fileName + '_' + k + '.json'
                    newFile = open(newPath, mode='w', encoding='utf8')
                    for item in resList:
                        schemaFile = open(schemaPath, mode='r', encoding='utf8')
                        schema = json.load(schemaFile)[fileName.lower()][str(len(resList))]
                        if schema is not None:
                            dicKey = schema[resList.index(item)]
                            resDic[dicKey] = item
                        schemaFile.close

                    newFile.write(json.dumps(resDic, ensure_ascii=False))
                    print(k)

            fileRaw.close

        print(type(data))
        print(fileName, fileLocal)


def main():
    getUpackFile(path, list)
    checkFileList(list)
    print(list)
    print(len(list))


main()
