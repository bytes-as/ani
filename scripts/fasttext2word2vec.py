import sys
import os

def main():
	count = 0
	lines = []
	with open(sys.argv[1], 'r') as readFile:
		for line in readFile:
			lines.append(line)
			count += 1

	with open(sys.argv[1], 'w') as writeFile:
		writeFile.write(str(count) + ' 100\n')
		for line in lines:
			writeFile.write(line)

if __name__ == '__main__':
	main()
