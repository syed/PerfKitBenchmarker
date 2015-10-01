# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Cloudstack utils"""

import csapi
import os
from perfkitbenchmarker import flags

flags.DEFINE_string('CS_API_URL',
                    'http://127.0.0.1:8080/client/api',
                    'API endpoint for Cloudstack.')

flags.DEFINE_string('CS_API_KEY', 
                    os.environ.get('CS_API_KEY'), 
                    'Key for API authentication')

flags.DEFINE_string('CS_API_SECRET', 
                    os.environ.get('CS_API_KEY'),
                    'Secret for API authentication')

FLAGS = flags.FLAGS


class CsClient(object):

    def __init__(self, url, api_key, secret, project=None):
        # self.cs = csapi.API(api_key, secret, url)

        self.project_id = None
        if project:
            self.project_id = self._get_project_id(project)

    def _get_project_id(self, project_name):
        cs_args = {
            'command': 'listProjects'
        }

        self.project_id = self.cs.request(cs_args)
