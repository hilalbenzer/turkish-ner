#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import numpy as np
from sklearn.externals import joblib
from sklearn.neural_network import MLPClassifier

model = MLPClassifier(hidden_layer_sizes=(), learning_rate_init=0.01)

tempMap = {}
dicMap = {}
with open('dictionary.txt','r',encoding="utf-8") as file:
	for line in file:
		tempMap = { line.split()[0]:line.split()[1] }
		dicMap.update(tempMap)


dicLength = len(dicMap) + 1


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
		window1[int(dicMap.get(window[0]))] = 1
	else:
		window1[dicLength-1] = 1
	if window[2] in dicMap:
		window2[int(dicMap.get(window[0]))] = 1
	else:
		window2[dicLength-1] = 1
	if window[3] in dicMap:
		window3[int(dicMap.get(window[0]))] = 1
	else:
		window3[dicLength-1] = 1
	if window[4] in dicMap:
		window4[int(dicMap.get(window[0]))] = 1
	else:
		window4[dicLength-1] = 1
	quintet = window0 + window1 + window2 + window3 + window4
		
	return quintet

def createRecognition(rec,pos):
	
	if rec == "ORG":
		if pos == "B":
			return 0
		elif pos == "I":
			return 1
		elif pos=="L":
			return 2
		elif pos=="U":
			return 3
	elif rec=="LOC":
		if pos=="B":
			return 4
		elif pos=="I":
			return 5
		elif pos=="L":
			return 6
		elif pos=="U":
			return 7
	elif rec=="PER":
		if pos=="B":
			return 8
		elif pos=="I":
			return 9
		elif pos=="L":
			return 10
		elif pos=="U":
			return 11
	else:
		return 12

def check_valid(token):
	if token == "[LOC":
		return False
	elif token == "[ORG":
		return False
	elif token == "[PER":
		return False
	elif token == "]":
		return False
	else:
		return True

classes=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ,11, 12]
batch_count = 0

with open('reyyan.train.txt','r',encoding="utf-8",errors="ignore") as f:
	recognition_array = []
	feature_vector = []
	for line_count, line in enumerate(f):
		print(str(line_count) + "/" + str(24813) + " (" + str(batch_count) + ")")
		tokens = line.split()
		# ********* TODO *********
		if len(tokens) <= 5:
			continue
		current_entity_type = ""
		for token_number, token in enumerate(tokens):
			print(str(token_number) + "/" + str(len(tokens)))

			current_position = "O"
			# ********* TODO *********
			if token_number == 0 or token_number == 1:
				continue
			# ********* TODO *********
			if token_number == len(tokens) - 2 or token_number == len(tokens) - 1:
				continue
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

			recognition_array.append(createRecognition(current_entity_type, current_position))
			#print (token + " " + current_position + " (" + current_entity_type + ")")

			window = ["", "", "", "", ""]
			count = 1
			window_count = 0
			while window_count < 2:
				if check_valid(tokens[token_number - count]):
					window[1-window_count] = tokens[token_number - count]
					window_count += 1
				count += 1
			count = 1
			window_count = 0
			while window_count < 2:
				if check_valid(tokens[token_number + count]):
					window[3+window_count] = tokens[token_number + count]
					window_count += 1
				count += 1

			window[2] = token
			feature_vector.append(createQuintet(window))
			#print (token + " " + str(window))

		if line_count % 100 == 0:
			model = model.partial_fit(feature_vector, recognition_array, classes)
			model_name = "batch" + str(batch_count) + ".pkl"
			joblib.dump(model, model_name)
			batch_count += 1
			recognition_array = []
			feature_vector = []	

	


























