import sys
import paramiko

from delfin import context
from unittest import TestCase, mock
from delfin.tests.unit.drivers.hpe.hpe_msa import test_constans
from delfin.drivers.utils.ssh_client import SSHPool
from delfin.drivers.hpe.hpe_msa.ssh_handler import SSHHandler
from delfin.drivers.hpe.hpe_msa.hpe_msastor import HpeMsaStorDriver

sys.modules['delfin.cryptor'] = mock.Mock()

ACCESS_INFO = {
    "storage_id": "kkk",
    "ssh": {
        "host": "110.143.132.231",
        "port": 22,
        "username": "user",
        "password": "pass",
        "pub_key": "ddddddddddddddddddddddddd"
    }
}


class TestHpeMsaStorageDriver(TestCase):

    @mock.patch.object(SSHPool, 'do_exec')
    @mock.patch.object(SSHPool, 'get')
    def test_list_ports(self, mock_ssh_get, mock_control):
        mock_ssh_get.return_value = {paramiko.SSHClient()}
        mock_control.side_effect = [test_constans.LIST_PORTS]
        ports = HpeMsaStorDriver(**ACCESS_INFO).list_ports(context)
        self.assertEqual(ports, test_constans.ports_result)

    @mock.patch.object(SSHPool, 'do_exec')
    @mock.patch.object(SSHPool, 'get')
    def test_list_disks(self, mock_ssh_get, mock_control):
        mock_ssh_get.return_value = {paramiko.SSHClient()}
        mock_control.side_effect = [test_constans.LIST_DISKS]
        disks = HpeMsaStorDriver(**ACCESS_INFO).list_disks(context)
        self.assertEqual(disks, test_constans.disks_result)

    @mock.patch.object(SSHPool, 'do_exec')
    @mock.patch.object(SSHPool, 'get')
    def test_list_controllers(self, mock_ssh_get, mock_control):
        mock_ssh_get.return_value = {paramiko.SSHClient()}
        mock_control.side_effect = [test_constans.LIST_CONTROLLERS]
        controller = HpeMsaStorDriver(**ACCESS_INFO).\
            list_controllers(context)
        self.assertEqual(controller, test_constans.controller_result)

    @mock.patch.object(SSHPool, 'do_exec')
    @mock.patch.object(SSHPool, 'get')
    def test_list_volumes(self, mock_ssh_get, mock_control):
        mock_ssh_get.return_value = {paramiko.SSHClient()}
        mock_control.side_effect = [test_constans.LIST_VOLUMES,
                                    test_constans.LIST_POOLS]
        volumes = HpeMsaStorDriver(**ACCESS_INFO).list_volumes(context)
        self.assertEqual(volumes, test_constans.volume_result)

    @mock.patch.object(SSHPool, 'do_exec')
    @mock.patch.object(SSHPool, 'get')
    @mock.patch.object(SSHHandler, 'list_storage_pools')
    @mock.patch.object(SSHHandler, 'list_storage_disks')
    @mock.patch.object(SSHHandler, 'list_storage_volume')
    def test_list_storage(self, mock_system, mock_ssh_get,
                          mock_pools, mock_disks, mock_volume):
        mock_volume.side_effect = [test_constans.LIST_SYSTEM,
                                   test_constans.LIST_VISION]
        mock_disks.return_value = {paramiko.SSHClient()}
        mock_pools.side_effect = [test_constans.pools_result]
        mock_ssh_get.side_effect = [test_constans.disks_result]
        mock_system.side_effect = [test_constans.volume_result]
        system = HpeMsaStorDriver(**ACCESS_INFO).get_storage(context)
        self.assertEqual(system, test_constans.system_info)

    @mock.patch.object(SSHPool, 'do_exec')
    @mock.patch.object(SSHPool, 'get')
    @mock.patch.object(SSHHandler, 'list_storage_volume')
    def test_list_storage_pools(self, mock_ssh_get, mock_control,
                                mock_volume):
        mock_ssh_get.return_value = test_constans.volume_result
        mock_control.side_effect = {paramiko.SSHClient()}
        mock_volume.side_effect = [test_constans.LIST_POOLS]
        pools = HpeMsaStorDriver(**ACCESS_INFO).list_storage_pools(context)
        self.assertEqual(pools, test_constans.pools_result)

    @mock.patch.object(SSHPool, 'do_exec')
    @mock.patch.object(SSHPool, 'get')
    def test_list_alerts(self, mock_ssh_get, mock_control):
        query_para = None
        mock_ssh_get.return_value = {paramiko.SSHClient()}
        mock_control.side_effect = [test_constans.LIST_ERROR]
        alerts = HpeMsaStorDriver(**ACCESS_INFO).list_alerts(query_para)
        self.assertEqual(alerts, test_constans.error_result)
