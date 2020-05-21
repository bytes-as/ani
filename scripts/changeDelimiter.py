import argparse

def parser():
	parser = argparse.ArgumentParser(description='convert delimiter for every row')
	parser.add_argument('input', help='input File path')
	parser.add_argument('output', help='output file path')
	parser.add_argument('--in_dlim', help='original delimter, default is tab', default='\t')
	parser.add_argument('--out_dlim', help='output delimiter, default is tab', default='\t')
	return parser.parse_args()

def main(args):
	readFile = open(args.input, 'r')
	writeFile = open(args.output, 'w')
	for line in readFile:
		tokens = line.rstrip().split(args.in_dlim)
		writeFile.write(args.out_dlim.join(tokens) + '\n')
	readFile.close()
	writeFile.close()
	print('output file written in the file:', args.output)

if __name__ == '__main__':
	main(parser())
