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
import glob
def threadExit():
    os._exit(0)

timer1 = threading.Timer(18000.0, threadExit)
timer1.start()


loginName = sys.argv[2].split('/')[0]
passName = sys.argv[1]
repoName = sys.argv[2].split('/')[1]

archivePass = sys.argv[3]
archiveUrl = sys.argv[4]
branchName = sys.argv[0].split('/')[-1].split('.py')[0]

folderName = "/tmp/works/"
folderGitClone = "/tmp/gitClone/"

if os.path.exists(folderName):
    shutil.rmtree(folderName)

os.system('mkdir '+folderName)
os.system('cd '+folderName+' && wget '+archiveUrl+' -O 1.7z > /dev/null 2>&1')
os.system('cd '+folderName+' && 7z x 1.7z -p'+archivePass)

dataVersion = requests.get('https://github.com/github/codeql-cli-binaries/releases/latest')
dataVerIns = dataVersion.text.split('<title>Release v')[1].split(' · github/codeql-cli-binaries')[0]

os.system("cd /opt/&&sudo mkdir codeqlmy&&cd codeqlmy&&sudo git clone https://github.com/github/codeql.git codeql-repo") 
os.system("cd /opt/codeqlmy&&sudo wget https://github.com/github/codeql-cli-binaries/releases/download/v"+dataVerIns+"/codeql-linux64.zip&&sudo unzip codeql-linux64.zip&&sudo rm codeql-linux64.zip")



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


issueTable = pd.read_csv(folderName+'issueTable.csv')
down_git_branch(loginName,passName,repoName,folderGitClone,branchName)
threadCommit()

findFolder = folderGitClone
for f in glob.glob(findFolder+'*.7z'):
    if not issueTable.isin([f.split(findFolder)[1].split('.7z')[0]]).any().any():
        os.system('rm -rf '+f)
#chechSize()
#if file exists but not in csv - delete

foldTP = '/tmp/forCheckQL/'
foldPrjTP = '/tmp/dbprj/'
foldLogTP = "/tmp/LOGsFolder/"
fileTP = '/tmp/fileOut.tmp'
fileExitCodeTP = '/tmp/echoExitCode'

for i in issueTable['HASH']:
    if os.path.exists(folderGitClone+i+'.7z'):
        continue

    if os.path.exists(foldTP):
        shutil.rmtree(foldTP)

    os.system("git clone "+issueTable.loc[issueTable['HASH']==i]['GITLINK'].tolist()[0]+' '+foldTP)

    if not os.path.exists(foldTP):
        continue
    os.system("cd "+foldTP+"&&&&git checkout "+issueTable.loc[issueTable['HASH']==i]['COMMIT'].tolist()[0])

    if os.path.exists(foldPrjTP):
        shutil.rmtree(foldPrjTP)
    os.system("rm -rf "+foldTP+"_lgtm*")
    os.system("sudo echo 321 > "+fileExitCodeTP)
    
    os.system("timeout 60m /opt/codeqlmy/codeql/codeql database create --language=cpp --source-root="+foldTP+" --logdir="+foldLogTP+" -- "+foldPrjTP+" &&sudo echo $? > "+fileExitCodeTP)

    echoCode = open(fileExitCodeTP, 'r').read()
    if echoCode.startswith("0"):
        os.system('7z -mhc=on -mhe=on -p123123 a '+folderGitClone+i+'.7z '+foldPrjTP) 
        save_repo_branch_commit(loginName,passName,repoName,folderGitClone,branchName,"one db commit")

save_repo_branch_commit(loginName,passName,repoName,folderGitClone,branchName,"fin commit")

os._exit(0)