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
Authorises AFS via shelling out and using a kerberos keytab
and performing aklog
"""

import os, subprocess
from autopkglib import Processor, ProcessorError

__all__ = ["AFSAuth"]

class AFSAuth(Processor):

	input_variables = {
		'auth_method': {
				 'description': 'keytab is the only option atm'
				 'required': False.
			       },
	}

	def gettoken(self):

		keytabname = os.environ.get("KEYTABNAME", None)
		principal = os.environ.get("PRINCIPAL",None)

		subprocess.call(["kinit","-t",keytabname,principal])
		subprocess.call(["aklog"])
	
	def main(self):
		self.gettoken()

if __name__ == '__main__':
	PROCESSOR = AFSAuth()
