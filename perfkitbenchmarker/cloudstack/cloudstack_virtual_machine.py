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
from perfkitbenchmarker.cloudstack import util



FLAGS = flags.FLAGS

NVME = 'nvme'
SCSI = 'SCSI'
UBUNTU_IMAGE = 'Ubuntu 14.04.2 HVM base (64bit)'
RHEL_IMAGE = 'CentOS 7 HVM base (64bit)'


class CloudStackVirtualMachine(virtual_machine.BaseVirtualMachine):
  """Object representing a Google Compute Engine Virtual Machine."""

  DEFAULT_ZONE = 'QC-1'
  DEFAULT_MACHINE_TYPE = '1vCPU.1GB'
  DEFAULT_TEMPLATE = 'Ubuntu 14.04.2 HVM base (64bit)'
  DEFAULT_USERNAME = 'cca-user'
  DEFAULT_PROJECT = 'PerfKitBenchmark'


  def __init__(self, vm_spec):
    """Initialize a CloudStack virtual machine.

    Args:
      vm_spec: virtual_machine.BaseVirtualMachineSpec object of the vm.
    """
    super(CloudStackVirtualMachine, self).__init__(vm_spec)
    self.project = self.DEFAULT_PROJECT
    self.network = cloudstack_network.CloudStackNetwork.GetNetwork(None)
    self.username = self.DEFAULT_USERNAME

    self.cs = util.CsClient(
        FLAGS.CS_API_URL,
        FLAGS.CS_API_KEY,
        FLAGS.CS_API_SECRET
    )



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
    # TODO: Create a public ip for the VM
    print "Create deps\n"
    pass

  def _DeleteDependencies(self):
    """Delete VM dependencies."""
    print "Delete deps\n"
    # TODO: Remove the keypair
    pass

  def _Create(self):
    """Create a GCE VM instance."""
    # TODO: Create VM

    print "-" * 30
    print "CREATE VM\n"

    project_id = self.cs.get_project_id("cloudops-Engineering")
    zone_id = self.cs.get_zone_id("QC-1")
    service_offering_id = self.cs.get_serviceoffering_id("1vCPU.1GB")
    template_id = self.cs.get_template_id(
        "Ubuntu 14.04.2 HVM base (64bit)",
        project_id
    )
    vpc_id = self.cs.get_vpc_id("syed-vpc", project_id)

    network_id = self.cs.get_network_id(
        "tier1",
        project_id,
        vpc_id
    )


    self._vm = self.cs.create_vm(
        self.name,
        zone_id,
        service_offering_id,
        template_id,
        [network_id],
        project_id
    )

    # TODO: get corret id
    self.id = self._vm['virtualmachine']['id']

    # TODO: Raise retryable excception if not able to create

  @vm_util.Retry()
  def _PostCreate(self):
    """Get the instance's data."""

    # assosiate the public ip created with the VMid
    network_interface = self._vm['virtualmachine']['nic'][0]
    self.internal_ip = network_interface['ipaddress']
    self.ip_address = None  # TODO should be public IP

  def _Delete(self):
    """Delete the VM instance."""
    # TODO: Delete the VM
    pass

  def _Exists(self):
    """Returns true if the VM exists."""
    # TODO: Check if VM exisits

  def CreateScratchDisk(self, disk_spec):
    """Create a VM's scratch disk.

    Args:
      disk_spec: virtual_machine.BaseDiskSpec object of the disk.
    """
    # TODO: Create a volume
    pass

  def GetLocalDisks(self):
    """Returns a list of local disks on the VM.

    Returns:
      A list of strings, where each string is the absolute path to the local
          disks on the VM (e.g. '/dev/sdb').
    """
    # TODO: Return list of local disks
    pass


class DebianBasedCloudStackVirtualMachine(CloudStackVirtualMachine,
                                          linux_vm.DebianMixin):
  DEFAULT_IMAGE = UBUNTU_IMAGE


class RhelBasedCloudStackVirtualMachine(CloudStackVirtualMachine,
                                        linux_vm.RhelMixin):
  DEFAULT_IMAGE = RHEL_IMAGE
