from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import gensim
import os

with open ("newscor.txt", 'rb') as f:
	for i, line in enumerate (f):
		corpus.append(line.split())

model = gensim.models.Word2Vec(
			corpus,
			size=150,
			window=5,
			min_count=1,
			workers=4)

model.train(corpus, total_examples=1, epochs=1)

model.save("word2vec.model")