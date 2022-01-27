#!/usr/bin/python3
import os
os.system('apt-get update&& apt-get install -y python3-pip python3-setuptools python3-pandas python3-yaml&& apt-get install -y git curl psmisc p7zip-full wget')
os.system('!apt-get install -y cmake pkg-config libicu-dev zlib1g-dev libcurl4-openssl-dev libssl-dev ruby-dev&&!apt-get install -y rubygems')
os.system('gem install github-linguist')
import sys
import shutil
import time
import json
import pandas as pd
import yaml
import threading
import signal
import hashlib

def threadExit():
    os._exit(0)

timer1 = threading.Timer(18000.0, threadExit)
timer1.start()

loginName = sys.argv[2].split('/')[0]
passName = sys.argv[1]
repoName = sys.argv[2].split('/')[1]

archivePass = sys.argv[3]
archiveUrl = sys.argv[4]

folderName = "/tmp/works/"
folderGitClone = "/tmp/gitClone/"
folderTmp = "/tmp/tmpW'
fileTmp = 'tmpW'
fileSkeepName = "skeepData"
fileDataName = "loguistDtatResult.csv'
branchName = sys.argv[0].split('/')[-1].split('.py')[0]
dictLanguageControlZero = {'objc':0, 'C':0,'CPP':0,'PY':0,'Other':0}
if os.path.exists(folderName):
    shutil.rmtree(folderName)
else:
    os.system('mkdir '+folderName)
os.system('cd '+folderName+' && wget '+archiveUrl+' -O 1.7z > /dev/null 2>&1')
os.system('cd '+folderName+' && 7z x 1.7z -p'+archivePass)


def down_git_branch(lname,pname,rname,foldrep,branch):
    if os.path.exists(foldrep):
        shutil.rmtree(foldrep)
    os.system("git clone https://"+lname+":"+pname+"@github.com/"+lname+"/"+rname+".git "+foldrep)
    os.system("cd "+foldrep+"&&git checkout "+branch+" || git checkout -b "+branch+" clean")

def save_repo_branch_commit(lname,pname,rname,foldrep,branch,commit):
    os.system("cd "+foldrep+"&&git remote remove origin")
    os.system("cd "+foldrep+"&&git config --global user.name \""+lname+"\"")
    os.system("cd "+foldrep+"&&git config --global user.email "+lname+"@github.com")
    os.system("cd "+foldrep+"&&git remote add -f origin https://"+lname+":"+pname+"@github.com/"+lname+"/"+rname+".git")
    os.system("cd "+foldrep+"&&git checkout "+branch+" || git checkout -b "+branch+" clean")
    os.system("cd "+foldrep+"&&git add -A")
    os.system("cd "+foldrep+"&&git commit -m \""+commit+"\"")
    os.system("cd "+foldrep+"&&git push origin "+branch)

def threadCommit():
    save_repo_branch_commit(loginName,passName,repoName,folderGitClone,branchName,"threadCommit add")
    timer = threading.Timer(1800.0, threadCommit)
    timer.start()

def chechSize():
    st = os.statvfs('/')
    ba = (st.f_bavail * st.f_frsize)
    if ba < 3*3221225472:
        save_repo_branch_commit(loginName,passName,repoName,folderGitClone,branchName,"chechSize small free space")
        os._exit(0)
    else:
        timer2 = threading.Timer(600.0, chechSize)
        timer2.start()

def linguistParse(urlP,foldTP,fileTP):
    if os.path.exists(foldTP):
        shutil.rmtree(foldTP)
     os.system("git clone "+i.splitlines()[0]+' '+foldTP)
    if not os.path.exists(foldTP):
        return dictLanguageControlZero
    if os.path.exists(foldTP+fileTP):
        os.remove(foldTP+fileTP)
    os.system('github-linguist '+foldTP+' -j >> '+foldTP+fileTP)
    if not os.path.exists(foldTP+fileTP):
        return dictLanguageControlZero

    dT = dictLanguageControlZero
    f = open(foldTP+fileTP)
    data = json.load(f)
    for i in data:
        dT[i] = 
        print(i)

    f.close()
commonTable = pd.read_csv(folderName+'commonTable.csv')

down_git_branch(loginName,passName,repoName,folderGitClone,branchName)

fileSkeepData = open(folderGitClone+fileSkeepName,"a+")
fileSkeepData.seek(0, 0)
readSkeepData = fileSkeepData.readlines()

resultData = pd.read_csv(folderGitClone+fileDataName)

for i in commonTable['HASH']:
    if len(commonTable.loc[commonTable['HASH'] == i]['URL']) > 1:
        for urlForWork in commonTable.loc[commonTable['HASH'] == i]['URL']:
            dictTmp = linguistParse(urlForWork,folderTmp,fileTmp)
     elif len(commonTable.loc[commonTable['HASH'] == i]['URL']) < 1:
        continue
    elif i.splitlines()[0] in str(readSkeepData) or not i.startswith('https:') or not i.splitlines()[0].endswith('.git'):
        urlForWork = commonTable.loc[commonTable['HASH'] == i]['URL'][0] 
        dictTmp = linguistParse(urlForWork,folderTmp,fileTmp)
        
    resultData = resultData.append(dictLanguageControl,ignore_index=True)
    
    fileSkeepData.write(i)
    fileSkeepData.flush()
    os.fsync(fileSkeepData.fileno())
os.system('github-linguist --help')
os._exit(0)
