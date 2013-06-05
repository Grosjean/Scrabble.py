import os, os.path
import operator
from urllib2 import urlopen
from urllib2 import URLError

# Author: Alex Grosjean
# 31 March 2013
# Takes a rack of letters for a game of scrabble as input
# returns each possible word and the value

def compute_score(word):
	"""computes the dictionary word against scrabble score"""
	return sum(scores[c.lower()] for c in word)

def get_fileLocation(location1, location2, fileName):
	"""	returns the location of the specified file, using a specified path
		if path does not exist, create it"""
	
	prof_path = os.environ['USERPROFILE']
	fileDirectory = os.path.join(prof_path,location1,location2)
	
	if not os.path.exists(fileDirectory):
			os.makedirs(fileDirectory)
			
	fileLocation = os.path.join(fileDirectory,fileName)
	return fileLocation
	
scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
         "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
         "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
         "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
         "x": 8, "z": 10}
 
wordList = []
continueScrabble = True
	
print "Hello and welcome to the scrabble cheating engine!\n"

fileLocation = get_fileLocation('Documents','','sowpods.txt')

if not os.path.exists(fileLocation):
	#if sowpods.txt is not saved in my documents then open up textfile from website and read each dictionary word
	
	print "\tCould not find sowpods dictionary file from the documents folder: %s" % (get_fileLocation('Documents','','sowpods.txt'))
	print "\tOpening 3MB sowpods dictionary file from internet. This could take a few seconds..\n"
	
	try:
	
		target_url = "https://raw.github.com/Grosjean/Scrabble.py/master/sowpods.txt"
		wordDoc = urlopen(target_url)
		
		for word in wordDoc:
			word = word.strip('\n')
			wordList.append(word)
			
	except URLError:
		
		print "~" * 75
		print "Uh oh.. looks like your firewall is preventing us from connecting to server."
		print "Please save the 'sowpods.txt' file to your 'Documents' folder.\n"
		print target_url
		print "~" * 75
		continueScrabble = False

else:
	#else... file IS saved in my documents lets open it and read each dictionary word
	
	with open(fileLocation,"r") as wordDoc:
		for word in wordDoc:
			word = word.strip('\n')
			wordList.append(word)


while continueScrabble:
	
	valid_list = []
	usedRack = []
	wordListScore = {}
	
	myRack = raw_input("Please enter the letters in your rack: ").upper()
	print "...validating word against dictionary and computing values...\n"

	for dictWord in wordList:

		usedRack = []
		
		for letter in myRack:
			usedRack.append(letter)
		
		myWord = ""
		
		if len(dictWord) <= len(myRack):
			
			for dictLetter in dictWord:

				index = 0
				for myLetter in usedRack:

					if len(usedRack) > 0:
						if dictLetter == myLetter:
							myWord += dictLetter
							del(usedRack[index])
							break
					index += 1
				
				if myWord == dictWord:
					valid_list.append(myWord)
					break
		
	for word in valid_list:
		wordListScore[word] = compute_score(word)
	
	if len(valid_list) > 30:
			
		fileLocation = get_fileLocation('Desktop','Scrabble',myRack.title() + "_WordList.txt")
		
		with open(fileLocation,"w") as wordDoc:
			wordDoc.write("List of possible words that can be spelled with: " + myRack + "\n\n")
			wordDoc.write("word \t\t : \t value\n")
			wordDoc.write("-----------------------------\n")
			for word in sorted(wordListScore, key=wordListScore.get, reverse = True):
				if len(word) >= 7:
					wordDoc.write(word + " \t : \t " + str(wordListScore[word]) + "\n")
				else:
					wordDoc.write(word + " \t\t : \t " + str(wordListScore[word]) + "\n")
		print "Complete! Your scrabble words have been printed to your desktop: %s%s " % (myRack.title(),"WordList")
		print "\t" + fileLocation
		
	else:
		
		print "There are %i words in your list:" % len(valid_list)
		print "\tword \t : \t value"
		print "\t----------------------"
		for word in sorted(wordListScore, key=wordListScore.get, reverse=True):
			print "\t" + word + " \t : \t " + str(wordListScore[word])
			
	if len(myRack) > 1:
		try:
			print "The largest value word in your rack is: %s : %i" % (max(wordListScore, key=wordListScore.get),wordListScore[max(wordListScore, key=wordListScore.get)])
		except:
			pass
			
	response = raw_input("\nWould you like to play again? (y \ n) : ")
		
	if response[0].lower() != "y":
		continueScrabble = False
	else:
		print ""
else:
	print "\nThanks for playing!"