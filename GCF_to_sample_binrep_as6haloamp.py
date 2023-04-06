#!usr/env/bin python3

"""
Author: Catarina Loureiro

A script to parse BGC table and extract GCF, samples, bins, binrep
"""

import os
import argparse
import pandas as pd

def get_cmds():
	"""
	Capture args from the cmdline
	"""

	parser = argparse.ArgumentParser(description='')

	parser.add_argument('-g', '-gcf', dest='gcf', help='gcf info file',\
		 required=True, metavar='<file>')

	parser.add_argument('-o', '-out', dest='out', help='updated intersect file',\
		 required=True, metavar='<file>')

	return parser.parse_args()


def parse_gcf(gcf_file, out_file):
	"""
	A function to extract gcf - eco info

	gcf_file: str, filepath

	gcf_eco_dict: dict{gcf:{samples,bins,bin_rep}}
	"""

	file_obj = open(gcf_file, 'r')

	gcf_eco_dict = {}

	for line in file_obj:
		line = line.strip()

		if line.startswith("#"):
			header = line
		else:

			BGC,contig,gcf,sample,bin,b_rep,c_rep = line.split('\t')

			if gcf not in gcf_eco_dict.keys():
				gcf_eco_dict[gcf] = {'samples':[sample], 'bins':[bin],'bin_rep':[b_rep], 'class':[c_rep]}

			else:
				if sample not in gcf_eco_dict[gcf]['samples']:
					gcf_eco_dict[gcf]['samples'].append(sample)
				if bin not in gcf_eco_dict[gcf]['bins']:
					gcf_eco_dict[gcf]['bins'].append(bin)
				if b_rep not in gcf_eco_dict[gcf]['bin_rep']:
					gcf_eco_dict[gcf]['bin_rep'].append(b_rep)
				if c_rep not in gcf_eco_dict[gcf]['class']:
					gcf_eco_dict[gcf]['class'].append(c_rep)

	gcf_eco_df = pd.DataFrame.from_dict(gcf_eco_dict, orient='index')
	print(gcf_eco_df)

	#gcf_eco_df.to_csv(out_file, sep='\t')

	outfile = open(out_file, 'w')

	outfile.write(f'GCF\tSamples\tBins\tBin_reps\n')

	for key, value in gcf_eco_dict.items():
		samples = ','.join(gcf_eco_dict[key]['samples'])
		bins = ','.join(gcf_eco_dict[key]['bins'])
		bin_rep = ','.join(gcf_eco_dict[key]['bin_rep'])
		c_rep = ','.join(gcf_eco_dict[key]['class'])
		outfile.write(f'{key}\t{samples}\t{bins}\t{bin_rep}\t{c_rep}\n')
	outfile.close()

	return None


if __name__ == '__main__':

	cmds = get_cmds()

	gcf_f = cmds.gcf
	out_f = cmds.out

	parse_gcf(gcf_f, out_f)
