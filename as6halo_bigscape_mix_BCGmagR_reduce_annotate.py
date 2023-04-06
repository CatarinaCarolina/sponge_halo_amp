#!usr/env/bin python3

"""
Author: Catarina Loureiro

A script to dereplicate a set of bigscape bgcs based on mag presence and annotate them
"""

import os
import argparse


def get_cmds():
	"""
	Capture args from the cmdline
	"""

	parser = argparse.ArgumentParser(description='')

	parser.add_argument('-i', '-info', dest='info', help='already annotated bgcs',\
			 required=True, metavar='<file>')

	parser.add_argument('-m', '-mix', dest='mix', help='input mixed file',\
			 required=True, metavar='<file>')

	parser.add_argument('-o', '-out', dest='out', help='output',\
			 required=True, metavar='<file>')

#	parser.add_argument('-', '-', dest='', help='', required=True, metavar='<>')

	return parser.parse_args()


def process_info(info_file):
	"""
	parse and store info file

	info_file: str, filepath
	info_dict: dict, {bgc:'info'}
	"""
	info_dict = {}

	fileobj = open(info_file, 'r')
	for line in fileobj:
		line = line.strip()
		if line.startswith('#'):
			header = line
		else:
			elms = line.split('\t')
			bgc_name = elms[0]
			bgc_info = elms[3:]
			info_dict[bgc_name] = bgc_info
	fileobj.close()

	return info_dict


def parse_bgcs(bgc_file):
	"""
	parse bgc file

	bgc_file: str, filepath
	contig/mag_dict: dict, {bgc:annotations}
	"""

	contig_dict = {}
	mag_dict = {}

	fileobj = open(bgc_file, 'r')
	for line in fileobj:
		line = line.strip()
		if line.startswith('#'):
			header = line
		else:
			elms = line.split('\t')
			bgc_name = elms[0]
			bgc_info = elms[1:]
			if 'bin' in line:
				mag_dict[bgc_name] = bgc_info
			else:
				contig_dict[bgc_name] = bgc_info

	return (contig_dict,mag_dict)

def reduce(contig_dict,mag_dict,info_dict,file_out):
	"""
	dereplicated bgcs

	contig/mag_dict: dict, {bgc:annotations}
	reducted_dict: dict, {bgc:annotations}
	"""
	fileobj = open(file_out, 'w')

	for c_bgc, c_vals in contig_dict.items():
		print(c_bgc, c_vals, info_dict[c_bgc])
		cbgc_bin = info_dict[c_bgc][1]
		fbgc = [c_bgc, c_vals[0]]
		fbgc.extend(info_dict[c_bgc])
		if 'bin' in cbgc_bin:
			name_bin = cbgc_bin[:-2]
			len_cbgc = c_vals[0].split('_')[3]
			for m_bgc,m_vals in mag_dict.items():
				if name_bin in m_bgc:
					print(m_bgc,m_vals)
					len_mbgc = m_bgc.split('length_')[1]
					len_mbgc = len_mbgc.split('_')[0]
					if int(len_mbgc) > int(len_cbgc):
						fbgc = [m_bgc, m_vals[0]]
						fbgc.extend(info_dict[c_bgc])
					break
		print(fbgc)
		print('--------')
		newline = '\t'.join(fbgc)
		fileobj.write(f'{newline}\n')
	fileobj.close()
	return None


if __name__ == '__main__':

	cmds = get_cmds()
	dict_info = process_info(cmds.info)
	dict_contig,dict_mag = parse_bgcs(cmds.mix)
	reduce(dict_contig,dict_mag,dict_info, cmds.out)
	
