#!/usr/bin/python3
""""
Misc CLI functions Library v0.1 
Version 0.1 Build 1 (8/18/23)
Author: Stephen Friederichs
License: Beerware License: If you find this program useful and you ever met me, buy me a beer. (I like Saisons)
Miscellaneous functionality best suited to a library file instead of the main file
"""

import textwrap
import logging
import getopt
import sys
import datetime
import os
import shutil
import re

def prettyPrint(uglyString):
    """This function properly formats docstrings for printing on the console"""

    #Remove all newlines
    uglyString = uglyString.replace('\n','').replace('\r','')
    #Use textwrap module to automatically wrap lines at 79 characters of text
    print(textwrap.fill(uglyString,width=79))

def formatPath(path):
    """This function returns a tuple of a well-formated absolute path and a boolean that tells whether that path exists"""
    newPath = os.path.abspath(os.path.normpath(str(path)))
    exists = os.path.exists(newPath)
    return exists,newPath

def ynUserPrompt(msg,default="y"):
    if 'y' in str(str(input(str(msg) + " ("+str(default)+") ")).lower() or str(default)):
        return True
    else:
        return False

def branch(branchPath):
    exists,branchPath = formatPath(branchPath)

    if exists and not os.path.isdir(branchPath):
        print("Can't branch to " +str(branchPath) + " - Path is not a directory")
        sys.exit(2)

    prjName = os.path.basename(branchPath)
    print("Branching template to " +str(branchPath))
    print("New project name is " + str(prjName))

    #1 - Make directory for new project
    if exists and os.path.isdir(branchPath):
        if ynUserPrompt("Target directory exists - overwrite?"):
            #delete directory and all of its contents
            shutil.rmtree(branchPath)
        else:
            print("Can't overwrite target directory - aborting.")
            sys.exit(2)
    elif exists and not os.path.isdir(branchPath):
        print("Target path exists already - but as a file. Aborting.")
        sys.exit(2);

    #Make the directory
    os.mkdir(branchPath)

    #2 - Add subdirectories
    print("Making subdirectories...")
    prjSubDirs = ["logs","src","cfg","res","lib","release","build"]
    for subDir in prjSubDirs:
        subDirPath = os.path.join(branchPath,subDir)
        os.mkdir(subDirPath)

    #3 - Copy over .gitignore and LICENSE.md as-is
    print("Copying files...")
    copyPaths = [".gitignore","LICENSE.md","build/install.nsi","src/pyCli.py","lib/cliLib.py","Pipfile","README.md","cfg/default.cfg",".env"]

    for filePath in copyPaths:
        try:
            newPath = os.path.join(branchPath,filePath)
            oldPath = os.path.join("./",filePath)
            shutil.copyfile(os.path.join("./",filePath),os.path.join(branchPath,filePath))
            print(str(oldPath) + "->"+ str(newPath))
        except IOError:	#File does not exist, usually
            continue
    print("Finished branch, exiting...")

    sys.exit(2)


def getCliOpts(docString):

    shortOpts = []
    longOpts = []
    funcNames = []

    for line in docString.splitlines():

        matches = re.match("(-[a-z]+), (--[a-z]+=?)",line)
        if matches:
            shortOpt,longOpt = matches.groups()
            funcName = longOpt.strip("=").strip("--")
            longOpt=longOpt.strip("--")
            shortOpt = shortOpt.strip("-")

            if "=" in longOpt:
                shortOpt = shortOpt + ":"

            shortOpts.append(shortOpt)
            longOpts.append(longOpt)
            funcNames.append(funcName)

    return shortOpts,longOpts,funcNames

def progId(docString):
    prettyPrint(docString.splitlines()[1])

if __name__=="__main__":
    pass
