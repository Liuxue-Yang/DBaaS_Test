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
        # files = os.listdir(abs_path)
        files = [
        '100mb_player.csv',
        '10mb_player.csv', 
        '10列_player.csv', 
        '10行数据_player.csv', 
        '1mb_player.csv', 
        '1列_player.csv', 
        '1行数据_player.csv', 
        '50mb_player.csv', 
        '50列_player.csv', 
        '上传多个文件1_player.csv', 
        '上传多个文件2_player.csv', 
        '上传多个文件3_player.csv', 
        '特殊字符_中英文_长度_2%$%$^player.csv', 
        '非csv文件'
        ]
        # 循环文件
        for file in files:
            # 拼接文件的绝对路径
            file_path = os.path.join(abs_path, file)
            # 打印文件路径
            print(file_path)
            csv_name = file
            code = InterfaceExplorer.import_add_csv(str(file_path),csv_name).json()["code"]
            assert 0 == code

        # 调取列表 循环判断文件名称
        csv_data = InterfaceExplorer.import_get_csv()
        json_data  = csv_data.json()["data"]["list"]
        for i in range(0, len(files)):
            print(json_data[i]['name'])
            assert files[i] == json_data[i]['name']

        # 校验列数、行数
        json_data = csv_data.json()
        A = json_data["data"]["list"][5]["sample"].strip().split('\r\n') # 1列数据
        B = json_data["data"]["list"][2]["sample"].strip().split('\r\n') # 10列数据
        C = json_data["data"]["list"][8]["sample"].strip().split('\r\n') # 50列数据
        D = json_data["data"]["list"][6]["sample"].strip().split('\r\n') # 1行数据
        E = json_data["data"]["list"][3]["sample"].strip().split('\r\n') # 10行只展示5行
        assert 1 == len(A[0].strip().split(','))
        assert 10 == len(B[0].strip().split(','))
        assert 50 == len(C[0].strip().split(','))
        assert 1 == len(D)  # 1行
        assert 5 == len(E)  # 默认最多展示5行数据

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