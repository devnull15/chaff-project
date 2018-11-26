import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import subprocess
import shutil
import getopt

## VARS ##
addrs = {'Samurai': '10.5.6.2',
         'PPP': '10.5.1.2',
         '[Technopandas]': '10.5.2.2',
         'raon_ASRT': '10.5.4.2',
         'pwnies': '10.5.5.2',
         'The_European_Nopseld_Team': '10.5.7.2',
         'more_smoked_leet_chicken':'10.5.9.2',
         'blue_lotus': '10.5.10.2',
         'routards': '10.5.11.2',
         'shell_corp': '10.5.12.2',
         'shellphish': '10.5.13.2',
         'WOWHacker_BIOS': '10.5.14.2',
         '9447': '10.5.15.2',
         'men_in_black_hats': '10.5.16.2',
         'clgt': '10.5.3.2',
         'sutegoma2': '10.5.8.2',
         'pwningyeti': '10.5.17.2',
         'Alternatives': '10.5.19.2',
         'Robot_Mafia': '10.5.20.2',
         'LegitimateBusinessSyndicate': '10.5.22.2',
         'APT8': '10.5.18.2'
}
## /VARS ##

def makeHistograms(inDir): # BROKEN, but don't care
    print "* Making Histograms..."
    outDir = inDir+'/histograms/'
    print "Writing histograms to: " + outDir
    
    try: os.makedirs(outDir)
    except(OSError): print("Directory exists")

    for infn in os.listdir(inDir):
        if not os.path.isdir(inDir+infn):
            f = open(inDir+infn,'r')
            rates = []
            outfn = infn.split('.')[0]+'.png'
            outfnpath = outDir+outfn
            for line in f: rates.append(float(line.split(',')[4].strip()))
            bins = range(1,len(rates)+1)
            print("Making histogram %s" % outfn)
            fig = plt.bar(bins, rates, width=0.1)
            plt.title(outfn)
            plt.ylabel('Rate (pkts/sec)')
            plt.xlabel('Second')

            try:
                plt.ylim(0,max(rates))
                print("Max: %f" % max(rates)) # THIS BROKEN
            except(ValueError): plt.ylim(0,1000)
            plt.savefig(outfnpath)
            
    print()

def makeCSVTeam(silkPath, team):

    print "** Making CSVs..."

    ## Input Dir
    inDir = os.getcwd() + '/' + silkPath + '/'
    if not os.path.isdir(inDir):
        print("Error: skipping directory %s" % inDir)
        return
    print("Input directory: " + inDir)

    ## Output Dir
    outDir = os.getcwd() + '/csvs/' + silkPath[6:] + '/' ##WORKING
    print("Output directory: " + outDir)
    print("Making output directory...")
    try: os.makedirs(outDir)
    except(OSError): print("Directory exists")
                
    print("** Making CSVs for team %s" % team)
    for fn in os.listdir(inDir):
         for name,addr in addrs.iteritems():
             ## Args set up
             csvfn = "%s--%s.csv" % (team,name)
             saddress = addrs[team]
             daddress = addr
             inAbsPath = inDir+fn
             outAbsPath = outDir+csvfn
             ## /Args

             ## Incantation setup
             rwfiltercmd = ['rwfilter' , '-saddress='+saddress, '-daddress='+daddress,
                            '--pass-destination=stdout', inAbsPath]             
             rwfilter = subprocess.Popen(rwfiltercmd, stdout=subprocess.PIPE, shell=False)
             rwuniqcmd = ['rwuniq', '--plugin=flowrate.so', '--bin-time=1',
                          '--fields=sip,dip,sport,dport,protocol,stime,etime',
                          '--values=pckts/sec', '--sort-output']
             rwuniq = subprocess.Popen(rwuniqcmd, stdin=rwfilter.stdout,
                                       stdout=subprocess.PIPE, shell=False)
             grepcmd = ['grep', '-v', 'sIP']
             grep = subprocess.Popen(grepcmd, stdin=rwuniq.stdout,
                                    stdout=subprocess.PIPE, shell=False)
             sedcmd = ['sed', '--regexp-extended', '--expression=s/\|/\,/g']
             sed = subprocess.Popen(sedcmd, stdin=grep.stdout,
                                    stdout=subprocess.PIPE, shell=False)
             #print("**Executing: %s | %s  " % (str(rwfiltercmd),str(rwuniqcmd)))
             ## /Incantation
             
             ## Execute and save output
             print("**Writing file: %s..." % outAbsPath)
             with open(outAbsPath, 'a') as f: f.write(sed.communicate()[0])
             ##Execute


    print

def cleanCSVs():
    print("**Killing CSVs...")
    try: shutil.rmtree(os.getcwd()+'/csvs/')
    except(OSError): print
    print



def makeCSVDAY(silkPath):
    for fn in os.listdir(os.getcwd()+silkPath):
        print fn
        makeCSVTeam(silkPath+'/'+fn, fn)

    
def makeCSVDEFCON(silkPath):
    silkPath += '/pcaps/'
    
    for fn in os.listdir(os.getcwd()+silkPath):
        makeCSVDAY(silkPath+'/'+fn)


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
        silkPath = '/silk/' + argv[0] + '/'
        cleanCSVs()
        makeCSVDEFCON(silkPath)
        #makeCSVDAY(silkPath)
        #makeCSVTeam(silkPath

        #makeHistograms(outDir) # these aren't very helpful...


if __name__ == "__main__":
    main(sys.argv[1:])

