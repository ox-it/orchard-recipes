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
				 'description': 'keytab is the only option atm',
				 'required': False,
				 'default': 'keytab',
				
			       },
		'aklog_path': {
				 'description': 'Path to aklog binary',
				 'required': False,
				 'default': '/usr/local/bin/aklog',
			       },
	}

	output_variables = {
	              'test': {
			         'description': 'for testing',
				 'required': False,
                              },
        }

	def gettoken(self):

		keytabname = os.environ.get("KEYTABNAME", None)
		principal = os.environ.get("PRINCIPAL",None)

                if keytabname is None:
                    raise ProcessorError('Missing keytab environment variable')

                self.output('Using Keytab %s with principal %s'
                              % (keytabname, principal), verbose_level=3)

                self.output('Calling kinit ...', verbose_level=5)

                try:
		    subprocess.call(["kinit","-t",keytabname,principal])
                except Exception as kiniterror:
                    raise ProcessorError('Problem running kinit %s' % kiniterror)

                aklog = self.env['aklog_path']
                if aklog is None:
                    raise ProcessorError('Missing aklog_path setting')

                self.output('Calling aklog %s ...' % aklog, verbose_level=5 )
                try:
		    subprocess.call([ aklog ])
                except Exception as aklogerror:
                    raise ProcessorError('Problem running aklog %s' % aklogerror)
	
	def main(self):
		auth_method = self.env['auth_method']
                if auth_method != 'keytab':
                    raise
                       ProcessorError('Unsupported authentication method: %s'
                                       % (auth_method) )
		self.gettoken()

if __name__ == '__main__':
	PROCESSOR = AFSAuth()
