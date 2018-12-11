import numpy as np
from gensim.models import KeyedVectors
import Util

word2vec_model = Util.word2vec_model

known_word_count = 0
unknown_word_count = 0

unknown_words = {}  

with open('reyyan.train.txt', 'r', encoding="utf-8", errors="ignore") as f:
	for line_count, line in enumerate(f):
		tokens = line.split()
		current_entity_type = ""
		for token_number, token in enumerate(tokens):
			if Util.is_beggining_tag(token):
				continue
			elif Util.is_ending_tag(token):
				continue
			if token in word2vec_model:
				known_word_count += 1
			elif token.lower() in word2vec_model:
				known_word_count += 1
			elif token.upper() in word2vec_model:
				known_word_count += 1
			elif token.capitalize() in word2vec_model:
				known_word_count += 1
			else:
				unknown_word_count += 1
				if token in unknown_words.keys():
					unknown_words[token] += 1
				else:
					unknown_words[token] = 1

with open('unknown.txt', 'w', encoding="utf-8", errors="ignore") as f:
	unknown_words_sorted = sorted(unknown_words.items(), key=lambda kv: kv[1])
	f.write("# of known words:\t" + str(known_word_count))
	f.write("\n")
	f.write("# of unknown words:\t" + str(unknown_word_count))
	f.write("\n")
	for key, value in unknown_words_sorted:
		f.write(str(key) + "\t->\t" + str(value))
		f.write("\n")
		