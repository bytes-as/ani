import argparse
import os

def readDictionry(args):
	readFile = open(args.DICTIONARY, 'r')
	dictionary = {}
	for line in readFile:
		tokens = line.rstrip().split('\t')
		if tokens[0] not in dictionary:
			dictionary[tokens[0]] = tokens[1:]
		else :
			print('word already present {}'.format(tokens[0]))
	return dictionary

def createQueries(args, output):
	writeFile = open(output, 'w')
	dictionary = readDictionary(args)
	count = 0
	with open(args.INPUT, 'r') as readFile:
		for line in readFile:
			tokens = line.rstrip().split(args.DELIMITER)
			if args.LANGUAGE[0] == 'e':
				tokens[0] = tokens[0].split('/')[0]
			try:
				if int(tokens[1]) >= args.MIN and tokens[0] in dictionary:
					count += 1
					writeFile.write(tokens[0] + '\n')
			except: 
				# print('ignoring,', tokens)
				pass
	print('Totla number of tokens written : {}'.format(count))

def parser():
	parser = argparse.ArgumentParser(description='create queries for word vectors')
	parser.add_argument('INPUT', help='file path for the frequencies file')
	parser.add_argument('LANGUAGE', help='language for the file nameing')
	parser.add_argument('ROOT', help='Root output directory for saving file')
	parser.add_argument('MIN', help='Minimum frequency for cutting off', type=int)
	parser.add_argument('DICTIONARY', help='Path for the dicionary file (raw), default delimiter is tab')
	parser.add_argument('--DELIMITER', help='delimiter for the fequencie file\nDefault is TAB')
	parser.add_argument('--OVERWRITE', help='overwrite the output files', action='store_true')
	return parser.parse_args()

if __name__ == '__main__':
	args = parser()
	output = os.path.join(os.path.abspath(args.ROOT), args.LANGUAGE+ '_' + str(args.MIN) +'.queries')
	process = False
	print('asdfasdfasdfasdfasd ":::::::::::::::: ', output)
	if not os.path.isfile(output):
		process = True
	if process or args.OVERWRITE:
		createQueries(args, output)
		print('done creating queries file : {}'.format(output))
	else:
		print('Ignoring processing as the files are already present')
		print(output)

