R = 256 # number of character values in alphabet
CUTOFF = 0 # length of string when insertion sort is used (instead of some other string sorting method)

def exch(a_sequence, i, j):
	'''exchange values a_sequence[i] and a_sequence[j]'''
	swap = a_sequence[i]
	a_sequence[i] = a_sequence[j]
	a_sequence[j] = swap
	return a_sequence

# def exch(alist, i, j):
# 	'''exchange alist[i] and alist[j]'''
# 	swap = alist[i].offset
# 	alist[i].offset = alist[j].offset
# 	alist[j].offset = swap
# 	return alist

def lcp(text1, text2):
	'''return longest common prefix'''
	length = min(len(text1), len(text2))
	for i in range(length):
		if text1[i] != text2[i]:
			return i
	return length

def compareTo(string1, string2):
	'''compare string1 to string2'''
	if string1 < string2:
		return -1
	elif string1 > string2:
		return 1
	else:
		return 0

def insertion(a, lo, hi, d):
	'''sort from a[lo] to a[hi], starting from the dth character'''
	for i in range(lo, hi + 1):
		# a[i] is a string
		for j in range(i, lo, -1):
			# j is an index into the string a[i]
			if less(a[j], a[j - 1], d):
				exch(a, j, j - 1)

def less(string1, string2, d):
	return string1[d:] < string2[d:]


def charsfromfile(f):
	'''a generator for reading a buffered file'''
	while True:
		a = array.array('c')
		a.fromstring(f.read(1000))
		if not a:
			break
		for x in a:
			yield x
