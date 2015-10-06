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
"""Module containing classes related to GCE disks.

Disks can be created, deleted, attached to VMs, and detached from VMs.
Use 'gcloud compute disk-types list' to determine valid disk types.
"""

from perfkitbenchmarker import disk
from perfkitbenchmarker import flags
from perfkitbenchmarker.cloudstack import util

FLAGS = flags.FLAGS

flags.DEFINE_string('cs_disk_offering',
                    '20GB - 100 IOPS Min.',
                    'Name of the network offering')



class CloudStackDisk(disk.BaseDisk):
  """Object representing a Cloudstack Disk."""

  DEFAULT_DISK_OFFERING = "20GB - 100 IOPS Min."

  def __init__(self, disk_spec, name, zone, project, image=None):
    super(CloudStackDisk, self).__init__(disk_spec)

    self.cs = util.CsClient(
        FLAGS.CS_API_URL,
        FLAGS.CS_API_KEY,
        FLAGS.CS_API_SECRET
    )

    self.attached_vm_name = None
    self.attached_vm_id = None
    self.image = image
    self.name = name

    self.zone = zone
    cs_zone = self.cs.get_zone(zone)
    assert cs_zone, "Zone not found"

    self.zone_id = cs_zone['id']

    self.project = project
    cs_project = self.cs.get_project(project)
    assert cs_project, "Project not found"

    self.project_id = cs_project['id']

    disk_offering = self.cs.get_disk_offering(self.DEFAULT_DISK_OFFERING)
    assert disk_offering, "Disk offering not found"

    self.disk_offering_id = disk_offering['id']

  def _Create(self):
    """Creates the disk."""

    volume = self.cs.create_volume(self.name,
                                   self.disk_offering_id,
                                   self.zone_id,
                                   self.project_id)

    assert volume, "Unable to create volume"
    self.volume_id = volume['id']


  def _Delete(self):
    """Deletes the disk."""
    self.cs.delete_volume(self.volume_id)


  def _Exists(self):
    """Returns true if the disk exists."""
    vol = self.cs.get_volume(self.name)

    if vol:
        return True

    return False

  def Attach(self, vm):
    """Attaches the disk to a VM.

    Args:
      vm: The GceVirtualMachine instance to which the disk will be attached.
    """
    self.cs.attach_volume(self.volume_id, vm.id)

  def Detach(self):
    """Detaches the disk from a VM."""

    self.cs.detach_volume(self.volume_id)

  def GetDevicePath(self):
    """Returns the path to the device inside the VM."""
    pass
