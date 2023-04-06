#!usr/env/bin python3

"""
Author: Catarina Loureiro

A script to add binrep & bin eco to GCF table
"""

import os
import argparse


def get_cmds():
	"""
	Capture args from the cmdline
	"""

	parser = argparse.ArgumentParser(description='')

	parser.add_argument('-b', '-bin', dest='bin', help='bin rep table',\
		 required=True, metavar='<file>')

	parser.add_argument('-g', '-gcf', dest='gcf', help='bcg to gcf table',\
		 required=True, metavar='<file>')

	parser.add_argument('-o', '-out', dest='out', help='out updated gcf table',\
			 required=True, metavar='<file>')

	return parser.parse_args()


def parse_binrep(binrep_file):
	"""
	A function to extract binrep info

	binrep_file: str, filepath
	rep_bins_dict: dict{rep:[bins]}
	rep_eco_dict: dict{rep:[eco]}
	"""

	file_obj = open(binrep_file, 'r')


	rep_bins_dict = {}
	rep_eco_dict = {}

	for line in file_obj:
		line = line.strip()
		if line.startswith('#'):
			header = line
		else:
			clu,rep,samples,bins = line.split('\t')

			rep_bins_dict[rep] = bins.split(',')
			#rep_eco_dict[rep] = eco.split(',')
	#print(rep_bins_dict)
	#print(rep_eco_dict)
	file_obj.close()

	return(rep_bins_dict,rep_eco_dict)



def update_gcf(gcf_file,out_gcf_file,rep_bins_dict,rep_eco_dict):
	"""
	A function to update gcf file with binrep

	gcf_file: str, filepath
	out_gcf_file: str, filepath
	rep_bins_dict: dict{rep:[bins]}
	rep_eco_dict: dict{rep:[eco]}
	"""
	
	gcf_fobj = open(gcf_file, 'r')
	out_fobj = open(out_gcf_file, 'w')

	
	for line in gcf_fobj:
		line = line.strip()
		if line.startswith('#'):
			header = '#BGC\tcontig\tGCF\tBGC_sample\tBin\tBin_rep\n'
			out_fobj.write(header)
		else:
			bin = line.split('\t')[4]
			
			if bin.startswith('-'):
				out_fobj.write('{}\t-\n'.format(line))
			else:
				for binrep, bins in rep_bins_dict.items():
					if bin in bins:
						rep = binrep
						#eco = rep_eco_dict[rep]
						break
					else:
						rep = '-'
						#eco = '-'
				out_fobj.write('{}\t{}\n'.format(line,rep))	

	gcf_fobj.close()
	out_fobj.close()

	return None

if __name__ == '__main__':

	cmds = get_cmds()

	binrep_tsv = cmds.bin
	gcf_tsv = cmds.gcf
	out_tsv = cmds.out

	rep_bins_d,rep_eco_d = parse_binrep(binrep_tsv)

	update_gcf(gcf_tsv, out_tsv, rep_bins_d,rep_eco_d)
