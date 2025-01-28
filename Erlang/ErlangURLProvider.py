#!/usr/bin/python
# encoding: utf-8
'''
ErlangURLProvider.py

Custom Processor for autopkg that provides URL to specific version of
ESL Erlang

Copyright (C) University of Oxford 2015
    Ben Goodstein <ben.goodstein at it.ox.ac.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib.request
import json
import re
import ssl

from autopkglib import Processor, ProcessorError

__all__ = [u'ErlangURLProvider']

# Define constants
BASE_URL = u'https://packages.erlang-solutions.com/site/'
JSON_URL = BASE_URL + u'erlang/packages.json'
DOWNLOAD_BASE_URL = BASE_URL + 'esl/'
_FLAVOURS = { 0: u'general',
              1: u'esl'
             }
DEFAULT_FLAVOUR = u'general'
DEFAULT_TARGET = u'10.10'
DEFAULT_VERSION = u'latest'

class ErlangURLProvider(Processor):
    '''Provides URL to the latest ESL Erlang release.'''
    description = __doc__
    input_variables = {
            'target_os': {
                'required': False,
                'description': ('OS X version. Defaults to %s. Can be 10.10, 10.9 or 10.6.8'
                                % DEFAULT_TARGET)
                },
            'flavour': {
                'required': False,
                'description': ('Flavour of Erlang. Defaults to %s. Can be general or esl'
                                % DEFAULT_FLAVOUR)
                },
            'version': {
                'required': False,
                'description': ('Download version number. Defaults to %s'
                                % DEFAULT_VERSION)
                }
            }
    output_variables = {
            'url': {
                'description': ('URL to the required version of Erlang')
                },
            'version': {
                'description': ('Version for this download')
                }
            }

    def lookup_flavour(self, flav_name):
        '''Return flavour code from flavour name'''
        for k, v in _FLAVOURS.items():
            if v == flav_name:
                return k

    def main(self):
        '''Do our processor task!'''
        target_os = self.env.get('target_os', DEFAULT_TARGET)
        flavour = self.env.get('flavour', DEFAULT_FLAVOUR)
        get_version = self.env.get('version', DEFAULT_VERSION)

    try:
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(JSON_URL) as response:
             response_data = response.read().decode('utf-8')
        response.data = re.sub(r'\);', '', re.sub('^jsonCallback\(', '', response_data))
        erlang_tabs = json.loads(response_data)['tabs']
    except Exception as e:
        raise ProcessorError(f"Failed to fetch or process the JSON data: {e}")

        # Use OS X information from json
        osx_tab = next(tab for tab in erlang_tabs if tab['name'] == 'osx')
        # Select packages based on 'flavour'
        flavour_index = self.lookup_flavour(flavour)
        packages = osx_tab['flavours'][flavour_index]['packages']
        # Filter the list based on the OS version we require
        filtered_packages = [package for package in packages
                             if package['os'] == 'Mac OS X ' + target_os]

        if get_version == 'latest':
            idx=0
            # Select the latest *DMG* as this is what the of the recipe
            # rest expects (and there are .tgz links around)
            # 
            while idx < len(filtered_packages):
                url = DOWNLOAD_BASE_URL + filtered_packages[idx]['path']
                if re.match(r'.+\.dmg$', url):
                    break
                idx=idx+1
        else:
            try:
                url = DOWNLOAD_BASE_URL + next (package for package in filtered_packages
                        if package['version'] == get_version).next()['path']
            except StopIteration:
                raise ProcessorError('Specified package version %s could not be found for specified OS version %s'
                                      % (get_version, target_os))
        
        version = re.match(r'.+erlang_(.+)~osx.+', url).group(1)

        self.env['url'] = url
        self.env['version'] = version

if __name__ == '__main__':
    PROCESSOR = ErlangURLProvider()
    PROCESSOR.execute_shell()
