#!/usr/bin/env python
#
# LightworksURLProvider custom processor for autopkg
#
# Copyright (C) 2015 Oxford University
#    Ben Goodstein <ben.goodstein(at)it.ox.ac.uk>
#
# This program is free software; you can redistribute
# it and/or modify it under the terms of the GNU
# General Public License version 3 as published by
# the Free Software Foundation.
#
###############################################################################

from autopkglib import Processor, ProcessorError
# from subprocess import Popen, PIPE
import re
import urllib2

BASE_URL = "http://www.lwks.com/index.php?option=com_docman&task=doc_download&gid=210"
REGEX = "\d+.\d+.\d+"

__all__ = ["LightworksURLProvider"]

class LightworksURLProvider(Processor):
    """Provides a download URL for latest version of Lightworks"""
    description = __doc__
    input_variables = {}
    output_variables = {
            "url": {
                "description": "URL to latest download",
                },
            "version": {
                "description": "Version number downloaded",
                }
            }
    
    def get_version(self, url):
        m = re.search(REGEX, url)
        if m:
            return m.group()
        else:
            raise ProcessorError("Couldn't get version from download")

    def main(self):
        try:
            response = urllib2.urlopen(BASE_URL)
            real_url = response.geturl()
        except BaseException as err:
            raise ProcessorError("Problem obtaining URL: %s" % err)

        self.env["url"] = real_url
        self.env["version"] = self.get_version(real_url)

if __name__ == "__main__":
    PROCESSOR = LightworksURLProvider()
    PROCESSOR.execute_shell()
