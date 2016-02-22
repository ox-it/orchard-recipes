#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © University of Oxford
# Author
# Name: Gary Ballantine
# Email: gary.ballantine at it.ox.ac.uk
# GitHub: AltMeta

"""
list files in the specified path, performs regex and Version checking
The highest version is returned as file
"""

import re, os
from distutils.version import LooseVersion
from autopkglib import Processor, ProcessorError

__all__ = ["FSFileProvider"]

class FSFileProvider(Processor):


	input_variables = {
		're_pattern': {
				'description': 'Regular expression (Python) to match against.',
				'required': True,

			},
		'path': {
			      'description': 'provide the afs path',
			      'required': True,
			},
		'result_output_var_name': {
			      'description': 'desc',
			      'required': False,
                              'default': 'match',
		        },
	}

	output_variables = {
		'result_output_var_name': {
			     'description': 'desc',
		},
	}	

	def get_path_and_search(self, path, re_pattern):


		try:
			software = os.listdir(path)
			highestver = software[0]


			for x in range(len(software)):
					if re.search(re_pattern,software[x]) and LooseVersion(software[x]) > LooseVersion(highestver):
						highestver = software[x]
		except OSError:
			raise ProcessorError('Error Messages will get better with time'(path, re_pattern))

		try:
			re_pattern = re.compile(re_pattern)
			match = re_pattern.search(highestver)

			return (match.group(match.lastindex or 0), match.groupdict())
		except:
			pass


	def main(self):

		output_var_name = self.env['result_output_var_name']
		

		if 'path' in self.env:
			path = self.env['path']
		if 're_pattern' in self.env:
			re_pattern = self.env['re_pattern']

		groupmatch, groupdict = self.get_path_and_search(path,re_pattern)
		
	        if output_var_name not in groupdict.keys():
			groupdict[output_var_name] = groupmatch

		self.output_variables = {}
		for key in groupdict.keys():
			self.env[key] = groupdict[key]
			self.output('Found matching text (%s): %s' % (key, self.env[key], ))
			self.output_variables[key] = {
				'description': 'Matched regular expression group'}

if __name__ == '__main__':
	PROCESSOR = FSFileProvider()
