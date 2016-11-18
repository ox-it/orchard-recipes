#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © University of Oxford
# Author
# Name: Ian Collier
# Email: imc at cs.ox.ac.uk
# GitHub: imc0

"""
Run a build script for a package that has already been unpacked
in order to compile or gather the files that should be placed into
the eventual package.
"""

import subprocess
from autopkglib import Processor, ProcessorError

__all__ = ["BuildScriptRunner"]

class BuildScriptRunner(Processor):
  input_variables = {
    'script': {
      'description': 'Shell commands to run',
      'required': True,
    },
  }

  output_variables = { }

  def main(self):
    script = self.env['script']
    rc = subprocess.call(["/bin/bash", "-c", script]);
    if rc != 0:
      raise ProcessorError('The build subprocess exited with code ' + str(rc))

