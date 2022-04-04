'''
Scrape JS functions and turn them into python that can be rendered with Sphinx

Flow:
    - Load in the JS as txt
    - Parse the text line by line and look for function beginnings and endings
    - When we see the keyword 'function', we want to get:
        - Function name
        - Input parameters
        - The entire contents of /* up to */, bearing in mind that JS multi-line comments start with *
'''

import sys
import os

def asciiArtIntro(verbose=True):

    if verbose:

        print("""
         ______        _     _               
        / _____)      | |   (_)              
        ( (____  ____ | |__  _ ____  _   _   
        \____ \|  _ \|  _ \| |  _ \( \ / )  
        _____) ) |_| | | | | | | | |) X (   
        (______/|  __/|_| |_|_|_| |_(_/ \_)  
                |_|                          
           ___               _______ ______ 
          / __)             (_______) _____)
        _| |__ ___   ____        _ ( (____  
       (_   __) _ \ / ___)   _  | | \____ \ 
        | | | |_| | |      | |_| | _____) )
        |_|  \___/|_|       \___/ (______/ 
                                            
        """)

def getSourceDir():

    # TODO Handle exceptions

    if sys.argv[1] == '.':
        return ''
    else:
    # Return the second CL argument
        return sys.argv[1]

def createParsedPythonDir():
    """
    Summary:
        - Create a folder that will hold all the JS docstrings converted to Python type if one doesn't already exist
    """

    if os.path.exists("parsedPython"):
        return None
    else:
        os.mkdir("parsedPython")

def generateDummyPython(jsTxt):
    """
    Summary:
        - Takes in js as text format (in a string) and extracts the docstring, then converts it to a Python format
    """

    # Parse functions from inside the JS
    # ['function GreatFunction() {\n', '    /*\n', '        Summary: Generates Alex a bunch of times in the console\n', '    */\n', '    while (True) {\n', '        console.log("Alex");\n', '    }\n', '}']

    numFunctions = 0

    # All of our docstrings
    pythonDocstrings = []

    for line in jsTxt:
        if 'function' in line:
            # Keep track of how many functions we've got
            numFunctions = numFunctions + 1
            # And get the main part, including the function name and the input params
            # Split by ()
            funcMain = line.split("(")
            # Grab the second part, which will be just the function name text
            funcName = funcMain[0].split(" ")[1]
            # Take the second item in the list, and split by closing brackets ')', then split by spaces
            funcParams = funcMain[1].split(")")[0].split(",")

            # And formulate the python function opener:
            pythonEquivalent = ("def %s(" % (funcName))

            # Need index of last item so we know when to close the brackets
            indexOfLast = funcParams.index(funcParams[-1])
            # Iterate over each of the parameters we got from the substring list
            for entry in funcParams:
                if funcParams.index(entry) == indexOfLast:
                    pythonEquivalent = pythonEquivalent + entry + "):"
                else:
                    pythonEquivalent = pythonEquivalent + entry + ", "

            # This leaves us with a string of the function parameters
            newPythonDocstring = pythonEquivalent

            # Will be true when the line we're cuurently iterating over is a doctstring line (i.e we haven't seen '*/' yet)
            trackingFunc = True

        # Get the next line after our function
        if trackingFunc:
            # Get the start and end indices:
            if '/*' in line:
                docstringStartIndex = jsTxt.index(line)
            if '*/' in line:
                docstringEndIndex = jsTxt.index(line)
                # Got the ending, so we can stop tracking our function:
                trackingFunc = False

                # and then commentText is all the lines between these 2
                commentText = jsTxt[docstringStartIndex+1:docstringEndIndex]

                # This includes all the leading whitespace for tabs, so we can keep it

                pythonCommentMarker = ' """ '

                newPythonDocstring = newPythonDocstring + "\n" + pythonCommentMarker

                for item in commentText:
                    # TODO: Check this, might encounter problems removing the newline character this way?
                    newPythonDocstring = newPythonDocstring + item

                # Append closing structure
                newPythonDocstring = newPythonDocstring + pythonCommentMarker

                # And finally add it to the cumulative list for all functions in the JS file
                pythonDocstrings.append(newPythonDocstring)

                trackingFunc = False

    print("Converted %d JS functions into python..." % (numFunctions))

    return pythonDocstrings

def saveTxtAsPython(allPython, filename):
    filepath = 'parsedPython/' + filename + '.py'
    with open(filepath, 'w') as f:
        for item in allPython:
            f.write("%s\n" % item)

    print("JS written to disk as Python!")

    return None

def handleCLI(inputs):

    CONFIG = {
            "VERBOSE" : False
        }

    if len(inputs) < 2:
        # No additional flags, skip
        return CONFIG

    for flag in inputs[2:]:
        if "-v" in flag:
            CONFIG["VERBOSE"] = True

    return CONFIG


def parseJsAsText():

    CONFIG = handleCLI(sys.argv)
    print(CONFIG)

    asciiArtIntro(verbose=CONFIG["VERBOSE"])

    # Get the source dir:
    sourceDir = str(getSourceDir())
    
    # Get list of all js files in the specified dir
    jsFiles = [f for f in os.listdir(sourceDir) if f.endswith('.js')]

    # And iterate over all these files
    for jsf in jsFiles:
        # Load in each file line by line as txt
        with open(sourceDir + jsf) as f:
            jsTxt = f.readlines()

        # With our js as txt, create a dedicated python dir (or pass if existing)
        createParsedPythonDir()

        # Parse the jsTxt and convert to dummy python - TODO: now need to make a change to handle multiple functions in a file:
        allPython = generateDummyPython(jsTxt)

        # And save the new Python dosctrings to disk - using the original filename but replacing it with .py
        saveTxtAsPython(allPython, jsf[:-3])

    return None


def main():

    parseJsAsText()

    print("\n Done! Now go and run Sphinx!")

    return None

if __name__ == "__main__" : main()