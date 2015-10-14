#! /usr/bin/python
# coding=utf8
 
from compiler.ast import Break

__author__="Mohammad Sadegh Rasooli <rasooli@cs.columbia.edu>"
__date__ ="Feb, 2013"

import sys
import os
import codecs
from collections import defaultdict
import operator
import math


sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

progDir=os.path.dirname(sys.argv[0])
if not progDir.endswith('/') and progDir!='':
    progDir+='/'
currdir=os.getcwd()

trainFile=os.path.abspath(sys.argv[1])
devFile=os.path.abspath(sys.argv[2])
outputLMFile=os.path.abspath(sys.argv[3])

trigramtable=defaultdict()
allTri=0.0
alphaTri=0.0
bigramtable=defaultdict()
allBi=0.0
alphaBi=0.0
unigramtable=defaultdict()
allUni=0.0
alphaUni=0.0

lines=codecs.open(trainFile,'r',encoding='utf-8').read().split('\n')
count=0
for line in lines:
	count+=1
	if count%10000==0:
		print 'train',count
	sentence='<s> <s> '+line.strip()+' </s>'
	words=sentence.split(' ')
	for i in range(0,len(words)):
		allUni+=1
		if not unigramtable.has_key(words[i]):
			unigramtable[words[i]]=0.0
		unigramtable[words[i]]+=1.0
		if i<len(words)-1:
			allBi+=1
			if not bigramtable.has_key(words[i]+' '+words[i+1]):
				bigramtable[words[i]+' '+words[i+1]]=0.0
			bigramtable[words[i]+' '+words[i+1]]+=1.0
		if i<len(words)-2:
			allTri+=1
			if not trigramtable.has_key(words[i]+' '+words[i+1]+' '+words[i+2]):
				trigramtable[words[i]+' '+words[i+1]+' '+words[i+2]]=0.0
			trigramtable[words[i]+' '+words[i+1]+' '+words[i+2]]+=1.0
print 'trigram'
for tri in trigramtable.keys():
	bigram=tri.split(' ')[0]+' '+tri.split(' ')[1]
	trigramtable[tri]/=bigramtable[bigram]
	#print 'trigram\t'+tri+'\t'+str(trigramtable[tri])
print 'bigram'
for bi in bigramtable.keys():
	unigram=bi.split(' ')[0]
	bigramtable[bi]/=unigramtable[unigram]
	#print 'bigram\t'+bi+'\t'+str(bigramtable[bi])
print 'unigram'
for uni in unigramtable.keys():
	unigramtable[uni]/=allUni
	#print 'unigram\t'+uni+'\t'+str(unigramtable[uni])


devTrigramtable=defaultdict()
lines=codecs.open(devFile,'r',encoding='utf-8').read().split('\n')
count=0
for line in lines:
	count+=1
	if count%1000==0:
		print 'dev',count
	sentence='<s> <s> '+line.strip()+' </s>'
	words=sentence.split(' ')
	for i in range(0,len(words)):
		if i<len(words)-2:
			if not devTrigramtable.has_key(words[i]+' '+words[i+1]+' '+words[i+2]):
				devTrigramtable[words[i]+' '+words[i+1]+' '+words[i+2]]=0.0
			devTrigramtable[words[i]+' '+words[i+1]+' '+words[i+2]]+=1.0

l1=0.4
l2=0.3
l3=0.3
l4=0
smooth=0.000001
for i in range(1,20):
	c1=0.0
	c2=0.0
	c3=0.0
	c4=0.0
	print 'learning',i
	for tri in devTrigramtable.keys():
		uniprob=0.0
		biprob=0.0
		triprob=0.0
		bi=tri.split(' ')[1]+' '+tri.split(' ')[2]
		uni=tri.split(' ')[2]
		if trigramtable.has_key(tri):
			triprob=trigramtable[tri]
		if bigramtable.has_key(bi):
			biprob=bigramtable[bi]
		if unigramtable.has_key(uni):
			uniprob=unigramtable[uni]
		cprime=devTrigramtable[tri]
		denom=l4+l3*uniprob+l2*biprob+l1*triprob+smooth
		c1+=(smooth/3+ cprime*l1*triprob)/denom
		c2+=(smooth/3+ cprime*l2*biprob)/denom
		c3+=(smooth/3+ cprime*l3*uniprob)/denom
		c4+=cprime*l4/denom
	denom=c1+c2+c3+c4
	l1=c1/denom
	l2=c2/denom
	l3=c3/denom
	l4=c4/denom
	print l1,l2,l3,l4


outopen=codecs.open(outputLMFile,'w',encoding='utf-8')
content=''
outopen.write('l1\t'+str(l1)+'\n')
outopen.write('l2\t'+str(l2)+'\n')
outopen.write('l3\t'+str(l3)+'\n')
outopen.write('l4\t'+str(l4)+'\n')
outopen.write('allUni\t'+str(allUni)+'\n')
outopen.write('allBi\t'+str(allBi)+'\n')
outopen.write('allTri\t'+str(allTri)+'\n')
print 'trigram'
for tri in trigramtable.keys():
	outopen.write(  't\t'+tri+'\t'+str(trigramtable[tri])+'\n')
print 'bigrams'
for bi in bigramtable.keys():
	outopen.write(  'b\t'+bi+'\t'+str(bigramtable[bi])+'\n')
print 'unigrams'
for uni in unigramtable.keys():
	outopen.write(  'u\t'+uni+'\t'+str(unigramtable[uni])+'\n')


