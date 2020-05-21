import argparse
import os
import pickle

def loadPickle(file_path):
	print('reading from the file: {}'.format(file_path))
	with open(file_path, 'rb') as readFile:
		return pickle.load(readFile)

def writePickle(dictionary, file_path):
	with open(file_path, 'wb') as writeFile:
		pickle.dump(dictionary, file_path)
	print('file written : {}'.format(file_path))

def processGraph(args, freq):
	graph = open(args.INPUT, 'r')
	arr = []
	count = 0
	for line in graph:
		count += 1
		tokens = line.rstrip().split(args.IN_DELIMITER)
		if args.LANGUAGE[0] == 'e':
			tokens[0] = tokens[0].split('/')[0]
			tokens[1] = tokens[1].split('/')[1]
			tokens[2] = float(tokens[2])
			valid = False
			for word in tokens[:2]:
				if word not in freq: continue
				if freq[word] >= args.MIN: valid = True
			if valid: arr.append(tokens[:3])
		else: 
			valid = False
			for word in tokens[:2]:
				if word not in freq: continue
				if freq[word] >= args.MIN: valid=True
			if valid:
				try:
					arr.append([tokens[0], tokens[1], float(tokens[2])])
				except:
					print('ignoring line : {}'.format(tokens))
		if count % 10000000 == 0: print('{} lines have parsed'.format(count))
	return arr
			

def writeGraph(graph, file_path, delimiter, word2int=None, inted=False, weighted=False):
	writeFile = open(file_path, 'w')
	if not inted:
		for tokens in graph:
			if weighted : writeFile.write(delimiter.join([tokens[0], tokens[1], str(tokens[2])]) + '\n')
			else: writeFile.write(delimiter.join(tokens[:2]) + '\n')
	else:
		if word2int is None:
			raise Exception('word 2 int dictionary missing, check the argument passed')
		for tokens in graph:
			if tokens[0] not in word2int or tokens[1] not in word2int: continue
			if not weighted: writeFile.write(delimiter.join([str(word2int[tokens[0]]), str(word2int[tokens[1]])]) + '\n')
			else: writeFile.write(delimiter.join([str(word2int[tokens[0]]), str(word2int[tokens[1]]), str(tokens[2])]) + '\n')
	print('Graph written in file: {}'.format(file_path))

def main(args):
	try:
		#print(os.path.join(os.path.abspath(args.ROOT), args.LANGUAGE+'.freq    '))
		frequencies = loadPickle(os.path.join(os.path.abspath(args.ROOT), args.LANGUAGE+'.freq'))
		#int2word = loadPickle(os.path.join(os.path.abspath(args.ROOT), args.LANGUAGE+'.int2word'))
		word2int = loadPickle(os.path.join(os.path.abspath(args.ROOT), args.LANGUAGE+'.word2int'))
	except:
		raise Exception('dictionries pickle file not found\nProcess frequenmcy file first')
	#process = False
	#if args.OVERWRITE: process=True
	#if not os.path.isfile(os.path.join(os.path.abspath(args.ROOT), args.LANGUAGE+'_word.graph')) and \
	 #  not os.path.isfile(os.path.join(os.path.abspath(args.ROOT), args.LANGUAGE+'_int.graph')):
	#	process = True
	#if process:
	int_graph_path = os.path.join(os.path.abspath(args.ROOT), args.LANGUAGE+'_int_'+ str(args.MIN) + '.graph')
	word_graph_path = os.path.join(os.path.abspath(args.ROOT), args.LANGUAGE+'_word_' + str(args.MIN) + '.graph')
	arr = processGraph(args, frequencies)
	if not os.path.isfile(word_graph_path) or args.OVERWRITE:
		writeGraph(arr, word_graph_path, args.OUT_DELIMITER, inted=False)
	else: print('file found: {}'.format(int_graph_path))
	print('file completed...')
	if not os.path.isfile(int_graph_path) or args.OVERWRITE:
		writeGraph(arr, int_graph_path, args.OUT_DELIMITER, word2int=word2int, inted=True)
	else: print('file found: {}'.format(int_graph_path))
	#else:
	#	print('File Already in the output directory: {}\n{}'.format(word_graph_path, int_graph_path))

def parser():
	parser = argparse.ArgumentParser(description='Graph processin, converting the word to numbers and apply minimum freq ')
	parser.add_argument('INPUT', help='file path for the graph file')
	parser.add_argument('LANGUAGE', help='language for the file nameing')
	parser.add_argument('ROOT', help='Root output directory for saving file')
	parser.add_argument('MIN', help='minimum frequency for cutting graph', type=int)
	parser.add_argument('--IN_DELIMITER', default='\t', help='delimiter for the Graph file\nDefault is TAB')
	parser.add_argument('--OUT_DELIMITER', default='\t', help='delimiter for the output graph\nDefault is TAB')
	parser.add_argument('--WEIGHTED', help='enables saving weight in output graph file')
	parser.add_argument('--OVERWRITE', help='Overwrite output files', action='store_true', default=False)
	return parser.parse_args()

if __name__ == '__main__':
	args = parser()
	process = False
	if not os.path.isfile(os.path.join(os.path.abspath(args.ROOT), args.LANGUAGE+'_word_' + str(args.MIN) + '.graph')) or \
           not os.path.isfile(os.path.join(os.path.abspath(args.ROOT), args.LANGUAGE+'_int_' + str(args.MIN) + '.graph')):
		process = True	
	if args.OVERWRITE: process=True
	if process: 
		main(args)
	else:
		print('Files are already present in the output directory')
	print(os.path.join(os.path.abspath(args.ROOT), args.LANGUAGE+'_word.graph'))
	print(os.path.join(os.path.abspath(args.ROOT), args.LANGUAGE+'_int.graph'))
	print('done processing graph for language : {}'.format(args.LANGUAGE))
