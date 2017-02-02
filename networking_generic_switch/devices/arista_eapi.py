# Copyright 2016 Paweł Socha pawel.socha@intel.com
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import pyeapi

from networking_generic_switch.devices import GenericSwitchDevice
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class AristaEapi(GenericSwitchDevice):

    def __init__(self, device_cfg):
        super(AristaEapi, self).__init__(device_cfg)

        self.node = pyeapi.connect(
            transport=self.config.get('transport', 'http'),
            username=self.config['username'],
            password=self.config['password'],
            host=self.config['ip'],
            port=self.config.get('port', 80),
            return_node=True,
        )

    def add_network(self, segmentation_id, network_id):
        vlan = self.node.api('vlans')
        vlan.create(str(segmentation_id))
        vlan.set_name(str(segmentation_id), str(network_id))

    def del_network(self, segmentation_id):
        vlan = self.node.api('vlans')
        vlan.delete(str(segmentation_id))

    def plug_port_to_network(self, segmentation_id, port):
        ports = self.node.api('switchports')
        ports.set_access_vlan(str(port), str(segmentation_id))
