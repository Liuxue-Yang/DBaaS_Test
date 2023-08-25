import asyncio
import time
import random
import pytest
import base64
from explorer_auto.common.yaml_util import read_yaml_by_key
from explorer_auto.action.action_explorer import ActionExplorer
from explorer_auto.interface.interface_explorer import InterfaceExplorer


class Testlogin:
    
    @pytest.mark.login
    # def test_login(self):
    #     # 特密码存在特殊字符
    #     ngql = {"gql":"ALTER USER `root` WITH PASSWORD 'nebula~!@#$%^&*';"}
    #     asyncio.run(InterfaceExplorer.test_WebSocket_ngql(ngql))
    #     time.sleep(10)
    #     userName = "root"
    #     password = "nebula~!@#$%^&*"
    #     data = {"address":"192.168.8.48","port":9669}
    #     code = InterfaceExplorer.interface_connect_failed(userName,password,data).json()["code"]
    #     assert 0 == code

    #     # 登录失败、错误密码、错误用户名
    #     userName = "QA"
    #     password = "Error"
    #     data = {"address":"192.168.8.48","port":9669}
    #     code = InterfaceExplorer.interface_connect_failed(userName,password,data).json()["code"]
    #     assert 0 != code

    #     # #ip、port为空 登录失败
    #     userName = "root"
    #     password = "nebula"
    #     data = {"address":"","port":" "}
    #     code = InterfaceExplorer.interface_connect_failed(userName,password,data).json()["code"]
    #     assert 40004001 == code

    #     # 使用更改后的密码登录
    #     ngql = {"gql":"ALTER USER `root` WITH PASSWORD 'nebula';"}
    #     asyncio.run(InterfaceExplorer.test_WebSocket_ngql(ngql)).json()
    #     time.sleep(10)
    #     userName = "root"
    #     password = "nebula"
    #     data = {"address":"192.168.8.48","port":9669}
    #     code = InterfaceExplorer.interface_connect_failed(userName,password,data).json()["code"]
    #     assert 0 == code
    def test_login(self):
        login_data = [
            # 正确的密码登录
            {
                'res':{"email":"dbaas-test@vesoft.com","password":"Nebula123"},
                'req':0
            },
            # 错误的密码
            # {
            #     'res':{"email":"dbaas-test@vesoft.com","password":"123"},
            #     'req':40001021
            # },
            
        ]
        for i in login_data:
            data = i['res']
            code = i['req']
            code_req = InterfaceExplorer.interface_connect_login(data).json()["code"]
            print(code_req)
            assert code == code_req
            
        InterfaceExplorer.interface_info()
        InterfaceExplorer.interface_projects_get()
        data_name ={"name":"test","platform":"AWS"}
        InterfaceExplorer.interface_projects_post(data_name) 
        id = InterfaceExplorer.interface_projects_get().json()["data"]["items"][-1]["id"]
        print(id)
        InterfaceExplorer.interface_projects_delete(id)
        InterfaceExplorer.interface_projects_get()