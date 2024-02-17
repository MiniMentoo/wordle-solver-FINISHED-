WORDLE_SIZE = 5
#comment whichever one you're not using, I recommend using the full words.txt since answers.txt is outdated and might miss answers
FILENAME = "words.txt"
#FILENAME = "answers.txt"

from string import ascii_lowercase

with open(FILENAME, "r") as words:
    lines = words.readlines()
for i in range(len(lines)):
    lines[i] = lines[i].rstrip()

def charInWord(char, word):
    for c in word:
        if(char == c):
            return True
    return False

def eliminateLetter(char, words): #if there's a double letter and one is grey, it'll eliminate all single letters too
    for x in range(len(words)-1, -1, -1):
        if charInWord(char, words[x]):
            words.pop(x)
    return words

def eliminateYellow(char, pos, words):
    for x in range(len(words)-1, -1, -1):
        if (not charInWord(char, words[x])):
            words.pop(x)
        elif (words[x][pos] == char):
            words.pop(x)
    return words

def findMatch(char, i, words):
    for x in range(len(words)-1, -1, -1):
        if (words[x][i] != char):
            words.pop(x)
    return words

def findDupes(word):
    dupes = []
    chars = []
    for c in word:
        if c in chars and (not c in dupes):
            dupes.append(c)
        else:
            chars.append(c)
    return dupes

def hasDupe(char, word):
    count = 0
    for c in word:
        if c == char:
            count += 1
    return count > 1

def deleteDupes(char, words):
    for x in range(len(words)-1, -1, -1):
        if(hasDupe(char, words[x])):
            words.pop(x)
    return words

def filterNonDupes(char, pos, words):
    for x in range(len(words)-1, -1, -1):
        if (not hasDupe(char, words[x])):
            words.pop(x)
        elif (words[x][pos] == char):
            words.pop(x)
    return words

def rankList(words):
    rankList = [] #stores 5 dictionaries, each keeping track of how many times the letter appeared in that position
    for i in range (WORDLE_SIZE):
        dict = {}
        for c in ascii_lowercase:
            dict.update({c : 0})
        rankList.append(dict)
    
    for x in range(len(words)-1, -1, -1):
        for i in  range(WORDLE_SIZE):
            c = words[x][i]
            rankList[i][c] = rankList[i][c] + 1    
    return rankList

def computeValue(word, rankList):
    value = 0
    for i in range(WORDLE_SIZE):
        value += rankList[i][word[i]]
    return value

def findBestGuess(words, rankList):
    bestVal = -1
    bestWord = None
    for word in words:
        val = computeValue(word, rankList)
        if val > bestVal:
            bestVal = val
            bestWord = word
    return bestWord

loop = "t"
print("----Finding best guess----")
print (findBestGuess(lines, rankList(lines)))
while (loop == "t"):
    word = input("Enter a 5 letter word: ")
    accuracy = input("How correct was the word? 0 = grey, 1 = yellow, 2 = green: ")
    dupes = [] #keeps a record of characters checked so it can track dupes
    for i in range (5):
        char = word[i]
        acc = accuracy[i]
        if (acc == '0' and (char in dupes)):
            lines = deleteDupes(char, lines)
        elif (acc == '1' and (char in dupes)):
            lines = filterNonDupes(char, i, lines)
        elif (acc == '0'):
            lines = eliminateLetter(char, lines)
        elif (acc == '1'):
            lines = eliminateYellow(char, i, lines)
            dupes.append(char)
        elif (acc == '2'): #edge case if sanes has acc 00002 (will remove all s first)
            lines = findMatch(char, i, lines)
            dupes.append(char)    
    print(lines)
    print("----Finding best guess----")
    print (findBestGuess(lines, rankList(lines)))

    loop = input("Continue? (t or f): ")