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

import logging
import os
from csapi import API
from perfkitbenchmarker import flags

flags.DEFINE_string('CS_API_URL',
                    'http://127.0.0.1:8080/client/api',
                    'API endpoint for Cloudstack.')

flags.DEFINE_string('CS_API_KEY',
                    os.environ.get('CS_API_KEY'),
                    'Key for API authentication')

flags.DEFINE_string('CS_API_SECRET',
                    os.environ.get('CS_API_SECRET'),
                    'Secret for API authentication')

FLAGS = flags.FLAGS


class CsClient(object):

    def __init__(self, url, api_key, secret):

        self._cs = API(
            api_key,
            secret,
            url,
            logging=True,
            log="/home/syed/csapi.log"
        )

    def get_zone_id(self, zone_name):

        cs_args = {
            'command': 'listZones'
        }

        zones = self._cs.request(cs_args)
        for zone in zones['zone']:
            if zone['name'] == zone_name:
                return zone['id']

        return None

    def get_template_id(self, template_name, project_id=None):

        cs_args = {
            'command': 'listTemplates',
            'templatefilter': 'executable'
        }

        if project_id:
            cs_args.update({'projectid': project_id})


        templates = self._cs.request(cs_args)
        for temp in templates['template']:
            if temp['name'] == template_name:
                return temp['id']

        return None

    def get_serviceoffering_id(self, service_offering_name):

        cs_args = {
            'command': 'listServiceOfferings',
        }

        service_offerings = self._cs.request(cs_args)

        for servo in service_offerings['serviceoffering']:
            if servo['name'] == service_offering_name:
                return servo['id']

        return None


    def get_project_id(self, project_name):

        cs_args = {
            'command': 'listProjects'
        }

        projects = self._cs.request(cs_args)

        if projects and 'project' in projects:
            for proj in projects['project']:
                if proj['name'] == project_name:
                    return proj['id']

        logging.warn("Project %s not found, \
                     continuing without project" % project_name)

        return None

    def get_network_id(self, network_name, project_id=None, vpc_id=None):

        cs_args = {
            'command': 'listNetworks',
        }

        if project_id:
            cs_args.update({"projectid": project_id})

        if vpc_id:
            cs_args.update({"vpcid": vpc_id})

        networks = self._cs.request(cs_args)

        for network in networks['network']:
            print network['name']
            if network['name'] == network_name:
                return network['id']

        return None

    def get_vpc_id(self, vpc_name, project_id=None):

        cs_args = {
            'command': 'listVPCs',
        }

        if project_id:
            cs_args.update({"projectid": project_id})


        vpcs = self._cs.request(cs_args)

        for vpc in vpcs['vpc']:
            if vpc['name'] == vpc_name:
                return vpc['id']

        return None

    def get_virtual_machine_id(self, vm_name, project_id=None):

        cs_args = {
            'command': 'listVirtualMachines',
        }

        if project_id:
            cs_args.update({"projectid": project_id})

        vms = self._cs.request(cs_args)

        for vm in vms['virtualmachine']:
            if vm['name'] == vm_name:
                return vm['id']

        return None


        pass

    def create_vm(self,
                  name,
                  zone_id,
                  service_offering_id,
                  template_id,
                  network_ids=None,
                  project_id=None):

        create_vm_args = {
            'command': 'deployVirtualMachine',
            'serviceofferingid': service_offering_id,
            'templateid': template_id,
            'zoneid': zone_id,
            'name': name
        }

        if network_ids:
            create_vm_args.update({"networkids": network_ids})

        if project_id:
            create_vm_args.update({"projectid": project_id})

        res = self._cs.request(create_vm_args)

        return res

    def delete_vm(self, vm_id):

        cs_args = {
            'command': 'destroyVirtualMachine',
            'id': vm_id
        }

        res = self._cs.request(cs_args)
        return res
