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

os.system("apt-get install -y autoconf libtool autoconf-archive build-essential automake pkg-config doxygen bison byacc gettext meson")

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
dictCheckMake = {'HASH':'', 'METHOD':'' ,'ADDONS':'' ,'STATS':'' ,'DATE':dateNow}
listMakeCommand = ['./configure','./autogen.sh && ./configure','build/autogen.sh &&./configure','./bootstrap.sh&&./configure','autoreconf -i && ./configure','cmake ./','./bootstrap&&./configure']

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
def checkInstall(command,strAddonP,gitFolderP,tmpLogsP,tmpLogsHistP):
    if os.path.exists(tmpLogsP):
        os.system('mv '+tmpLogsP+' '+tmpLogsHistP)
    outBuildCode = 0
    if '&&' in command:
        for k in command.split('&&'):
            outBuildCode = os.system('cd '+gitFolderP+' && '+k+' 2> '+tmpLogsP)
            if outBuildCode != 0:
                break
    else:
        outBuildCode = os.system('cd '+gitFolderP+' && '+command+' 2> '+tmpLogsP)
    flagRepeat = False
    listRepeat = []
    if os.path.exists(tmpLogsHistP):
        with open(tmpLogsHistP,'r') as file:
            listRepeat = file.readlines()
    if  outBuildCode != 0:
        with open(tmpLogsP,'r') as file:
            lines = file.readlines()
            for l in lines:
                if l in listRepeat:
                    continue
                if l.startswith('No package') and l.rstrip().endswith('found'):
                    strAddonP +=' '+ l.split('\'')[1]
                    os.system('sudo apt-get install -y '+l.split('\'')[1])
                    os.system('sudo apt-get install -y '+l.split('\'')[1]+'-dev')
                    os.system('sudo apt-get install -y lib'+l.split('\'')[1]+'-dev')
                    flagRepeat = True
                elif l.rstrip().endswith('header not installed'):
                    strAddonP += ' '+ l.split('header not installed')[0].split()[-1]
                    os.system('sudo apt-get install -y '+l.split('header not installed')[0].split()[-1]+'-dev')
                    flagRepeat = True
                elif 'Try to install ' in l:
                    strAddonP += ' '+ l.split('Try to install ')[1].split()[0]
                    os.system('sudo apt-get install -y '+l.split('Try to install ')[1].split()[0])
                    flagRepeat = True
                elif l.startswith('configure: error:') and 'Consider ' in l and 'configure' in command:
                    strAddonP['makeLine'][-1] = command
                    command = command.split('configure')[0]+'configure '+command.split('Consider')[1]+command.split('configure')[1]
                    flagRepeat = True
                elif l.startswith('configure: error:') and ' package not found' in l:
                    strAddonP += ' '+ l.split('configure: error: ')[1].split(' package not found')[0]
                    os.system('sudo apt-get install -y '+l.split('configure: error: ')[1].split(' package not found')[0])
                    os.system('sudo apt-get install -y '+l.split('configure: error: ')[1].split(' package not found')[0]+'-dev')
                    os.system('sudo apt-get install -y lib'+l.split('configure: error: ')[1].split(' package not found')[0]+'-dev')
                    flagRepeat = True
                elif 'Could not find prerequisite package \'' in l:
                    strAddonP += ' '+ l.split('\'')[1].lower()  
                    os.system('sudo apt-get install -y '+l.split('\'')[1].lower())
                    os.system('sudo apt-get install -y '+l.split('\'')[1].lower()+'-dev')
                    os.system('sudo apt-get install -y lib'+l.split('\'')[1].lower()+'-dev')
                    flagRepeat = True

    if flagRepeat:
        outBuildCode,strAddonP = checkInstall(command,strAddonP)
    return outBuildCode,strAddonP

def checkBuildMake(hashP,urlP):
    dT = dict(dictCheckMake)
    dT['HASH'] = hashP
    gitFolder= '/tmp/workGit/'
    tmpLogs = '/tmp/AllLogs'
    tmpLogsHist = '/tmp/AllLogsHist'
    if os.path.exists(gitFolder):
        shutil.rmtree(gitFolder)
    os.system("git clone --recursive "+urlP.splitlines()[0]+' '+gitFolder)
    if not os.path.exists(gitFolder):
        dT['STATS'] = 'NULL'
        dT['METHOD'] = 'NULL'
        dT['ADDONS'] = 'NULL'
        return dT
    outCode = 7788
    strAddons = ''
    for j in listMakeCommand:
        if '&&' in j and (j.startswith('./') or (not './' in j.split('&&')[0] and  '/' in j.split('&&')[0])):
            if (j.startswith('./') and not os.path.exists(gitFolder+'/'+j.split('&&')[0].split('./')[1].rstrip())) or (not j.startswith('./') and not os.path.exists(gitFolder+'/'+j.split('&&')[0].rstrip())):
                continue
        elif j.startswith('./') or (not './' in j and  '/' in j):
            if (j.startswith('./') and not os.path.exists(gitFolder+'/'+j.split('./')[1].rstrip())) or (not j.startswith('./') and not os.path.exists(gitFolder+'/'+j.rstrip())):
                continue
        elif j.startswith('autoreconf'):
            if not os.path.exists(gitFolder+'/configure.ac') and not os.path.exists(gitFolder+'/configure.in'):
                continue
        elif j.startswith('cmake'):
            if not os.path.exists(gitFolder+'/CMakeLists.txt'):
                continue
        elif j.startswith('make'):
            if not os.path.exists(gitFolder+'/Makefile'):
                continue
        outCode,strAddons = checkInstall(j,strAddons,gitFolder,tmpLogs,tmpLogsHist)
        if outCode == 0:
            dT['STATS'] = 'OK'
            dT['METHOD'] = j
            dT['ADDONS'] = strAddons
        else:
            dT['STATS'] = 'ERR'
            dT['METHOD'] = j
            dT['ADDONS'] = strAddons
    if dT['STATS'] == '':
        dT['STATS'] == 'NULL'
        dT['METHOD'] = 'SKEEP'
        dT['ADDONS'] = 'NULL'
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
        w = csv.DictWriter(f, dictCheckMake.keys())
        w.writeheader()

resultDataTmp = open(folderGitClone+fileDataName,"a+")
resultData = csv.DictWriter(resultDataTmp, dictCheckMake.keys())

for i in commonTable['HASH']:
# add update by date old
    if len(commonTable.loc[commonTable['HASH'] == i]['URL']) > 1:
        for urlForWork in commonTable.loc[commonTable['HASH'] == i]['URL']:
            dictTmp = checkBuildMake(i,urlForWork)
            resultData.writerow(dictTmp)
    elif len(commonTable.loc[commonTable['HASH'] == i]['URL']) < 1:
        continue
    elif not i in str(readSkeepData):
        urlForWork = list(commonTable.loc[commonTable['HASH'] == i]['URL'])[0] 
        dictTmp = checkBuildMake(i,urlForWork)
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
