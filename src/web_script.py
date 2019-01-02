from . import Util
from sklearn.externals import joblib
import warnings

warnings.filterwarnings("ignore")


model_directory = 'src/model.pkl'
dictionary_directory = 'src/dictionary.txt'

model = joblib.load(model_directory)
dicMap = Util.read_dictionary_from_file(dictionary_directory)

location_color = "#0584F2"
person_color = "#EDF259"
organization_color = "#ABA6BF"

colors = {"Location": location_color, "Person": person_color, "Organization": organization_color}

def get_annotated_text(entity, entity_type):
	annotated_text = ""
	annotated_text += "<b><span style=\"background-color: "
	annotated_text += colors[entity_type]
	annotated_text += "\">"
	annotated_text += entity
	annotated_text += "</span></b> "
	return annotated_text

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

def run_ner(raw_text):
	sentences = raw_text.split("\n")
	processed_sentences = Util.apply_preprocessing(sentences)
	found_class, found_entity_token = find_classes(processed_sentences)
	output = "<p style=\"font-size:14px\"><font face=\"verdana\">"
	for sentence_index, sentence in enumerate(found_entity_token):
		current_entity = ""
		current_entity_type = ""
		for token_index, token in enumerate(sentence):
			word_class = found_class[sentence_index][token_index]
			if word_class != Util.position_O:
				if "U-" in word_class:
					entity = ""
					if Util.entity_type_LOC in word_class:
						entity = "Location"
					elif Util.entity_type_PER in word_class:
						entity = "Person"
					elif Util.entity_type_ORG in word_class:
						entity = "Organization"
					output += get_annotated_text(token, entity)
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
					current_entity = current_entity + token
					output += get_annotated_text(current_entity, current_entity_type)
					output += " "
					current_entity = ""
					current_entity_type = ""
			else:
				output += token
				output += " "
		output += "<br>"
	output += "</font></p>"
	return output
