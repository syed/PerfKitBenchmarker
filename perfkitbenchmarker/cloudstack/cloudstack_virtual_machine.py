# Copyright 2014 Google Inc. All rights reserved.
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

from perfkitbenchmarker import flags
from perfkitbenchmarker import linux_virtual_machine as linux_vm
from perfkitbenchmarker import virtual_machine
from perfkitbenchmarker import vm_util
from perfkitbenchmarker.cloudstack import cloudstack_network
from perfkitbenchmarker.cloudstack import cloudstack_disk
from perfkitbenchmarker.cloudstack import util


UBUNTU_IMAGE = 'Ubuntu 14.04.2 HVM base (64bit)'
RHEL_IMAGE = 'CentOS 7 HVM base (64bit)'

FLAGS = flags.FLAGS


class CloudStackVirtualMachine(virtual_machine.BaseVirtualMachine):
  """Object representing a CloudStack Virtual Machine."""

  DEFAULT_ZONE = 'QC-1'
  DEFAULT_MACHINE_TYPE = '1vCPU.1GB'
  DEFAULT_IMAGE = 'Ubuntu 14.04.2 HVM base (64bit)'
  DEFAULT_USER_NAME = 'cca-user'
  DEFAULT_PROJECT = 'cloudops-Engineering'


  def __init__(self, vm_spec):
    """Initialize a CloudStack virtual machine.

    Args:
      vm_spec: virtual_machine.BaseVirtualMachineSpec object of the vm.
    """
    super(CloudStackVirtualMachine, self).__init__(vm_spec)

    self.network = \
        cloudstack_network.CloudStackNetwork.GetNetwork(self.DEFAULT_ZONE)

    self.cs = util.CsClient(
        FLAGS.CS_API_URL,
        FLAGS.CS_API_KEY,
        FLAGS.CS_API_SECRET
    )

    self.project_id = None
    if FLAGS.project:
        project = self.cs.get_project(FLAGS.project)
        assert project, "Project not found"
        self.project_id = project['id']

    zone = self.cs.get_zone(self.zone)
    assert zone, "Zone not found"

    self.zone_id = zone['id']

    # XXX: How do we genralize this?
    self.user_name = self.DEFAULT_USER_NAME


  @classmethod
  def SetVmSpecDefaults(cls, vm_spec):
    """Updates the VM spec with cloud specific defaults."""
    if vm_spec.machine_type is None:
      vm_spec.machine_type = cls.DEFAULT_MACHINE_TYPE
    if vm_spec.zone is None:
      vm_spec.zone = cls.DEFAULT_ZONE
    if vm_spec.image is None:
      vm_spec.image = cls.DEFAULT_IMAGE

  def _CreateDependencies(self):
    """Create VM dependencies."""

    # Create an ssh keypair
    with open(self.ssh_public_key) as keyfd:
        self.ssh_keypair_name = 'perfkit-sshkey-%s' % FLAGS.run_uri
        pub_key = keyfd.read()

        if not self.cs.get_ssh_keypair(self.ssh_keypair_name, self.project_id):

            res = self.cs.register_ssh_keypair(self.ssh_keypair_name,
                                               pub_key,
                                               self.project_id)

            assert res, "Unable to create ssh keypair"


    # Allocate a public ip
    network_id = self.network.id
    if self.network.is_vpc:
        network_id = self.network.vpc_id

    public_ip = self.cs.alloc_public_ip(network_id, self.network.is_vpc)

    if public_ip:
        self.ip_address = public_ip['ipaddress']
        self.ip_address_id = public_ip['id']


  def _DeleteDependencies(self):
    """Delete VM dependencies."""
    print "Delete deps\n"
    # Remove the keypair


    if self.cs.get_ssh_keypair(self.ssh_keypair_name, self.project_id):
        self.cs.unregister_ssh_keypair(self.ssh_keypair_name, self.project_id)

    # Remove the IP
    if self.ip_address_id:
        self.cs.release_public_ip(self.ip_address_id)

  def _Create(self):
    """Create a Cloudstack VM instance."""

    print "-" * 30
    print "CREATE VM\n"

    zone = self.cs.get_zone(self.zone)
    assert zone, "No zone found"

    service_offering = self.cs.get_serviceoffering(self.machine_type)
    assert service_offering, "No service offering found"

    template = self.cs.get_template(self.image, self.project_id)
    assert template, "No template found"

    network_id = self.network.id

    self._vm = self.cs.create_vm(
        self.name,
        zone['id'],
        service_offering['id'],
        template['id'],
        [network_id],
        self.ssh_keypair_name,
        self.project_id
    )

    # TODO: Raise retryable excception if not able to create
    assert self._vm, "Unable to create VM"

    self.id = self._vm['virtualmachine']['id']


  @vm_util.Retry()
  def _PostCreate(self):
    """Get the instance's data."""

    # assosiate the public ip created with the VMid
    network_interface = self._vm['virtualmachine']['nic'][0]
    self.internal_ip = network_interface['ipaddress']

    # Create a Static NAT rule
    snat_rule = self.cs.enable_static_nat(
        self.ip_address_id,
        self.id,
        self.network.id
    )

    if snat_rule:
        self.snat_rule_id = snat_rule['id']


  def _Delete(self):
    """Delete the VM instance."""
    # Delete the VM
    self.cs.delete_vm(self.id)

  def _Exists(self):
    """Returns true if the VM exists."""

    # Check if VM exisits
    vm = self.cs.get_virtual_machine(self.name, self.project_id)
    if vm and 'id' in vm:
        return True

    return False

  def CreateScratchDisk(self, disk_spec):
    """Create a VM's scratch disk.

    Args:
      disk_spec: virtual_machine.BaseDiskSpec object of the disk.
    """

    # Cloudstack doesn't really have a concept of local or remote disks A VM
    # starts with one disk and all other volumes have to be attached via the
    # API

    self.disks = []

    for i in xrange(disk_spec.num_striped_disks):

        name = 'disk-%s-%s' % (self.name, i + 1)
        scratch_disk = cloudstack_disk.CloudStackDisk(disk_spec,
                                                      name,
                                                      self.zone_id,
                                                      self.project_id)

        self.disks.append(scratch_disk)

    self._CreateScratchDiskFromDisks(disk_spec, self.disks)


class DebianBasedCloudStackVirtualMachine(CloudStackVirtualMachine,
                                          linux_vm.DebianMixin):
  DEFAULT_IMAGE = UBUNTU_IMAGE


class RhelBasedCloudStackVirtualMachine(CloudStackVirtualMachine,
                                        linux_vm.RhelMixin):
  DEFAULT_IMAGE = RHEL_IMAGE
