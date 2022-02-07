import os
os.system('c:\\hostedtoolcache\\windows\\python\\3.7.9\\x64\\python.exe -m pip install --upgrade pip')
os.system('pip install pandas requests')
import sys
import shutil
import time
import threading
import signal

import csv
import json
import pandas as pd
import hashlib
import requests
import datetime

def threadExit():
    os._exit(0)

timer1 = threading.Timer(18000.0, threadExit)
timer1.start()

folderName = "c:\\Temp\\works\\"
folderGitClone = "c:\\Temp\\gitClone\\"

fileSkeepName = "skeepData"
branchName = sys.argv[0].split('/')[-1].split('.py')[0]
fileDataName = branchName+".csv"

dateNow = datetime.datetime.today().strftime('%d%m%Y')
dictCheckBuildQL = {'HASH':'', 'STATS':'', 'DATE':dateNow}

if os.path.exists(folderName):
    os.system('rmdir /S /Q "{}"'.format(folderName))

os.system('dir c:\\&&echo 1230')
os.system('mkdir '+folderName)
os.system('echo 1231&&dir c:\\Temp\\')
os.system('echo 12311&&cd /d '+folderName+' &&dir&&C:\\msys64\\usr\\bin\\wget.exe https://google.com -O 2.7z&&c:\\Program Files\\7-Zip\\7z.exe')
os.system('dir && cd /d '+folderName+' &&dir && C:\\msys64\\usr\\bin\\wget.exe '+archiveUrl+' -O 1.7z')# > /dev/null 2>&1')
os.system('echo 1232')
os.system('cd /d '+folderName+' && C:\\msys64\\usr\\bin\\7z.exe x 1.7z ')#-p'+archivePass)
os.system('echo 1233')

dataVersion = requests.get('https://github.com/github/codeql-cli-binaries/releases/latest')
dataVerIns = dataVersion.text.split('<title>Release v')[1].split(' · github/codeql-cli-binaries')[0]

os.system( "mkdir codeqlmy&&cd codeqlmy&& git clone https://github.com/github/codeql.git codeql-repo")
os.system("cd /d codeqlmy&&C:\\msys64\\usr\\bin\\wget.exe https://github.com/github/codeql-cli-binaries/releases/download/v"+dataVerIns+"/codeql-win64.zip && unzip codeql-win64.zip && del codeql-win64.zip")

def down_git_branch(lname,pname,rname,foldrep,branch):
    if os.path.exists(foldrep):
         os.system('rmdir /S /Q "{}"'.format(foldrep))
    os.system("git clone https://"+lname+":"+pname+"@github.com/"+lname+"/"+rname+".git "+foldrep)
    os.system("cd /d "+foldrep+"&& git fetch --all")
    os.system("cd /d "+foldrep+"&&git checkout "+branch+" || git checkout -b "+branch+" origin/clean")

def save_repo_branch_commit(lname,pname,rname,foldrep,branch,commit):
    os.system("cd /d "+foldrep+"&&git remote remove origin")
    os.system("cd /d "+foldrep+"&&git config --global user.name \""+lname+"\"")
    os.system("cd /d "+foldrep+"&&git config --global user.email "+lname+"@github.com")
    os.system("cd /d "+foldrep+"&&git remote add -f origin https://"+lname+":"+pname+"@github.com/"+lname+"/"+rname+".git")
    os.system("cd /d "+foldrep+"&&git checkout "+branch+" || git checkout -b "+branch+" origin/clean")
    os.system("cd /d "+foldrep+"&&git add -A")
    os.system("cd /d "+foldrep+"&&git commit -m \""+commit+"\"")
    os.system("cd /d "+foldrep+"&&git push origin "+branch)
    
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

def checkBuildQLWin(hashP,urlP):
    dT = dict(dictCheckBuildQL)
    dT['HASH'] = hashP
    foldTP = 'c:\\Temp\\forCheckQL\\'
    foldPrjTP = 'c:\\Temp\\dbprj\\'
    foldLogTP = "c:\\Temp\\LOGsFolder\\"
    fileTP = 'c:\\Temp\\fileOut.tmp'
    fileExitCodeTP = 'c:\\Temp\\echoExitCode'
    if os.path.exists(foldTP):
        os.system('rmdir /S /Q "{}"'.format(foldTP))
    os.system("git clone "+urlP.splitlines()[0]+' '+foldTP)
    if not os.path.exists(foldTP):
        dT['STATS'] = 'NULL'
        return dT
    if os.path.exists(foldPrjTP):
        os.system('rmdir /S /Q "{}"'.format(foldPrjTP))
    #os.system("rm -rf "+foldTP+"/_lgtm*")
    os.system("sudo echo 321 > "+fileExitCodeTP)
    os.system("cd /d codeqlmy/codeql&&codeql.exe database create --language=cpp --source-root="+foldTP+"  -- "+foldPrjTP+"&&echo %ERRORLEVEL% > ../../echoExitCode")

    echoCode = open(fileExitCodeTP, 'r').read()
    if echoCode.startswith("0"):
        dT['STATS'] = 'OK'
    else:
        dT['STATS'] = 'ERR'
    return dT

commonTable = pd.read_csv(folderName+'commonTable.csv')

down_git_branch(loginName,passName,repoName,folderGitClone,branchName)
threadCommit()
chechSize()
fileSkeepData = open(folderGitClone+fileSkeepName,"a+")
fileSkeepData.seek(0, 0)
readSkeepData = fileSkeepData.readlines()

if not os.path.exists(folderGitClone+fileDataName):
    with open(folderGitClone+fileDataName, 'a+') as f:
        w = csv.DictWriter(f, dictCheckBuildQL.keys())
        w.writeheader()

resultDataTmp = open(folderGitClone+fileDataName,"a+")
resultData = csv.DictWriter(resultDataTmp, dictCheckBuildQL.keys())

for i in commonTable['HASH']:
# add update by date old
    if len(commonTable.loc[commonTable['HASH'] == i]['URL']) > 1:
        for urlForWork in commonTable.loc[commonTable['HASH'] == i]['URL']:
            dictTmp = checkBuildQLWin(i,urlForWork)
            resultData.writerow(dictTmp)
    elif len(commonTable.loc[commonTable['HASH'] == i]['URL']) < 1:
        continue
    elif not i in str(readSkeepData):
        urlForWork = list(commonTable.loc[commonTable['HASH'] == i]['URL'])[0] 
        dictTmp = checkBuildQLWin(i,urlForWork)
        resultData.writerow(dictTmp)
    
    fileSkeepData.write(i)
    fileSkeepData.flush()
    os.fsync(fileSkeepData.fileno())
    resultDataTmp.flush()
    os.fsync(resultDataTmp.fileno())
fileSkeepData.close()
resultDataTmp.close()
save_repo_branch_commit(loginName,passName,repoName,folderGitClone,branchName,"fin commit")
os._exit(0)
