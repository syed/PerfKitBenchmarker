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
"""Module containing classes related to GCE VM networking.

The Firewall class provides a way of opening VM ports. The Network class allows
VMs to communicate via internal ips and isolates PerfKitBenchmarker VMs from
others in the
same project. See https://developers.google.com/compute/docs/networking for
more information about GCE VM networking.
"""

from perfkitbenchmarker import flags
from perfkitbenchmarker import network
from perfkitbenchmarker.cloudstack import util

flags.DEFINE_string('cs_network_offering',
                    'DefaultIsolatedNetworkOfferingForVpcNetworksNoLB',
                    'Name of the network offering')

flags.DEFINE_string('cs_vpc_offering',
                    'Default VPC offering',
                    'Name of the VPC offering')

flags.DEFINE_boolean('cs_use_vpc', True,
                     'Use VPC to create networks')


FLAGS = flags.FLAGS


class CloudStackFirewall(network.BaseFirewall):
  """An object representing the Cloudstack Firewall.
  We use static NAT hence do not need explicit
  firewall rules all ports are open by default
  """


class CloudStackNetwork(network.BaseNetwork):
  """Object representing a CloudStack Network."""

  def __init__(self, zone_name):

    print "INIT Network"
    super(CloudStackNetwork, self).__init__()

    self.cs = util.CsClient(
        FLAGS.CS_API_URL,
        FLAGS.CS_API_KEY,
        FLAGS.CS_API_SECRET
    )

    self.project_id = None


    if FLAGS.project:
        project = self.cs.get_project(FLAGS.project)
        if project:
            self.project_id = project['id']

    self.zone_id = None

    zone = self.cs.get_zone(zone_name)
    if zone:
        self.zone_id = zone['id']
        self.zone = zone_name

    assert self.zone_id, "Zone required to create a network"

    self.network_name = None

    nw_off = self.cs.get_network_offering(FLAGS.cs_network_offering,
                                          self.project_id)

    assert nw_off, "Network offering not found"

    self.network_offering_id = nw_off['id']
    self.network_name = 'perfkit-network-%s' % FLAGS.run_uri

    self.is_vpc = FLAGS.cs_use_vpc
    self.vpc_id = None

    if FLAGS.cs_use_vpc:
        vpc_off = self.cs.get_vpc_offering(FLAGS.cs_vpc_offering)

        assert vpc_off, "Use VPC specified but VPC offering not found"

        self.vpc_offering_id = vpc_off['id']
        self.vpc_name = 'perfkit-vpc-%s' % FLAGS.run_uri

    self.id = None

  def Create(self):
    """Creates the actual network."""
    print "Creating Network"

    gateway = None
    netmask = None

    if self.is_vpc:
        # Create a VPC first

        cidr = '10.0.0.0/16'
        vpc = self.cs.create_vpc(self.vpc_name,
                                 self.zone_id,
                                 cidr,
                                 self.vpc_offering_id,
                                 self.project_id)
        self.vpc_id = vpc['id']
        gateway = '10.0.0.1'
        netmask = '255.255.0.0'


    # Create the network

    network = self.cs.create_network(self.network_name,
                                     self.network_offering_id,
                                     self.zone_id,
                                     self.project_id,
                                     self.vpc_id,
                                     gateway,
                                     netmask)

    self.network_id = network['id']
    self.id = self.network_id

  def Delete(self):
    """Deletes the actual network."""

    self.cs.delete_network(self.network_id)
    if self.is_vpc:
        self.cs.delete_vpc(self.vpc_id)

    self.cs.delete_network(self.network_id)
