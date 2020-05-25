import os
import pickle
import argparse
import random

def parser():
	parser = argparse.ArgumentParser(description='Merge walks')
	parser.add_argument('INPUT1', help='input file path of the first walks')
	parser.add_argument('INPUT2', help='input file path of the second walks')
	parser.add_argument('DICT', help='Dictionary file path for translation')
	parser.add_argument('OUTPUT', help='Output file path for converted walks')
	parser.add_argument('--WALKS_DELIMITER', help='delimiter for input walks file. Default is tab', default='\t')
	parser.add_argument('--OUTPUT_DELIMITER', help='delimiter for the output merged walks', default='\t')
	parser.add_argument('--DICT_DELIMITER', help='delimiter for output walks file. Default is tab', default='\t')
	parser.add_argument('--OVERWRITE', help='Enables overwriting the output file', action='store_true', default=False)
	parser.add_argument('--CHANCE', help='probability of not writing the sentence in final file', type=float, default=0.8)
	return parser.parse_args()

def main(args):
	file1 = open(args.INPUT1, 'r')
	file2 = open(args.INPUT2, 'r')
	translation1 = {}
	translation2 = {}
	with open(args.DICT, 'r') as readFile:
		for line in readFile:
			tokens = line.rstrip().split(args.DICT_DELIMITER)
			translation1[tokens[0]] = tokens[1:]
			for word in tokens[1:]:
				if word not in translation2:
					translation2[word] = []
			for word in tokens[1:]:
				translation2[word].append(tokens[0])
	walks1 = []
	for line in file1:
		tokens = line.rstrip().split(args.WALKS_DELIMITER)
		walks1.append(tokens)
	print('number of walks read: {}'.format(len(walks1)))
	walks2 = []
	for line in file2:
		tokens = line.rstrip().split(args.WALKS_DELIMITER)
		walks2.append(tokens)
	print('walks2[0]:', walks2[0])
	print('number of walks read: {}'.format(len(walks2)))
	invert1 = {}
	invert2 = {}
	for i, walk in enumerate(walks1):
		for token in walk:
			if token not in invert1: invert1[token] = set()
			invert1[token].add(i)
	for j, walk in enumerate(walks2):
		for token in walk:
			if token not in invert2: invert2[token] = set()
			invert2[token].add(j)
	count = 0
	output = open(args.OUTPUT, 'w')
	for token in invert1:
		if token not in translation1: continue
		for walk_index1 in invert1[token]:
			for translated_word in translation1[token]:
				if translated_word not in invert2: continue
				if random.random() > args.CHANCE: continue
				for walk_index2 in invert2[translated_word]:
					count += 1
					output.write(args.OUTPUT_DELIMITER.join(walks1[walk_index1]))
					output.write(args.OUTPUT_DELIMITER)
					output.write(args.OUTPUT_DELIMITER.join(walks2[walk_index2]))
					output.write('\n')
					if count % 100000000 == 0 :print('{}/{} walks written successfully'.format(count, len(walks1)*len(walks2)))
	print('Merged completed in file:  {}'.format(args.OUTPUT))

if __name__ == '__main__':
	args = parser()
	if os.path.isfile(args.OUTPUT) and not args.OVERWRITE:
		print('File found: {}'.format(args.OUTPUT))
		print('Mind the OVERWRITE flag if you want to overwrite')
	else: main(args)
