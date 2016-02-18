#! /usr/bin/env python
#
# Copyright 2016 University of Oxford
#
# Author
# Name: Gary Ballantine
# Email: gary.ballantine at it.ox.ac.uk
# GitHub: AltMeta
# Distributed under terms of the MIT license.

"""
De-authenticates AFS via unlog and kdestroy
"""
import 
from autopkglib import Processor, ProcessorError

__all__ = ["AFSDeauth"]

class AFSDeauth(Processor):
	
	input_variables = {
		'auth_method': {
				 'description': 'keytab is the only option atm'
				 'required': False.
			       },
	}

	def killtoken(self):
		subprocess.call(["unlog"], shell=True)
		subprocess.call(["kdestroy"], shell=True)
	
	def main(self):
		self.killtoken()

if __name__ == '__main__':
	PROCESSOR = AFSDeauth()
