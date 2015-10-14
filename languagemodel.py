#! /usr/bin/python
# coding=utf8
 
__author__="Mohammad Sadegh Rasooli <rasooli@cs.columbia.edu>"
__date__ ="March, 2013"

import sys
import os
import codecs
from collections import defaultdict
import operator
import math


class LanguageModel:
	trigramTable=defaultdict()
	bigramTable=defaultdict()
	unigramTable=defaultdict()
	l1=0.0
	l2=0.0
	l3=0.0
	
	def __init__(self, lmfile):
		lines=codecs.open(lmfile,'r',encoding='utf-8').read().split('\n')
		self.smoothvalue = 0.00001
		for line in lines:
			splited=line.strip().split('\t')
			if splited[0]=='l1':
				self.l1=float(splited[1])
			if splited[0]=='l2':
				self.l2=float(splited[1])
			if splited[0]=='l3':
				self.l3=float(splited[1])
			if splited[0]=='t':
				words=splited[1].strip()
				prob=float(splited[2])
				if not self.trigramTable.has_key(words):
					self.trigramTable[words]=prob
			if splited[0]=='b':
				words=splited[1].strip()
				prob=float(splited[2])
				if not self.bigramTable.has_key(words):
					self.bigramTable[words]=prob
			if splited[0]=='u':
				words=splited[1].strip()
				prob=float(splited[2])
				if not self.unigramTable.has_key(words):
					self.unigramTable[words]= prob

	def score_arr(self, words):
		senprob=math.log(len(words))
		for i in range(2,len(words)):
			uniprob=0.0
			biprob=0.0
			triprob=0.0
			
			unigram=words[i]
			if self.unigramTable.has_key(unigram):
				uniprob=self.unigramTable[unigram]
			
			bigram=words[i-1]+' '+words[i]
			if self.bigramTable.has_key(bigram):
				biprob= self.bigramTable[bigram]
			
			trigram=words[i-2]+' '+words[i-1]+' '+words[i]
			if self.trigramTable.has_key(trigram):
				triprob=self.trigramTable[trigram]
			
			prob=self.l1*triprob+self.l2*biprob+self.l3*uniprob
			prob=self.smoothvalue+(1- self.smoothvalue)*prob
			senprob+=math.log(prob)

		return senprob

	def score(self, s):
		newS='<s> <s> '+s.strip()+' </s>'
		words=newS.split(' ')
		return self.score_arr(words)