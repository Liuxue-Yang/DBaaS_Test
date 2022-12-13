import time
import random
import pytest
from explorer_auto.common.yaml_util import read_yaml_by_key
from explorer_auto.action.action_explorer import ActionExplorer
from explorer_auto.interface.interface_explorer import InterfaceExplorer

class Testicons:
    @pytest.mark.icons
    def test_Icons(self):
        # 新建图标组
        QA_random = random.randint(1,100000000)
        data = {
                "name":"new_group" + str(QA_random),
                "type":"svg"
                }
        icon_id_Group = InterfaceExplorer.add_Icon_Group(data).json()["data"]["id"]
        print(icon_id_Group)
        
        # 获取图标组列表并取出id
        icon_list = InterfaceExplorer.get_Icon_Group().json()["data"]["items"][-1]["id"]
        assert  icon_id_Group == icon_list

        # 编辑图标组名称
        data = {"name":"test"}
        InterfaceExplorer.put_Icon_Group(icon_id_Group,data)

        # 添加图标
        data = {"name":"icon-abnormal.svg","icon":"<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\">\n<path d=\"M16 8C16 12.4183 12.4183 16 8 16C3.58172 16 0 12.4183 0 8C0 3.58172 3.58172 0 8 0C12.4183 0 16 3.58172 16 8ZM8.88889 6.22222H7.11111V12.4444H8.88889V6.22222ZM8.88889 5.33333V3.55556H7.11111V5.33333H8.88889Z\" fill=\"black\"/>\n</svg>\n"}
        InterfaceExplorer.add_Icon(icon_id_Group,data)

        # 获取组内图标
        icon_id = InterfaceExplorer.get_Icon(icon_id_Group).json()["data"]["items"][-1]["id"]
        print(icon_id)

        # 删除组内图标
        InterfaceExplorer.delete_Icon(icon_id_Group,icon_id)

        # 删除图标组并获取列表
        InterfaceExplorer.delete_Icon_Group(icon_id_Group)
        icon_list = InterfaceExplorer.get_Icon_Group().json()["data"]["items"][-1]["id"]
        assert  icon_id_Group != icon_list