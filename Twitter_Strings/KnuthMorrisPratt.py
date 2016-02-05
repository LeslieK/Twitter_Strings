import numpy as np
import StringUtils

class DFA(object):
	def __init__(self, pat):
		self.pat = pat

		# build dfa from pattern
		self.M = len(self.pat)
		self.dfa = np.zeros((StringUtils.R, self.M+1))
		# initialize dfa construction
		self.dfa[ord(self.pat[0])][0] = 1
		# X refers to state after matching pat on text[1:] (shifted to the right 1 character)
		X = 0
		for j in range(1, self.M):
			for c in range(StringUtils.R):
				# on a mismatch: set the state transitions from j to be identical to those from X
				self.dfa[c][j] = self.dfa[c][X]
			# on a match: set state transition from j to j + 1
			self.dfa[ord(self.pat[j])][j] = j + 1
			# update state X
			X = self.dfa[ord(self.pat[j])][X]
		# needed to find next match after a match has been found
		for c in range(StringUtils.R):
			self.dfa[c][self.M] = self.dfa[c][X]

	def next(self, text_i, patindex_j):
		'''return next state given curr_state and pattern index

		ex: next("B", 3) => 4
		next("B", 5) => 0

		'''
		return self.dfa[ord(text_i)][patindex_j]

	def patlen(self):
		return self.M


class KMP(object):
	def __init__(self, pat):
		# build dfa from pattern
		self.dfa = DFA(pat)
		self.M = len(pat)
		self.count = 0

	def search(self, txt):
		'''search for pattern in text'''
		
		N = len(txt)
		i = 0 # indext into txt
		j = 0 # index into pattern
		# compare txt[i] and pat[j]
		for i in range(N):
			# read each char txt[i] in text
			if j < self.M:
				# move through dfa until reach end of pattern
				# go to next state given curr state and txt[i]
				j = self.dfa.next(txt[i], j)
				self.count += 1
			else:
				# found match
				#print 'match', i - self.Ms
				return i - self.M # index in text at start-of-pattern 		
		# check for last match
		if j == self.M:
			#print 'match', i, i - (self.M - 1)
			return i - self.M + 1
		return 'no match', N # length of text

	def findall(self, txt, overlap=True):
		'''return offset of all occurrences of pattern in text'''
		results = []
		N = len(txt)
		i = 0 # indext into txt
		j = 0 # index into pattern
		# compare txt[i] and pat[j]
		while True:
			for i in range(N):
				# read each char txt[i] in text
				if j < self.M:
					# move through dfa until reach end of pattern
					# go to next state given curr state and txt[i]
					j = self.dfa.next(txt[i], j)
				else:
					# found match
					results.append(i - self.M)
					# reset index into pattern and continue to match
					if overlap:
						j = self.dfa.next(txt[i], j)
					else:
						j = 0
			# check for last match
			if j == self.M:
				#print 'match', i, i - (self.M - 1)
				results.append(i - self.M + 1) 
			break
		#print 'matches: {}'.format(len(results)) # number of matches
		return results


	def stream(self, c, pat_index):
		'''scans character from streaming input'''
		pat_index = self.dfa.next(c, pat_index)
		return pat_index







		
		
		
		

