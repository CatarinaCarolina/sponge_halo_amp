#!usr/env/bin python3

"""
Author: Catarina Loureiro

A script to extract CDS prot sequences from a gbk
"""

import os
import argparse
from Bio import SeqIO

def get_cmds():
	"""
	Capture args from the cmdline
	"""

	parser = argparse.ArgumentParser(description='')

	parser.add_argument('-g', '-gbk', dest='gbk', help='gbk file',\
		 required=True, metavar='<file>')
	parser.add_argument('-o', '-out', dest='out', help='fasta out file',\
		required=True, metavar='<file>')
	return parser.parse_args()



def extract_CDS(in_file, out_file):
	"""
	"""

	outfile = open(out_file, 'w')

	gbk_contents = SeqIO.parse(in_file, 'genbank')

	for record in gbk_contents:
		nodename = record.description
		for feature in record.features:
			if feature.type == 'CDS':
				locus_tag = feature.qualifiers['locus_tag'][0]
				seq = feature.qualifiers['translation'][0]
				
				fasta_entry = f'>{nodename}_{locus_tag}\n{seq}\n'
				outfile.write(fasta_entry)

	return None


if __name__ == '__main__':

	cmds = get_cmds()

	extract_CDS(cmds.gbk, cmds.out)
