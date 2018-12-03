import os
import sys
import math

###PSUEDO###

###/PSUEDO###

def roundup(x):
    return int(math.floor(x / 10.0)) * 10

# def setThresh(inDir, outFile):
#     rates = []
#     for fn in os.listdir(inDir):
#         for line in open(inDir+fn,'r'):
#             rate = float(line.split(',')[7])
#             rates.append(rate)

#     #thresh = mean(rates)+stdev(rates)*2
#     thresh = 1000
#     outFile.write("Overall Average: %f\n" % mean(rates))
#     outFile.write("Standard Deviation: %f\n" % stdev(rates))
#     outFile.write("Threshold set to: %f\n" % thresh)
#     return thresh

# def overThresh(inDir, outFile, thresh):
#     total = 0.0
#     overThresh = 0.0
#     for fn in os.listdir(inDir):
#         for line in open(inDir+fn,'r'):
#             rate = float(line.split(',')[7])
#             total+=1
#             if float(rate) > thresh:
#                 outFile.write(line)
#                 overThresh+=1

#     outFile.write("Percentage over threshold: %f\n" % (overThresh/total))

def initDict():
    ret = dict()
    for i in xrange(0,3000,10):
        ret[i] = 0
    return ret
    
    
def histoTeam(csvPath, outDir, team):

    outfn = outDir+'-'+team+'-histo.csv'
    print("Making output file: %s" % outfn)
    outFile = open(outfn, 'w')
    
    print("** Analyzing thresholds for team %s ** " % team)
    
    ## Input Dir
    inDir = os.getcwd() + '/' + csvPath + '/'
    if not os.path.isdir(inDir):
        print("Error: skipping directory %s" % inDir)
        return
    print("Input directory: " + inDir)

    bins = initDict()
    for fn in os.listdir(inDir):
        for line in open(inDir+fn,'r'):
            bins[roundup(float(line.split(',')[7]))]+=1

    for key,value in bins.iteritems():
        outFile.write(str(key)+','+str(value)+',\n')
    print


def histoDay(csvPath,outDir):
    for fn in os.listdir(os.getcwd()+csvPath):
        histoTeam(csvPath+'/'+fn, outDir, fn)

    
def histoDEFCON(csvPath):
    ## Output Dir
    outDir = os.getcwd() + '/results/' + csvPath[6:] + '/'
    print("Output file: " + outDir)
    print("Making output directory...")
    try: os.makedirs(outDir)
    except(OSError): print("Directory exists")

    csvPath += '/pcaps/'
    
    for fn in os.listdir(os.getcwd()+csvPath):
        histoDay(csvPath+'/'+fn, outDir+'/'+fn)


def main(argv):
    
    if len(argv) is not 1:
       print("Usage: python makeFlow.py <DEFCON name>")
       sys.exit(1)
    else:
        csvPath = '/csvs/' + argv[0] + '/'
        histoDEFCON(csvPath)
        #threshDay(csvPath)
        #makeCSVTeam(silkPath



if __name__ == "__main__":
    main(sys.argv[1:])
