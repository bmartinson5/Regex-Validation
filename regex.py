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
            return preProcessParens(pattern, string)

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
            #repeats = findMinAndMaxRepeats(pattern, 2)
            repeats = findRepeats(pattern, 2)
            return handleBrackets(pattern, string, repeats)
            #return handleBrackets(pattern[0], string, repeats) and regexV(pattern[repeats[2]:], string[repeats[0]:])

        elif match:
            #Just needed next chars to match (now check rest of string)
            return regexV(pattern[1:], string[1:])
        else:
            return False

def preProcessParens(pattern, string):
    #Start of parens, inside is treated as seperate pattern
    entireP = catchEntireParens(pattern[1:])
    #Search for or symbol '|' inside parens and retrieve array of seperate regex's

    return handleParens(pattern, string, entireP)


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

def handleBrackets(pattern, string, matchesNeeded):
    #checks if string chars match for the specified # of times
    toMatch = pattern[0]
    minMatches = matchesNeeded[0]
    if len(string) < minMatches:
        return False

    if minMatches != 0:
        #next char must match
        if string[0] is not toMatch:
            return False
        else:
            #check next string char until minMatches == 0
            matchesNeeded[0] -= 1
            return handleBrackets(pattern, string[1:], matchesNeeded)
    else:
        #only choice is to move on to next pattern char
        return regexV(pattern[matchesNeeded[1]:], string)


def handleParens(pattern, string, i):
    #i now equals length of string inside parens
    afterParens = pattern[i+2]
    if afterParens == '*':
        #use pattern[i+3] to skip ()* chars
        return regexV(pattern[i+3:], string) or checkRestOfString(i, pattern[1:], string, True, 2)
    elif afterParens == '+':
        return checkRestOfString(i, pattern[1:], string, True, 2)

    elif afterParens == '?':
        return regexV(pattern[i+3:], string) or checkRestOfString(i, pattern[1:], string, False, 2)
    elif afterParens == '{':
        repeats = findRepeats(pattern, i+3)
        print('rep = ', repeats)
        return checkRestOfStringLimit(i, pattern[1:], string, repeats)


def findRepeats(pattern, offset):
    repeats = getRepeatNumber(pattern[offset:])
    endOfBrackets = checkEndOfBrackets(pattern, offset)
    return [repeats, endOfBrackets]

def getRepeatNumber(pattern):
    number = ''
    idx = 0
    while pattern[idx] != '}':
        number += pattern[idx]
        idx += 1

    return int(number)

def checkEndOfBrackets(pattern, offset):
    index = 3 #to include both brackets and the first char
    while pattern[offset] != '}':
        index += 1
        offset += 1
    return index

def checkRestOfString(cutoff, pattern, string, canItRepeat, endOfParens):
    #Will check repeats of full regex within parens (or just once if '?' is after parens)
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
    endOfBrackets = repeats[1]

    for i in range(len(string)+1):
        if regexV(pattern[:cutoff], string[:i]):
            if minTimesToCheck-1 == 0:
                return regexV(pattern[cutoff+endOfBrackets:], string[i:])

            repeats[0] -= 1
            return checkRestOfStringLimit(cutoff, pattern, string[i:], repeats)

    #Entire string has been checked for parens repeats and all lead to false
    return False

#the following is for testing purposes
if __name__ == "__main__":
 with open(sys.argv[1]) as f:
     pattern = f.readline()[:-1]
     stringCheck = f.readline()[:-1]

     print(regexV(pattern, stringCheck))
