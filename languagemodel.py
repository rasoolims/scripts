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
	fivegramTable=defaultdict(float)
	fourgramTable=defaultdict(float)
	trigramTable=defaultdict(float)
	bigramTable=defaultdict(float)
	unigramTable=defaultdict(float)
	l1=0.0
	l2=0.0
	l3=0.0
	l4=0.0
	l5=0.0
	
	def __init__(self, lmfile):
		lines=codecs.open(lmfile,'r',encoding='utf-8').read().split('\n')
		self.smoothvalue = 0.00001
		for line in lines:
			splited=line.strip().split('\t')
			if splited[0]=='l1':
				self.l1=float(splited[1])
			elif splited[0]=='l2':
				self.l2=float(splited[1])
			elif splited[0]=='l3':
				self.l3=float(splited[1])
			elif splited[0]=='l4':
				self.l4=float(splited[1])
			elif splited[0]=='l5':
				self.l5=float(splited[1])
			elif splited[0]=='fv':
				words=splited[1].strip()
				prob=float(splited[2])
				self.fivegramTable[words]=prob
			elif splited[0]=='fr':
				words=splited[1].strip()
				prob=float(splited[2])
				self.fourgramTable[words]=prob
			elif splited[0]=='t':
				words=splited[1].strip()
				prob=float(splited[2])
				self.trigramTable[words]=prob
			elif splited[0]=='b':
				words=splited[1].strip()
				prob=float(splited[2])
				self.bigramTable[words]=prob
			elif splited[0]=='u':
				words=splited[1].strip()
				prob=float(splited[2])
				self.unigramTable[words]= prob

	def score_arr(self, words):
		senprob=math.log(len(words))
		for i in range(4,len(words)):
			unigram=words[i]
			uniprob=self.unigramTable[unigram]
			
			bigram=words[i-1]+' '+words[i]
			biprob= self.bigramTable[bigram]
			
			trigram=words[i-2]+' '+words[i-1]+' '+words[i]
			triprob=self.trigramTable[trigram]

			fourgram=words[i-3]+' '+words[i-2]+' '+words[i-1]+' '+words[i]
			fourprob=self.fourgramTable[fourgram]

			fivegram=words[i-4]+' '+words[i-3]+' '+words[i-2]+' '+words[i-1]+' '+words[i]
			fiveprob=self.fivegramTable[fivegram]
			
			prob=self.l1*fiveprob+self.l2*fourprob+self.l3*triprob+self.l4*biprob+self.l5*uniprob
			prob=self.smoothvalue+(1- self.smoothvalue)*prob
			senprob+=math.log(prob)

		return senprob

	def score(self, s):
		newS='<s> <s> '+s.strip()+' </s>'
		words=newS.split(' ')
		return self.score_arr(words)