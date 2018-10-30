import numpy as np

def create_quintet(window, dictionary):
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

def find_recognition_string(rec):
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