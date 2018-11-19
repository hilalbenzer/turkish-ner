import numpy as np

position_B = "B"
position_I = "I"
position_L = "L"
position_O = "O"
position_U = "U"

entity_type_LOC = "LOC"
entity_type_PER = "PER"
entity_type_ORG = "ORG"

def get_dict_lookup(word, dictionary):
	dic_length = len(dictionary) + 1
	vector = np.zeros((dic_length,), dtype=int)
	if word in dictionary:
		vector[int(dictionary.get(word))] = 1
	else:
		vector[dic_length-1] = 1
	return vector

def get_capitalization(word):
	if word.islower():
		return 0
	elif word.istitle():
		return 1
	elif word.isupper():
		return 2
	else:
		return 3

def replace_digit(word):
	return "".join(["#" if char.isdigit() else char for char in word])


def get_feature_vector(word, dictionary):
	word = replace_digit(word)
	capitalization_feature = [get_capitalization(word)]
	dict_feature = get_dict_lookup(word, dictionary)
	total_feature = np.concatenate((dict_feature, capitalization_feature))
	return total_feature

def create_quintet(window, dictionary):
	quintet = np.concatenate([get_feature_vector(word, dictionary) for word in window])		
	return quintet

def create_window(token_number, tokens):
	window = ["", "", "", "", ""]
	count = 1
	window_count = 0
	tokens_length = len(tokens)
	while window_count < 2:
		if token_number - count < 0:
			if token_number - count == -1:
				window[2-count] = "<SEN-1>"
			elif token_number - count == -2:
				if token_number == 0:
					window[0] = "<SEN-2>"
		elif check_valid_token(tokens[token_number - count]):
			window[1-window_count] = tokens[token_number - count]
		window_count += 1	
		count += 1
	count = 1
	window_count = 0
	while window_count < 2:
		if token_number + count > tokens_length - 1:
			if token_number + count == tokens_length:
				window[2+count] = "<SEN+1>"
			elif token_number + count == tokens_length + 1:
				if token_number == tokens_length - 1:
					window[4] = "<SEN+2>"
		elif check_valid_token(tokens[token_number + count]):
			window[3+window_count] = tokens[token_number + count]
		window_count += 1	
		count += 1

	window[2] = tokens[token_number]

	return window

def find_recognition_id(rec, pos):
	if rec == entity_type_ORG:
		if pos == position_B:
			return 0
		elif pos == position_I:
			return 1
		elif pos == position_L:
			return 2
		elif pos == position_U:
			return 3
	elif rec == entity_type_LOC:
		if pos == position_B:
			return 4
		elif pos == position_I:
			return 5
		elif pos == position_L:
			return 6
		elif pos == position_U:
			return 7
	elif rec == entity_type_PER:
		if pos == position_B:
			return 8
		elif pos == position_I:
			return 9
		elif pos == position_L:
			return 10
		elif pos == position_U:
			return 11
	else:
		return 12

def find_recognition_string(rec):
	if rec == 12:
		return "O"
	elif rec == 0:
		return "B-ORG"
	elif rec == 1:
		return "I-ORG"
	elif rec == 2:
		return "L-ORG"
	elif rec == 3:
		return "U-ORG"
	elif rec == 4:
		return "B-LOC"
	elif rec == 5:
		return "I-LOC"
	elif rec == 6:
		return "L-LOC"
	elif rec == 7:
		return "U-LOC"
	elif rec == 8:
		return "B-PER"
	elif rec == 9:
		return "I-PER"
	elif rec == 10:
		return "L-PER"
	elif rec == 11:
		return "U-PER"

def check_valid_token(token):
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

def get_entity_type(token):
	if token == "[LOC":
		return entity_type_LOC
	elif token == "[ORG":
		return entity_type_ORG
	elif token == "[PER":
		return entity_type_PER
	else:
		return ""

def is_beggining_tag(token):
	if token == "[LOC" or token == "[ORG" or token == "[PER":
		return True
	else:
		return False

def is_ending_tag(token):
	if token == "]":
		return True
	else:
		return False

def change_to_BIO(BILOU_classes):
	BIO_classes = []
	for tag in BILOU_classes:
		if tag == 'L-ORG':
			BIO_classes.append('I-ORG')
		elif tag == 'U-ORG':
			BIO_classes.append('B-ORG')
		elif tag == 'L-PER':
			BIO_classes.append('I-PER')
		elif tag == 'U-PER':
			BIO_classes.append('B-PER')
		elif tag == 'L-LOC':
			BIO_classes.append('I-LOC')
		elif tag == 'U-LOC':
			BIO_classes.append('B-LOC')
		else:
			BIO_classes.append(tag)
	return BIO_classes

def read_dictionary_from_file(filename):
	tempMap = {}
	dicMap = {}
	with open(filename,'r',encoding="utf-8") as file:
		for line in file:
			tempMap = { line.split()[0]:line.split()[1] }
			dicMap.update(tempMap)
	return dicMap