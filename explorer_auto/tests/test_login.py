import time
import random
import pytest
import base64
from explorer_auto.common.yaml_util import read_yaml_by_key
from explorer_auto.action.action_explorer import ActionExplorer
from explorer_auto.interface.interface_explorer import InterfaceExplorer


class Testlogin:
    
    @pytest.mark.login
    def test_login(self):
        # 特密码存在特殊字符
        ngql = {"gql":"ALTER USER `root` WITH PASSWORD 'nebula~!@#$%^&*';"}
        InterfaceExplorer.Single_ngql(ngql)
        time.sleep(10)
        userName = "root"
        password = "nebula~!@#$%^&*"
        data = {"address":"192.168.8.131","port":9669}
        code = InterfaceExplorer.interface_connect_failed(userName,password,data).json()["code"]
        assert 0 == code

        # 登录失败、错误密码、错误用户名
        userName = "QA"
        password = "Error"
        data = {"address":"192.168.8.131","port":9669}
        code = InterfaceExplorer.interface_connect_failed(userName,password,data).json()["code"]
        assert 0 != code

        # #ip、port为空 登录失败
        userName = "root"
        password = "nebula"
        data = {"address":"","port":" "}
        code = InterfaceExplorer.interface_connect_failed(userName,password,data).json()["code"]
        assert 40004001 == code

        # 使用更改后的密码登录
        ngql = {"gql":"ALTER USER `root` WITH PASSWORD 'nebula';"}
        InterfaceExplorer.Single_ngql(ngql)
        time.sleep(10)
        userName = "root"
        password = "nebula"
        data = {"address":"192.168.8.131","port":9669}
        code = InterfaceExplorer.interface_connect_failed(userName,password,data).json()["code"]
        assert 0 == code