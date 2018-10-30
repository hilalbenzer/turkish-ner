#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from sklearn.externals import joblib
from sklearn.metrics import f1_score
import Util

model = joblib.load('model.pkl')

tempMap = {}
dicMap = {}
actual_class = []
found_class = []

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

with open('reyyan.test.txt','r',encoding='utf-8',errors="ignore") as f:
	for line_count, line in enumerate(f):
		print("Line: " + str(line_count))
		tokens = line.split()
		current_entity_type = ""
		for token_number, token in enumerate(tokens):

			current_position = "O"
			if current_entity_type == "":
				if token == "[LOC":
					current_entity_type = "LOC"
					continue
				elif token == "[ORG":
					current_entity_type = "ORG"
					continue
				elif token == "[PER":
					current_entity_type = "PER"
					continue
			elif token == "]":
				current_entity_type = ""
				continue
			else:
				if tokens[token_number - 1] == "[LOC" or tokens[token_number - 1] == "[PER" or tokens[token_number - 1] == "[ORG":
					if tokens[token_number + 1] == "]":
						current_position = "U"
					else:
						current_position = "B"
				elif tokens[token_number + 1] == "]":
					current_position = "L"
				else:
					current_position = "I"

			actual_class.append(str(Util.find_recognition(current_entity_type, current_position)))

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

			classFound = findClass(Util.create_quintet(window, dicMap))
			found_class.append(classFound)

success = 0
failure = 0
for index, current in enumerate(found_class):
	if str(actual_class[index]) == str(current):
		success += 1
	else:
		failure += 1

print("Success: " + str(success))
print("Failure: " + str(failure))

print("Success rate: " + str((success/(success + failure)) * 100))


print("Macro average: " + str(f1_score(actual_class, found_class, average='macro')))
print("Micro average: " + str(f1_score(actual_class, found_class, average='micro')))
















