#! /bin/python
import os, sys, time
import random
import shutil

def CheckPathOrFail(path, isFile=True):
    if os.path.exists(path):
        if isFile:
            if os.path.isfile(path):
                return True
            else:
                print("path %s not a valid file, exit"%path)
                exit(1)
        if not isFile:
            if os.path.isdir(path):
                return True
            else:
                print("path %s not a valid folder, exit"%path)
                exit(1)    

def getTimestampStr():
    return str(int(time.time()))

def CreateImageTree(dataPath, dataFilePath):
    os.system("tree -i -f %s |grep \".jpg\|.png\|.bmp\" > %s"%(dataPath, dataFilePath))

def GetImageListFromFile(fileName):
    f=open(fileName,"rb")
    lines = [line.strip() for line in f.readlines()]
    return lines

def GetClassNameFromImageList(imageList, dataPath):
    classList=[]
    for image in imageList:
        className=image.replace(dataPath,"").split("/")[3]
        classList.append(className)
    return list(set(classList))

def SplitImageFileListIntoTrainAndVal(imageFileList, classNameList, ratio=0.8, countFilter=0, limits=None):
    trainSet=[]
    valSet=[]
    labelSet=[]
    labelId = 0
    index =0 
    for className in classNameList:
        searchKey="/"+className+"/"
        currentClassList =[]
        for image in imageFileList:
            if image.find(searchKey)>=0:
                currentClassList.append(image)
        if len(currentClassList)<countFilter:
            #skip small image set.
            pass
        else:
            labelSet.append((labelId,className))
            random.shuffle (currentClassList)
            if limits is None:
                size_train = int(len(currentClassList)*ratio)
                for item in currentClassList[:size_train]:
                    trainSet.append((index, labelId, item))
                    index +=1
                for item in currentClassList[size_train:]:
                    valSet.append((index, labelId, item))
                    index +=1
            else:
                size_train = int(limits*ratio)
                for item in currentClassList[:size_train]:
                    trainSet.append((index, labelId, item))
                    index +=1
                for item in currentClassList[size_train:limits]:
                    valSet.append((index, labelId, item))
                    index +=1
            labelId+=1
    return (trainSet, valSet, labelSet)

def WriteDownToFile(dataSet, fileName):
    ft=open(fileName,"w")
    if len(dataSet[0])==2:
        for line in dataSet:
            wline=str(line[0])+" \t "+str(line[1]) + "\n"
            ft.write(wline)
    else:
        for line in dataSet:
            wline=str(line[0])+" \t "+str(line[1])+" \t "+str(line[2])+ "\n"
            ft.write(wline)
    ft.flush()
    ft.close()

if __name__=="__main__":
    start = time.time()
    timestamp = getTimestampStr()
    MXNETHome = os.getenv("MXNET_HOME","/home/haria/mxnet")
    if MXNETHome is None:
        print("MXNET_HOME is not defined!")
        exit(1)

    if len(sys.argv) <4:
        print("Usage: python %s dataPath train_out.bin val_out.bin shape [ratio countFilter limits]")
        exit(1)
    dataPath=os.path.abspath(sys.argv[1])
    trainPath =os.path.abspath(sys.argv[2])
    valPath =os.path.abspath(sys.argv[3])
    CheckPathOrFail(dataPath, False)
    print("Data Path check PASS.")
    
    shape=28
    ratio = 0.8
    countFilter = 0
    limits = None
    if len(sys.argv) >4:
        shape = int(sys.argv[4])
    if len(sys.argv) >5:
        ratio = float(sys.argv[5])
    if len(sys.argv) >6:
        countFilter = int(sys.argv[6])  
    if len(sys.argv) >7:
        limits = int(sys.argv[7])  
    ##################################################################

    dataFilePath = "./data.txt"
    labelsFilePath =  "./labels.txt"
    trainFilePath = "./train.txt"
    valFilePath = "./val.txt"
    
    CreateImageTree(dataPath, dataFilePath)
    imageFileList = GetImageListFromFile(dataFilePath)
    # remove dataPath in beginning
    imageFileList = [image.replace(os.path.abspath(dataPath),"") for image in imageFileList]
    classNameList = GetClassNameFromImageList(imageFileList, dataPath)
    trainSet, valSet, labelSet = SplitImageFileListIntoTrainAndVal(imageFileList, classNameList, ratio, countFilter, limits)
    random.shuffle (trainSet)
    WriteDownToFile(trainSet, trainFilePath)
    WriteDownToFile(valSet,   valFilePath)
    WriteDownToFile(labelSet, labelsFilePath)
    
    
    ##################################################################
    im2rec = os.path.join(MXNETHome, "bin/im2rec")
    command = "%s %s %s %s resize=%s"%(im2rec, trainFilePath, dataPath, trainPath, shape)
    print command
    os.system(command)
        
    command = "%s %s %s %s resize=%s"%(im2rec, valFilePath, dataPath, valPath, shape)
    print command
    os.system(command)
   
    end = time.time()
    print ("Time Elapsed: %.3fs."%(end-start))



