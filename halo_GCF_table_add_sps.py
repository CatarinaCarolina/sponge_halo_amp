#!usr/env/bin python3

"""
Author: Catarina Loureiro

A script to add a column with host sponge sps based on sample column
"""

import os
import argparse


def get_cmds():
	"""
	Capture args from the cmdline
	"""

	parser = argparse.ArgumentParser(description='')

	parser.add_argument('-g', '-gcf', dest='gcf', help='gcf annotation file',\
			 required=True, metavar='<file>')

	parser.add_argument('-s', '-sps', dest='sps',help='sps sample mapping file',\
			 required=True, metavar='<file>')

	parser.add_argument('-o', '-out', dest='out', help='updated gcf file',\
			 required=True, metavar='<file>')

#	parser.add_argument('-', '-', dest='', help='', required=True, metavar='<>')

	return parser.parse_args()



def parse_mapping(map_file):
	"""
	generate dict from mapping file

	map_file: str, filepath
	map_dict: dict{sample:sps}
	"""

	map_dict = {}

	fileobj = open(map_file, 'r')

	for line in fileobj:
		line = line.strip()
		elms = line.split('\t')
		map_dict[elms[0]] = elms[1]


	return map_dict


def update_GCF(gcf_file, map_dict, out_file):
	"""
	update with sps column

	gcf_file, out_file: str, path
	map_dict: dict{sample:sps}
	"""

	gcf_fileobj = open(gcf_file, 'r')
	out_fileobj = open(out_file, 'w')
	out_fileobj.write(f'GCF\tSamples\tHost_taxa\tCount\tBins\tBin_rep\tBin_taxa\n')

	for line in gcf_fileobj:
		line = line.strip()
		if line.startswith('GCF'):
			header = line
		else:
			elms = line.split('\t')
			GCF = elms[0]
			samples = elms[1].split(',')
			bins = elms[2]
			bin_rep = elms[3]
			bin_taxa = elms[4]
			sps = [map_dict[sample] for sample in samples]
			sps = [species for species in set(sps)]
			sps_str = ','.join(sps)
			sps_len = str(len(sps))
			out_fileobj.write(f'{GCF}\t{elms[1]}\t{sps_str}\t{sps_len}\t{bins}\t{bin_rep}\t{bin_taxa}\n')

	return None

if __name__ == '__main__':

	cmds = get_cmds()

	dict_map = parse_mapping(cmds.sps)

	update_GCF(cmds.gcf, dict_map, cmds.out)
