import sys

specialCharacters = ['*', '+', '?', '}', '{', '(']

def checkV(pattern):
    functions = [checkForStartWithChar, checkForRepeatingChar, checkForParensImbalance, checkForAfterParens, checkForBracketLegal]
    messages = []
    for functionCall in functions:
        messages = functionCall(pattern, messages)
    return messages


def checkForBracketLegal(pattern, messages):
    #Searches pattern for a open bracket
    #if found format must match {x} where x is any positive number
    #also checks for imbalance of brackets
    prevOpenBracket = False
    for index in range(0, len(pattern)):
        if pattern[index] == '}':
            if not prevOpenBracket:
                messages.append('Imbalanced Brackets')
                return messages
            else:
                prevOpenBracket = False
        if pattern[index] == '{':
            prevOpenBracket = True
            restOfString = pattern[index:]
            #bracket found
            print(pattern[index:])
            if len(restOfString) < 3:
                #must have at least one digit
                messages.append('Bracket must include a number')
            else:
                #collect entire number (in string form) and verify that
                #it is a valid positive number
                numberInBrackets = searchRestOfString(restOfString[1:])
                if numberInBrackets.isdigit() == False or int(numberInBrackets) <= 0:
                    messages.append('Bracket must include number greater than zero')
    return messages


def searchRestOfString(restOfString):
        #collects number before '}'
        number = ''
        for character in restOfString:
            if character == '}':
                return number
            number += character
        #closing bracket not found
        return -1


def checkForAfterParens(pattern, messages):
    for ind in range(0, len(pattern)):
        if pattern[ind] == ')':
            if len(pattern) < ind+2 or pattern[ind+1] not in specialCharacters:
                messages.append('A quantifier must follow parenthesis')
    return messages


def checkForStartWithChar(startingChar, messages):
    #This function checks the start of the pattern for special characters (which is illegal)
    for character in specialCharacters:
        if character == startingChar[0]:
            messages.append('Pattern Can\'t start with special character')
    return messages


def checkForRepeatingChar(pattern, messages):
    #This function searches pattern for special characters and checks to see if
    #next char was also special (illegal move)
    for ind in range(0, len(pattern)):
        if pattern[ind] in specialCharacters:
            if len(pattern) > ind+1 and pattern[ind+1] in specialCharacters:
                messages.append('Can\' repeat special characters')
    return messages


def checkForParensImbalance(pattern, messages):
    charsStack = []
    patternChars = list(pattern)
    specialCharHandlers = [('(', handleOpenParens), (')', handleCloseParens)]
    for pChar in patternChars:
        for specialChars in specialCharHandlers:
            if specialChars[0] == pChar:
                #Parens found, make call to handler
                messages = specialChars[1](specialChars[0], charsStack, messages)

    if len(charsStack) != 0:
        messages.append('Imbalanced Parenthesis')
    return messages


def handleOpenParens(passed, charsStack, messages):
    charsStack.append('(')
    return messages


def handleCloseParens(passed, charsStack, messages):
    if len(charsStack) == 0:
        messages.append('Imbalanced Parenthesis')
    else:
        charsStack.pop()
    return messages
