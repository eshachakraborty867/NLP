import sys
import time
import math
from collections import defaultdict

#creating global dictionaries for the 't' and 'q' parameters
t=defaultdict()
q=defaultdict()

# function "Count_for_t(corpus_en, corpus_de)" creates a dictionary for t 
# t will be indexed by English word (en_word) and German word (de_word)
def Count_for_t(corpus_en, corpus_de):
	t['NULL'] = defaultdict(float) 

	for en_line in open(corpus_en):
		en_words = en_line.strip().split(" ")
		for en_word in en_words:			#create a t parameter for every unique en_word
			if en_word not in t:
				t[en_word] = defaultdict(float)

	for en_line, de_line in zip(open(corpus_en), open(corpus_de)):
		en_words = en_line.strip().split(" ")
		de_words = de_line.strip().split(" ")
		for en_word in en_words:
			for de_word in de_words:      # associate possible de_words
				t[en_word][de_word]+=1
		for de_word in de_words:
			t['NULL'][de_word]+=1

# function "Count_for_q(corpus_en, corpus_de)" creates a dictionary for q
# t will be indexed by (i,l,m) and j
def Count_for_q(corpus_en, corpus_de):	
	for en_line, de_line in zip(open(corpus_en), open(corpus_de)):
		en_words = en_line.strip().split(" ")
		de_words = de_line.strip().split(" ")
		l=len(en_words)
		m=len(de_words)
		for i in xrange(m):
			if (i,l,m) not in q:
				q[(i,l,m)] = defaultdict(float)

	for en_line, de_line in zip(open(corpus_en), open(corpus_de)):
		en_words = en_line.strip().split(" ")
		de_words = de_line.strip().split(" ")
		l=len(en_words)
		m=len(de_words)
		for i in xrange(m):
			for j in xrange(l+1):
				q[(i,l,m)][j] = 1.0

"""def Print_t():
	fp = open("output/Tparameters","w")
	for e in t:
		for f in t[e]:
			fp.write(e)
			fp.write(" ")
			fp.write(f)
			fp.write(" ")
			fp.write(str(t[e][f]))
			fp.write("\n")
	fp.close()"""

"""def Print_q():
	fp = open("output/Qparameters","w")
	for (i,l,m) in q:
		for j in q[(i,l,m)]:
			fp.write(str(i))
			fp.write(" ")
			fp.write(str(l))
			fp.write(" ")
			fp.write(str(m))
			fp.write(" ")
			fp.write(str(j))
			fp.write(" ")
			fp.write(str(q[(i,l,m)][j]))
			fp.write("\n")
	fp.close()"""

def Init_t():
	print "Initializing the t paramters..."
	for e in t:
		ne = len(t[e])
		for f in t[e]:
			t[e][f] = float(1.0/float(ne))

def Init_q():
	print "Initializing the q paramters..."
	for (i,l,m) in q:
		ne = len(q[(i,l,m)])   # len(q[(i,l,m)]) is l+1
		for j in q[(i,l,m)]:
			q[(i,l,m)][j] = 1.0/ne

def EM_IBM1(corpus_en, corpus_de):
	print "Implementing IBM Model 1..."
	number_iteration=5
	#Print_t()
	for s in xrange(number_iteration):
		print (("\tIteration: %d")%(s+1))
		c = defaultdict(float)
		#Print_t()
		for en_line, de_line in zip(open(corpus_en), open(corpus_de)):
			en_words = en_line.strip().split(" ")
			en_words = ['NULL'] + en_words			#'NULL' will be the beginning of every English sentence
			de_words = de_line.strip().split(" ")
			#calculate the denominator of delta
			for de_word in de_words:
				temp=0.0
				for en_word in en_words:
					temp += t[en_word][de_word]	
				for en_word in en_words:
					delta = t[en_word][de_word]/temp
					c[(en_word,de_word)] += delta
					c[en_word] += delta
		for en_word in t:
			for de_word in t[en_word]:
				t[en_word][de_word] = c[(en_word, de_word)]/c[en_word]

	
	fp=open("output/log_devwords.txt","w")
	print "Operating on devwords.txt..."
	for line in open("devwords.txt"):
		word = line.strip()
		
		fp.write(word)
		#fp.write("\n")
		#fp.write('------------')
		fp.write("\n")
		fp.write("[")
		if word in t:
			temp = defaultdict(float)
			for f in t[word]:
				temp[f] = t[word][f]
			cnt=0
			for w in sorted(temp, key=temp.get, reverse=True):
				#fp.write(("('%s', %f), ") %(w,temp[w]))
				if cnt == 9:
					fp.write(("('%s', %f)") %(w,temp[w]))
					break
				else:
					fp.write(("('%s', %f), ") %(w,temp[w]))
				cnt+=1
				#if cnt==10:
				#	break
		fp.write("]")
		fp.write("\n\n")
	fp.close()

def CalculateAlignmentsIBM1(corpus_en, corpus_de):
	print "Calculating alignments for IBM model 1..."
	output = open("output/alignments4IBM1.txt","w")
	for en_line, de_line, cnt in zip(open(corpus_en), open(corpus_de), xrange(20)):
		a=[]
		en_words = en_line.strip().split(" ")
		en_words = ['NULL'] + en_words
		de_words = de_line.strip().split(" ")
		i=1
		for de_word in de_words:
			j=0
			temp=-1
			aj=j
			for en_word in en_words:
				if t[en_word][de_word]>temp:
					temp=t[en_word][de_word]
					aj=j
				j+=1
			a.append(aj)
			i+=1
		output.write(en_line)
		output.write(de_line)
		output.write(str(a))
		output.write("\n")
		output.write("\n")
	output.close()

