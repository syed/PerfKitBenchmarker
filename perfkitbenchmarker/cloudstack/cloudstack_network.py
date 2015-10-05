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


FLAGS = flags.FLAGS


class CloudStackFirewall(network.BaseFirewall):
  """An object representing the Cloudstack Firewall.
  We use static NAT hence do not need explicit
  firewall rules all ports are open by default
  """


class CloudStackNetwork(network.BaseNetwork):
  """Object representing a CloudStack Network."""

  def __init__(self, zone):
    print "INIT Network"
    super(CloudStackNetwork, self).__init__()
    self.zone = zone
    self.network_offering = ""
    self.vpc_offering = ""
    self.is_vpc = True
    self.id = "0ff8a360-8660-4937-9d7d-1a37d79e887b"  # VPC id


  def Create(self):
    """Creates the actual network."""
    print "Creating Network"
    pass

  def Delete(self):
    """Deletes the actual network."""
    print "Deleting Network"
