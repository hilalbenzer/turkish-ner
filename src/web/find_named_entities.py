import sys
import Util
from sklearn.externals import joblib
import warnings

warnings.filterwarnings("ignore")

model_directory = 'model.pkl'
dictionary_directory = 'dictionary.txt'

model = joblib.load(model_directory)
dicMap = Util.read_dictionary_from_file(dictionary_directory)

terminal = [".", "?", "...", "!", "…"]
separate_both = [",", "/", "\"", "(", ")", "?", "!", "…", ";", "%", "#", "$", "=", "@", "+", "&"]
separate_nondigit = [".", ":"]
separate_left = ["\'"]
unwanted_apostrophe = ["`", "´", "‘", "’"]
unwanted_quote = ["“", "”"]
remove = ["[", "]"]

location_color = "#FFFF00"
person_color = "#FF00FF"
organization_color = "#00FFFF"

colors = {"Location": location_color, "Person": person_color, "Organization": organization_color}

def apply_preprocessing(sentences):
	"""
	Applies preprocessing to raw text
	Returns processed sentences
	"""
	processed_sentences = []
	for sentence in sentences:
		# Acquire tokens
		tokens = sentence.split()
		temp_sentence = []
		for token_index, token in enumerate(tokens):
			# If token is the last token in sentence, get rid of punctuation
			# Since train/test sets do not contain . ? ! in the end of the sentences
			if token_index == len(tokens) - 1:
				for punc in terminal:
					token = token.replace(punc, '')
				if token != "":
					temp_sentence.append(token)
			else:
				if token != "":
					# Remove these characters
					for punc in remove:
						token = token.replace(punc, '')
					# Convert different types of apostrophe into single '
					for punc in unwanted_apostrophe:
						token = token.replace(punc, "\'")
					# Convert different types of quote into single "
					for punc in unwanted_quote:
						token = token.replace(punc, "\"")
					# Separate these characters from tokens at both sides
					for punc in separate_both:
						token = token.replace(punc, " "+punc+" ")
					# Separate these characters from tokens at left only
					for punc in separate_left:
						token = token.replace(punc, " "+punc)
					new_token = []
					# Separate these characters from sides that are not digits
					for index in range(len(token)):
						append = False
						if token[index] in separate_nondigit:
							if index != 0 and not token[index-1].isdigit():
								new_token.append(" ")
							if index != len(token)-1 and not token[index+1].isdigit():
								append = True
						new_token.append(token[index])
						if append:
							new_token.append(" ")
					token = "".join(new_token)
					if token != "":
						temp_sentence.append(token)
		processed_sentences.append(" ".join(temp_sentence))
	return processed_sentences

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
	print("Raw text ", raw_text)
	sentences = raw_text.split("\n")
	processed_sentences = apply_preprocessing(sentences)
	found_class, found_entity_token = find_classes(processed_sentences)
	output = ""
	for sentence_index, sentence in enumerate(found_entity_token):
		current_entity = ""
		current_entity_type = ""
		for token_index, token in enumerate(sentence):
			word_class = found_class[sentence_index][token_index]
			if word_class != Util.position_O:
				if "U-" in word_class:
					output += "<span style=\"background-color: "
					if Util.entity_type_LOC in word_class:
						output += colors["Location"]
					elif Util.entity_type_PER in word_class:
						output += colors["Person"]
					elif Util.entity_type_ORG in word_class:
						output += colors["Organization"]
					output += "\">"
					output += token
					output += "</span> "
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
					output += "<span style=\"background-color: "
					output += colors[current_entity_type]
					output += "\">"
					output += current_entity
					output += "</span> "
					current_entity = ""
					current_entity_type = ""
			else:
				output += token
				output += " "
		output += "\n"
	return output
