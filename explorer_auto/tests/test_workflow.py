import time
import random
import json
import pytest
from explorer_auto.common.yaml_util import read_yaml_by_key
from explorer_auto.action.action_explorer import ActionExplorer
from explorer_auto.interface.interface_explorer import InterfaceExplorer

class Testworkflow:
    
    @pytest.mark.workflow
    def test_controller(self):
        # 将错误graphd密码写入dag
        data = {"method":"POST","path":"/config/graphd/pwd","requestData":"{\"graphdIp\":\"192.168.8.48:9669\",\"userName\":\"root\",\"password\":\"ISXxte7HukUok89Oi2a+HrvUz0h5JzKyZwbLePbMfphCset/bU123j1Kvw0TpgdTF6Rg2ylQQf4ohQ5WiDVGmEXAHAlk63yPZiq9WlgOYA9lIdsS7huSc0w949hE+u9r21ezSmB3QBhKNBh4/NwQfvT8e3+PVmiVIRcZ2epvP/fv6w=\"}"}
        graphd_dag_code = InterfaceExplorer.add_controller(data).json()["code"]
        assert 50004002 == graphd_dag_code

        # 将graphd密码写入dag
        data = {"method":"POST","path":"/config/graphd/pwd","requestData":"{\"graphdIp\":\"192.168.8.48:9669\",\"userName\":\"root\",\"password\":\"ENbRIaDCsD7PngbDIKREozznA19tl1PfsRG/5CWot8zcSf/JjGqRniFPbIgNt8Hq2S5KL5bPv4CKv+UdcnkWeazuIbgcuhgkeMd9MUaXNi2Zn4mteAfKd/JvqghVS+P+tZocI74KLoKAE0dbtnGVgvgMe1IfMD7vvp4oDCdVGcI=\"}"}
        graphd_dag = InterfaceExplorer.add_controller(data).json()["message"]
        assert 'Success' == graphd_dag

        # ping dag 已启动
        dag = InterfaceExplorer.get_dag().json()["data"]["ok"]
        assert True == dag

    @pytest.mark.workflow
    def test_config(self):
        # 配置错误hdfs并获取配置详情中hdfs name 进行判断
        data = {"value":"{\"hdfs\":[{\"name\":\"1\",\"value\":\"1\",\"user\":\"1\"}],\"metad\":\"\",\"graphd_timeout\":60000,\"metad_timeout\":60000,\"storaged_timeout\":60000,\"isCompleted\":true}"}
        InterfaceExplorer.put_config(data)
        str = InterfaceExplorer.get_config().json()['data']['schema']
        hdfs = json.loads(str)["hdfs"][0]["name"]
        assert "1" == hdfs

        # 更新配置 无hdfs并查看列表判断 global
        data = {"value":"{\"hdfs\":[],\"metad\":\"\",\"graphd_timeout\":60000,\"metad_timeout\":60000,\"storaged_timeout\":60000,\"isCompleted\":true}"}
        InterfaceExplorer.put_config(data)
        name = InterfaceExplorer.get_config().json()["data"]["name"]
        assert 'global' == name

        # 添加hdfs至配置并获取配置详情中的hdfs name 进行判断
        data = {"value":"{\"hdfs\":[{\"name\":\"test\",\"value\":\"hdfs://192.168.8.168:9000/ll_test\",\"user\":\"root\"}],\"metad\":\"\",\"graphd_timeout\":60000,\"metad_timeout\":60000,\"storaged_timeout\":60000,\"isCompleted\":true}"}
        InterfaceExplorer.put_config(data)
        str = InterfaceExplorer.get_config().json()['data']['schema']
        hdfs = json.loads(str)["hdfs"][0]["name"]
        assert "test" == hdfs
        print('-------------更新成功')

    @pytest.mark.workflow
    def test_workflow(self):
        # 创建一个空workflow并获取列表取出workflow_id进行校验
        QA_random = random.randint(1,1000000)
        data = {"name":'QA_空workflow_' + str(QA_random),"schema":""}
        workflow_id = InterfaceExplorer.interface_create_workflow(data).json()["data"]["id"]
        workflow_list = InterfaceExplorer.interface_get_workflow().json()["data"]["items"][0]["id"]
        assert workflow_id == workflow_list

        # # for循环创建200个workflow
        # for i in range(200):
        #     data = {"name":'QA_创建多个workflow_' + str(QA_random),"schema":""}
        #     workflow_id = InterfaceExplorer.interface_create_workflow(data).json()["data"]["id"]
        #     workflow_list = InterfaceExplorer.interface_get_workflow().json()["data"]["items"][0]["id"]
        #     assert workflow_id == workflow_list
    
        # 创建workflow Schema参数填写、特殊字符、小数点并获取列表取出workflow_id进行校验
        data = {"name":'QA_！@#￥%&￥*@·、/特殊Schema_' + str(QA_random),"schema":"219837219847.123.24.123！@#！@%@！%！@.中文、英文"}
        workflow_id = InterfaceExplorer.interface_create_workflow(data).json()["data"]["id"]
        workflow_list = InterfaceExplorer.interface_get_workflow().json()["data"]["items"][0]["id"]
        assert workflow_id == workflow_list

        # 更新workflow 添加APSP算法
        data = {"name":"更新添加APSP_" + str(QA_random),"schema":"{\"datasources\":[{\"type\":\"hdfs\",\"name\":\"test\",\"spec\":{\"user\":\"root\",\"url\":\"hdfs://192.168.8.168:9000/ll_test\"}}],\"tasks\":[{\"id\":\"analytics_apsp_1\",\"name\":\"APSP\",\"clusterSize\":1,\"type\":\"analytics_apsp\",\"spec\":{\"vtype\":\"string\",\"processes\":1,\"threads\":3,\"nebula_input_edges\":\"follow,serve\",\"nebula_input_edges_props\":\",\"},\"graph\":{\"x\":278,\"y\":-1,\"params\":[],\"groupName\":\"path\",\"input\":[{\"name\":\"src\",\"dataType\":\"string\"},{\"name\":\"dst\",\"dataType\":\"string\"},{\"name\":\"weight\",\"dataType\":\"string\"}],\"output\":[{\"name\":\"src\",\"dataType\":\"string\"},{\"name\":\"dst\",\"dataType\":\"string\"},{\"name\":\"count\",\"dataType\":\"string\"}]},\"datasink\":{\"type\":\"hdfs\",\"spec\":{\"url\":\"${test}/analytics/${job_id}/tasks/${task_id}/\",\"hdfsName\":\"test\",\"hdfsPath\":\"/analytics/${job_id}/tasks/${task_id}/\",\"user\":\"root\"}},\"datasource\":{\"type\":\"nebula\",\"spec\":{\"type\":\"nebula\",\"space\":\"demo_basketballplayer\",\"graphd\":\"192.168.8.48:9669\",\"user\":\"root\",\"graphd_timeout\":60000,\"metad_timeout\":60000,\"storaged_timeout\":60000}}}],\"deps\":[]}"}
        InterfaceExplorer.interface_update_workflow(workflow_id,data)
        tasks = InterfaceExplorer.interface_get_id_workflow(workflow_id).json()["data"]["schema"]
        tasks_id = json.loads(tasks)["tasks"][0]["id"]
        assert "analytics_apsp_1" == tasks_id

        # 更新workflow 删除apsp算法
        data = {"name":"更新删除APSP_" + str(QA_random),"schema":"12342112312"}
        InterfaceExplorer.interface_update_workflow(workflow_id,data)
        tasks = InterfaceExplorer.interface_get_id_workflow(workflow_id).json()["data"]["schema"]
        assert '12342112312' == tasks

        # 更新workflow Schema参数中填写特殊字符 小数点 浮点数
        data = {"name":'QA_！@#￥%&￥*@·、/特殊Schema_' + str(QA_random),"schema":"219837219847.123.24.123！@#！@%@！%！@.中文、英文"}
        InterfaceExplorer.interface_update_workflow(workflow_id,data)
        tasks = InterfaceExplorer.interface_get_id_workflow(workflow_id).json()["data"]["schema"]
        assert "219837219847.123.24.123！@#！@%@！%！@.中文、英文" == tasks

        # 查看空workflow版本
        code1 = InterfaceExplorer.interface_history_workflow(workflow_id).json()["code"]
        assert 0 == code1

        # 更新workflow运行job生成版本后查看workflow版本
        data = {"name":"QA_生成版本_" + str(QA_random),"schema":"{\"datasources\":[{\"type\":\"hdfs\",\"name\":\"test\",\"spec\":{\"user\":\"root\",\"url\":\"hdfs://192.168.8.168:9000/ll_test\"}}],\"tasks\":[{\"id\":\"analytics_apsp_1\",\"name\":\"APSP\",\"clusterSize\":1,\"type\":\"analytics_apsp\",\"spec\":{\"vtype\":\"string\",\"processes\":1,\"threads\":3,\"nebula_input_edges\":\"follow,serve\",\"nebula_input_edges_props\":\",\"},\"graph\":{\"x\":278,\"y\":-1,\"params\":[],\"groupName\":\"path\",\"input\":[{\"name\":\"src\",\"dataType\":\"string\"},{\"name\":\"dst\",\"dataType\":\"string\"},{\"name\":\"weight\",\"dataType\":\"string\"}],\"output\":[{\"name\":\"src\",\"dataType\":\"string\"},{\"name\":\"dst\",\"dataType\":\"string\"},{\"name\":\"count\",\"dataType\":\"string\"}]},\"datasink\":{\"type\":\"hdfs\",\"spec\":{\"url\":\"${test}/analytics/${job_id}/tasks/${task_id}/\",\"hdfsName\":\"test\",\"hdfsPath\":\"/analytics/${job_id}/tasks/${task_id}/\",\"user\":\"root\"}},\"datasource\":{\"type\":\"nebula\",\"spec\":{\"type\":\"nebula\",\"space\":\"demo_basketballplayer\",\"graphd\":\"192.168.8.48:9669\",\"user\":\"root\",\"graphd_timeout\":60000,\"metad_timeout\":60000,\"storaged_timeout\":60000}}}],\"deps\":[]}"}
        InterfaceExplorer.interface_update_workflow(workflow_id,data)
        data = {"flowId":workflow_id}
        InterfaceExplorer.interface_add_job(data)
        time.sleep(2)
        data = {"name":"QA_回滚版本_" + str(QA_random),"schema":"{\"datasources\":[{\"type\":\"hdfs\",\"name\":\"test\",\"spec\":{\"user\":\"root\",\"url\":\"hdfs://192.168.8.168:9000/ll_test\"}}],\"tasks\":[{\"id\":\"analytics_pagerank_1\",\"name\":\"PageRank\",\"clusterSize\":1,\"type\":\"analytics_pagerank\",\"spec\":{\"iterations\":\"10\",\"is_directed\":\"true\",\"eps\":\"0.0001\",\"damping\":\"0.85\",\"vtype\":\"string\",\"processes\":1,\"threads\":3,\"nebula_input_edges\":\"follow,serve\",\"nebula_input_edges_props\":\",\"},\"graph\":{\"x\":495,\"y\":263.76668548583984,\"params\":[],\"groupName\":\"nodeImportance\",\"input\":[{\"name\":\"src\",\"dataType\":\"string\"},{\"name\":\"dst\",\"dataType\":\"string\"}],\"output\":[{\"name\":\"vid\",\"dataType\":\"string\"},{\"name\":\"value\",\"dataType\":\"string\"}]},\"datasink\":{\"type\":\"hdfs\",\"spec\":{\"url\":\"${test}/analytics/${job_id}/tasks/${task_id}/\",\"hdfsName\":\"test\",\"hdfsPath\":\"/analytics/${job_id}/tasks/${task_id}/\",\"user\":\"root\"}},\"datasource\":{\"type\":\"nebula\",\"spec\":{\"type\":\"nebula\",\"space\":\"demo_basketballplayer\",\"graphd\":\"192.168.8.48:9669\",\"user\":\"root\",\"graphd_timeout\":60000,\"metad_timeout\":60000,\"storaged_timeout\":60000}}}],\"deps\":[]}"}
        InterfaceExplorer.interface_update_workflow(workflow_id,data)
        data = {"flowId":workflow_id}
        InterfaceExplorer.interface_add_job(data)
        history1 = InterfaceExplorer.interface_history_workflow(workflow_id).json()["data"]["items"][0]["id"]
        history2 = InterfaceExplorer.interface_history_workflow(workflow_id).json()["data"]["items"][1]["id"]
        print(history1,history2)

        # 回滚存在版本的workflow并通过tasks进行判断
        history_id = history2
        print(history_id)
        InterfaceExplorer.interface_repair_history_workflow(workflow_id,history_id)
        tasks = InterfaceExplorer.interface_get_id_workflow(workflow_id).json()["data"]["schema"]
        tasks_id = json.loads(tasks)["tasks"][0]["id"]
        assert "analytics_apsp_1" == tasks_id

        # 回滚不存在的版本并判读Schema为空
        InterfaceExplorer.interface_repair_history_workflow(workflow_id,123456)
        schema = InterfaceExplorer.interface_get_id_workflow(workflow_id).json()["data"]["schema"]
        assert '' == schema

        # 删除workflow并获取workflow列表调用id进行判断
        InterfaceExplorer.interface_delete_workflow(workflow_id)
        workflow_list = InterfaceExplorer.interface_get_workflow().json()["data"]["items"][0]["id"]
        assert workflow_list != workflow_id

        # 删除不存在的workflow
        code = InterfaceExplorer.interface_delete_workflow(123532141234).json()["code"]
        assert 0 == code

    @pytest.mark.workflow
    def test_job(self):
        # 存在workflow 起始task无需参数	单tasks_不输入参数 创建并执行成功
        workflow_id = read_yaml_by_key("不需要参数_单tasks_不输入参数", "/conf/tmp.yaml")
        print(workflow_id)
        data = {"flowId":str(workflow_id)}
        job_id =  InterfaceExplorer.interface_add_job(data).json()["data"]["id"]
        ActionExplorer.action_check_job_task_status(job_id, 2)

        # 存在workflow 起始task无需参数	单tasks_输入参数,创建失败(参数错误)
        workflow_id = read_yaml_by_key("不需要参数_单tasks_输入参数","/conf/tmp.yaml")
        data = {"id":str(workflow_id),"input":{"query_1":{"1234":"1234"}}}
        print(data)
        message = InterfaceExplorer.interface_add_job(data).json()["message"]
        assert 'ErrParam' == message

        # 存在workFlow，起始task需要输入一个参数 输入不同类型的参数并通过job列表判断创建成功
        workflow_id = read_yaml_by_key("需要1个参数_单tasks_不同类型参数","/conf/tmp.yaml")
        data = {"id":str(workflow_id),"input":{"analytics_sssp_7":{"root":12.01},"query_8":{"True":"True","\"你好，新年快乐\"":"\"你好，新年快乐~~~\"","\"123\":\"root\"":"\"123\":\"root\"","2022-8-19":"2022-8-19"},"analytics_bfs_9":{"root":12},"analytics_bnc_11":{"chosen":1},"analytics_jaccard_similarity_12":{"ids1":11,"ids2":1}}}
        job_id = InterfaceExplorer.interface_submit_job(workflow_id,data).json()["data"]["id"]
        job_list = InterfaceExplorer.interface_get_jobs().json()["data"]["items"][0]["id"]
        assert job_list == job_id

        # 存在workFlow，起始task需要输入一个参数 不输入参数创建失败
        workflow_id = read_yaml_by_key("需要1个参数_单tasks_不输入参数","/conf/tmp.yaml")
        data = {"id":str(workflow_id)}
        job_code = InterfaceExplorer.interface_submit_job(workflow_id,data).json()["code"]
        assert 50004002 == job_code

        # 存在workflow，其实task需要多参数 输入不同类型参数并创建成功
        workflow_id = read_yaml_by_key("需要多个参数_单tasks_不同类型参数",'/conf/tmp.yaml')
        data = {"id":str(workflow_id),"input":{"query_13":{"“你好”":"\"你好\"","1.0000000000000001":"1.00000000001","1000-01-01/9999-12":"1000-01-01/9999-12","True":"True","@！￥！@#%！#@%@！@#":"#!@$!#@%#@!%!#@%!#@"}}}
        job_id = InterfaceExplorer.interface_submit_job(workflow_id,data).json()["data"]["id"]
        job_list = InterfaceExplorer.interface_get_jobs().json()["data"]["items"][0]["id"]
        assert job_list == job_id

        # 存在workflow，其实task需要多参数 不输入参数并创建失败
        workflow_id = read_yaml_by_key("需要多个参数_单tasks_不输入参数",'/conf/tmp.yaml')
        data = {"id":str(workflow_id),"input":{}}
        job_code = InterfaceExplorer.interface_submit_job(workflow_id,data).json()["code"]
        assert 50004002 == job_code
        
        # 创建job_不同组件的参数输入
        workflow_id = read_yaml_by_key("创建job_不同组件的参数输入",'/conf/tmp.yaml')
        data = {"id":str(workflow_id),"input":{"query_1":{"\"你好\"":"你好"}}}
        job_id = InterfaceExplorer.interface_submit_job(workflow_id,data).json()["data"]["id"]
        job_list = InterfaceExplorer.interface_get_jobs().json()["data"]["items"][0]["id"]
        assert job_id == job_list
        
        # 创建job_输入参数格式参数非法校验
        workflow_id = read_yaml_by_key("创建job_输入参数非法格式,/conf/tmp.yaml")
        data = {"id":str(workflow_id),"input":{"analytics_bfs_3":{"root":123}}}
        code = InterfaceExplorer.interface_submit_job(workflow_id,data).json()["code"]
        assert 50004001 == code


        # job为等待状态
        workflow_id = read_yaml_by_key("创建job_不同组件的参数输入",'/conf/tmp.yaml')
        data = {"id":str(workflow_id),"input":{"query_1":{"\"你好\"":"你好"}}}
        job_id = InterfaceExplorer.interface_submit_job(workflow_id,data).json()["data"]["id"]
        job_list = InterfaceExplorer.interface_get_jobs().json()["data"]["items"][0]["id"]
        assert job_id == job_list
        job_list = InterfaceExplorer.interface_get_jobs().json()["data"]["items"][0]["status"]
        assert 0 == job_list


        # job状态为停止
        ctlJobId = InterfaceExplorer.interface_get_id_job(job_id).json()["data"]["ctlJobId"]
        print(ctlJobId)
        data = {"method":"POST","path":"/job/{}/cancel".format(ctlJobId)}
        InterfaceExplorer.interface_stop_job(data)
        job_status = InterfaceExplorer.interface_get_job_detail(job_id).json()["data"]["status"]
        assert 4 == job_status

        # job状态循环获取状态 过程中状态为运行中 最终状态为成功
        workflow_id = read_yaml_by_key("创建job_不同组件的参数输入",'/conf/tmp.yaml')
        data = {"id":str(workflow_id),"input":{"query_1":{"\"你好\"":"你好"}}}
        job_id = InterfaceExplorer.interface_submit_job(workflow_id,data).json()["data"]["id"]
        ActionExplorer.action_check_job_task_status(job_id, 2)

        # 停止不存在的job
        data = {"method":"POST","path":"/job/{}/cancel".format('12344566678687687687576')}
        code = InterfaceExplorer.interface_stop_job(data).json()["code"]
        assert 50004002 == code

        # 获取不存在的job详情
        code = InterfaceExplorer.interface_get_job_detail(123456).json()["code"]
        assert 50004001 == code
        
        # 场景TP-AP-TP 并循环获取job状态为成功
        workflow_id = read_yaml_by_key("TP-AP-TP",'/conf/tmp.yaml')
        data = {"flowId":str(workflow_id)}
        job_id = InterfaceExplorer.interface_add_job(data).json()["data"]["id"]
        ActionExplorer.action_check_job_task_status(job_id, 2)

        # 场景AP-AP-AP 并循环获取job状态为成功
        workflow_id = read_yaml_by_key("AP-AP-AP",'/conf/tmp.yaml')
        data = {"flowId":str(workflow_id)}
        job_id = InterfaceExplorer.interface_add_job(data).json()["data"]["id"]
        ActionExplorer.action_check_job_task_status(job_id, 2)

        # 场景18个tasks 同时运行 并循环获取job状态为成功
        workflow_id = read_yaml_by_key("所有tasks",'/conf/tmp.yaml')
        data = {"flowId":str(workflow_id)}
        job_id = InterfaceExplorer.interface_add_job(data).json()["data"]["id"]
        ActionExplorer.action_check_job_task_status(job_id, 2)

        # 获取tasks_id结果 条数
        ctlJobId = InterfaceExplorer.interface_get_id_job(job_id).json()["data"]["ctlJobId"]
        data = {"jobId":job_id,"taskId":"query_1","type":"hdfs","params":{"hdfsPath":"hdfs://192.168.8.168:9000/ll_test/analytics/{}/tasks/query_1/".format(ctlJobId),"username":"root"}}
        result1 = InterfaceExplorer.interface_result_job(data).json()["data"]["items"][0]
        assert 1 == len(result1)

        # TP返回结果为空
        workflow_id = read_yaml_by_key("workflow_列数", "/conf/tmp.yaml")
        data = {"flowId":str(workflow_id)}
        job_id = InterfaceExplorer.interface_add_job(data).json()["data"]["id"]
        ctlJobId = InterfaceExplorer.interface_get_id_job(job_id).json()["data"]["ctlJobId"]
        data = {"jobId":job_id,"taskId":"{}".format("query_5"),"type":"hdfs","params":{"hdfsPath":"hdfs://192.168.8.168:9000/ll_test/analytics/{}/tasks/{}/".format(ctlJobId,"query_5"),"username":"root"}}
        print(data)
        result = InterfaceExplorer.interface_result_job(data)
        ActionExplorer.action_check_job_task_status(job_id, 2)
        assert 0 == len(result.json()["data"]["items"])

        # TP结果为一列
        data = {"jobId":job_id,"taskId":"{}".format("query_5"),"type":"hdfs","params":{"hdfsPath":"hdfs://192.168.8.168:9000/ll_test/analytics/{}/tasks/query_6/".format(ctlJobId),"username":"root"}}
        result = InterfaceExplorer.interface_result_job(data)
        assert 1 == len(result.json()["data"]["items"][0])

        # TP结果为两列
        data = {"jobId":job_id,"taskId":"{}".format("query_7"),"type":"hdfs","params":{"hdfsPath":"hdfs://192.168.8.168:9000/ll_test/analytics/{}/tasks/query_7/".format(ctlJobId),"username":"root"}}
        result = InterfaceExplorer.interface_result_job(data)
        assert 2 == len(result.json()["data"]["items"][0])

        # TP输出队列不同格式
        data = {"jobId":job_id,"taskId":"{}".format("query_8"),"type":"hdfs","params":{"hdfsPath":"hdfs://192.168.8.168:9000/ll_test/analytics/{}/tasks/query_8/".format(ctlJobId),"username":"root"}}
        result = InterfaceExplorer.interface_result_job(data)
        assert 6 == len(result.json()["data"]["items"][0])

        # AP结果为两列
        data = {"jobId":job_id,"taskId":"{}".format("analytics_pagerank_9"),"type":"hdfs","params":{"hdfsPath":"hdfs://192.168.8.168:9000/ll_test/analytics/{}/tasks/analytics_pagerank_9/".format(ctlJobId),"username":"root"}}
        result = InterfaceExplorer.interface_result_job(data)
        assert 2 == len(result.json()["data"]["items"][0])

        # AP结果为四列
        data = {"jobId":job_id,"taskId":"{}".format("analytics_degree_with_time_10"),"type":"hdfs","params":{"hdfsPath":"hdfs://192.168.8.168:9000/ll_test/analytics/{}/tasks/analytics_degree_with_time_10/".format(ctlJobId),"username":"root"}}
        result = InterfaceExplorer.interface_result_job(data)
        assert 4 == len(result.json()["data"]["items"][0])

        # AP结果为一列
        data = {"jobId":job_id,"taskId":"{}".format("analytics_triangle_count_11"),"type":"hdfs","params":{"hdfsPath":"hdfs://192.168.8.168:9000/ll_test/analytics/{}/tasks/analytics_triangle_count_11/".format(ctlJobId),"username":"root"}}
        result = InterfaceExplorer.interface_result_job(data)
        assert 1 == len(result.json()["data"]["items"][0])

        # AP结果为三列
        data = {"jobId":job_id,"taskId":"{}".format("analytics_apsp_12"),"type":"hdfs","params":{"hdfsPath":"hdfs://192.168.8.168:9000/ll_test/analytics/{}/tasks/analytics_apsp_12/".format(ctlJobId),"username":"root"}}
        result = InterfaceExplorer.interface_result_job(data)
        assert 3 == len(result.json()["data"]["items"][0])

        # # 循环创建200个job
        # for i in range(200):
        #     workflow_id = read_yaml_by_key("TP-AP-TP",'/conf/tmp.yaml')
        #     data = {"flowId":str(workflow_id)}
        #     job_code = InterfaceExplorer.interface_add_job(data).json()["code"]
        #     assert 0 == job_code