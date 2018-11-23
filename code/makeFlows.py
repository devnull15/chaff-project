import os
import sys
import subprocess

## VARS ##


def makeFlowTeam(relPath):

    inDir = os.getcwd() + '/' + relPath +'/'
    print("Input directory: " + inDir)
    if not os.path.isdir(inDir):
        print("Ignoring file: %s" % inDir)
        return


    outDir = os.getcwd() + '/silk/' + relPath + '/'
    print("Output directory: " + outDir)
    print("Making output directory...")
    try: os.makedirs(outDir)
    except(OSError): print("Directory exists")

    
    for fn in os.listdir(inDir):
        f = open(inDir+fn, "r")
        command = "rwp2yaf2silk --in=%s --out=%s" % (inDir+fn, outDir+fn)
        print("**Executing: " + command) 
        subprocess.call(command.split())
        print


def makeFlowDay(relPath):
    for fn in os.listdir(os.getcwd()+relPath):
        makeFlowTeam(relPath+'/'+fn)
        
        
def makeFlowDEFCON(relPath):

    relPath = '/' + relPath + '/pcaps/'
    for fn in os.listdir(os.getcwd()+relPath):
        makeFlowDay(relPath+'/'+fn)
    
        
    


if __name__ == "__main__":
    if len(sys.argv) is not 2:
        print("Usage: python makeFlow.py <dir path>")
        sys.exit()
    else:
        makeFlowDay('/'+sys.argv[1])
        #makeFlowDEFCON(sys.argv[1])
