#!usr/env/bin python3

"""
Author: Catarina Loureiro

A script to trim AS^ gbk file based on candidate cluster halo AMP
"""

import os
import argparse
import pandas as pd
from Bio import SeqIO
from Bio import SeqFeature

def get_cmds():
	"""
	Capture args from the cmdline
	"""

	parser = argparse.ArgumentParser(description='')

	parser.add_argument('-g', '-gbks', dest='gbks', help='folder with input gbks',\
		required=True, metavar='<path>')

	parser.add_argument('-o', '-out', dest='out', help='folder with trimmed gbks',\
		 required=True, metavar='<path>')

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
				if f.endswith('.gbk'):
					yield (os.path.join(dirpath, f))
	except:
		pass


def parse_gbk(gbk_file, out_path):
	"""
	parse gbk file to find region of interest

	gbk_file: str, filepath
	out_path: str, folderpath
	"""

	gbk_fullname = gbk_file.split('/')[-1]
	gbk_name = gbk_fullname.split('.gbk')[0]
	gbk_outname = gbk_name + '_haloAMP.gbk'
	gbk_out = os.path.join(out_path, gbk_outname)
	#print(gbk_out)


	gbkcontents = SeqIO.parse(gbk_file, "genbank")
	for record in gbkcontents:
		#print(record.annotations)
		record_annotations = record.annotations
		for feature in record.features:
			if feature.type == 'cand_cluster' and 'Halo_AMP' in feature.qualifiers['product']:
#feature.qualifiers['product'] == ['Halo_AMP']: # and feature.qualifiers['kind'] == ['single']
				print(gbk_file)
				print(gbk_out)
				#print(feature)
				curr_subrecord = record[feature.location.start:feature.location.end]
				curr_subrecord.annotations = record_annotations
				#print(curr_subrecord.annotations)
				SeqIO.write(curr_subrecord, gbk_out, 'genbank')

	return None

if __name__ == '__main__':

	cmds = get_cmds()
	out_folder = cmds.out

#	test_gbk = '/work/sales001/halo_analysis/all_BGC_as6_halo_amp/Pf12_c00118_NODE_11...region001.gbk'
#	parse_gbk(test_gbk,out_folder)

	for filepath in get_gbk_files(cmds.gbks):
		#print(filepath)
		parse_gbk(filepath, out_folder)

