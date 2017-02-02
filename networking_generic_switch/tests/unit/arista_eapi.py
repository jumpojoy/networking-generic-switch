# Copyright 2016 Mirantis, Inc.
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

import mock

from networking_generic_switch.devices import arista_eapi
from networking_generic_switch.tests.unit.netmiko import test_netmiko_base


class TestNetmikoAristaEapi(test_netmiko_base.NetmikoSwitchTestBase):

    def setUp(self):
        super(TestNetmikoAristaEapi, self).setUp()
        self.switch = self._make_switch_device()
        self.p_connect = mock.Mock()
        patcher = mock.patch('pyeapi.connect' return_value=self.connect)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.napi = mock.MagicMock()
        self.p_connect.node.api.return_value = self.napi

    def _make_switch_device(self):
        device_cfg = {'username': 'user',
                      'password': 'password',
                      'ip': 'arista.eapi'}
        return arista_eapi.AristaEpi(device_cfg)

    def test_add_network(self):
        self.switch.add_network(33, '0ae071f5-5be9-43e4-80ea-e41fefe85b21')
        self.napi.assert_called_once_with('vlans')
        self.napi.create.assert_called_once_with('33')
        self.napi.set_name.assert_called_once_with('33', '0ae071f5-5be9-43e4-80ea-e41fefe85b21')
        

    def test_del_network(self):
        self.switch.del_network(33)
        self.napi.assert_called_once_with('vlans')
        self.napi.delete.assert_called_once_with('33')

    def test_plug_port_to_network(self):
        self.switch.plug_port_to_network(3333, 33)
        self.napi.assert_called_once_with('switchports')
        self.napi.set_access_vlan('33', '3333')
