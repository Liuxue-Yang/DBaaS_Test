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
        # 当前密码为nebula  **~!@#$ 包含特殊字符 空格 登录成功
        auth = 'Bearer WyJyb290IiwibmVidWxhICAqKn4hQCMkIl0='
        data = {"address":"192.168.8.48","port":9669}
        message = InterfaceExplorer.interface_connect_failed(auth,data).json()["message"]
        assert 'Success' == message,"判断状态为Success"
        InterfaceExplorer.interface_disconnect()

        # 使用错误密码登录失败
        auth = 'Bearer WyJyb290IiwiMTIzIl0='
        data = {"address":"192.168.8.48","port":9669}
        code = InterfaceExplorer.interface_connect_failed(auth,data).json()["code"]
        assert 40004000 == code

        #ip、port为空 登录失败
        auth = 'Bearer WyJyb290IiwiMTIzIl0='
        data = {"address":"","port":" "}
        code = InterfaceExplorer.interface_connect_failed(auth,data).json()["code"]
        assert 40004001 == code