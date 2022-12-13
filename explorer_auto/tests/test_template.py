import time
import random
import pytest
from explorer_auto.common.yaml_util import read_yaml_by_key
from explorer_auto.action.action_explorer import ActionExplorer
from explorer_auto.interface.interface_explorer import InterfaceExplorer

class Testtemplate:

    @pytest.mark.template
    def test_template(self):
        ngql = {"gql":"show spaces;"}

        # 添加模板
        data = {
                "name":"test",
                "space":"nba",
                "description":"test_测试",
                "content":"show spaces",
                "result":"show spaces",
                "marks":[]
                    }
                
        InterfaceExplorer.add_template(data)

        # 查询模板列表
        template_id = InterfaceExplorer.get_template().json()["data"]["items"][0]["id"]

        # 更新模板
        data = {
                "name":"test_put",
                "space":"nba",
                "description":"test_测试",
                "content":"show spaces",
                "result":"show spaces",
                "marks":[]
                    }
        InterfaceExplorer.put_template(template_id,data)

        # 删除模板
        InterfaceExplorer.delete_template(template_id)

        # 注销Explorer
        InterfaceExplorer.interface_disconnect()