import sys
import Util
from sklearn.externals import joblib
import warnings

warnings.filterwarnings("ignore")

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

sentences = ""

def find_classes(sentences):
	"""
	Predicts named entity tags of tokens using model
	Returns a list of predicted tags and a list of tokens
	"""
	found_class = []
	found_entity_token = []
	for line_count, line in enumerate(sentences):
		if line == "":
			continue
		tokens = line.split()
		previous_tags = [12, 12]
		temp_class = []
		temp_token = []
		for token_number, token in enumerate(tokens):
			window = Util.create_window(token_number, tokens)
			quintet = Util.create_quintet(window, dicMap, previous_tags)
			class_found = model.predict([quintet])
			previous_tags = [previous_tags[1], class_found]
			temp_class.append(Util.find_recognition_string(class_found))
			temp_token.append(token)
		found_class.append(temp_class)
		found_entity_token.append(temp_token)
	return found_class, found_entity_token

with open(input_file, 'r', encoding="utf-8", errors="ignore") as f:
	sentences = f.read().split("\n")

processed_sentences = Util.apply_preprocessing()

found_class, found_entity_token = find_classes(processed_sentences)

named_entities = []

with open(output_file, 'w', encoding="utf-8", errors="ignore") as f:
	for sentence_index, sentence in enumerate(found_entity_token):
		current_entity = ""
		current_entity_type = ""
		for token_index, token in enumerate(sentence):
			f.write(token)
			f.write(" ")
			word_class = found_class[sentence_index][token_index]
			if word_class != Util.position_O:
				f.write("[")
				f.write(word_class)
				f.write("] ")
				if "U-" in word_class:
					if Util.entity_type_LOC in word_class:
						named_entities.append((token, "Location"))
					elif Util.entity_type_PER in word_class:
						named_entities.append((token, "Person"))
					elif Util.entity_type_ORG in word_class:
						named_entities.append((token, "Organization"))
				elif "B-" in word_class:
					current_entity = current_entity + token + " "
					if Util.entity_type_LOC in word_class:
						current_entity_type = "Location"
					elif Util.entity_type_PER in word_class:
						current_entity_type = "Person"
					elif Util.entity_type_ORG in word_class:
						current_entity_type = "Organization"
				elif "I-" in word_class:
					current_entity = current_entity + token + " "
				elif "L-" in word_class:
					current_entity = current_entity + token + " "
					named_entities.append((current_entity, current_entity_type))
					current_entity = ""
					current_entity_type = ""
		f.write("\n")

for entity, entity_type in named_entities:
	print(entity)
	print(entity_type)
	print("\n")