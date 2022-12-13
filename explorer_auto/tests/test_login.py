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
        # 当前密码为nebula~!@#$%^&* 包含特殊字符 空格 登录成功
        ngql = {"gql":"ALTER USER `root` WITH PASSWORD 'nebula~!@#$%^&*';"}
        InterfaceExplorer.Single_ngql(ngql)
        time.sleep(10)
        auth = 'Bearer WyJyb290IiwibmVidWxhfiFAIyQlXiYqIl0='
        data = {"address":"192.168.8.131","port":9669}
        code = InterfaceExplorer.interface_connect_failed(auth,data).json()["code"]
        assert 0 == code

        # 使用错误密码登录失败
        auth = 'Bearer WyJyb290IiwiMTIzIl0='
        data = {"address":"192.168.8.131","port":9669}
        code = InterfaceExplorer.interface_connect_failed(auth,data).json()["code"]
        assert 40004000 == code

        #ip、port为空 登录失败
        auth = 'Bearer WyJyb290IiwiMTIzIl0='
        data = {"address":"","port":" "}
        code = InterfaceExplorer.interface_connect_failed(auth,data).json()["code"]
        assert 40004001 == code

        # 成功登录
        ngql = {"gql":"ALTER USER `root` WITH PASSWORD 'nebula';"}
        InterfaceExplorer.Single_ngql(ngql)
        time.sleep(10)
        auth = 'Bearer WyJyb290IiwibmVidWxhIl0='
        data = {"address":"192.168.8.131","port":9669}
        code = InterfaceExplorer.interface_connect_failed(auth,data).json()["code"]
        assert 0 == code