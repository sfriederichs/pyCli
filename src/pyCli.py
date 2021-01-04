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
"""

import textwrap
import logging
import getopt
import sys
import datetime

def prettyPrint(uglyString):
    """This function properly formats docstrings for printing on the console"""
    
    #Remove all newlines
    uglyString = uglyString.replace('\n','').replace('\r','')
    #Use textwrap module to automatically wrap lines at 79 characters of text
    print(textwrap.fill(uglyString,width=79))
    

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
        
def main():
    progId()
    
    logFilePath = datetime.datetime.now().strftime('logs/log_%H_%M_%d_%m_%Y.log')

    logLevel = logging.DEBUG 
    formatStr = '%(asctime)s - %(threadName)s - %(funcName)s  - %(levelname)-8s %(message)s'
    try: 
        opts, args = getopt.getopt(sys.argv[1:], 'hvlf:e:', ['help','version','license','logfile=','loglevel='])    
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

if __name__ == "__main__":
    # execute only if run as a script
    main()