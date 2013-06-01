import os

# Author: Alex Grosjean
# 31 March 2013
# Takes a rack of letters for a game of scrabble as input
# returns each possible word and the value

def compute_score(word):
	#value = 0
	#for letter in word:
	#	value += scores[letter.lower()]
	#return value
	return sum(scores[c.lower()] for c in word)

scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
         "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
         "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
         "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
         "x": 8, "z": 10}
 
wordList = []
valid_list = []
usedRack = []

with open("C:\Users\AlexGrosjean\Documents\Python\Supplements\sowpods\sowpods.txt","r") as wordDoc:
	for word in wordDoc.readlines():
		word = word.strip('\n')
		wordList.append(word)
	
myRack = raw_input("Please enter your word: ")
myRack = myRack.upper()
print "...validating word against dictionary and computing values..."

for dictWord in wordList:
	#AB
	usedRack = []
	for letter in myRack:
		usedRack.append(letter)
	myWord = ""
	
	for dictLetter in dictWord:
		#A
		#B
		index = 0
		for myLetter in usedRack:
			#A
			#B
			#B
			#A
			if len(usedRack) > 0:
				if dictLetter == myLetter:
					myWord += dictLetter
					del(usedRack[index])
					break
			index += 1
		
		if myWord == dictWord:
			valid_list.append(myWord)
			break


wordListScore = {}
	
for word in valid_list:
	wordListScore[word] = compute_score(word)
	
if len(valid_list) > 50:
	print "...printing word to word document..."

	fileLocation = os.path.join(r"C:\Users\AlexGrosjean\Documents\Python\Supplements\sowpods",myRack.title()+"WordList")
	fileLocation += ".txt"
	
	with open(fileLocation,"w") as wordDoc:
		for word in wordListScore:
			wordDoc.write(word + " : " + str(wordListScore[word]) + "\n")
	print "Complete! Your words have been printed to: %s%s " % (myRack.title(),"WordList")
else:
	print "There are %i words in your list." % len(valid_list)
	for word in sorted(wordListScore):
		print word + " : " + str(wordListScore[word])

print "The largest value word in your rack is: %s : %i" % (max(wordListScore, key=wordListScore.get),wordListScore[max(wordListScore, key=wordListScore.get)])