import time
import os
import json
import random
import pytest
from explorer_auto.common.yaml_util import read_yaml_by_key
from explorer_auto.action.action_explorer import ActionExplorer
from explorer_auto.interface.interface_explorer import InterfaceExplorer

class Testfiles:

    @pytest.mark.files
    def test_files(self):
        # 相对路径
        path = 'explorer_auto/csv'
        # 转换为绝对路径
        abs_path = os.path.abspath(path)
        # 获取相对路径内所有文件
        files = os.listdir(abs_path)
        # 循环文件
        for file in files:
            # 拼接文件的绝对路径
            file_path = os.path.join(abs_path, file)
            # 打印文件路径
            print(file_path)
            code = InterfaceExplorer.import_add_csv(str(file_path)).json()["code"]
            assert 0 == code
        print(files)

        # 调取列表 循环判断文件名称
        json_data  = InterfaceExplorer.import_get_csv().json()["data"]["list"]
        for i in range(0, len(files)):
            assert files[i] == json_data[i]['name']

        # 校验列数、行数
        json_data = InterfaceExplorer.import_get_csv().json()
        assert 1 == len(json_data["data"]["list"][5]["content"][0])   # 1列
        assert 10 == len(json_data["data"]["list"][2]["content"][0])  # 10列 
        assert 50 == len(json_data["data"]["list"][8]["content"][0])  # 10列
        assert 1 == len(json_data["data"]["list"][6]["content"])  # 1行
        assert 3 == len(json_data["data"]["list"][3]["content"])  # 10行只展示3行

        # 循环删除所有文件
        for i in range(0, len(files)):
            csv_name = files[i]
            code = InterfaceExplorer.import_delete_csv(csv_name).json()["code"]
            assert 0 == code

        # 删除不存在和已删除的文件'
        csv_name = ["123456","100mb_player"]
        for i in range(0,len(csv_name)):
            code = InterfaceExplorer.import_delete_csv(csv_name[i]).json()["code"]
            assert code != 0