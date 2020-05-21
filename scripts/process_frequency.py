import argparse
import os
import pickle

def loadPickle(file_path):
	print('reading from the file: {}'.format(file_path))
	with open(file_path, 'rb') as readFile:
		return pickle.load(readFile)

def writePickle(dictionary, file_path):
	with open(file_path, 'wb') as writeFile:
		pickle.dump(dictionary, writeFile)
	print('file written : {}'.format(file_path))

def processFrequencies(args):
	frequencies = {}
	int2word = {}
	word2int = {}
	count = 1
	with open(args.INPUT, 'r') as readFile:
		for line in readFile:
			tokens = line.rstrip().split(args.DELIMITER)
			if args.LANGUAGE[0] == 'e':
				tokens[0] = tokens[0].split('/')[0]
			
			try:
				frequencies[tokens[0]] = int(tokens[1])
			except:
				print('Ignoring line with tokens: {}'.format(tokens))
				continue
			if tokens[0] in word2int: continue
			word2int[tokens[0]] = count
			int2word[count] = tokens[0]
			count += 1
			
	return frequencies, int2word, word2int

def parser():
	parser = argparse.ArgumentParser(description='create int2word and word2int and frequencies pickle files')
	parser.add_argument('INPUT', help='file path for the frequencies file')
	parser.add_argument('LANGUAGE', help='language for the file nameing')
	parser.add_argument('ROOT', help='Root output directory for saving file')
	parser.add_argument('--DELIMITER', help='delimiter for the fequencie file\nDefault is TAB')
	parser.add_argument('--OVERWRITE', help='overwrite the output files', action='store_true')
	return parser.parse_args()

if __name__ == '__main__':
	args = parser()
	freq_path = os.path.join(os.path.abspath(args.ROOT), args.LANGUAGE+'.freq')
	word2int_path = os.path.join(os.path.abspath(args.ROOT), args.LANGUAGE+'.word2int')
	int2word_path = os.path.join(os.path.abspath(args.ROOT), args.LANGUAGE+'.int2word')
	process = False
	if not os.path.isfile(freq_path):
		process = True
	if not os.path.isfile(word2int_path):
		process = True
	if not os.path.isfile(int2word_path):
		process = True
	if process or args.OVERWRITE:
		freq, int2word, word2int = processFrequencies(args)
		writePickle(freq, freq_path)
		writePickle(word2int, word2int_path)
		writePickle(int2word, int2word_path)
		print('done processing frequencie file for language : {}'.format(args.LANGUAGE))
	else:
		print('Ignoring processing as the files are already present')
		print(freq_path)
		print(word2int_path)
		print(int2word_path)
