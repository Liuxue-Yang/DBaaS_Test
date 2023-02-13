import json
import threading
import requests
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
from explorer_auto.action.action_explorer import ActionExplorer
from explorer_auto.common.request_util import RequestMain
from requests_toolbelt import MultipartEncoder
from multiprocessing import Process, Lock
from explorer_auto.common.yaml_util import read_yaml_by_key
from explorer_auto.interface.interface_explorer import InterfaceExplorer
from threading import Thread

import json
import requests
import time
import concurrent.futures

import concurrent.futures
import json
import requests

class InterfaceExplorer:
    Cookie = '_ga=GA1.1.1191885678.1669711563; nsid=7bb9f88a-07e0-46ee-907b-70ca0e66e488; lang=ZH_CN; explorer_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMTkyLjE2OC44LjQ4IiwicG9ydCI6OTY2OSwidXNlcm5hbWUiOiJyb290IiwicGFzc3dvcmQiOiJyb290IiwibnNpZCI6IjBlZDAzOGUzLTdiNmUtNGMxMC1iOTdkLWEyNTcxM2ViOTdhNyIsImV4cCI6MTY3NTY0ODc5OH0.-qz8Y4urn_CRrBUtQUgdbMnFmcBmmgkBTb3vEns8EOw; nh=192.168.8.48:9669; nu=root; _ga_MV0JTF00K0=GS1.1.1675388435.15.1.1675389632.0.0.0'

class RequestMain:
    @staticmethod
    def request_main(method, url, headers, data, default_assert=True):
        if method == "post":
            response = requests.post(url, headers=headers, data=data)
        elif method == "get":
            response = requests.get(url, headers=headers)
        else:
            print("unsupported method")
            return None

        if default_assert and response.status_code != 200:
            print("request failed")
            return None

        return response.json()

def interface_add_job(data, default_assert=True):
    print('Running job')
    url = 'http://192.168.8.48:7002/api-analytics/jobs'
    headers = {
        'Content-Type': 'application/json;',
        'Cookie': InterfaceExplorer.Cookie
    }
    data = json.dumps(data)
    time.sleep(1)
    result = RequestMain.request_main(method="post", url=url, headers=headers,
                                      data=data, default_assert=default_assert)
    return result

def run_interface_add_job(data, default_assert=True, thread_id=0):
    start_time = time.time()
    result = interface_add_job(data, default_assert)
    assert result["code"] == 0
    end_time = time.time()
    print(f"Time for a single task: {end_time - start_time} seconds")
    return result

class JobThread(Thread):
    def __init__(self, thread_id, data, default_assert=True):
        Thread.__init__(self)
        self.thread_id = thread_id
        self.data = data
        self.default_assert = default_assert
        self.results = []
        
    def run(self):
        for i in range(100):
            result = run_interface_add_job(self.data, self.default_assert, self.thread_id)
            self.results.append(result)
        print(f"Thread {self.thread_id} finished, executed 100 tasks, last 10 results: {self.results[-10:]}")

if __name__ == '__main__':
    data = {"flowId":"3172244467"}
    threads = []
    start_time = time.time()
    for i in range(10):
        t = JobThread(i, data)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
        
    end_time = time.time()
    print(f"Total time: {end_time - start_time} seconds")
