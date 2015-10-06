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

FLAGS = flags.FLAGS


class CloudStackDisk(disk.BaseDisk):
  """Object representing a Cloudstack Disk."""

  def __init__(self, disk_spec, name, zone, project, image=None):
    super(CloudStackDisk, self).__init__(disk_spec)
    self.attached_vm_name = None
    self.image = image
    self.name = name
    self.zone = zone
    self.project = project

  def _Create(self):
    """Creates the disk."""
    pass

  def _Delete(self):
    """Deletes the disk."""
    pass

  def _Exists(self):
    """Returns true if the disk exists."""
    return False

  def Attach(self, vm):
    """Attaches the disk to a VM.

    Args:
      vm: The GceVirtualMachine instance to which the disk will be attached.
    """
    pass

  def Detach(self):
    """Detaches the disk from a VM."""
    pass

  def GetDevicePath(self):
    """Returns the path to the device inside the VM."""
    pass
