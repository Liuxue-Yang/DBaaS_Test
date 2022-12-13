import time
import random
import pytest
from explorer_auto.common.yaml_util import read_yaml_by_key
from explorer_auto.action.action_explorer import ActionExplorer
from explorer_auto.interface.interface_explorer import InterfaceExplorer

class TestSmoke:

 
    """
    冒烟用例1：提交无参数的job，并查询运行结果（hdfs、graph）
    """
    # @pytest.mark.smoke
    # def test_smoke_01_no_params(self):
    #     # 1. submit job
    #     workflow_id = read_yaml_by_key("no_params_workflow", "/conf/tmp.yaml")
    #     data = { 
    #          "input": {}
    #         }
    #     result = InterfaceExplorer.interface_submit_job(workflow_id,data)
    #     job_id = result.json()["data"]["id"]
        
    #     # 2. get job list
    #     query_params ={
            
    #         "pageSize" : 2,
    #         "page" : 1,
    #         "filter" : "{\"name\": \"no_params_workflow\",\"orderByCreateTime\":\"desc\"}"
            
    #     }   
    #     job_list = InterfaceExplorer.interface_get_jobs(query_params)
    #     assert job_id == job_list.json()["data"]["items"][0]["id"]

    #     # 3. get job_detail 
    #     print("获取job详情")
    #     job_detail = InterfaceExplorer.interface_get_job_detail(job_id)

        
    #     # 4. get task result
    #     job_status = ActionExplorer.action_check_job_task_status(job_id, 2)
    #     result_1 = InterfaceExplorer.interface_get_task_result(job_id,"query_1")
    #     # 校验返回的条数是否为10
    #     assert 10 == len(result_1.json()["data"]["items"])
    #     # TODO:校验读取hdfs返回的内容与预期的是否一致

    #     result_2 = InterfaceExplorer.interface_get_task_result(job_id,"analytics_sssp_2")
    #     # 校验返回的条数是否为10
    #     assert 10 == len(result_2.json()["data"]["items"])
    #     # TODO:校验读取nebula返回的内容与预期的是否一致

        
    #     # 5. disconnect
    #     result = InterfaceExplorer.interface_disconnect()

    #     # 6. Check whether disconnect is valid
    #     InterfaceExplorer.interface_submit_job(workflow_id, data,default_assert=False)
    #     InterfaceExplorer.interface_cancel_job(job_id, default_assert=False)
    #     InterfaceExplorer.interface_get_jobs(default_assert=False)
    #     InterfaceExplorer.interface_get_jobs_by_workflow(workflow_id, default_assert=False)
    #     InterfaceExplorer.interface_get_job_detail(job_id, default_assert=False)
    #     InterfaceExplorer.interface_get_task_result(job_id, "query_1", default_assert=False)
    #     ActionExplorer.action_connect()

    @pytest.mark.smoke
    def test_smoke_02_one_params_one_task_workflow(self):
        # 1. submit job
        workflow_id = read_yaml_by_key("one_params_one_task_workflow", "/conf/tmp.yaml")
        data = {  
            "input":{
                "query_1":{
                    "input0": "player101"
                    }
                }
        }
        print(data)
        print(type(data))
        result = InterfaceExplorer.interface_submit_job(workflow_id,data)
        job_id = result.json()["data"]["id"]

        
    #     # 2. get job list
    #     query_params ={
    #         #"filter" : "{\"name\": \"123\"}",
    #         "pageSize" : 20,
    #         "page" : 1
    #     }   
    #     job_list = InterfaceExplorer.interface_get_jobs(query_params)
    #     assert job_id == job_list.json()["data"]["items"][0]["id"]

    #     # 3. get job list by workflow
    #     query_params ={
    #         # "filter" : "{\"name\": \"one_params_one_task_workflow\"}",
    #         "pageSize" : 20,
    #         "page" : 1
    #     }   
    #     job_list = InterfaceExplorer.interface_get_jobs_by_workflow(workflow_id,query_params)
    #     assert job_id == job_list.json()["data"]["items"][0]["id"]
        
        
    #     ActionExplorer.action_check_job_task_status(job_id, 2)
       


    # @pytest.mark.smoke
    # def test_smoke_03_one_params_multiple_task_workflow(self):
    #     # 1. submit job
    #     workflow_id = read_yaml_by_key("one_params_multiple_task_workflow", "/conf/tmp.yaml")
    #     data = { 
    #         "input":{
    #         "query_1":{
    #             "input0": "player101",
    #             "input1": 4
    #             }
    #         }
    #     }
    #     result = InterfaceExplorer.interface_submit_job(workflow_id,data)
    #     job_id = result.json()["data"]["id"]

        # ActionExplorer.action_check_job_task_status(job_id, 2)
        
    # @pytest.mark.smoke
    # def test_smoke_04_multiple_params_multiple_task_workflow(self):
    #     # 1. submit job
    #     workflow_id = read_yaml_by_key("multiple_params_multiple_task_workflow", "/conf/tmp.yaml")
    #     data = { 
    #         "input":{
    #             "query_1":{
    #                 "input0": "player101",
    #                 "input1": 4,
    #             },
    #             "analytics_jaccard_similarity_2":{
    #                 "ids1": "palyer101,player102",
    #                 "ids2":"palyer111,player112"
    #             }
    #         }
    #     }
    #     result = InterfaceExplorer.interface_submit_job(workflow_id,data)
    #     job_id = result.json()["data"]["id"]
    #     ActionExplorer.action_check_job_task_status(job_id, 2)

    # @pytest.mark.smoke
    # def test_smoke_05_cancel_job(self):
    #      # 1. submit job
    #     workflow_id = read_yaml_by_key("sf100_workflow", "/conf/tmp.yaml")
    #     data = {
    #         "input" :{}
    #     }
    #     result = InterfaceExplorer.interface_submit_job(workflow_id,data)
    #     job_id = result.json()["data"]["id"]
        
    #     # 2. get job list
    #     job_list = InterfaceExplorer.interface_get_jobs()
    #     assert job_id == job_list.json()["data"]["items"][0]["id"]
    #     assert 2 > job_list.json()["data"]["items"][0]["status"]

    #     # 3. cancel job
    #     InterfaceExplorer.interface_cancel_job(job_id)

    #     # 4. get job detail
    #     job_detial = InterfaceExplorer.interface_get_job_detail(job_id)
    #     assert 4 == job_detial.json()["data"]["status"]
        
    #     # 5. get joblist by workflow
    #     job_detial = InterfaceExplorer.interface_get_jobs_by_workflow(workflow_id)
    #     assert 4 == job_detial.json()["data"]["items"][0]["status"]
    # @pytest.mark.smoke
    # def test_import(self):
    #     # 新建workflow
    #     data = {
    #         "name":"",
    #         "schema":"{\"datasources\":[{\"type\":\"hdfs\",\"name\":\"test\",\"spec\":{\"user\":\"root\",\"url\":\"hdfs://192.168.8.168:9000/ll_test\"}}],\"tasks\":[{\"id\":\"analytics_apsp_1\",\"name\":\"APSP\",\"clusterSize\":1,\"type\":\"analytics_apsp\",\"spec\":{\"nebula_input_edges\":\"Assessment passed,Capital dispersion,Capital inflow,First transaction,Risk control testing\",\"nebula_input_edges_props\":\",,,,\",\"vtype\":\"string\",\"processes\":1,\"threads\":3},\"graph\":{\"x\":360,\"y\":-40,\"groupName\":\"path\",\"input\":[{\"name\":\"src\",\"dataType\":\"string\"},{\"name\":\"dst\",\"dataType\":\"string\"},{\"name\":\"weight\",\"dataType\":\"string\"}],\"output\":[{\"name\":\"src\",\"dataType\":\"string\"},{\"name\":\"dst\",\"dataType\":\"string\"},{\"name\":\"count\",\"dataType\":\"string\"}]},\"datasink\":{\"type\":\"hdfs\",\"spec\":{\"url\":\"${test}/analytics/${job_id}/tasks/${task_id}/\",\"hdfsName\":\"test\",\"hdfsPath\":\"/analytics/${job_id}/tasks/${task_id}/\",\"user\":\"root\"}},\"datasource\":{\"type\":\"nebula\",\"spec\":{\"type\":\"nebula\",\"space\":\"Anti-money laundering\",\"graphd\":\"192.168.8.131:9669\",\"user\":\"root\",\"graphd_timeout\":60000,\"metad_timeout\":60000,\"storaged_timeout\":60000}}}],\"deps\":[]}"
    #     }
    #     workflow_id = InterfaceExplorer.interface_create_workflow(data).json()["data"]["id"]
    #     print(workflow_id)
        # # 更新 workflow
        # data = {
        #     "name":"",
        #     "schema":"jzirjiqwejrqwjekrljewqk)(#@!*$!)(#@*$%#)($*#@!)($*#@!)($"
        # }
        # InterfaceExplorer.interface_update_workflow(workflow_id,data)

        # # 查看历史版本
        # hestory_id = InterfaceExplorer.interface_history_workflow(workflow_id).json()["data"]["items"][0]["id"]
        # print(hestory_id)

        # # 查看workflow版本详情
        # InterfaceExplorer.interface_history_id_workflow(workflow_id,hestory_id)

        #回滚workflow版本
        # InterfaceExplorer.interface_repair_history_workflow(workflow_id,hestory_id)

        # 运行job
        # InterfaceExplorer.interface_add_job(workflow_id)

        # # 获取job列表
        # InterfaceExplorer.interface_get_job()

        # #查看job详情
        # job_id = 30
        # InterfaceExplorer.interface_get_id_job(job_id)

        # InterfaceExplorer.interface_rerun_job(job_id)

        # InterfaceExplorer.interface_delete_job(job_id)

        # data = {"jobId":job_id,"taskId":"analytics_pagerank_1","type":"hdfs","params":{"hdfsPath":"hdfs://192.168.8.168:9000/ll_test/analytics/30/tasks/analytics_pagerank_1/","username":"root"}}
        # InterfaceExplorer.interface_result_job(data)


        # 删除workflow
        # InterfaceExplorer.interface_delete_workflow(workflow_id)

        # # 上传文件
        # path = r'C:\\data_player.csv'
        # InterfaceExplorer.import_add_csv(path)
    
        # # 获取csv name
        # csv_name = InterfaceExplorer.import_get_csv().json()["data"]["list"][0]["name"]
        # print(csv_name)

        # # 删除csv
        # InterfaceExplorer.import_delete_csv(csv_name)

        # # 获取csv list
        # InterfaceExplorer.import_get_csv()


        # # 创建单个导入任务
        # data = {"config":{"version":"v2","description":"web console import","clientSettings":{"retry":3,"concurrency":10,"channelBufferSize":128,"space":"CC"
        #             ,"connection":{"user":"root","password":"nebula","address":"192.168.8.131:9669"}},"files":[{"path":"data_player.csv","failDataPath":"vertex_playerFail.csv","batchSize":60
        #                 ,"type":"csv","csv":{"withHeader":False,"withLabel":False},"schema":{"type":"vertex","vertex":{"vid":{"index":0,"type":"string"},"tags":[{"name":"player","props":[{"name":"age","type":"int","index":1},{"name":"name","type":"string","index":2}]}]}}}]},"name":"task-16690113825114"}
        # import_tasks_id = InterfaceExplorer.import_tasks(data).json()["data"]["id"]
        # print(import_tasks_id)

        # # 获取单个任务
        # status = InterfaceExplorer.import_tasks_get_id(import_tasks_id).json()["data"]["status"]
        # assert 'Running' == status

        # # 获取日志文件名称
        # InterfaceExplorer.import_log_csv(import_tasks_id)

        # # 获取日志内容
        # InterfaceExplorer.import_log(import_tasks_id)

        # # # 暂停导入任务
        # # InterfaceExplorer.import_tasks_stop(import_tasks_id)
        
        # # 获取导入列表
        # id = InterfaceExplorer.import_tasks_get().json()["data"]["list"][0]["id"]
        # assert import_tasks_id == id

        # # 删除导入任务
        # InterfaceExplorer.import_tasks_delete(import_tasks_id)
        # id = InterfaceExplorer.import_tasks_get().json()["data"]["list"][0]["id"]
        # assert import_tasks_id != id
        # print('删除成功')

        
        # # 创建多个任务
        # import_tasks = [ 
        #             {"config":{"version":"v2","description":"web console import","clientSettings":{"retry":3,"concurrency":10,"channelBufferSize":128,"space":"CC","connection":{"user":"root","password":"nebula","address":"192.168.8.131:9669"}},"files":[{"path":"vertex_player.csv","failDataPath":"vertex_playerFail.csv","batchSize":60,"type":"csv","csv":{"withHeader":False,"withLabel":False},"schema":{"type":"vertex","vertex":{"vid":{"index":0,"type":"string"},"tags":[{"name":"player","props":[{"name":"age","type":"int","index":1},{"name":"name","type":"string","index":2}]}]}}}]},"name":"task-16690113825114"}
        #             ,
        #             {"config":{"version":"v2","description":"web console import","clientSettings":{"retry":3,"concurrency":10,"channelBufferSize":128,"space":"CC","connection":{"user":"root","password":"nebula","address":"192.168.8.131:9669"}},"files":[{"path":"vertex_player.csv","failDataPath":"vertex_playerFail.csv","batchSize":60,"type":"csv","csv":{"withHeader":False,"withLabel":False},"schema":{"type":"vertex","vertex":{"vid":{"index":0,"type":"string"},"tags":[{"name":"player","props":[{"name":"age","type":"int","index":1},{"name":"name","type":"string","index":2}]}]}}}]},"name":"task-16690113825114"}
        #             ,
        #             {"config":{"version":"v2","description":"web console import","clientSettings":{"retry":3,"concurrency":10,"channelBufferSize":128,"space":"CC","connection":{"user":"root","password":"nebula","address":"192.168.8.131:9669"}},"files":[{"path":"vertex_player.csv","failDataPath":"vertex_playerFail.csv","batchSize":60,"type":"csv","csv":{"withHeader":False,"withLabel":False},"schema":{"type":"vertex","vertex":{"vid":{"index":0,"type":"string"},"tags":[{"name":"player","props":[{"name":"age","type":"int","index":1},{"name":"name","type":"string","index":2}]}]}}}]},"name":"task-16690113825114"}
        #             ,
        #             {"config":{"version":"v2","description":"web console import","clientSettings":{"retry":3,"concurrency":10,"channelBufferSize":128,"space":"CC","connection":{"user":"root","password":"nebula","address":"192.168.8.131:9669"}},"files":[{"path":"vertex_player.csv","failDataPath":"vertex_playerFail.csv","batchSize":60,"type":"csv","csv":{"withHeader":False,"withLabel":False},"schema":{"type":"vertex","vertex":{"vid":{"index":0,"type":"string"},"tags":[{"name":"player","props":[{"name":"age","type":"int","index":1},{"name":"name","type":"string","index":2}]}]}}}]},"name":"task-16690113825114"}
        #             ,
        #             {"config":{"version":"v2","description":"web console import","clientSettings":{"retry":3,"concurrency":10,"channelBufferSize":128,"space":"CC","connection":{"user":"root","password":"nebula","address":"192.168.8.131:9669"}},"files":[{"path":"vertex_player.csv","failDataPath":"vertex_playerFail.csv","batchSize":60,"type":"csv","csv":{"withHeader":False,"withLabel":False},"schema":{"type":"vertex","vertex":{"vid":{"index":0,"type":"string"},"tags":[{"name":"player","props":[{"name":"age","type":"int","index":1},{"name":"name","type":"string","index":2}]}]}}}]},"name":"task-16690113825114"}
        #             ,
        #             {"config":{"version":"v2","description":"web console import","clientSettings":{"retry":3,"concurrency":10,"channelBufferSize":128,"space":"CC","connection":{"user":"root","password":"nebula","address":"192.168.8.131:9669"}},"files":[{"path":"vertex_player.csv","failDataPath":"vertex_playerFail.csv","batchSize":60,"type":"csv","csv":{"withHeader":False,"withLabel":False},"schema":{"type":"vertex","vertex":{"vid":{"index":0,"type":"string"},"tags":[{"name":"player","props":[{"name":"age","type":"int","index":1},{"name":"name","type":"string","index":2}]}]}}}]},"name":"task-16690113825114"}
        #             ,
        #             {"config":{"version":"v2","description":"web console import","clientSettings":{"retry":3,"concurrency":10,"channelBufferSize":128,"space":"CC","connection":{"user":"root","password":"nebula","address":"192.168.8.131:9669"}},"files":[{"path":"vertex_player.csv","failDataPath":"vertex_playerFail.csv","batchSize":60,"type":"csv","csv":{"withHeader":False,"withLabel":False},"schema":{"type":"vertex","vertex":{"vid":{"index":0,"type":"string"},"tags":[{"name":"player","props":[{"name":"age","type":"int","index":1},{"name":"name","type":"string","index":2}]}]}}}]},"name":"task-16690113825114"}
        #             ,
        #             {"config":{"version":"v2","description":"web console import","clientSettings":{"retry":3,"concurrency":10,"channelBufferSize":128,"space":"CC","connection":{"user":"root","password":"nebula","address":"192.168.8.131:9669"}},"files":[{"path":"vertex_player.csv","failDataPath":"vertex_playerFail.csv","batchSize":60,"type":"csv","csv":{"withHeader":False,"withLabel":False},"schema":{"type":"vertex","vertex":{"vid":{"index":0,"type":"string"},"tags":[{"name":"player","props":[{"name":"age","type":"int","index":1},{"name":"name","type":"string","index":2}]}]}}}]},"name":"task-16690113825114"},
        #         ]

        # for data in import_tasks:
        #     print(data)
        #     InterfaceExplorer.import_tasks(data)
        #     print("--------创建多个任务成功")

        # # 执行单条语句
        # ngql = '{"gql":"use `sf1`"}'
        # InterfaceExplorer.Single_ngql(ngql)
        # # 批量执行语句
        # ngql = '{"gqls":["MATCH ()-[e:`HAS_CREATOR`]->() RETURN e LIMIT 10;","MATCH ()-[e:`HAS_INTEREST`]->() RETURN e LIMIT 10;","MATCH ()-[e:`CONTAINER_OF`]->() RETURN e LIMIT 10;","MATCH ()-[e:`HAS_MODERATOR`]->() RETURN e LIMIT 10;","MATCH ()-[e:`HAS_MEMBER`]->() RETURN e LIMIT 10;","MATCH ()-[e:`HAS_TAG`]->() RETURN e LIMIT 10;","MATCH ()-[e:`HAS_TYPE`]->() RETURN e LIMIT 10;","MATCH ()-[e:`IS_PART_OF`]->() RETURN e LIMIT 10;","MATCH ()-[e:`IS_LOCATED_IN`]->() RETURN e LIMIT 10;","MATCH ()-[e:`KNOWS`]->() RETURN e LIMIT 10;","MATCH ()-[e:`IS_SUBCLASS_OF`]->() RETURN e LIMIT 10;","MATCH ()-[e:`LIKES`]->() RETURN e LIMIT 10;","MATCH ()-[e:`REPLY_OF`]->() RETURN e LIMIT 10;","MATCH ()-[e:`STUDY_AT`]->() RETURN e LIMIT 10;","MATCH ()-[e:`WORK_AT`]->() RETURN e LIMIT 10;"]}'
        # InterfaceExplorer.batch_ngql(ngql)

        # 创建快照
        # QA_random = random.randint(1,100000000)
        # ngql = '{"gql":"use `nba`"}'
        # InterfaceExplorer.Single_ngql(ngql)
        # data = {"name":"nba_" + str(QA_random),
        #         "space":"nba",
        #         "data":"{\"imagesCache\":[],\"name\":\"nba\",\"space\":\"nba\",\"nowDataMap\":{},\"nodes\":[],\"links\":[],\"nodesSelected\":[],\"linksSelected\":[],\"nodeHovering\":null,\"nodeDragging\":null,\"hideTooltip\":false,\"linkHovering\":null,\"filterIds\":[],\"handleMode\":\"\",\"exploreRules\":{\"edgeTypes\":[],\"edgeDirection\":\"outgoing\",\"stepsType\":\"single\",\"step\":1,\"vertexStyle\":\"groupByTag\"},\"tagsFields\":[],\"tags\":[\"bachelor\",\"player\",\"team\"],\"edgeTypes\":[\"like\",\"serve\",\"teammate\"],\"spaceVidType\":\"FIXED_STRING(32)\",\"edgesFields\":[],\"nodeVidShow\":true,\"showTagFields\":[],\"showEdgeFields\":[],\"filterExclusionIds\":{},\"layout\":\"force\",\"viewMode\":\"2d\",\"showTableData\":false,\"detectionMode\":\"\",\"tableData\":{},\"edgePropsCalcItems\":[],\"transform\":{\"k\":1.001,\"x\":-0.16657329118773959,\"y\":-0.00002123775138480105},\"threeGraphData\":{\"mode\":1},\"vertexFilters\":[],\"tagFilteredSet\":[]}"}
        # snapshot_id = InterfaceExplorer.add_Snapshot(data).json()["data"]["id"]

        # # 获取快照列表
        # snapshot_list = InterfaceExplorer.get_Snapshot().json()["data"]["snapshots"][0]["id"]
        # print(snapshot_list)

        # assert snapshot_id == snapshot_list

        # # 删除成功
        # InterfaceExplorer.delete_Snapshot(snapshot_id)
        # assert snapshot_id == snapshot_list

        # # 注销Explorer
        # InterfaceExplorer.interface_disconnect()


        