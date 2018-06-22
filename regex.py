import sys
import pdb

def regexV(pattern, string):
    """
    print(pattern)
    print(string)
    """

    if not pattern:
        return not string

    else:
        #Both strings length greater than 1
        #Match bool to make if statements more readable
        match = bool(string) and (pattern[0] == string[0] or pattern[0] == '.')

        if pattern[0] == '(':
            i = 0
            while pattern[i+1] != ')': i += 1
            #i now equals length of string inside parens
            afterParens = pattern[i+2]
            if afterParens == '*':
                #use pattern[i+3] to skip ()* chars
                return regexV(pattern[i+3:], string) or checkRestOfString(i, pattern[1:], string)

        elif len(pattern) >= 2 and pattern[1] == '*':
            return regexV(pattern[2:], string) or (match and regexV(pattern, string[1:]))
        elif match:
            return regexV(pattern[1:], string[1:])
        else:
            return False

def checkRestOfString(cutoff, pattern, string):
    for i in range(len(string)+1):
        if regexV(pattern[:cutoff], string[:i]):
            if regexV(pattern[cutoff+2:], string[i:]) or checkRestOfString(cutoff, pattern, string[i:]):
                return True
            return False
    
    return False


def matchMultiple(length, pattern, string):
    #goal is to check match of entire string inside parens of pattern
    #first check len of string is long enough to match

    if len(string) < length:
        return False

    for i in range(length):
        #pattern starts with '(' so use i+1 to skip it
        if pattern[i] != string[i]:
            return False
    return True


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        pattern = f.readline()[:-1]
        stringCheck = f.readline()[:-1]

        print(regexV(pattern, stringCheck))


