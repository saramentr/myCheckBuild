#!/usr/bin/python3
import os
os.system('apt-get update&& apt-get install -y python3-pip python3-setuptools python3-pandas python3-yaml python3-requests&& apt-get install -y git curl psmisc p7zip-full wget')
import sys
import shutil
import time
import datetime
import threading
import signal
import csv

import json
import pandas as pd
import hashlib
import requests

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

fileSkeepName = "skeepData"
branchName = sys.argv[0].split('/')[-1].split('.py')[0]
fileDataName = branchName+".csv"

dateNow = datetime.datetime.today().strftime('%d%m%Y')
dictChecks = {'HASH':'', 'STARS':'', 'FORKS':'', 'DATE':dateNow}

if os.path.exists(folderName):
    shutil.rmtree(folderName)

os.system('mkdir '+folderName)
os.system('cd '+folderName+' && wget '+archiveUrl+' -O 1.7z > /dev/null 2>&1')
os.system('cd '+folderName+' && 7z x 1.7z -p'+archivePass)




def down_git_branch(lname,pname,rname,foldrep,branch):
    if os.path.exists(foldrep):
        shutil.rmtree(foldrep)
    os.system("git clone https://"+lname+":"+pname+"@github.com/"+lname+"/"+rname+".git "+foldrep)
    os.system("cd "+foldrep+"&& git fetch --all")
    os.system("cd "+foldrep+"&&git checkout "+branch+" || git checkout -b "+branch+" origin/clean")

def save_repo_branch_commit(lname,pname,rname,foldrep,branch,commit):
    os.system("cd "+foldrep+"&&git remote remove origin")
    os.system("cd "+foldrep+"&&git config --global user.name \""+lname+"\"")
    os.system("cd "+foldrep+"&&git config --global user.email "+lname+"@github.com")
    os.system("cd "+foldrep+"&&git remote add -f origin https://"+lname+":"+pname+"@github.com/"+lname+"/"+rname+".git")
    os.system("cd "+foldrep+"&&git checkout "+branch+" || git checkout -b "+branch+" origin/clean")
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

def checkStars(hashP,urlP):
    dT = dict(dictChecks)
    dT['HASH'] = hashP
    if urlP.startswith('https://github.com/'):
        time.sleep(10)
        if urlP.endswith('.git'):
            response = requests.get('https://api.github.com/repos/'+urlP.split('https://github.com/')[1].split('.git')[0])
        else:
            response = requests.get('https://api.github.com/repos/'+urlP.split('https://github.com/')[1])
        json_data = json.loads(response.text)
    else:
        json_data=''
    try:
        forksCount = json_data['forks_count']
    except:
        forksCount='NULL'
    try:
        starsCount = json_data['stargazers_count']
    except:
        starsCount = "NULL"
    dT['STARS'] = str(starsCount)
    dT['FORKS'] = str(forksCount)
    return dT

if os.path.exists(folderName+'commonTableAll.csv'):
    commonTable = pd.read_csv(folderName+'commonTableAll.csv')
else:
    os._exit(0)
down_git_branch(loginName,passName,repoName,folderGitClone,branchName)
threadCommit()
#chechSize()
fileSkeepData = open(folderGitClone+fileSkeepName,"a+")
fileSkeepData.seek(0, 0)
readSkeepData = fileSkeepData.readlines()

if not os.path.exists(folderGitClone+fileDataName):
    with open(folderGitClone+fileDataName, 'a+') as f:
        w = csv.DictWriter(f, dictChecks.keys())
        w.writeheader()

resultDataTmp = open(folderGitClone+fileDataName,"a+")
resultData = csv.DictWriter(resultDataTmp, dictChecks.keys())

for i in commonTable['HASH']:
    if len(commonTable.loc[commonTable['HASH'] == i]['URL']) > 1:
        for urlForWork in commonTable.loc[commonTable['HASH'] == i]['URL']:
            if urlForWork!=urlForWork:
                continue

            dictTmp = checkStars(i,urlForWork)
            resultData.writerow(dictTmp)
    elif len(commonTable.loc[commonTable['HASH'] == i]['URL']) < 1:
        continue
    elif not i in str(readSkeepData):
        fileSkeepData.write(i+'\n')
        fileSkeepData.flush()
        os.fsync(fileSkeepData.fileno())

        urlForWork = list(commonTable.loc[commonTable['HASH'] == i]['URL'])[0] 
        if urlForWork!=urlForWork:
            continue
        dictTmp = checkStars(i,urlForWork)
        resultData.writerow(dictTmp)

    resultDataTmp.flush()
    os.fsync(resultDataTmp.fileno())
fileSkeepData.close()
resultDataTmp.close()
save_repo_branch_commit(loginName,passName,repoName,folderGitClone,branchName,"fin commit")

os._exit(0)