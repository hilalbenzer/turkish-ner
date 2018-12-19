"""
Creates dictionary
Dict includes unique words and their ids
"""
from gensim.corpora import Dictionary

dictionary = Dictionary() 

def replace_digit(word):
	if check_sentence_border(word):
		return word
	return "".join(["#" if char.isdigit() else char for char in word])

with open('reyyan.train.txt', encoding="utf-8") as fp:
	for line in fp:

		tokens = line.split()
		tokens = [replace_digit(word) for word in tokens]

		dictionary.doc2bow(tokens, allow_update=True);

with open("dictionary.txt", "w", encoding="utf-8") as f:
	f.write("<SEN-2> 0\n")
	f.write("<SEN-1> 1\n")
	f.write("<SEN+1> 2\n")
	f.write("<SEN+2> 3\n")
	id = 4
	for s in dictionary.token2id:
		f.write(str(s) + " " + str(id) + "\n")
		id += 1
