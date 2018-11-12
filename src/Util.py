import numpy as np

def get_dict_lookup(word, dictionary):
	dic_length = len(dictionary) + 1
	#vector = np.zeros((dic_length,), dtype=int)
	vector = [0] * dic_length
	if word in dictionary:
		vector[int(dictionary.get(word))] = 1
	else:
		vector[dic_length-1] = 1
	return vector

def get_feature_vector(word, dictionary):
	dict_feature = get_dict_lookup(word, dictionary)
	return dict_feature



def create_quintet(window, dictionary):
	quintet = []
	#for word in window:
	#	quintet += get_dict_lookup(word, dictionary)

	dic_length = len(dictionary) + 1
	window0 = np.zeros((dic_length,), dtype=int)
	window1 = np.zeros((dic_length,), dtype=int)
	window2 = np.zeros((dic_length,), dtype=int)
	window3 = np.zeros((dic_length,), dtype=int)
	window4 = np.zeros((dic_length,), dtype=int)
	if window[0] in dictionary:
		window0[int(dictionary.get(window[0]))] = 1
	else:
		window0[dic_length-1] = 1
	if window[1] in dictionary:
		window1[int(dictionary.get(window[1]))] = 1
	else:
		window1[dic_length-1] = 1
	if window[2] in dictionary:
		window2[int(dictionary.get(window[2]))] = 1
	else:
		window2[dic_length-1] = 1
	if window[3] in dictionary:
		window3[int(dictionary.get(window[3]))] = 1
	else:
		window3[dic_length-1] = 1
	if window[4] in dictionary:
		window4[int(dictionary.get(window[4]))] = 1
	else:
		window4[dic_length-1] = 1
	quintet = window0 + window1 + window2 + window3 + window4

		
	return quintet

def create_window(token_number, tokens):
	window = ["", "", "", "", ""]
	count = 1
	window_count = 0
	tokens_length = len(tokens)
	while window_count < 2:
		if token_number - count < 0:
			if token_number - count == -1:
				if token_number == 0:
					window[1] = "<SEN-1>"
				elif token_number == 1:
					window[0] = "<SEN-1>"
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
				if token_number == tokens_length - 1:
					window[3] = "<SEN+1>"
				elif token_number == tokens_length - 2:
					window[4] = "<SEN+1>"
			elif token_number + count == tokens_length + 1:
				if token_number == tokens_length - 1:
					window[4] = "<SEN+2>"
		elif check_valid_token(tokens[token_number + count]):
			window[3+window_count] = tokens[token_number + count]
		window_count += 1	
		count += 1

	window[2] = tokens[token_number]

	return window

def find_recognition(rec, pos):
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

def find_full_recognition(rec, pos):
	if pos == "O":
		return "O"
	else:
		return pos + "-" + rec

def find_recognition_string(rec):
	if rec == "12":
		return "O"
	elif rec == "0":
		return "B-ORG"
	elif rec == "1":
		return "I-ORG"
	elif rec == "2":
		return "L-ORG"
	elif rec == "3":
		return "U-ORG"
	elif rec == "4":
		return "B-LOC"
	elif rec == "5":
		return "I-LOC"
	elif rec == "6":
		return "L-LOC"
	elif rec == "7":
		return "U-LOC"
	elif rec == "8":
		return "B-PER"
	elif rec == "9":
		return "I-PER"
	elif rec == "10":
		return "L-PER"
	elif rec == "11":
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