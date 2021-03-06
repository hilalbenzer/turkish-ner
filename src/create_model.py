#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from sklearn.externals import joblib
from sklearn.neural_network import MLPClassifier
import Util

model = MLPClassifier(hidden_layer_sizes=(), learning_rate_init=0.01)

train_set_directory = 'corpus/reyyan.train.txt'
dictionary_directory = 'dictionary.txt'
model_directory = 'model.pkl'

dicMap = Util.read_dictionary_from_file(dictionary_directory)

classes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ,11, 12]
batch_count = 0

with open(train_set_directory, 'r', encoding="utf-8", errors="ignore") as f:
	recognition_array = []
	feature_vector = []
	for line_count, line in enumerate(f):
		print(str(line_count) + "/" + str(24813) + " (" + str(batch_count) + ")")
		tokens = line.split()
		current_entity_type = ""
		previous_tags = [12, 12]
		for token_number, token in enumerate(tokens):
			# Default encoding is O
			current_position = Util.position_O
			# If currently not on an entity
			if current_entity_type == "":
				current_entity_type = Util.get_entity_type(token)
				# If current token is the beginning of an entity
				if current_entity_type != "":
					continue
			# If current token is the end of an entity
			elif Util.is_ending_tag(token):
				current_entity_type = ""
				continue
			# If we are currently on an entity
			else:
				if Util.is_beggining_tag(tokens[token_number - 1]):
					if Util.is_ending_tag(tokens[token_number + 1]):
						current_position = Util.position_U
					else:
						current_position = Util.position_B
				elif Util.is_ending_tag(tokens[token_number + 1]):
					current_position = Util.position_L
				else:
					current_position = Util.position_I

			recognition_id = Util.find_recognition_id(current_entity_type, current_position)

			recognition_array.append(recognition_id)

			window = Util.create_window(token_number, tokens)
			
			quintet = Util.create_quintet(window, dicMap, previous_tags)

			previous_tags = [previous_tags[1], recognition_id]

			feature_vector.append(quintet)

		if line_count % 100 == 0 and line_count != 0:
			model = model.partial_fit(feature_vector, recognition_array, classes)
			batch_count += 1
			recognition_array = []
			feature_vector = []	
	joblib.dump(model, model_directory)
