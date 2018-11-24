#!/usr/bin/python3.5
from statistics import mean, stdev
import os
import sys
import getopt

###PSUEDO###
# For each day...
# For every team...
# For every CSV...
## For every line...
## if rate meets a threshold, grab that record and write it to output file
###/PSUEDO###

###VARS###
thresh = 700
###/VARS###


def threshTeam(csvPath, outFile, team):
    
    print("** Analyzing thresholds for team %s ** " % team)
    outFile.write("*** %s ***\n" % team)
    
    ## Input Dir
    inDir = os.getcwd() + '/' + csvPath + '/'
    if not os.path.isdir(inDir):
        print("Error: skipping directory %s" % inDir)
        return
    print("Input directory: " + inDir)

    total = 0.0
    overThresh = 0.0
    rates = []
    for fn in os.listdir(inDir):
        for line in open(inDir+fn,'r'):
            rate = float(line.split(',')[4])
            rates.append(rate)
            total+=1
            if float(rate) > thresh:
                outFile.write(line)
                overThresh+=1
    outFile.write("Percentage over threshold: %f\n" % (overThresh/total))
    outFile.write("Overall Average: %f\n" % mean(rates))
    outFile.write("Standard Deviation: %f\n" % stdev(rates))

    print


def threshDay(csvPath,outFile):
    for fn in os.listdir(os.getcwd()+csvPath):
        threshTeam(csvPath+'/'+fn, outFile, fn)

    
def threshDEFCON(csvPath):
    ## Output Dir
    outDir = os.getcwd() + '/results/' + csvPath[6:] + '/'
    print("Output file: " + outDir)
    print("Making output directory...")
    try: os.makedirs(outDir)
    except(OSError): print("Directory exists")

    csvPath += '/pcaps/'
    
    for fn in os.listdir(os.getcwd()+csvPath):
        outfn = outDir+'/'+fn+'-results.txt'
        print("Making output file: %s" % outfn)
        outFile = open(outfn, 'w')
        threshDay(csvPath+'/'+fn, outFile)


def main(argv):
    # try: opts, args = getopt.getopt(argv,"c:d:t:")
    # except getopt.GetoptError:
    #     print("Usage: python makeFlow.py [-c (defcon), -d (day), -t (team)] <relative path>")
    #     sys.exit(2)

    # print opts
    # print args
    # silkPath = '/silk/' + args[0] + '/'
    # cleanCSVs() # need to fix this so that it doesn't nuke everything
    # print opts
    # for opt,arg in opts:
    #     print opt,arg
    #     if opt=='--defcon':
    #         makeCSVDEFCON(silkPath)
    #     elif opt=='--day':
    #         makeCSVDAY(silkPath)
    #     elif opt=='--team':
    #         makeCSVTeam(silkPath)
    
    if len(argv) is not 1:
       print("Usage: python makeFlow.py <DEFCON name>")
       sys.exit(1)
    else:
        csvPath = '/csvs/' + argv[0] + '/'
        threshDEFCON(csvPath)
        #makeCSVDAY(silkPath)
        #makeCSVTeam(silkPath



if __name__ == "__main__":
    main(sys.argv[1:])
