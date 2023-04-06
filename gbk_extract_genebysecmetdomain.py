#!usr/env/bin python3

"""
Author: Catarina Loureiro

A script to extract aa fasta for specific genes by sec_met_domain from AS6 output set of gbks
"""

import os
import argparse
from Bio import SeqIO

def get_cmds():
	"""
	Capture args from the cmdline
	"""

	parser = argparse.ArgumentParser(description='')

	parser.add_argument('-d', '-domain', dest='domain', help='sec_met_domain',\
		 required=True, metavar='<str>')

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



def extract_domain(filepath, secmetdomain, fasta_obj):
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
		for index, feature in enumerate(record.features):
			if feature.type == 'CDS' and 'sec_met_domain' in feature.qualifiers and secmetdomain in '_'.join(feature.qualifiers['sec_met_domain']):

				location = str(feature.location)
				start = location.split(':')[0][1:]
				end = location.split(':')[1].split(']')[0]

				locus_tag = feature.qualifiers['locus_tag'][0].split('_')[1]

				sequence = feature.qualifiers['translation'][0]
				name = f'>{header}_{query}_{locus_tag}_{start}_{end}'

				fasta_obj.write(f'{name}\n{sequence}\n')

	return None


if __name__ == '__main__':

	cmds = get_cmds()
	fileobj = open(cmds.out,'w')
	query = cmds.domain
	
	test_gbk1 = '/work/sales001/cblaster_analysis/as6_halo_runs/as6_haloAMP10_5_gbks/bin_gb5_40_9272.region001.gbk' 

	for filepath in get_gbk_files(cmds.gbks):
		print(filepath)
		extract_domain(filepath, query, fileobj)

#	extract_domain(test_gbk1, query, fileobj)

	fileobj.close()
