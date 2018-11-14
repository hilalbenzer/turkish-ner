#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from sklearn.externals import joblib
from sklearn.metrics import classification_report
from conlleval import evaluate
import Util

model = joblib.load('model.pkl')

dicMap = Util.read_dictionary_from_file('dictionary.txt')

actual_class = []
found_class = []

	for line in file:
def find_class(quintet):
	aBatch=[]
	aBatch.append(quintet)
	for i in range(13):
		output = model.score(aBatch,[12-i])
		if(output == 1):
			return 12-i

with open('reyyan.test.txt','r',encoding='utf-8',errors="ignore") as f:
	for line_count, line in enumerate(f):
		print("Line: " + str(line_count) + "/" + str(2750))
		tokens = line.split()
		current_entity_type = ""
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
			actual_class.append(Util.find_recognition_string(recognition_id))

			window = Util.create_window(token_number, tokens)

			classFound = find_class(Util.create_quintet(window, dicMap))
			found_class.append(Util.find_recognition_string(classFound))

actual_class_BIO = Util.change_to_BIO(actual_class)
found_class_BIO = Util.change_to_BIO(found_class)

success = 0
failure = 0
success_BIO = 0
failure_BIO = 0
for index, current in enumerate(found_class):
	if actual_class[index] == current:
		success += 1
	else:
		failure += 1
	if actual_class_BIO[index] == found_class_BIO[index]:
		success_BIO += 1
	else:
		failure_BIO += 1

print("\n=====================================\n")

print("BILOU results")
print("Success: " + str(success))
print("Failure: " + str(failure))
print("Success rate: " + str((success/(success + failure)) * 100))

prec, rec, f1 = evaluate(actual_class, found_class, verbose=True)

print ("Precision: " + str(prec))
print ("Recall: " + str(rec))
print ("F1: " + str(f1))

print("\n=====================================\n")

print("BIO results")
print("Success: " + str(success_BIO))
print("Failure: " + str(failure_BIO))
print("Success rate: " + str((success_BIO/(success_BIO + failure_BIO)) * 100))

prec, rec, f1 = evaluate(actual_class_BIO, found_class_BIO, verbose=True)

print ("Precision: " + str(prec))
print ("Recall: " + str(rec))
print ("F1: " + str(f1))

print("\n=====================================\n")

#target_names = ['O', 'B-ORG', 'I-ORG', 'L-ORG', 'U-ORG', 'B-LOC', 'I-LOC', 'L-LOC', 'U-LOC', 'B-PER', 'I-PER', 'L-PER', 'U-PER']

#print(classification_report(actual_class, found_class, target_names=target_names))
