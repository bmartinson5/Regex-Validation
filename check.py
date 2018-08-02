import sys

def checkV(pattern):
    charsStack = []
    patternChars = list(pattern)
    for pChar in patternChars:
        print(pChar)
        if pChar == '(':
            charsStack.append('(')
        elif pChar == ')':
            if len(charsStack) == 0:
                return False
            charsStack.pop()

    if len(charsStack) == 0:
        return True
    return False
