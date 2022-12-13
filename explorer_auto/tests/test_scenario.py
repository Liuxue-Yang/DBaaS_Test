import pytest
from explorer_auto.common.yaml_util import read_yaml_by_key
from explorer_auto.action.action_explorer import ActionExplorer
from explorer_auto.interface.interface_explorer import InterfaceExplorer

class TestScenario:
    
    @pytest.mark.scenario
    def test_submit_job_no_params(self):
        # 获取无参数workflow的id
        workflow_id = read_yaml_by_key("no_params_workflow", "/conf/tmp.yaml")
        # case 1. 提交job不指定data, job提交失败，提示参数错误
        data = ""
        InterfaceExplorer.interface_submit_job(workflow_id,data,default_assert=False)
        
        # case 2. 提交job执行参数, job提交失败，提示参数错误
        data = {
            "input" : {
                "query_1": "11"
            }
        }
        InterfaceExplorer.interface_submit_job(workflow_id,data,default_assert=False)
        
        # case 3. 提交job input格式不正确, job提交失败，提示参数错误
        data = {
            "input" : ""
        }
        InterfaceExplorer.interface_submit_job(workflow_id,data,default_assert=False)
        

        # case 4. 提交job input为空, job提交成功,作业成功运行
        data = {
            "input" : {}
        }
        result = InterfaceExplorer.interface_submit_job(workflow_id,data)
        job_id= result.json()["data"]["id"]
        ActionExplorer.action_check_job_task_status(job_id, 2)

    @pytest.mark.scenario
    def test_submit_job_one_params_one_task(self):
        # 获取1个task需要一个参数的workflow的id
        workflow_id = read_yaml_by_key("one_params_one_task_workflow", "/conf/tmp.yaml")
        
        # # case 1. 提交job，输入参数为空, job提交失败，提示参数错误
        # data = {
        #     "input" : {
        #     }
        # }
        # InterfaceExplorer.interface_submit_job(workflow_id,data,default_assert=False)
        
        # # case 2. 提交job input中未包含需要参数的task, job提交失败，提示参数错误
        # data = {
        #     "input" : {
        #         "task_id": {"input1": "aaa"}
        #     }
        # }
        # InterfaceExplorer.interface_submit_job(workflow_id,data,default_assert=False)

        # # case 3. 提交job input包含的参数格式与预期的不一致（预期string、实际输入int）, job提交失败, 提示参数错误
        # data = {
        #     "input" : {
        #         "query_1": 3
        #     }
        # }
        # InterfaceExplorer.interface_submit_job(workflow_id,data,default_assert=False)

        # # case 4. 提交job input包含正确的task和不正确的task(task_id不存在), job提交失败, 提示参数错误
        # data = {
        #     "input" : {
        #         "query_1": {"input0":"player101"},
        #         "query_2": {"input0" :"player101"}
        #     }
        # }
        # InterfaceExplorer.interface_submit_job(workflow_id,data,default_assert=False)

        # # case 5. 提交job input包含正确的task和不正确的task(task_id存在但是无入参), job提交失败, 提示参数错误
        # data = {
        #     "input" : {
        #         "query_1": {"input0":"player101"},
        #         "analytics_apsp_2": {"input0" :"player101"}
        #     }
        # }
        # InterfaceExplorer.interface_submit_job(workflow_id,data,default_assert=False)

        # # case 7. 提交job input包含正确的task(但是多了一个入参), job提交失败, 提示参数错误
        # data = {
        #     "input" : {
        #         "query_1": {"input0":"player101","input1":"111"}
                
        #     }
        # }
        # InterfaceExplorer.interface_submit_job(workflow_id,data,default_assert=False)


        # case 8. 提交job的参数格式与预期的一致, job提交成, job运行成功
        data = {
            "input" : {
                "query_1": {
                    "input0": "player102"
                }
            }
        }
        result = InterfaceExplorer.interface_submit_job(workflow_id,data)
        job_id= result.json()["data"]["id"]
        ActionExplorer.action_check_job_task_status(job_id, 2)

    @pytest.mark.scenario
    def test_params_TP_data_type(self):
        # 获取TP_参数类型测试的workflow的ID
        workflow_id = read_yaml_by_key("tp_data_type", "/conf/tmp.yaml")

        # # case1：不传必填参数，task运行失败
        # print("case1：不传必填参数，task运行失败")
        # data = {
        #     "input" :{}
        # }
        # InterfaceExplorer.interface_submit_job(workflow_id,data,default_assert=False)

        # # case2: 两个task需要参数，只传入一个task的参数（完整的参数），task运行失败
        # print("case2: 两个task需要参数，只传入一个task的参数（完整的参数），task运行失败")
        # data = {
        #     "input" :{
        #         # 字符串、list、整数
        #         "query_1":{
        #             "string": "Tim Duncan",
        #             "list": "player101\", \"player102",
        #             "int": 34
        #         }
        #     }
        # }
        # InterfaceExplorer.interface_submit_job(workflow_id,data,default_assert=False)

        # # case3：两个task需要参数，两个都传参，1个传入不完整的参数，task运行失败
        # print("case3：两个task需要参数，两个都传参，1个传入不完整的参数，task运行失败")
        # data = {
        #     "input" :{
        #         # 字符串、list、整数
        #         "query_1":{
        #             "string": "Tim Duncan",
        #             "list": "player101\", \"player102"
        #         }
        #         ,
        #         # 小数，日期
        #         "query_2":{
        #             "date": "2022-01-01",
        #             "float": 34.1,
        #             "datetime": "2017-03-04 22:30:40",
        #             "boolean": True
        #         },
        #     }
        # }
        # InterfaceExplorer.interface_submit_job(workflow_id,data,default_assert=False)

        # case4：多个task，传入完整的参数，task运行成功
        print("case4：多个task，传入完整的参数，task运行成功")
        data = {
            "input" :{
                # 字符串、list、整数
                "query_1":{
                    "string": "Tim Duncan",
                    "list": "player101\", \"player102",
                    "int": 34
                }
                ,
                # 小数，日期，datetime，boolean
                "query_2":{
                    "date": "2022-01-01",
                    "float": 34.1,
                    "datetime": "2017-03-04 22:30:40",
                    "boolean": "True"
                },
            }
        }
        result = InterfaceExplorer.interface_submit_job(workflow_id,data)
        job_id= result.json()["data"]["id"]
        ActionExplorer.action_check_job_task_status(job_id, 2)

    @pytest.mark.scenario
    def test_params_AP_data_type(self):
        # 获取TP_参数类型测试的workflow的ID
        workflow_id = read_yaml_by_key("ap_data_type", "/conf/tmp.yaml")
        
        # # 不输入必填参数，应该执行失败
        # data = {
        #     "input" :{
        #     }
        # }
        # result = InterfaceExplorer.interface_submit_job(workflow_id,data,default_assert=False)

        # 输入正确的参数，执行成功
        data = {
            "input" :{
                "analytics_sssp_1" :{"root":"player101"}, 
                "analytics_bnc_2" :{"chosen":"player103"}, 
                "analytics_bfs_3" :{"root":"player103"}, 
                "analytics_jaccard_similarity_4" :{"ids1": "100,101","ids2":"102,103"}
            }
        }
        result = InterfaceExplorer.interface_submit_job(workflow_id,data)
        job_id= result.json()["data"]["id"]
        ActionExplorer.action_check_job_task_status(job_id, 2)
    
    @pytest.mark.scenario
    def test_params_component_deps(self):
        # 获取TP_参数类型测试的workflow的ID
        workflow_id = read_yaml_by_key("component_deps", "/conf/tmp.yaml")

        # case 1:  都输入参数时，使用手动输入的值，job运行成功
        data = {
            "input":{
                "analytics_sssp_2":{"root":"team204"},
                "analytics_bnc_3":{"chosen":"team208"}
            }
        }
        result = InterfaceExplorer.interface_submit_job(workflow_id,data)
        job_id= result.json()["data"]["id"]
        ActionExplorer.action_check_job_task_status(job_id, 2)

        # case 2: 配置了上游的不输入参数，使用上游的结果，job运行成功
        data = {
            "input":{
                
                "analytics_bnc_3":{"chosen":"team208"}
            }
        }
        

        # case 3: 未配置上游的不输入参数，job运行失败
        data = {
            "input":{
            }
        }
        result = InterfaceExplorer.interface_submit_job(workflow_id,data)
        job_id= result.json()["data"]["id"]
        ActionExplorer.action_check_job_task_status(job_id, 3)

    @pytest.mark.scenario
    def test_sample_result_rows(self):
        # 1. submit job
        workflow_id = read_yaml_by_key("no_params_workflow", "/conf/tmp.yaml")
        data = { 
             "input": {}
            }
        result = InterfaceExplorer.interface_submit_job(workflow_id,data)
        job_id = result.json()["data"]["id"]

        # 2. 判断job是否运行完成
        job_status = ActionExplorer.action_check_job_task_status(job_id, 2)
        
        # 3. 获取hdfs的结果，判断默认值是否为10
        result = InterfaceExplorer.interface_get_task_result(job_id,"query_1")
        assert 10 == len(result.json()["data"]["items"])
        
        # 4. 获取hdfs的结果，指定返回结果为1，判断是否生效
        result_2 = InterfaceExplorer.interface_get_task_result(job_id,"analytics_sssp_2",params="limit=1")
        # 校验返回的条数是否为10
        assert 1 == len(result_2.json()["data"]["items"])

        

    @pytest.mark.scenario
    def test_sample_result_column(self):
        # 1. submit job
        workflow_id = read_yaml_by_key("result_column", "/conf/tmp.yaml")
        data = { 
             "input": {}
            }
        result = InterfaceExplorer.interface_submit_job(workflow_id,data)
        job_id = result.json()["data"]["id"]

        # 2. 判断job是否运行完成
        job_status = ActionExplorer.action_check_job_task_status(job_id, 2)
        
        # 3. 获取job的结果，判断返回列是否正确
        # a. TP返回结果为空
        result = InterfaceExplorer.interface_get_task_result(job_id,"query_5")
        assert 0 == len(result.json()["data"]["items"])
        # b. TP返回1列
        result = InterfaceExplorer.interface_get_task_result(job_id,"query_6")
        assert 1 == len(result.json()["data"]["items"][0])
        result = InterfaceExplorer.interface_get_task_result(job_id,"query_7")
        assert 2 == len(result.json()["data"]["items"][0])
        result = InterfaceExplorer.interface_get_task_result(job_id,"query_8")
        assert 6 == len(result.json()["data"]["items"][0])
        result = InterfaceExplorer.interface_get_task_result(job_id,"analytics_apsp_12")
        assert 3 == len(result.json()["data"]["items"][0])
        result = InterfaceExplorer.interface_get_task_result(job_id,"analytics_pagerank_9")
        assert 2 == len(result.json()["data"]["items"][0])
        result = InterfaceExplorer.interface_get_task_result(job_id,"analytics_degree_with_time_10")
        assert 4 == len(result.json()["data"]["items"][0])
        result = InterfaceExplorer.interface_get_task_result(job_id,"analytics_triangle_count_11")
        assert 1 == len(result.json()["data"]["items"][0])
        result = InterfaceExplorer.interface_get_task_result(job_id,"analytics_apsp_12","limit=500")
        assert 500 == len(result.json()["data"]["items"])
        result = InterfaceExplorer.interface_get_task_result(job_id,"analytics_apsp_12","limit=1000")
        assert 794 == len(result.json()["data"]["items"])
        
    @pytest.mark.scenario
    def test_sample_result_get_failure(self):
        # jobID不存在
        InterfaceExplorer.interface_get_task_result(11111111111000,"analytics_apsp_12","limit=1000",default_assert=False)

        # jobId存在，taskId不存在
        workflow_id = read_yaml_by_key("result_column", "/conf/tmp.yaml")
        InterfaceExplorer.interface_get_task_result(workflow_id,"test1111","limit=1000",default_assert=False)

        # jobId是其它人的
        workflow_id = read_yaml_by_key("result_column", "/conf/tmp.yaml")
        InterfaceExplorer.interface_get_task_result(2529257662,"query_1","limit=1000",default_assert=False)


    # @pytest.mark.scenario
    # def test_batch(self):
    #     # workflow_id = read_yaml_by_key("one_params_multiple_task_workflow", "/conf/tmp.yaml")
    #     # data = { 
    #     #     "input":{
    #     #     "query_1":{
    #     #         "input0": "player101",
    #     #         "input1": 4
    #     #         }
    #     #     }
    #     # }
    #     i = 100
    #     while i:
    #     #    InterfaceExplorer.interface_submit_job(workflow_id,data)
    #         InterfaceExplorer.interface_cancel_job(i)
    #         i=i-1
    #         if i == 29755:
    #             break

        