import sys
import pdb

def regexV(pattern, string):


    if not pattern:
        #if its an empty pattern return true if string is also empty
        return not string

    else:
        #Both strings length greater than 1
        #Match bool is used to make if statements more readable
        #First check if string is not empty then check for first char match, or '.' in pattern (which can match any char)
        match = bool(string) and (pattern[0] == string[0] or pattern[0] == '.')

        if pattern[0] == '(':
            #Start of parens, inside is treated as seperate pattern
            entireP = catchEntireParens(pattern[1:])
            return handleParens(pattern, string, entireP)
        elif len(pattern) >= 2 and pattern[1] == '*':
            #next char in pattern can repeat in the string (or not occur)
            return regexV(pattern[2:], string) or (match and regexV(pattern, string[1:]))

        elif len(pattern) >= 2 and pattern[1] == '+':
            #next char in pattern can repeat in the string (must occur at least once)
            return match and (regexV(pattern, string[1:]) or regexV(pattern[2:], string[1:]))

        elif len(pattern) >= 2 and pattern[1] == '?':
            #next char in pattern can either occur or not (but can't repeat)
            return regexV(pattern[2:], string) or (match and regexV(pattern[2:], string[1:]))

        elif len(pattern) >= 2 and pattern[1] == '{':
            #next char in pattern has to repeat the number of times specified by the int in the brackets
            repeats = findMinAndMaxRepeats(pattern, 2)
            return handleBrackets(pattern[0], string, repeats)

        elif match:
            #Just needed next chars to match (now check rest of string)
            return regexV(pattern[1:], string[1:])
        else:
            return False

def catchEntireParens(pattern):
    #Finds the length of current parens regex (which could have parens inside of it)
    countP = 1
    for i in range(len(pattern)):
        if pattern[i] == ')':
            countP -= 1
            if countP == 0:
                return i
        elif pattern[i] == '(':
            countP += 1

def handleBrackets(toMatch, string, repeats):
    #checks if string chars match for the specified # of times
    if len(string) < matchesNeeded:
        return False

    for i in range(matchesNeeded):
        if string[i] is not toMatch:
            return False
    return True


def handleParens(pattern, string, i):
    #i now equals length of string inside parens
    afterParens = pattern[i+2]
    print(afterParens)
    if afterParens == '*':
        #use pattern[i+3] to skip ()* chars
        return regexV(pattern[i+3:], string) or checkRestOfString(i, pattern[1:], string, True, 2)
    elif afterParens == '+':
        return checkRestOfString(i, pattern[1:], string, True, 2)

    elif afterParens == '?':
        return regexV(pattern[i+3:], string) or checkRestOfString(i, pattern[1:], string, False, 2)
    elif afterParens == '{':
        repeats = findMinAndMaxRepeats(pattern, i+3)
        return checkRestOfStringLimit(i, pattern[1:], string, repeats)


def findMinAndMaxRepeats(pattern, offset):
    minimumRepeats = int(pattern[offset])
    maximumRepeats = 0
    endOfBrackets = 3
    if pattern[offset+1] == ',':
        #maximum repeats is specified, could be {x,y} or {x,}
        if pattern[offset+2] == '}':
            #set to -1 to indicate infinity repeats after minimum threshold
            maximumRepeats = -1
            endOfBrackets = 4
        else:
            #maximum number of repeats is specified within brackets
            maximumRepeats = int(pattern[offset+2]) - minimumRepeats
            endOfBrackets = 5

    return [minimumRepeats, maximumRepeats, endOfBrackets]


def checkRestOfString(cutoff, pattern, string, canItRepeat, endOfParens):
    #Will check repeats of full regex within parens (or just once if '?' is after parens)
    print('cutt = ', cutoff)
    print('cutt = ', endOfParens)
    print('end of brackets = ', pattern[cutoff+endOfParens:])
    for i in range(len(string)+1):
        if regexV(pattern[:cutoff], string[:i]):
            if regexV(pattern[cutoff+endOfParens:], string[i:]) or \
                    (canItRepeat and checkRestOfString(cutoff, pattern, string[i:], True, endOfParens)):
                return True

    #Entire string has been checked for parens repeats
    return False


def checkRestOfStringLimit(cutoff, pattern, string, repeats):
    #Will check if regex inside parens repeats the correct # of times (specified by repeats array)
    minTimesToCheck = repeats[0]
    maxTimesToCheck = repeats[1]
    endOfBrackets = repeats[2] + 1
    print('min = ', minTimesToCheck)
    print('max = ', maxTimesToCheck)

    for i in range(len(string)+1):
        if regexV(pattern[:cutoff], string[:i]):
            if minTimesToCheck-1 == 0:
                if maxTimesToCheck == 0:
                    #Now make sure it doesn't repeat anymore times
                    print('patt = ', pattern)
                    #if not regexV(pattern, string[i:]) and regexV(pattern[cutoff+endOfBrackets:], string[i:]):
                    if not checkRestOfString(cutoff, pattern, string[i:], True, endOfBrackets) and regexV(pattern[cutoff+endOfBrackets:], string[i:]):
                        return True
                elif maxTimesToCheck == -1:
                    #This means the regex can repeat infinitely more times (so send it to checkRestOfString) or not at all
                    return checkRestOfString(cutoff, pattern, string[i:], True, endOfBrackets) or regexV(pattern[cutoff+endOfBrackets:], string[i:])
                else:
                    print('str = ', string[i:])
                    #extra > 1, meaning it can repeat a maximum # of times
                    #recursively check for repeats until maxTimesToCheck == 0
                    repeats[1] -= 1
                    return regexV(pattern[cutoff+endOfBrackets:], string[i:]) or checkRestOfStringLimit(cutoff, pattern, string[i:], repeats)


            repeats[0] -= 1
            if checkRestOfStringLimit(cutoff, pattern, string[i:], repeats):
                return True

    #Entire string has been checked for parens repeats and all lead to false
    return False



"""
if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        pattern = f.readline()[:-1]
        stringCheck = f.readline()[:-1]

        print(regexV(pattern, stringCheck))
"""
