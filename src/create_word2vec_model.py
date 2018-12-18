import logging
import sys
import multiprocessing

from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
 
bounCorpusFile = "word2vec_corpus/bounwebcorpus.txt"
# newsCorpusFile = "word2vec_corpus/newscor.txt"
newsCorpusFile = "word2vec_corpus/newscor_digitless.txt"

outputFile = "word2vec.model"

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

bounCorpusSentences = LineSentence(bounCorpusFile)
newsCorpusSentences = LineSentence(newsCorpusFile)
unknownSentence = LineSentence("unk.txt")

model = Word2Vec(size=200, window=5, min_count=1, workers=multiprocessing.cpu_count(), iter = 1)

model.build_vocab(unknownSentence, update=False)
model.train(unknownSentence, total_examples=model.corpus_count, epochs=model.iter)

model.build_vocab(bounCorpusSentences, update=True)
model.train(bounCorpusSentences, total_examples=model.corpus_count, epochs=model.iter)

model.build_vocab(newsCorpusSentences, update=True)
model.train(newsCorpusSentences, total_examples=model.corpus_count, epochs=model.iter)

model.wv.save_word2vec_format(outputFile, binary=True)
