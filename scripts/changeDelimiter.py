import argparse
import pickle
import random

def parser():
	parser = argparse.ArgumentParser(description='convert delimiter for every row')
	parser.add_argument('input', help='input File path')
	parser.add_argument('output', help='output directory')
	parser.add_argument('MIN1', type=int, help='Minimum frequency for the first language')
	parser.add_argument('MIN2', type=int, help='Minimum frequency for the second language')
	parser.add_argument('--in_dlim', help='original delimter, default is tab', default='\t')
	parser.add_argument('--out_dlim', help='output delimiter, default is tab', default='\t')
	return parser.parse_args()

def loadPickleFile(file_path):
	f = open(file_path, 'rb')
	return pickle.load(f)

def main(args):
	print('reading file :', args.input)
	readFile = open(args.input, 'r')
	output_path = args.output + '/train_dict_' + str(args.MIN1) + '_' + str(args.MIN2) + '.txt'
	print(' -----> writing file in :', output_path)
	writeFile = open(output_path, 'w')
	freq1 = loadPickleFile(args.output + '/english.freq')
	freq2 = loadPickleFile(args.output + '/hindi.freq')
	final_dictionary = []
	english = open(args.output + '/english_' + str(args.MIN1) + '.queries', 'w')
	hindi = open(args.output + '/hindi_' + str(args.MIN2) + '.queries', 'w')
	for line in readFile:
		tokens = line.rstrip().split(args.in_dlim)
		if tokens[0] not in freq1:
			continue
		if tokens[1] not in freq2:
			continue
		if freq1[tokens[0]] >= args.MIN1 and freq2[tokens[1]] >= args.MIN2:
			english.write(tokens[0] + '\n')
			for token in tokens[1:]:
				hindi.write(token + '\n')
			final_dictionary.append(tokens)
	readFile.close()
	random.shuffle(final_dictionary)
	for tokens in final_dictionary[:int(0.8 * len(final_dictionary))]:	
		writeFile.write(args.out_dlim.join(tokens) + '\n')
	writeFile.close()
	output_path = args.output + '/test_dict_' + str(args.MIN1) + '_' + str(args.MIN2) + '.txt'
	writeFile = open(output_path, 'w')
	for tokens in final_dictionary[int(0.8 * len(final_dictionary)):]:
		writeFile.write(args.out_dlim.join(tokens) + '\n')
	writeFile.close()
	print('---------------- >>>> output file written in the file:', output_path)
	english = open(args.output + '/english_' + str(args.MIN1) + '.queries', 'w')
	hindi = open(args.output + '/hindi_' + str(args.MIN2) + '.queries', 'w')

if __name__ == '__main__':
	print('===========> creating dictionry ')
	args = parser()
	print(args)
	main(args)
