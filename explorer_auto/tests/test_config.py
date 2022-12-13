import time
import random
import pytest
from explorer_auto.common.yaml_util import read_yaml_by_key
from explorer_auto.action.action_explorer import ActionExplorer
from explorer_auto.interface.interface_explorer import InterfaceExplorer

class Testconfig:

    @pytest.mark.config
    def test_config(self):

        data = {"value":"{\"hdfs\":[],\"metad\":\"\",\"graphd_timeout\":60000,\"metad_timeout\":60000,\"storaged_timeout\":60000,\"isCompleted\":true}"}
        InterfaceExplorer.put_config(data)
        InterfaceExplorer.get_config()

        data = {"value":"{\"hdfs\":[{\"name\":\"test\",\"value\":\"hdfs://192.168.8.48:9000\",\"user\":\"root\"}],\"metad\":\"\",\"graphd_timeout\":60000,\"metad_timeout\":60000,\"storaged_timeout\":60000,\"isCompleted\":false}"}
        InterfaceExplorer.put_config(data)
        InterfaceExplorer.get_config()
