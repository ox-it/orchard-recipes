#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © University of Oxford
# Author
# Name: Gary Ballantine
# Email: gary.ballantine at it.ox.ac.uk
# GitHub: AltMeta
# Distributed under terms of the MIT license.

"""

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
			      'required': True
			},
	}

	output_variables = {
		'file': {
			     'file': 'file to import',
			},
	}

	def get_path_and_search(self, path, re_pattern):

		try:
			software = os.listdir(path)
			highestver = software[0]
		
			for x in range(len(software)):
					if re.search(re_pattern,software[x]) and LooseVersion(software[x]) > LooseVersion(highestver):
						highestver = software[x]
			file = path + '/' + highestver
			return(file)
		except OSError:
			raise ProcessorError('Error Messages will get better with time'(path, re_pattern))

	def main(self):

		if 'path' in self.env:
			path = self.env['path']
		if 're_pattern' in self.env:
			re_pattern = self.env['re_pattern']

		self.env['file'] = self.get_path_and_search(path, re_pattern)
		self.output(file)

if __name__ == '__main__':
	PROCESSOR = FSFileProvider()
