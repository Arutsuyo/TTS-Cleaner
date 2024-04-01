from argparse import ArgumentParser
import re
from os import listdir
from os.path import isfile, join
from pathlib import Path

import json
import codecs
import sys




ConfigFileName = 'CleanerConfig.json'

def GetCleanerData():
    # Opening JSON file
    with codecs.open(ConfigFileName, 'r', 'utf-8-sig') as config:
        # returns JSON object as 
        # a dictionary
        data = json.load(config)
        return data["CleanerData"]
# End GetCleanerData()

def GetFileList(bookPath):
    onlyfiles = [f for f in listdir(bookPath) if isfile(join(bookPath, f))]
    if ConfigFileName in onlyfiles:
        onlyfiles.remove(CleanFileName)
    return onlyfiles
# End GetFileList()

def Clean(s):
    
    cleanConfig = GetCleanerData()
    
    cleanRemove = cleanConfig["Remove"]
    cleanReplace = cleanConfig["Replace"]
    cleanDelete = cleanConfig["Delete"]
    
    # Check for line deletion
    for cdlt in cleanDelete:
        if cdlt.casefold() in s.casefold():
            return ""

    # Check for Removals
    for crmv in cleanRemove:
        if crmv in s:
            s = s.replace(crmv, "")
        
    # Check for Replacements
    for key, value in cleanReplace.items():
        if key in s:
            s = s.replace(key, value)
        
    return s
# End Clean()



def CleanBook(bookPath, bookFileName):
    with open(join(bookPath, bookFileName), 'r', encoding="utf8") as book:
        content = book.read()

        # Remove excess newlines
        content = re.sub(r'\n\s*\n', '\n\n', content)

        contentLines = content.splitlines(keepends=True)

        for i in range(len(contentLines)):
            contentLines[i] = Clean(contentLines[i])
            
        # Clean empty lines
        contentLines = list(filter(None, contentLines))
        
        # Remove extra newlines
        for i in range(1, len(contentLines)):
            if contentLines[i] == '\n' and contentLines[i-1] == '\n':
                contentLines[i-1] = ""
                
        # Clean empty lines
        contentLines = list(filter(None, contentLines))
        

        Path(join(bookPath, "cleaned")).mkdir(parents=True, exist_ok=True)

        outfile = join(bookPath, "cleaned", f"{bookFileName[:-4]}_c.txt")
        with codecs.open(outfile, 'w', "utf-8") as f:
            f.writelines(contentLines)
# End CleanBook()

def PrintConfig(bookPath):
    print("Book dir: ")
    print(f"- {bookPath}")

    cleanConfig = GetCleanerData()
    print("Characters to remove:")
    
    cleanRemove = cleanConfig["Remove"]
    cleanReplace = cleanConfig["Replace"]
    cleanDelete = cleanConfig["Delete"]
    
    print("To Remove in-place:")
    for crmv in cleanRemove:
        print(f"- {crmv}")
        
    print("To Replace:")
    for key, value in cleanReplace.items():
        print(f"- {key} -> {value}")
        
    print("To Delete:")
    for cdlt in cleanDelete:
        print(f"- {cdlt}")

    print("")
# End PrintConfig()


def main():
    """
    Clean some stuff I guess.
    """
    cleanPath = input("Path to Text Files: ")
    PrintConfig(cleanPath)

    bookList = GetFileList(cleanPath)
    print("Target List:")
    for book in bookList:
        print(f"- {book}")
    print("")

    for book in bookList:
        print(f"Cleaning {book}. . .")
        CleanBook(cleanPath, book)

    print("All clean!")
    return
# End main()

if __name__ == "__main__":
    main()