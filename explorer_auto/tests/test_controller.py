import time
import random
import pytest
from explorer_auto.common.yaml_util import read_yaml_by_key
from explorer_auto.action.action_explorer import ActionExplorer
from explorer_auto.interface.interface_explorer import InterfaceExplorer

class Testcontroller:

    @pytest.mark.controller
    def test_controller(self):
        data = {"method":"POST","path":"/config/graphd/pwd","requestData":"{\"graphdIp\":\"192.168.8.131:9669\",\"userName\":\"root\",\"password\":\"ISXxte7HukUok89Oi2a+HrvUz0h5JzKyZwbLePbMfphCset/bUj1Kvw0TpgdTF6Rg2ylQQf4ohQ5WiDVGmEXAHAlk63yPZiq9WlgOYA9lIdsS7huSc0w949hE+u9r21ezSmB3QBhKNBh4/NwQfvT8e3+PVmiVIRcZ2epvP/fv6w=\"}"}
        InterfaceExplorer.add_controller(data)

        InterfaceExplorer.get_dag()

        data = {"method":"GET","path":"/config/analytics/cluster"}
        InterfaceExplorer.get_controller(data)