#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from sklearn.externals import joblib
import numpy as np

model = joblib.load('model.pkl')

tempMap = {}
dicMap = {}
allRecognitions = []
outputsAsLine = []
lineCounter = 0
with open('dictionary.txt','r',encoding="utf-8") as file:
	for line in file:
		tempMap = { line.split()[0]:line.split()[1] }
		dicMap.update(tempMap)


dicLength = len(dicMap) + 1

def findClass(quintet):
	aBatch=[]
	aBatch.append(quintet)
	for i in range(13):
		output=model.score(aBatch,[12-i])
		if(output == 1):
			return str(12-i)

def createQuintet(window):
	window0 = np.zeros((dicLength,), dtype=int)
	window1 = np.zeros((dicLength,), dtype=int)
	window2 = np.zeros((dicLength,), dtype=int)
	window3 = np.zeros((dicLength,), dtype=int)
	window4 = np.zeros((dicLength,), dtype=int)
	if window[0] in dicMap:
		window0[int(dicMap.get(window[0]))] = 1
	else:
		window0[dicLength-1] = 1
	if window[1] in dicMap:
		window1[int(dicMap.get(window[1]))] = 1
	else:
		window1[dicLength-1] = 1
	if window[2] in dicMap:
		window2[int(dicMap.get(window[2]))] = 1
	else:
		window2[dicLength-1] = 1
	if window[3] in dicMap:
		window3[int(dicMap.get(window[3]))] = 1
	else:
		window3[dicLength-1] = 1
	if window[4] in dicMap:
		window4[int(dicMap.get(window[4]))] = 1
	else:
		window4[dicLength-1] = 1
	quintet = window0 + window1 + window2 + window3 + window4
		
	return quintet


def nameClass(rec):
	if rec == "12":
		return "O"
	elif rec == "0":
		return "B-ORG"
	elif rec=="1":
		return "I-ORG"
	elif rec=="2":
		return "I-ORG"
	elif rec=="3":
		return "B-ORG"
	elif rec=="4":
		return "B-LOC"
	elif rec=="5":
		return "I-LOC"
	elif rec=="6":
		return "I-LOC"
	elif rec=="7":
		return "B-LOC"
	elif rec=="8":
		return "B-PER"
	elif rec=="9":
		return "I-PER"
	elif rec=="10":
		return "I-PER"
	elif rec=="11":
		return "B-PER"


with open('reyyan.test.txt','r',encoding='utf-8',errors="ignore") as f:
	for line in f:
		lineCounter = lineCounter + 1
		print("Line: " + str(lineCounter))
		counter=0
		tokens = line.split();
		while '[ORG' in tokens: tokens.remove('[ORG')
		while '[PER' in tokens: tokens.remove('[PER')
		while '[LOC' in tokens: tokens.remove('[LOC')
		while ']' in tokens: tokens.remove(']')

		for token_number, token in enumerate(tokens):
			print(str(token_number) + "/" + str(len(tokens)))

			window = ["", "", "", "", ""]
			count = 1
			window_count = 0
			tokens_length = len(tokens)
			while window_count < 2:
				if token_number - count < 0:
					break
				window[1-window_count] = tokens[token_number - count]
				window_count += 1	
				count += 1
			count = 1
			window_count = 0
			while window_count < 2:
				if token_number + count > tokens_length - 1:
					break
				window[3+window_count] = tokens[token_number + count]
				window_count += 1	
				count += 1

			window[2] = token

			classFound = findClass(createQuintet(window))
			allRecognitions.append(nameClass(classFound))
			counter = counter+1

counter = 0
success = 0
failure = 0
with open('recognitionsExpected.txt','r',encoding='utf-8',errors="ignore") as f:
	for line in f:
		if counter < len(allRecognitions):
			word = line.split()[0]
			if str(word) == str(allRecognitions[counter]):
				success += 1
			else:
				failure += 1
			counter = counter + 1

print("Success: " + str(success))
print("Failure: " + str(failure))

print("Success rate: " + str((success/(success + failure)) * 100))

"""with open('results.txt','w',encoding='utf-8',errors="ignore") as file:
	for current in allRecognitions:
		file.write(current)
		file.write("\n")"""


















