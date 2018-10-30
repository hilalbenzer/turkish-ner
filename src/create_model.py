#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from sklearn.externals import joblib
from sklearn.neural_network import MLPClassifier
import Util

model = MLPClassifier(hidden_layer_sizes=(), learning_rate_init=0.01)

tempMap = {}
dicMap = {}
with open('dictionary.txt','r',encoding="utf-8") as file:
	for line in file:
		tempMap = { line.split()[0]:line.split()[1] }
		dicMap.update(tempMap)


dicLength = len(dicMap) + 1

classes=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ,11, 12]
batch_count = 0

with open('reyyan.train.txt','r',encoding="utf-8",errors="ignore") as f:
	recognition_array = []
	feature_vector = []
	for line_count, line in enumerate(f):
		print(str(line_count) + "/" + str(24813) + " (" + str(batch_count) + ")")
		tokens = line.split()
		current_entity_type = ""
		for token_number, token in enumerate(tokens):
			print(str(token_number) + "/" + str(len(tokens)))

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

			recognition_array.append(Util.find_recognition(current_entity_type, current_position))
			#print (token + " " + current_position + " (" + current_entity_type + ")")

			window = ["", "", "", "", ""]
			count = 1
			window_count = 0
			tokens_length = len(tokens)
			while window_count < 2:
				if token_number - count < 0:
					break
				if Util.check_valid_token(tokens[token_number - count]):
					window[1-window_count] = tokens[token_number - count]
					window_count += 1
				count += 1
			count = 1
			window_count = 0
			while window_count < 2:
				if token_number + count > tokens_length - 1:
					break
				if Util.check_valid_token(tokens[token_number + count]):
					window[3+window_count] = tokens[token_number + count]
					window_count += 1
				count += 1

			window[2] = token
			feature_vector.append(Util.create_quintet(window, dicMap))
			#print (token + " " + str(window))

		if line_count % 100 == 0:
			model = model.partial_fit(feature_vector, recognition_array, classes)
			#model_name = "batch" + str(batch_count) + ".pkl"
			#joblib.dump(model, model_name)
			batch_count += 1
			recognition_array = []
			feature_vector = []	
	joblib.dump(model, 'model.pkl')

	


























