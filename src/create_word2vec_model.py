"""from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import gensim
import os
import multiprocessing

corpus = []

with open ("bounwebcorpus.txt", 'rb') as f:
	for i, line in enumerate (f):
		corpus.append(line.split())
		if i % 1000 == 0:
			print(str(i))

corpus.append("<UNKNOWN>")

model = gensim.models.Word2Vec(
			corpus,
			size=400,
			window=5,
			min_count=1,
			workers=4)

model.train(corpus, total_examples=1, epochs=1)

model.save("word2vec.model")"""


import logging
import sys
import multiprocessing

from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
 
inputFile = "bounwebcorpus.txt"
outputFile = "word2vec.model"

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(levelname)s %(message)s')

model = Word2Vec(LineSentence(inputFile), size=400, window=5, min_count=1, workers=multiprocessing.cpu_count(), iter = 1)
model.wv.save_word2vec_format(outputFile, binary=True)