def EM_IBM2(corpus_en, corpus_de):
	print "Implementing IBM Model 2..."
	number_iteration=5
	for s in xrange(number_iteration):
		print (("\tIteration: %d")%(s+1))
		c = defaultdict(float)
		for en_line, de_line in zip(open(corpus_en), open(corpus_de)):
			en_words = en_line.strip().split(" ")
			en_words = ['NULL'] + en_words				#already incorporated NULL
			de_words = de_line.strip().split(" ")
			m=len(de_words)
			l=len(en_words) 							#this actually is l+1 

			#calculate the denominator of delta
			for de_word,i in zip(de_words, xrange(m)):
				temp=0.0
				for en_word,j in zip(en_words, xrange(l)):
					#print en_word
					#print j
					a = t[en_word][de_word] * q[(i,l-1,m)][j]
					temp = temp + a

				for en_word,j in zip(en_words, xrange(l)):
					delta = (t[en_word][de_word]*q[(i,l-1,m)][j])/temp
					c[(en_word,de_word)] += delta
					c[en_word] += delta
					c[(j,i,l-1,m)] += delta
					c[(i,l-1,m)] += delta
		for en_word in t:
			for de_word in t[en_word]:
				t[en_word][de_word] = c[(en_word, de_word)]/c[en_word]
		for (i,l,m) in q:
			for j in q[(i,l,m)]:
				q[(i,l,m)][j] = c[(j,i,l,m)]/c[(i,l,m)]

def CalculateAlignmentsIBM2(corpus_en, corpus_de):
	print "Calculating alignments for IBM model 2..."
	output = open("output/alignments4IBM2.txt","w")
	for en_line, de_line, cnt in zip(open(corpus_en), open(corpus_de), xrange(20)):
		a=[]
		en_words = en_line.strip().split(" ")
		en_words = ['NULL'] + en_words
		de_words = de_line.strip().split(" ")
		m=len(de_words)
		l=len(en_words)
		i=1
		for de_word in de_words:
			j=0
			temp=-1
			aj=j
			for en_word in en_words:
				if (t[en_word][de_word]*q[(i-1,l-1,m)][j])>temp:
					temp=t[en_word][de_word]*q[(i-1,l-1,m)][j]
					aj=j
				j+=1
			a.append(aj)
			i+=1
		output.write(en_line)
		output.write(de_line)
		output.write(str(a))
		output.write("\n")
		output.write("\n")
	output.close()

def scoreforClaudia(de_words, en_words):
	a=[]
	en_words = ['NULL'] + en_words
	m=len(de_words)
	l=len(en_words)
	i=1
	for de_word in de_words:
		j=0
		temp=-1
		aj=j
		for en_word in en_words:
			if (t[en_word][de_word]*q[(i-1,l-1,m)][j])>temp:
				temp=t[en_word][de_word]*q[(i-1,l-1,m)][j]
				aj=j
			j+=1
		a.append(aj)
		i+=1
	temp_sum=0
	for i in xrange(len(a)):
		if t[en_words[a[i]]][de_words[i]]*q[(i,l-1,m)][a[i]] > 0:
			temp_sum += math.log(t[en_words[a[i]]][de_words[i]]*q[(i,l-1,m)][a[i]])
		else:
			temp_sum+=-999
	return temp_sum

def forClaudiaClumsy(original_de, scrambled_en):
	print "Working now for Claudia Clumsy..."
	output = open("output/unscrambled.en", "w")

	#account for unseen values of t 
	for en_line in open(scrambled_en):
		en_words = en_line.strip().split(" ")
		for en_word in en_words:
			if en_word not in t:
				t[en_word] = defaultdict(float)

	#account for unseen values of q
	for en_line in open(scrambled_en):
		en_words = en_line.strip().split(" ")
		l=len(en_words)

		for de_line in open(original_de):
			de_words = de_line.strip().split(" ")
			m=len(de_words)
			for i in xrange(m):
				if (i,l,m) not in q:
					q[(i,l,m)] = defaultdict(float)


	for de_line in open(original_de):
		de_words = de_line.strip().split(" ")
		temp=-99999
		for en_line in open(scrambled_en):
			en_words = en_line.strip().split(" ")
			score = scoreforClaudia(de_words, en_words)
			if score>temp:
				temp=score
				line = en_line
		output.write(line)
	output.close()




if __name__ == '__main__':
	Count_for_t("corpus.en", "corpus.de")
	Init_t()

	start_time = time.time()
	EM_IBM1("corpus.en", "corpus.de")
	print "\nTime (in minutes) to run 5 iterations of the EM algorith for IBM model 1:-"
	print (time.time() - start_time)/60

	CalculateAlignmentsIBM1("corpus.en", "corpus.de")

	Count_for_q("corpus.en", "corpus.de")
	Init_q()

	start_time = time.time()
	EM_IBM2("corpus.en", "corpus.de")
	print "\nTime (in minutes) to run 5 iterations of the EM algorith for IBM model 2:-"
	print (time.time() - start_time)/60

	CalculateAlignmentsIBM2("corpus.en", "corpus.de")

	start_time = time.time()
	forClaudiaClumsy("original.de", "scrambled.en")
	print "\nTime (in minutes) to generate unscrambled data for Claudia Clumsy"
	print (time.time() - start_time)/60
	
	#Print_t()
	#Print_q()