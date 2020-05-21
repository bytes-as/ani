import os
import pickle
import argparse

def parser():
	parser = argparse.ArgumentParser(description='Convert walks from int to word or word to int depending on the the dicitonar provided')
	parser.add_argument('INPUT', help='input file path of the walks')
	parser.add_argument('DICT', help='Dictionary file path for conversion')
	parser.add_argument('OUTPUT', help='Output file path for converted walks')
	parser.add_argument('--IN_DELIMITER', help='delimiter for input walks file. Default is tab', default='\t')
	parser.add_argument('--OUT_DELIMITER', help='delimiter for output walks file. Default is same as inut delimiter', default=None)
	parser.add_argument('--OVERWRITE', help='Enables overwriting the output file', action='store_true', default=False)
	args = parser.parse_args()
	if args.OUT_DELIMITER is None:
		args.OUT_DELIMITER = args.IN_DELIMITER
	return args

def main(args):
	walks = open(args.INPUT, 'r')
	output = open(args.OUTPUT, 'w')
	dictionary = pickle.load(open(args.DICT, 'rb'))

	count = 0
	for walk in walks:
		count += 1
		tokens = walk.rstrip().split(args.IN_DELIMITER)
		try:
			output.write(args.OUT_DELIMITER.join([str(dictionary[x]) for x in tokens]))
			output.write('\n')
		except:
			output.write(args.OUT_DELIMITER.join([dictionary[int(x)] for x in tokens]))
			output.write('\n')
		if count % 10000000 == 0:
			print('{} Walks coverted and written'.format(count))
	walks.close()
	output.close()

if __name__ == '__main__':
	args = parser()
	if os.path.isfile(args.OUTPUT) and not args.OVERWRITE:
		print('File found: {}'.format(args.OUTPUT))
		print('Mind the OVERWRITE flag if you want to overwrite')
	main(args)
