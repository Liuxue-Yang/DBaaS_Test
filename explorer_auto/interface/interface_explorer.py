import base64
import json
import time
import os
import uuid
import aiohttp
import asyncio
import requests
import time
import csv
import string
import websocket
import websockets
from urllib.parse import urlencode
from websocket import create_connection
from urllib3 import encode_multipart_formdata
from explorer_auto.common.request_util import RequestMain
from requests_toolbelt import MultipartEncoder
from multiprocessing import Process, Lock
from explorer_auto.common.yaml_util import read_yaml_by_key

class InterfaceExplorer:
    #API 接口
    Cookie = ""
    def interface_connect( data, default_assert=True):
        print("登录接口")
        # url = '/api-nebula/db/connect'
        url = '/api-cloud/users/login'
        
        headers = {
            'Content-Type': 'application/json;',
        }
        data = json.dumps(data)
        result = RequestMain.request_main(method="post", url=url, headers=headers,
                                                data=data, default_assert=default_assert)
        # InterfaceExplorer.Cookie = result.headers["Set-Cookie"].split('=')[1].split(' ')[0]
        # InterfaceExplorer.Cookie = result.headers["Set-Cookie"].split('=')[1]       
        InterfaceExplorer.Cookie = result.headers["Set-Cookie"].split(' ')[0]
        # # write token to tmp.yaml
        # write_yaml_by_key({"Cookie": explorer_token},"/conf/tmp.yaml")
        return result
    
    def interface_connect_login(data, default_assert=True):
        print("登录接口")
        # url = '/api-nebula/db/connect'
        url = '/api-cloud/users/login'
        
        headers = {
            'Content-Type': 'application/json;',
        }
        data = json.dumps(data)
        result = RequestMain.request_main(method="post", url=url, headers=headers,
                                                data=data, default_assert=default_assert)
        return result    
    
    def interface_info(default_assert=True):
        print('查看info')
        url = '/api-cloud/users/info'
        headers = {
            'Cookie':InterfaceExplorer.Cookie
            }
        result = RequestMain.request_main(method='get',url=url,headers=headers,
                                          default_assert=default_assert)  
    
    def interface_projects_get(default_assert=True):
        print("获取project列表")
        url = '/api-cloud/projects'
        
        headers ={
            'Cookie': InterfaceExplorer.Cookie
        }
        result = RequestMain.request_main(method="get", url=url, 
                                            headers=headers,default_assert=default_assert)
        return result  
    
    def interface_projects_post(data_name, default_assert=True):   
        print("创建project")
        url = '/api-cloud/projects'
        headers ={
            'Content-Type': 'application/json;',
            'Cookie': InterfaceExplorer.Cookie
        }
        data_name = json.dumps(data_name)
        result = RequestMain.request_main(method="post", url=url, headers=headers,
                                                data=data_name, default_assert=default_assert)
        return result 
    
    def interface_projects_delete(id,default_assert=True):
        print("删除pproject")
        url = '/api-cloud/projects/{}'.format(id)
        headers ={
            'Content-Type': 'application/json;',
            'Cookie': InterfaceExplorer.Cookie
        }
        result = RequestMain.request_main(method="delete", url=url, headers=headers,
                                          default_assert=default_assert)
        return result  
    # def interface_connect_failed(userName,password,data, default_assert=True):
    #     print("登录接口")
    #     # url = '/api-nebula/db/connect'
    #     url = '/api-nebula/db/connect'
    #     # Encrypted auth information
    #     auth_info = '["{}","{}"]'.format(userName,password).encode()
    #     auth_info = base64.b64encode(auth_info)
    #     auth = "Bearer "+ auth_info.decode('UTF-8')
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'Authorization': auth
    #     }
    #     data = json.dumps(data)
    #     result = RequestMain.request_main(method="post", url=url, headers=headers,
    #                                             data=data, default_assert=default_assert)
    #     return result

    # def interface_disconnect(default_assert=True):
    #     print("注销接口")
    #     url = '/api-nebula/db/disconnect'
    #     headers = {
    #         'Cookie': InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="post", url=url, headers=headers,
    #                                             default_assert=default_assert)
    #     # extract token
    #     InterfaceExplorer.Cookie = result.headers["Set-Cookie"].split(' ')[0]
    #     # # write token to tmp.yaml
    #     # write_yaml_by_key({"Cookie": explorer_token},"/conf/tmp.yaml")
    #     return result
        
    # def interface_submit_job(workflow_id, data, default_assert=True):
    #     print("提交job接口")
    #     url = '/api-open/v1/workflows/{}/jobs'.format(workflow_id)
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'Cookie': InterfaceExplorer.Cookie
    #     }
    #     data = json.dumps(data) 
    #     print(data)
    #     print(type(data))
    #     print(default_assert)
    #     result = RequestMain.request_main(method="post", url=url, headers=headers,
    #                                     data=data, default_assert=default_assert)
    #     return result

    # def interface_cancel_job(job_id, default_assert=True):
    #     print("取消job接口")
    #     url = '/api-open/v1/jobs/{}/cancel'.format(job_id)
    #     headers = {
    #         'Cookie': InterfaceExplorer.Cookie
    #     }

    #     result = RequestMain.request_main(method="put", url=url, headers=headers,
    #                                              default_assert=default_assert)
    #     return result

    # def interface_get_jobs(params="", default_assert=True):
    #     print("获取job列表接口")
    #     base_url = '/api-open/v1/jobs?'
    #     url = base_url+urlencode(params)
    #     headers = {
    #         'Cookie': InterfaceExplorer.Cookie
    #     }

    #     result = RequestMain.request_main(method="get", url=url, headers=headers,
    #                                              default_assert=default_assert)
    #     return result

    # def interface_get_job_detail(job_id, default_assert=True):
    #     print("获取job详情接口")
    #     url = '/api-open/v1/jobs/{}'.format(job_id)
    #     headers = {
    #         'Cookie': InterfaceExplorer.Cookie
    #     }

    #     result = RequestMain.request_main(method="get", url=url, headers=headers,
    #                                              default_assert=default_assert)
    #     return result

    # def interface_get_jobs_by_workflow(workflow_id, params="", default_assert=True):
    #     print("根据workflowID获取job列表接口")
    #     base_url = '/api-open/v1/workflows/{}/jobs?'.format(workflow_id)
    #     url = base_url+urlencode(params)
    #     headers = {
    #         'Cookie': InterfaceExplorer.Cookie
    #     }

    #     result = RequestMain.request_main(method="get", url=url, headers=headers,
    #                                              default_assert=default_assert)
    #     return result

    # def interface_get_task_result(job_id,task_id,params="", default_assert=True):
    #     print("获取结果接口")
    #     url = '/api-open/v1/jobs/{}/tasks/{}/sample_result?{}'.format(job_id,task_id,params)
    #     # print(base_url)
    #     # print(params)
    #     # url = base_url+urlencode(params)
    #     # print(url)
    #     headers = {
    #         'Cookie': InterfaceExplorer.Cookie
    #     }

    #     result = RequestMain.request_main(method="get", url=url, headers=headers,
    #                                              default_assert=default_assert)
    #     return result
    
    # # 非API 接口
    # def interface_create_workflow(data, default_assert=True):
    #     print("创建workflow接口")
    #     url = '/api-analytics/flows'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'Cookie': InterfaceExplorer.Cookie
    #     }
    #     data = json.dumps(data)
    #     result = RequestMain.request_main(method="post", url=url, headers=headers,
    #                                         data=data, default_assert=default_assert)
    #     return result
    
    # def interface_update_workflow(workflow_id, data, default_assert=True):
    #     print("更新workflow接口")
    #     url = '/api-analytics/flows/{}'.format(workflow_id)
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'Cookie': InterfaceExplorer.Cookie
    #     }
    #     data = json.dumps(data)
    #     print(data)
    #     result = RequestMain.request_main(method="put", url=url, headers=headers,
    #                                         data=data, default_assert=default_assert)
    #     return result

    # def interface_get_workflow(default_assert=True):
    #     print("获取workflow列表")
    #     url = '/api-analytics/flows?page=1&pageSize=10&filter=%7B%22name%22:%22%22%7D'
    #     header = {
    #         'Content-Type': 'application/json;',
    #         'Cookie': InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="get",url = url,headers=header,
    #                                         default_assert=default_assert)
    #     return result

    # def interface_get_id_workflow(workflow_id,default_assert=True):
    #     print("获取单个workflow")
    #     url = '/api-analytics/flows/{}'.format(workflow_id)
    #     header = {
    #         'Content-Type': 'application/json;',
    #         'Cookie': InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="get",url = url,headers=header,
    #                                         default_assert=default_assert)
    #     return result

    # def interface_delete_workflow(workflow_id,default_assert=True):
    #     print('删除workflow')
    #     url = '/api-analytics/flows/{}'.format(workflow_id)
    #     header = {
    #         'Content-Type': 'application/json;',
    #         'Cookie': InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="delete",url=url,headers=header,
    #                                         default_assert=default_assert)
    #     return result

    # def interface_history_workflow(workflow_id,default_assert=True):
    #     print('获取workflow历史列表')
    #     url = '/api-analytics/flows/{}/history?page=1&pageSize=100'.format(workflow_id)
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'Cookie': InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="get",url=url,headers=headers,
    #                                         default_assert=default_assert)
    #     return result

    # def interface_history_id_workflow(workflow_id,hestory_id,default_assert=True):
    #     print('获取workflow历史详情')
    #     url = '/api-analytics/flows/{}/history/{}'.format(workflow_id,hestory_id)
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'Cookie': InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="get",url=url,headers=headers,
    #                                         default_assert=default_assert)
    #     return result
    
    # def interface_repair_history_workflow(workflow_id,hestory_id,default_assert=True):
    #     print('workflow恢复历史')
    #     url = '/api-analytics/flows/{}/history/{}/restore'.format(workflow_id,hestory_id)
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'Cookie': InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="post",url=url,headers=headers,
    #                                         default_assert=default_assert)
    #     return result

    # def interface_add_job(data,default_assert=True):
    #     print('运行job')
    #     url = '/api-analytics/jobs'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'Cookie': InterfaceExplorer.Cookie
    #     }
    #     data = json.dumps(data)
    #     print(data)
    #     result = RequestMain.request_main(method="post",url=url,headers=headers,
    #                                         data=data,default_assert=default_assert)
    #     return result
    
    # def interface_stop_job(data,default_assert=True):
    #     print('停止job')
    #     url = '/api-analytics/controller'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'Cookie': InterfaceExplorer.Cookie
    #     }
    #     data = json.dumps(data)
    #     print(data)
    #     result = RequestMain.request_main(method="post",url=url,headers=headers,
    #                                         data=data,default_assert=default_assert)
    #     return result

    # def interface_get_job(default_assert=True):
    #     print('获取job列表')
    #     url = '/api-analytics/jobs?page=1&pageSize=10&filter=%7B%7D'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'Cookie': InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="get",url=url,headers=headers,
    #                                         default_assert=default_assert)
    #     return result

    # def interface_get_job_list(data,default_assert=True):
    #     print('获取job列表详情')
    #     url = '/api-analytics/jobs/sync'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'Cookie': InterfaceExplorer.Cookie
    #     }
    #     data = json.dumps(data)
    #     print(data)
    #     result = RequestMain.request_main(method="post",url=url,headers=headers,
    #                                         data=data,default_assert=default_assert)
    #     return result

    # def interface_get_id_job(job_id,default_assert=True):
    #     print('查看job详情')
    #     url = '/api-analytics/jobs/{}'.format(job_id)
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'Cookie': InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="get",url=url,headers=headers,
    #                                         default_assert=default_assert)
    #     return result

    # def interface_delete_job(job_id,defaultt_assert=True):
    #     print('删除job')
    #     url = '/api-analytics/jobs/{}'.format(job_id)
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'Cookie': InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="delete",url=url,headers=headers,
    #                                         default_assert=defaultt_assert)
    #     return result

    # def interface_rerun_job(job_id,defaultt_assert=True):
    #     print('重跑job')
    #     url = '/api-analytics/jobs/{}/rerun'.format(job_id)
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'Cookie': InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="put",url=url,headers=headers,
    #                                         default_assert=defaultt_assert)
    #     return result
    
    # def interface_result_job(data,defaultt_assert=True):
    #     print('查看job结果')
    #     url = '/api-analytics/jobs/result'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'Cookie': InterfaceExplorer.Cookie
    #     }
    #     data = json.dumps(data)
    #     result = RequestMain.request_main(method="post",url=url,headers=headers,
    #                                         data=data,default_assert=defaultt_assert)
    #     return result

    # def import_tasks(data,default_assert=True):
    #     print('创建导入任务')
    #     url = '/api/import-tasks'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     data = json.dumps(data)
    #     print(data)
    #     result = RequestMain.request_main(method="post",url=url,headers=headers,
    #                                         data=data,default_assert=default_assert)
    #     return result
        
    # def import_tasks_get_id(import_tasks_id,default_assert=True):
    #     print('获取单个导入任务')
    #     url = '/api/import-tasks/{}'.format(import_tasks_id)
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="get",url=url,headers=headers,
    #                                         default_assert=default_assert)
    #     return result
    # def import_tasks_get(default_assert=True):
    #     print('获取导入任务列表')
    #     url = '/api/import-tasks'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="get",url=url,headers=headers,
    #                                         default_assert=default_assert)
    #     return result

    # def import_tasks_stop(import_tasks_id,default_assert=True):
    #     print('终止导入任务')
    #     url = '/api/import-tasks/{}/stop'.format(import_tasks_id)

    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="get",url=url,headers=headers,
    #                                         default_assert=default_assert)
    #     return result

    # def import_tasks_delete(import_tasks_id,default_assert=True):
    #     print('删除导入任务')
    #     url = '/api/import-tasks/{}'.format(import_tasks_id)
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="delete",url=url,headers=headers,
    #                                         default_assert=default_assert)
    #     return result
    
    # def import_log_csv(import_tasks_id,default_assert=True):
    #     print('获取日志文件名称')
    #     url = '/api/import-tasks/{}/task-log-names'.format(import_tasks_id)
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="get",url=url,headers=headers,
    #                                         default_assert=default_assert)

    #     return result

    # def import_log(import_tasks_id,default_assert=True):
    #     print('获取日志内容')
    #     url = '/api/import-tasks/{}/logs?offset=0&limit=500&file=import.log'.format(import_tasks_id)
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="get",url=url,headers=headers,
    #                                         default_assert=default_assert)

    #     return result


    # def import_add_csv(file_path,csv_name,default_assert=True):
    #     print('上传csv文件')
    #     url = '/api/files'
    #     files = {
    #         'file': open(
    #             file_path,
    #              'rb'
    #              ),
    #         'config': (
    #             None, 
    #             json.dumps({
    #                 "name":csv_name,
    #                 "delimiter":",",
    #                 "withHeader":False
    #                 }), 
    #         'application/json')}
    #     result = RequestMain.request_main(method="put",url=url,files=files,
    #                                         default_assert=default_assert)
    #     print(result)
    #     return result

    # def import_add_Multiple_csv(path1,path2,path3,default_assert=True):
    #     print('上传多个csv文件')
    #     url = '/api/files'
    #     files = {
    #         'file1': open(path1, 'rb'),
    #         'file2': open(path2, 'rb'),
    #         'file3': open(path3, 'rb'),
    #     }
    #     result = RequestMain.request_main(method="put",url=url,files=files,
    #                                         default_assert=default_assert)
    #     return result

    # def import_get_csv(default_assert=True):
    #     print('获取csv文件')
    #     url = '/api/files'
    #     headers = {
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="get",url=url,headers=headers,
    #                                         default_assert=default_assert)
    #     return result

    # def import_delete_csv(csv_name,default_assert=True):
    #     print('删除csv文件')
    #     url = '/api/files'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     data = json.dumps({"names":[csv_name]})
    #     result = RequestMain.request_main(method="delete",url=url,headers=headers,
    #                                         data = data,default_assert=default_assert)
    #     return result
        
    # def Single_ngql(ngql,default_assert=True):
    #     print('执行单条语句')
    #     url = '/api-nebula/db/exec'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     data = json.dumps(ngql)
    #     result = RequestMain.request_main(method="post",url=url,headers=headers,
    #                                         data=data,default_assert=default_assert)
    #     return result

    # def batch_ngql(ngql,default_assert=True):
    #     print('批量执行语句')
    #     url = '/api-nebula/db/batchExec'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     data = json.dumps(ngql)
    #     result = RequestMain.request_main(method="post",url=url,headers=headers,
    #                                         data=data,default_assert=default_assert)
    #     return result

    # def add_Snapshot(data,default_assert=True):
    #     print('添加快照')
    #     url = '/api-snapshot/snapshots'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     data = json.dumps(data)
    #     result = RequestMain.request_main(method="post",url=url,headers=headers,
    #                                         data=data,default_assert=default_assert)
    #     return result

    # def get_Snapshot(default_assert=True):
    #     print('获取快照列表')
    #     url = '/api-snapshot/snapshots?page=1&pageSize=10&filter=%7B%7D'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="get",url=url,headers=headers,
    #                                         default_assert=default_assert)
    #     return result

    # def delete_Snapshot(snapshot_id,default_assrt=True):
    #     print('删除快照')
    #     url = '/api-snapshot/snapshots/{}'.format(snapshot_id)
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="delete",url=url,headers=headers,
    #                                         default_assert=default_assrt)
    #     return result

    # def add_Icon_Group(data,default_assrt=True):
    #     print('添加图标组')
    #     url = '/api-icongroup'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     data = json.dumps(data)
    #     result = RequestMain.request_main(method="post",url=url,headers=headers,
    #                                         data=data,default_assert=default_assrt)

    #     print(data)
    #     return result

    # def get_Icon_Group(default_assert=True):
    #     print('获取图标组')
    #     url = '/api-icongroup?type=svg'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="get",url=url,headers=headers,
    #                                         default_assert=default_assert)
    #     return result

    # def delete_Icon_Group(icon_id_Group,default_assert=True):
    #     print('删除图标组')
    #     url = '/api-icongroup/{}'.format(icon_id_Group)
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }   
    #     result = RequestMain.request_main(method="delete",url=url,headers=headers,
    #                                         default_assert=default_assert)
    #     return result

    # def put_Icon_Group(icon_id_Group,data,default_assert=True):
    #     print('更新图标组')
    #     url = '/api-icongroup/{}'.format(icon_id_Group)
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     data = json.dumps(data)
    #     result = RequestMain.request_main(method="put",url=url,headers=headers,
    #                                         data=data,default_assert=default_assert)
    #     print(data)
    #     return result
    
    # def add_Icon(icon_id_Group,data,default_assert=True):
    #     print('添加图标')
    #     url = '/api-icongroup/{}'.format(icon_id_Group)
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     data = json.dumps(data)
    #     result = RequestMain.request_main(method="post",url=url,headers=headers,
    #                                         data=data,default_assert=default_assert)
    #     return result

    # def get_Icon(icon_id_Group,default_assert=True):
    #     print('获取组内图标')
    #     url = '/api-icongroup/{}'.format(icon_id_Group)
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="get",url=url,headers=headers,
    #                                         default_assert=default_assert)
    #     return result

    # def delete_Icon(icon_id_Group,icon_id,default_assert=True):
    #     print('删除组内图标')
    #     url = '/api-icongroup/{}/icon/{}'.format(icon_id_Group,icon_id)
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="delete",url=url,headers=headers,
    #                                         default_assert=default_assert)
    #     return result

    # def add_template(data,default_assert=True):
    #     print('创建模板')
    #     url = '/api-templates/template'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     data = json.dumps(data)
    #     result = RequestMain.request_main(method='post',url=url,headers=headers,
    #                                         data=data,default_assert=default_assert)
    #     return result

    # def get_template(default_assert=True):
    #     print('查看模板列表')
    #     url = '/api-templates/templates?page=1&pageSize=10&keyword=&space='
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="get",url=url,headers=headers,
    #                                         default_assert=default_assert)
    #     return result
    
    # def delete_template(template_id,default_assert=True):
    #     print('删除模板')
    #     url = '/api-templates/templates/{}'.format(template_id)
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="delete",url=url,headers=headers,
    #                                         default_assert=default_assert)
    #     return result

    # def put_template(template_id,data,default_assert=True):
    #     print('更新模板')
    #     url = '/api-templates/templates/{}'.format(template_id)
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     data = json.dumps(data)
    #     result = RequestMain.request_main(method="put",url=url,headers=headers,
    #                                         data=data,default_assert=default_assert)
    #     return result


    # def put_config(data,default_assert=True):
    #     print('更新配置')
    #     url = '/api-config/global'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     data = json.dumps(data)
    #     result = RequestMain.request_main(method="put",url=url,headers=headers,
    #                                         data=data,default_assert=default_assert)
    #     return result

    # def get_config(default_assert=True):
    #     print('获取配置')
    #     url = '/api-config/global'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="get",url=url,headers=headers,
    #                                         default_assert=default_assert)
    #     return result
        
    # def add_controller(data,default_assert=True):
    #     print('将graphd密码写入dag')
    #     url = '/api-analytics/controller'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     data = json.dumps(data)
    #     result = RequestMain.request_main(method="post",url=url,headers=headers,
    #                                         data=data,default_assert=default_assert)
    #     return result

    # def get_dag(default_assert=True):
    #     print('ping controller')
    #     url = '/api-analytics/controller/ping/dagctl'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     result = RequestMain.request_main(method="get",url=url,headers=headers,
    #                                         default_assert=default_assert)
    #     return result

    # def get_controller(data,default_assert=True):
    #     print('查看存在dag的graphd信息')
    #     url = '/api-analytics/controller'
    #     headers = {
    #         'Content-Type': 'application/json;',
    #         'cookie':InterfaceExplorer.Cookie
    #     }
    #     data = json.dumps(data)
    #     result = RequestMain.request_main(method="post",url=url,headers=headers,
    #                                         data=data,default_assert=default_assert)
    #     return result

    # # WebSocket异步单条语句接口
    # async def test_WebSocket_ngql(ngql,*space):
    #     print('异步执行单条语句')
    #     msg_id = str(uuid.uuid4())
    #     headers = {
    #         'cookie': InterfaceExplorer.Cookie,
    #     }
    #     ip = read_yaml_by_key("graphd_ip",'/conf/conf.yaml')
    #     async with aiohttp.ClientSession() as session:
    #         async with session.ws_connect('ws://{}:7002/nebula_ws'.format(ip),headers=headers) as ws:
    #             await ws.send_json({
    #                 "header": {
    #                     "msgId": msg_id,
    #                     "version": "1.0"
    #                 },
    #                 "body": {
    #                     "product": "Studio",
    #                     "msgType": "ngql",
    #                     "content": {
    #                         "gql": ngql,
    #                         "space":space
    #                     }
    #                 }
    #             })
    #             result = await ws.receive()
    #             result_json = result.json()['header']['msgId']
    #             print(result)
    #             if msg_id == result_json:
    #                 print("UUID match")
    #             else:
    #                 print("UUID does not match")
    #             return result

    # # WebSocket异步多条语句接口
    # async def test_WebSocket_batch_ngql(ngql,space):
    #     print('异步执行多条语句')
    #     msg_id = str(uuid.uuid4())
    #     headers = {
    #         'cookie': InterfaceExplorer.Cookie,
    #     }
    #     ip = read_yaml_by_key("graphd_ip",'/conf/conf.yaml')
    #     async with aiohttp.ClientSession() as session:
    #         async with session.ws_connect('ws://{}:7002/nebula_ws'.format(ip),headers=headers) as ws:
    #             await ws.send_json({
    #                 "header": {
    #                     "msgId": msg_id,
    #                     "version": "1.0"
    #                 },
    #                 "body": {
    #                     "product": "Studio",
    #                     "msgType": "batch_ngql",
    #                     "content": {
    #                         "gqls": ngql,
    #                         'space':space
    #                     }
    #                 }
    #             })
    #             result = await ws.receive()
    #             print(result)
    #             result_json = result.json()['header']['msgId']
    #             if msg_id == result_json:
    #                 print("UUID match")
    #             else:
    #                 print("UUID does not match")
    #             return result