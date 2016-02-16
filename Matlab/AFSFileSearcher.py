#!/usr/bin/python

import os, subprocess, re
from distutils.version import LooseVersion


from autopkglib import Processor, ProcessorError

__all__ = ["AFSFileSearcher"]

class AFSFileSearcher(Processor):
	'''Provides path to the file that needs packaged'''

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
			highestver='0'
		
			for x in range(len(software)):
					if re.search(re_pattern,software[x]) and LooseVersion(software[x]) > LooseVersion(highestver):
						highestver = software[x]
			file = path + '/' + highestver
			return(file)
		except OSError:
			raise ProcessorError('Could not find software matching the regex provided'(path, re_pattern, stderr)

	def gettoken():
	
		keytabname = os.environ.get("keytabname", None)
		principal = os.environ.get("principal",None)

		subprocess.call(["kinit","-t",keytabname,principal])
		subprocess.call(["aklog"])
		subprocess.call(["klist"])


	def killtoken():
		subprocess.call(["unlog"])
		subprocess.call(["kdestroy"], shell=True)


	def main(self):


if __name__ == '__main__':
	PROCESSOR = AFSFileSearcher()
