#Deinterlinearizer v2
#Python script for data processing work on Sora conducted by Living Tongues
#
#11/11/2021
#Benjamin Hunt

#Procedure: take in standardized .txt files from the Sora data corpus 
#and split them into component data categories (phon, morphsyn, gloss) 
#to simplify the processing for ELAN. Assumes that spacing/line cleanup
#has been done. Input should be normalized text files.

import re
import os
import sys
import time

#############################
#     Deinterlinearize      #
#############################

#   Procedure:
#-------------------------------
#   1 - open and read txt file
#   2 - store text
#   3 - create output file with same name + "deint"
#   4 - create 3 dataframes/lists and store the 3 data types in each one
#   5 - delete header lines
#   6 - Split by \n and then by \t
#       lines 0,3,6,->end-2 are phonetic
#       lines 1,4,7,->end-1 are morphosyntax
#       lines 2,5,8,->end are english gloss
#   7 - print lists to output file (phon->morph->eng), one data item per line
#

class deinter:
    def __init__(self, lines):
        self.lines = [x for x in lines if "#" not in x]
        self.header = [x for x in lines if '#' in x]
        self.phon = []
        self.morph = []
        self.gloss = []
        self.deintList = self.deinterOpIter(self.lines)
        self.lineItems = self.lineItems()

    #Old deinter func; fails on non-cleaned phon and morph lines (stray spaces instead of tabs)
    def deinterOp(self, lines):
        self.phon = lines[0::3]
        self.morph = lines[1::3]
        self.gloss = lines[2::3]
        #temp = self.phon + self.morph + self.gloss
        #temp = [x.split("\t") for x in temp]
        tempPhon = [x.split() for x in self.phon]
        tempMorph = [x.split() for x in self.morph]
        tempGloss = [x.split("\t") for x in self.gloss]
        tempAll = tempPhon + tempMorph + tempGloss
        return tempAll

    def deinterOpIter(self, lines):
        #grab all gloss lines in either format '' or ‘’
        self.gloss = [x for x in lines if "‘" in x or "'" in x]
        #all other lines (phon and morph)
        self.other = [x for x in lines if not x in self.gloss]
        #assumes first line is phon, second is morph, third is phon, etc.
        self.phon = self.other[0::2]
        self.morph = self.other[1::2]
        #split on tabs and stray spaces if not cleaned properly
        tempPhon = [x.split() for x in self.phon]
        tempMorph = [x.split() for x in self.morph]
        tempGloss = [x.split("\t") for x in self.gloss]
        #concat all 3 lists
        tempAll = tempPhon + tempMorph + tempGloss
        return tempAll


    def lineItems(self):
        temp = []
        newline = ""
        #loop through deintList
        for x in self.deintList:
            for item in x:
                #add each data point in the list of lists to a new line
                temp.append(newline + item)
                newline = "\n"
        return temp

def splashScreen():
    #clear terminal when program starts
    os.system('cls' if os.name == 'nt' else 'clear')
    #resize window to look nice
    os.system('mode 73,40')
    dirPath = ""

    print(f"""
                        ___    ___    _   ________
                       /   |  /   |  / | / /_  __/
                      / /| | / /| | /  |/ / / /   
                     / ___ |/ ___ |/ /|  / / /    
                    /_/  |_/_/  |_/_/ |_/ /_/     

                               AANT
                      Automatic Annotation Tool
                             Version 0.6
           Living Tongues Institute for Endangered Languages (c)
                            Benjamin Hunt
                             12/13/2021
    

        AANT is a command-line utility for converting linguistic 
        fieldnotes from a file of interlinear glosses to a format 
        that can be imported to ELAN for automatic annotation of 
        corresponding audio recordings.

        Please enter the path to the directory you would like to 
        process.
    
    """)

    dirPath = input("        >Directory: ")
    return dirPath

def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()        
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()

def main():
    while True: 
        workDir = ""
        inFiles = []
        outFiles = []

        #Quick process without interface; takes inline argument for working directory
        if len(sys.argv) == 2:
            if os.path.isdir(sys.argv[1]):
                files = os.listdir(sys.argv[1])

                for item in files:
                    flName = item[:-4] + "_deint.txt"
                    
                    subPath = "deinter"
                    if not os.path.isdir(subPath):
                        os.makedirs(subPath)
                    with open(os.path.join(subPath, flName), "w", encoding="utf-8") as fout:
                        with open(os.path.join(sys.argv[1], item), encoding="utf-8") as fin:
                            text = fin.read()
                            text = text.splitlines()
                            output = deinter(text)

                            for line in output.lineItems:
                                fout.write(line)
            else:
                print("Directory not found.")
        #interactive interface; splashscreen and user input for working directory; prints results
        elif len(sys.argv) == 1:
            dirPath = splashScreen()
            workDir = dirPath
            #check that working dir exists
            if os.path.isdir(dirPath):
                files = os.listdir(dirPath)
                
                for item in files:
                    flName = item[:-4] + "_deint.txt"
                    inFiles.append(item)
                    outFiles.append(flName)

                    #create outputdir if it doesn't exist
                    subPath = "deinter"
                    if not os.path.isdir(subPath):
                        os.makedirs(subPath)
                    with open(os.path.join(subPath, flName), "w", encoding="utf-8") as fout:
                        with open(os.path.join(dirPath, item), encoding="utf-8") as fin:
                            text = fin.read()
                            text = text.splitlines()
                            output = deinter(text)

                            for line in output.lineItems:
                                fout.write(line)          
            else:
                print("Directory not found.")
            
            os.system('cls' if os.name == 'nt' else 'clear')

            for i in progressbar(files, "Processing: ", 40):
                time.sleep(0.1)

            print(f"""

                +-------------------------------+
                | Files successfully processed! |
                +-------------------------------+

    >Processed these files:\n""")
            for x in inFiles:
                print("\t./" + workDir + "/" + x + "\n")

            print("\n\n    >Locate the processed files at:\n")
            for y in outFiles:
                print("\t./deint/" + y + "\n")
        else:
            print(f"""\n\nUsage:\nQUICK PROCESS: python3 {sys.argv[0]} inputDir\n\nINTERACTIVE MODE: python3 {sys.argv[0]}\n\n""", file=sys.stderr, flush=True)
    
        ##Prompt for restart
        while True:
            answer = str(input('  Would you like to process additional files? (y/n): '))
            if answer in ('y', 'n'):
                break
            print("\n  invalid input.")
        if answer == 'y':
            continue
        else:
            print("\n  Goodbye")
            break

if __name__ == "__main__":
    main()