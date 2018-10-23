#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from gensim.corpora import Dictionary

dictionary = Dictionary() 

#file = open("testfile.txt","w") 

with open('reyyan.train.txt', encoding="utf-8") as fp:
    for line in fp:
        
        """linex = line.replace('%', ' % ')
        linex = linex.replace('.', ' . ')
        linex = linex.replace('\'', ' DICT_APOSTROPHE ')
        linex = linex.replace('’', ' DICT_APOSTROPHE ')
        linex = linex.replace('?', ' ? ')"""
        tokens = line.split()
        #tokens = ["DICT_NUMBER" if token.isdigit() else token for token in tokens]

        dictionary.doc2bow(tokens, allow_update=True);

with open("dictionary.txt", "w", encoding="utf-8") as f:
	id = 0
	for s in dictionary.token2id:
		f.write(str(s) + " " + str(id) + "\n")
		id += 1
