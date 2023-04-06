#!usr/env/bin python3

"""
Author: Catarina Loureiro

A script to extract aa seqs in one fasta from a set of gbks
"""

import os
import argparse
from Bio import SeqIO

def get_cmds():
	"""
	Capture args from the cmdline
	"""

	parser = argparse.ArgumentParser(description='')

	parser.add_argument('-g', '-gbks', dest='gbks', help='folder with input gbks',\
		required=True, metavar='<path>')

	parser.add_argument('-o', '-out', dest='out', help='aa fasta',\
		 required=True, metavar='<file>')

#	parser.add_argument('-', '-', dest='', help='', required=True, metavar='<>')

	return parser.parse_args()


def get_gbk_files(indir):
	"""
	Get gbk files from indir incl their paths

	indir: str, folder path
	"""

	try:
		for dirpath, dirnames, files in os.walk(indir):
			for f in files:
				bgc_name = f.split('/')[-1]
				yield(os.path.join(dirpath, f))
	except:
		pass



def extract_seq(filepath, fasta_obj):
	"""
	extract gene based on sec met domain query

	file_path, outdir: str, path
	secmetdomain: str
	fasta_obj: str, path
	"""

	infile = filepath.split('/')[-1]
	header = infile.split('.gb')[0]

	gbkcontents = SeqIO.parse(filepath, "genbank")
	for record in gbkcontents:
		sequence = record.seq
		name = f'>{header}'
		#print(f'{name}\n{sequence}')
		fasta_obj.write(f'{name}\n{sequence}\n')

	return None


if __name__ == '__main__':

	cmds = get_cmds()
	fileobj = open(cmds.out,'w')

	for filepath in get_gbk_files(cmds.gbks):
		print(filepath)
		extract_seq(filepath, fileobj)

	fileobj.close()
