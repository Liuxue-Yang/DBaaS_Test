import base64
import csv
import random
from time import sleep

import pytest
from explorer_auto.common.yaml_util import read_yaml_by_key, write_yaml_by_key
from explorer_auto.interface.interface_explorer import InterfaceExplorer


class ActionExplorer:
    def action_connect():
        # get login info:
        graphd_ip = read_yaml_by_key("graphd_ip") 
        graphd_port = read_yaml_by_key("graphd_port") 
        userName = read_yaml_by_key("graphd_username")
        password = read_yaml_by_key("graphd_password")

        # Encrypted auth information
        auth_info = '["{}","{}"]'.format(userName,password).encode()
        auth_info = base64.b64encode(auth_info)
        auth = "Bearer "+ auth_info.decode('UTF-8')
        
        # data
        data = {
            "address": graphd_ip,
            "port": graphd_port
        }
        login_info = InterfaceExplorer.interface_connect(auth, data)

        
    def action_ceate_workflow(workflow_name, workflow_dag):
        data = {
            "name": workflow_name,
            "schema": ""
        }

        result = InterfaceExplorer.interface_create_workflow(data)
        workflow_id = result.json()["data"]["id"]
        a = {workflow_name : int(workflow_id)}
        print(a)
        write_yaml_by_key(a,"/conf/tmp.yaml")

        data = {
            "name": workflow_name,
            "schema": workflow_dag
        }

        result = InterfaceExplorer.interface_update_workflow(workflow_id,data)
        

    # 校验job_task状态
    def action_check_job_task_status(job_id, expect_task_status):
        print("开始校验{}作业运行下task状态与预期状态是否一致".format(job_id))
        # step2: 等待作业运行,task的运行需要时间，等待1分钟，超过一分钟抛错;
        i = 1
        while i:
            print("状态校验中")
            result = InterfaceExplorer.interface_get_id_job(job_id)
            job_status = result.json()["data"]["status"]
            # 如果等待次数大于20（即1分钟），或者job的状态为完成状态，跳出循环
            if(i == 30 or job_status > 1):
                break
            sleep(3)
            i = i+1
        assert job_status == expect_task_status,"task状态与预期状态不一致，请查看日志分析原因~"