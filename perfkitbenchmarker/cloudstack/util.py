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
                    os.environ.get('CS_API_URL'),
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
            url
        )

    def get_zone(self, zone_name):

        cs_args = {
            'command': 'listZones'
        }

        zones = self._cs.request(cs_args)
        logging.debug(zones)

        if zones and 'zone' in zones:
            for zone in zones['zone']:
                if zone['name'] == zone_name:
                    return zone

        return None

    def get_template(self, template_name, project_id=None):

        cs_args = {
            'command': 'listTemplates',
            'templatefilter': 'executable'
        }

        if project_id:
            cs_args.update({'projectid': project_id})


        templates = self._cs.request(cs_args)
        logging.debug(templates)

        if templates and 'template' in templates:
            for templ in templates['template']:
                if templ['name'] == template_name:
                    return templ

        return None

    def get_serviceoffering(self, service_offering_name):

        cs_args = {
            'command': 'listServiceOfferings',
        }

        service_offerings = self._cs.request(cs_args)
        logging.debug(service_offerings)

        if service_offerings and 'serviceoffering' in service_offerings:
            for servo in service_offerings['serviceoffering']:
                if servo['name'] == service_offering_name:
                    return servo

        return None


    def get_project(self, project_name):

        cs_args = {
            'command': 'listProjects'
        }

        projects = self._cs.request(cs_args)
        logging.debug(projects)

        if projects and 'project' in projects:
            for proj in projects['project']:
                if proj['name'] == project_name:
                    return proj

        return None

    def get_network(self, network_name, project_id=None, vpc_id=None):

        cs_args = {
            'command': 'listNetworks',
        }

        if project_id:
            cs_args.update({"projectid": project_id})

        if vpc_id:
            cs_args.update({"vpcid": vpc_id})

        networks = self._cs.request(cs_args)
        logging.debug(networks)

        if networks and 'network' in networks:
            for network in networks['network']:
                print network['name']
                if network['name'] == network_name:
                    return network['id']

        return None

    def get_vpc(self, vpc_name, project_id=None):

        cs_args = {
            'command': 'listVPCs',
        }

        if project_id:
            cs_args.update({"projectid": project_id})

        vpcs = self._cs.request(cs_args)
        logging.debug(vpcs)

        if vpcs and 'vpc' in vpcs:
            for vpc in vpcs['vpc']:
                if vpc['name'] == vpc_name:
                    return vpc['id']

        return None

    def get_virtual_machine(self, vm_name, project_id=None):

        cs_args = {
            'command': 'listVirtualMachines',
        }

        if project_id:
            cs_args.update({"projectid": project_id})

        vms = self._cs.request(cs_args)
        logging.debug(vms)

        if vms and 'virtualmachine' in vms:
            for vm in vms['virtualmachine']:
                if vm['name'] == vm_name:
                    return vm['id']

        return None

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

        vm = self._cs.request(create_vm_args)
        logging.debug(vm)

        return vm

    def delete_vm(self, vm_id):

        cs_args = {
            'command': 'destroyVirtualMachine',
            'id': vm_id
        }

        res = self._cs.request(cs_args)
        logging.debug(res)

        return res

    def create_vpc(self, name, zone_id, cidr, vpc_offering_id, project_id=None):

        cs_args = {
            'command': 'createVPC',
            'name': name,
            'displaytext': name,
            'vpcofferingid': vpc_offering_id,
            'cidr': cidr,
            'zoneid': zone_id,
        }

        if project_id:
            cs_args.update({"projectid": project_id})

        vpc = self._cs.request(cs_args)
        logging.debug(vpc)

        return vpc

    def delete_vpc(self, vpc_id):

        cs_args = {
            'command': 'deleteVPC',
            'id': vpc_id
        }

        res = self._cs.request(cs_args)
        logging.debug(res)

        return res

    def create_network(self,
                       name,
                       network_offering_id,
                       zone_id,
                       projet_id=None,
                       vpc_id=None,
                       gateway=None,
                       netmask=None):

        cs_args = {
            'command': 'createNetwork',
            'name': name,
            'zoneid': zone_id,
            'networkofferingid': network_offering_id,
        }

        if vpc_id:
            cs_args.update({
                'vpcid': vpc_id,
                'gateway': gateway,
                'netmask': netmask
            })

        res = self._cs.request(cs_args)
        logging.debug(res)

        return res


    def delete_network(self, network_id):

        cs_args = {
            'command': 'deleteNetwork',
            'id': network_id
        }

        res = self._cs.request(cs_args)
        logging.debug(res)

        return res

    def alloc_public_ip(self, network_id, is_vpc=False):

        cs_args = {
            'command': 'associateIpAddress',
        }

        if is_vpc:
            cs_args.update({'vpcid': network_id})
        else:
            cs_args.update({'networkid': network_id})

        res = self._cs.request(cs_args)

        if res and 'ipaddress' in res:
            return res['ipaddress']

        return None

    def release_public_ip(self, ipaddress_id):

        cs_args = {
            'command': 'disassociateIpAddress',
            'id': ipaddress_id
        }

        res = self._cs.request(cs_args)

        return res

    def enable_static_nat(self, ip_address_id, vm_id, network_id):

        cs_args = {
            'command': 'enableStaticNat',
            'ipaddressid': ip_address_id,
            'virtualmachineid': vm_id
        }

        if network_id:
            cs_args.update({'networkid': network_id})

        res = self._cs.request(cs_args)

        if res and 'staticnat' in res:
            return res['staticnat']

        return None
