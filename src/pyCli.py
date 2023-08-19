#!/usr/bin/python3
"""
Generic Python CLI Script v0.1 
Version 0.1 Build 1 (8/18/23)
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

import logging
import getopt
import sys
import datetime
from cliLib import prettyPrint,ynUserPrompt,formatPath,branch

logFilePath = datetime.datetime.now().strftime('logs/log_%H_%M_%d_%m_%Y.log')
logLevel = logging.DEBUG
logFormatStr = '%(asctime)s - %(threadName)s - %(funcName)s  - %(levelname)-8s %(message)s'

def license(arg=None):
    for line in __doc__.splitlines()[2:4]:
        prettyPrint(line)
    sys.exit(0)

def help(arg=None):
    for line in __doc__.splitlines()[4:]:
        prettyPrint(line)
    sys.exit(0)

def version(arg=None):
    prettyPrint(__doc__.splitlines()[2])
    sys.exit(0)

def progId():
    prettyPrint(__doc__.splitlines()[1])

def getCliOpts(docString):

    shortOpts = []
    longOpts = []
    funcNames = []

    for line in docString.splitlines():
        pass
        #print(str(line))

    return shortOpts,longOpts,funcNames

def loglevel(arg):
    global logLevel

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

def logfilepath(arg):
    global logFilePath
    logFilepath = str(arg)

def init():
    global logFilePath
    global logLevel
    global formatStr

#    progId()

    #Read the command-line options from the docstring
    shortOpts,longOpts,funcNames = getCliOpts(__doc__)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "".join(shortOpts), longOpts)
    except getopt.GetoptError:
        print("Bad argument(s)")
        help()
        sys.exit(2)

    for opt, arg in opts:
        for shortOpt,longOpt,funcName in zip(shortOpts,longOpts,funcNames):
            if opt in (shortOpt, longOpt):
                eval( str(funcName)+"(arg)" )
            else:
                print("Bad Command line argument: " +str(opt)+ " - " +str(arg))
                help()
                sys.exit(2)

    logging.basicConfig(filename=logFilePath,filemode='a',level=logLevel,format=logFormatStr)

    #Then, retrieve a StreamHandler - this outputs log data to the console
    console = logging.StreamHandler()

    #Now configure the stream handler to the same settings as the file handler
    #Note, however that you don't need them both to be configured the same - it may be
    #entirely appropriate to have different settings for console vs. file.

    formatter = logging.Formatter(logFormatStr)
    console.setLevel(logLevel)
    console.setFormatter(formatter)

    #And finally, attach the console handler to the logger so the output goes both places
    logging.getLogger('').addHandler(console)

    logging.debug("Logging is configured - Log Level %s , Log File: %s",str(logLevel),logFilePath) 

if __name__=="__main__":
    
    init()
