#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Faire un mode remove ?
# verifier si 2 marqueurs sont present
import sys
import os
import yaml
import urllib.request
import colorama
import shutil
def printb(string):
    print(colorama.Back.WHITE+colorama.Fore.BLUE+colorama.Style.BRIGHT+string+colorama.Style.RESET_ALL)
def printg(string):
    print(colorama.Back.WHITE+colorama.Fore.GREEN+colorama.Style.BRIGHT+string+colorama.Style.RESET_ALL)
def readManifest(urlOrFile):
    printg("use "+urlOrFile)
    if "https://" in urlOrFile or "http://" in  urlOrFile:            
        #with urllib.request.urlopen(urlOrFile) as response:
        #    html = response.read()
        urllib.request.urlretrieve(urlOrFile, ".repo-deploy.yml")
        return yaml.load(open(".repo-deploy.yml", 'r'),Loader=yaml.SafeLoader)
        #return yaml.load(html,Loader=yaml.SafeLoader)
    else:
        if not urlOrFile == ".repo-deploy.yml":
            shutil.copy(urlOrFile,".repo-deploy.yml")
        return yaml.load(open(urlOrFile, 'r'),Loader=yaml.SafeLoader)
        # faire plutot une copie du file ici
#def addInFiles:
def exeAndPrint(string):
    printb(">>>CMD "+string)
    os.system(string)
def dig(_key,command):
    if type(command) == dict:
        for key in command: 
            for subCommand in command[key]:
                dig(_key+key,subCommand)
    else: exeAndPrint(_key+command)
def createDir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    #os.system("mkdir -p "+os.path.dirname(i["file"]))
def setFile(path,block):
    createDir(path)
    with open(path, 'w+') as filetowrite:
        filetowrite.write(block)
    #removeFileIfpresent

def executeSetFile(i_file,i_block):
    printb(">>>SET file "+i_file)
    setFile(os.path.expanduser(i_file),i_block)


def getUrl(url,path):
    createDir(path)
    urllib.request.urlretrieve(url, path)

def executeGetUrl(url,path):
    printb(">>>DOWNLOAD file "+url+"to "+path)
    getUrl(url,os.path.expanduser(path))


def markerIsPresent(path,marker,number):
    count=0
    with open(path,'a+') as file:
        pass
    with open(path,'r') as file:
        for line in file:
            if line.strip("\n") == marker : count=count+1
        if number == count:
            return True
        else: return False
def changeBlock(path,block,marker1,marker2):
    print("changeBlock")
    delete=False
    with open(path, "r") as f:
        lines = f.readlines()
    with open(path,"w+") as f:
        for line in lines:
            if line.strip("\n") == marker1 and delete == False:
                f.write(line)
                delete = True
                f.write(block)
            if delete == False:
                f.write(line) 
            if line.strip("\n") == marker2 and delete == True:
                f.write(line)
                delete = False
def addBlock(path,block,marker1,marker2):
    print("appendNewBlock")
    with open(path,"a+") as f:
        f.write(marker1+"\n")
        f.write(block)
        f.write(marker2+"\n")

def setBlock(path,block,markers):
    createDir(path)
    if len(markers) == 2 and markers[0] != markers[1]:
        if markerIsPresent(path,markers[0],1) and markerIsPresent(path,markers[1],1):
            changeBlock(path,block,markers[0],markers[1])
        elif markerIsPresent(path,markers[0],0) == True and markerIsPresent(path,markers[1],0) == True:
            addBlock(path,block,markers[0],markers[1])
    if len(markers) == 1 or markers[0] == markers[1]:
        if markerIsPresent(path,markers[0],2):
            changeBlock(path,markers[0],markers[0])
        elif markerIsPresent(path,markers[0],0) == True:
            addBlock(path,block,markers[0],markers[0])

def executeSetBlock(i_file,i_block,i_markers):
    printb(">>>ADD content to "+i_file)
    setBlock(os.path.expanduser(i_file),i_block,i_markers)


def getManifest():
    if len(sys.argv) > 2 and sys.argv[1]=="init" :
        result=readManifest(sys.argv[2])
    else:
        result=readManifest(".repo-deploy.yml")
    return result


def use_sudo(i,sudo_executed):
    if "use_sudo" in i and sudo_executed==False and i["use_sudo"]==True:
        os.system("sudo "+sys.argv[0]+" use_sudo")
        sudo_executed=True
        return True
    else:
        return False



sudo_executed=False
if len(sys.argv) > 1:
    result=getManifest()    
    # IF rd init
    if sys.argv[1] == "init":
        ##--[REPOS]    
        for category in result:
            if "repos" in category:
                for i in category["repos"]:
                    printb(">>>INIT REPO "+i["url"]+" to "+i["dir"])
                    if "onlyBranch" in i:
                        os.system("git clone -b "+i["onlyBranch"]+" "+i["url"]+" "+i["dir"])
                    else:
                        os.system("git clone "+i["url"]+" "+i["dir"])
                    if "branch" in i:
                        os.system("cd "+i["dir"]+"; git checkout "+i["branch"]+"; cd -") 
            #desactiver le yaml dump
            ##--[FILES]
            if "files" in category:
                for i in category["files"]:
                    sudo_executed=use_sudo(i,sudo_executed)
                    if "use_sudo" not in i or ( "use_sudo" in i and i["use_sudo"] == False):
                        ## URL type
                        if "url" in i : executeGetUrl(i["url"],i["dest_file"])
                        ## file type
                        if "file" in i :
                            ## with markers
                            if "markers" in i: executeSetBlock(i["file"],i["block"],i["markers"])
                            ## wtihout markers
                            else: executeSetFile(i["file"],i["block"])
            ##-[CMD]
            if "cmd" in category:
                for command in category["cmd"]:
                    dig("",command)

    elif sys.argv[1] == "use_sudo":
        print("execute with sudo")
        for category in result:
            if "files" in category:
                for i in category["files"]:
                    if  "use_sudo" in i and i["use_sudo"] == True:
                    ## file type
                        if "url" in i : executeGetUrl(i["url"],i["dest_file"])
                        if "file" in i:
                            ## with markers
                            if "markers" in i :
                                    executeSetBlock(i["file"],i["block"],i["markers"])
                            ## wtihout markers
                            else:
                                executeSetFile(i["file"],i["block"])
        print("end sudo")

    # IF rd git status
    else:
        for category in result:
            if "repos" in category:
                for i in category["repos"]:
                    printb(i["dir"])
                    os.system("cd "+i["dir"]+"; "+' '.join(sys.argv[1:])+" ;cd -")
else:
    print("error need arg")
    sys.exit(1)
