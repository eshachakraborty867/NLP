import difflib
import sys


def compareAlignments(file1, file2):
		diff = difflib.ndiff(open(file1).readlines(), open(file2).readlines(1))
		print ''.join(diff),

if __name__== '__main__':
	compareAlignments(sys.argv[1], sys.argv[2])