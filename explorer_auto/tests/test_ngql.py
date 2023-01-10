import time
import random
import aiohttp
import asyncio
import pytest
import base64
from websocket import create_connection

from explorer_auto.common.yaml_util import read_yaml_by_key
from explorer_auto.action.action_explorer import ActionExplorer
from explorer_auto.interface.interface_explorer import InterfaceExplorer
class Testlogin:
    
    @pytest.mark.ngql
    def test_qa(self):
        ngql1 = [
            'show spaces',
            'use sf1',
            'MATCH ()-[e3]->(v2:`Comment`) RETURN e3 LIMIT 1000'

        ]
        for ngql in ngql1:
            result = asyncio.run(InterfaceExplorer.test_WebSocket_ngql(ngql)).json()
            # result1 = result["body"]["content"]["data"]["tables"]
            print(result)