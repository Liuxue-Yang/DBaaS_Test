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

def interface_sync_job(data, default_assert=True):
    url = 'http://192.168.8.48:7002/api-analytics/jobs/sync'
    headers = {
        'Content-Type': 'application/json',
        'Cookie':'_ga=GA1.1.1191885678.1669711563; nsid=7bb9f88a-07e0-46ee-907b-70ca0e66e488; lang=ZH_CN; explorer_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMTkyLjE2OC44LjQ4IiwicG9ydCI6OTY2OSwidXNlcm5hbWUiOiJyb290IiwicGFzc3dvcmQiOiJyb290IiwibnNpZCI6IjBlZDAzOGUzLTdiNmUtNGMxMC1iOTdkLWEyNTcxM2ViOTdhNyIsImV4cCI6MTY3NTY0ODc5OH0.-qz8Y4urn_CRrBUtQUgdbMnFmcBmmgkBTb3vEns8EOw; nh=192.168.8.48:9669; nu=root; _ga_MV0JTF00K0=GS1.1.1675402554.17.1.1675405596.0.0.0'

    }
    data = json.dumps(data)
    result = RequestMain.request_main(method="post", url=url, headers=headers,
                                      data=data, default_assert=default_assert)
    print(data)
    return result

def run_interface_sync_job(data, default_assert=True, thread_id=0):
    start_time = time.time()
    result = interface_sync_job(data, default_assert)
    end_time = time.time()
    print(f"Thread {thread_id}: Time for a single task: {end_time - start_time} seconds")
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
            data = {"ids":[1000-10*i]}
            if data["ids"][0] <= 0:
                break
            result = run_interface_sync_job(data, self.default_assert, self.thread_id)
            self.results.append(result)
        print(f"Thread {self.thread_id} finished, last result: {self.results}")

if __name__ == '__main__':
    data = {"ids":[1000]}
    threads = []
    start_time = time.time()
    for i in range(10):
        t = JobThread(i, data)
        t.start()
        threads.append(t)
    end_time = time.time()
    print(f"All tasks finished at time: {end_time - start_time} seconds")