import sys
import Util
from sklearn.externals import joblib

arguments = sys.argv

if len(arguments) != 3:
	print("Usage: python3 find_named_entities <input_file> <output_file>")
	sys.exit(0)

input_file = arguments[1]
output_file = arguments[2]

model_directory = 'model.pkl'
dictionary_directory = 'dictionary.txt'

model = joblib.load(model_directory)
dicMap = Util.read_dictionary_from_file(dictionary_directory)

found_class = []
found_entity_token = []

def find_class(quintet):
	result = model.predict([quintet])
	return result

with open(input_file, 'r', encoding="utf-8", errors="ignore") as f:
	for line_count, line in enumerate(f):
		tokens = line.split()
		previous_tags = [12, 12]
		for token_number, token in enumerate(tokens):
			window = Util.create_window(token_number, tokens)
			quintet = Util.create_quintet(window, dicMap, previous_tags)
			classFound = find_class(quintet)
			previous_tags = [previous_tags[1], classFound]
			found_class.append(Util.find_recognition_string(classFound))
			found_entity_token.append(token)


# for index, token in enumerate(found_entity_token):
# 	print(token + "\t\t" + found_class[index])
# 	a = 1