#!/usr/bin/python
""""
Generic Python CLI Script v0.1 
Version 0.1 Build 1 (1/3/21)
Author: Stephen Friederichs
License: Beerware License: If you find this program useful and you ever met me, buy me a beer. (I like Saisons)
This script demonstrates the use of the getopt library to parse command-line arguments passed to the Python script.
The following command-line parameters control the behavior of the script:
-h, --help - Shows this screen and exits
-v, --version - Display version information
-l, --license - Display author and license information
-f, --logfilepath=<PATH> - Set the log file path
-e, --loglevel=<LEVEL> - Set log level: DEBUG, INFO, WARNING, ERROR
-b, --branch=<BRANCHPATH> - Create a new project based on this script at the
                            passed BRANCHPATH. The project name is assumed to be the last element of BRANCHPATH
"""

import textwrap
import logging
import getopt
import sys
import datetime
import os
import shutil

def prettyPrint(uglyString):
    """This function properly formats docstrings for printing on the console"""
    
    #Remove all newlines
    uglyString = uglyString.replace('\n','').replace('\r','')
    #Use textwrap module to automatically wrap lines at 79 characters of text
    print(textwrap.fill(uglyString,width=79))
    
def formatPath(path):
    newPath = os.path.abspath(os.path.normpath(str(path)))
    exists = os.path.exists(newPath)
    return exists,newPath

def ynUserPrompt(msg,default="y"):
    if "y" in (str(input(str(msg) + " ("+str(default)+") ")).lower() or str(default)):
        return True
    else:
        return False
        
def license():
    for line in __doc__.splitlines()[2:4]:
        prettyPrint(line)
        
def help():
    for line in __doc__.splitlines()[4:]:
        prettyPrint(line)

def version():
    prettyPrint(__doc__.splitlines()[2])
 
def progId():
    prettyPrint(__doc__.splitlines()[1])
    
def init():
    progId()
    
    logFilePath = datetime.datetime.now().strftime('logs/log_%H_%M_%d_%m_%Y.log')

    logLevel = logging.DEBUG 
    formatStr = '%(asctime)s - %(threadName)s - %(funcName)s  - %(levelname)-8s %(message)s'
    try: 
        opts, args = getopt.getopt(sys.argv[1:], 'hvlf:e:b:', ['help','version','license','logfile=','loglevel=','branch='])    
    except getopt.GetoptError:
        print("Bad argument(s)")
        help()
        sys.exit(2) 
        
    for opt, arg in opts:                 
        if opt in ('-h', '--help'):     
            help()                         
            sys.exit(0)                 
        elif opt in ('-l','--license'):    
            license()
        elif opt in ('-f','--logfilepath'):
            logFilePath=str(arg)
        elif opt in ('-e','--loglevel='):
            try:
                if str(arg).upper() == "DEBUG":
                    logLevel=logging.DEBUG
                elif str(arg).upper() == "INFO":
                    logLevel= logging.INFO
                elif str(arg).upper() == "WARNING":
                    logLevel= logging.WARNING
                elif str(arg).upper() == "ERROR":
                    logLevel = logging.ERROR
                else:
                    raise ValueError
            except ValueError:
                print("Bad logging level")
                help()
                sys.exit(2)
        elif opt in ('-v','--version'):
            version()
            sys.exit(0)
        elif opt in ('-b','--branch='):
            branch(arg)            
        else:
            print("Bad command line argument: "+str(opt)+" - " +str(arg))
            help()
            sys.exit(2)

    logging.basicConfig(filename=logFilePath,filemode='a',level=logLevel,format=formatStr)
    #Then, retrieve a StreamHandler - this outputs log data to the console
    console = logging.StreamHandler()

    #Now configure the stream handler to the same settings as the file handler
    #Note, however that you don't need them both to be configured the same - it may be
    #entirely appropriate to have different settings for console vs. file.

    formatter = logging.Formatter(formatStr)
    console.setLevel(logLevel)
    console.setFormatter(formatter)

    #And finally, attach the console handler to the logger so the output goes both places
    logging.getLogger('').addHandler(console)

    logging.debug("Logging is configured - Log Level %s , Log File: %s",str(logLevel),logFilePath) 

def branch(branchPath):
    branchPath = str(branchPath)

    branchPath = os.path.normpath(branchPath)
    branchPath = os.path.abspath(branchPath)
    if os.path.exists(branchPath) and not os.path.isdir(branchPath):
        print("Can't branch to " +str(branchPath) + " - Path is not a directory")
        sys.exit(2)
    prjName = os.path.basename(branchPath)
    print("Branching template to " +str(branchPath))
    print("New project name is " + str(prjName))
    
    #1 - Make directory for new project
    if os.path.exists(branchPath) and os.path.isdir(branchPath):
        if ynUserPrompt("Target directory exists - overwrite?"):
            
            #delete directory and all of its contents
            shutil.rmtree(branchPath)
            
        else:
            print("Can't overwrite target directory - aborting.")
            sys.exit(2)
    elif os.path.exists(branchPath) and not os.path.isdir(branchPath):
        print("Target path exists already - but as a file. Aborting.")
        sys.exit(2);
    #Make the directory
    
    #Make the necessary subdirectories
    os.mkdir(branchPath)
    
    #2 - Add subdirectories
    print("Making subdirectories...")
    prjSubDirs = ["logs","src","cfg","install","nsis","bin","res"]
    for subDir in prjSubDirs:
        subDirPath = os.path.join(branchPath,subDir)
        os.mkdir(subDirPath)
    
    #3 - Copy over .gitignore and LICENSE.md as-is
    print("Copying files...")
    copyPaths = [".gitignore","LICENSE.md","nsis\\install.nsi","src\\pyCli.py"]
    
    for filePath in copyPaths:
        shutil.copyfile(os.path.join(".\\",filePath),os.path.join(branchPath,filePath))
        
    print("Finished branch, exiting...")
    
    sys.exit(2)
if __name__=="__main__":
    
    init()