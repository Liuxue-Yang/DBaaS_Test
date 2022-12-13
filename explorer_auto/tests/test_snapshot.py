import time
import random
import pytest
from explorer_auto.common.yaml_util import read_yaml_by_key
from explorer_auto.action.action_explorer import ActionExplorer
from explorer_auto.interface.interface_explorer import InterfaceExplorer

class Testsnapshot:

    @pytest.mark.snapshot
    def test_snapshot(self):
        # 创建快照
        QA_random = random.randint(1,100000000)
        ngql = '{"gql":"use `nba`"}'
        InterfaceExplorer.Single_ngql(ngql)
        for i in range(2000):
            data = {"name":"nba_" + str(QA_random),
                    "space":"nba",
                    "data":"{\"imagesCache\":[],\"name\":\"nba\",\"space\":\"nba\",\"nowDataMap\":{},\"nodes\":[],\"links\":[],\"nodesSelected\":[],\"linksSelected\":[],\"nodeHovering\":null,\"nodeDragging\":null,\"hideTooltip\":false,\"linkHovering\":null,\"filterIds\":[],\"handleMode\":\"\",\"exploreRules\":{\"edgeTypes\":[],\"edgeDirection\":\"outgoing\",\"stepsType\":\"single\",\"step\":1,\"vertexStyle\":\"groupByTag\"},\"tagsFields\":[],\"tags\":[\"bachelor\",\"player\",\"team\"],\"edgeTypes\":[\"like\",\"serve\",\"teammate\"],\"spaceVidType\":\"FIXED_STRING(32)\",\"edgesFields\":[],\"nodeVidShow\":true,\"showTagFields\":[],\"showEdgeFields\":[],\"filterExclusionIds\":{},\"layout\":\"force\",\"viewMode\":\"2d\",\"showTableData\":false,\"detectionMode\":\"\",\"tableData\":{},\"edgePropsCalcItems\":[],\"transform\":{\"k\":1.001,\"x\":-0.16657329118773959,\"y\":-0.00002123775138480105},\"threeGraphData\":{\"mode\":1},\"vertexFilters\":[],\"tagFilteredSet\":[]}"}
            snapshot_id = InterfaceExplorer.add_Snapshot(data).json()["data"]["id"]

        # 获取快照列表
        snapshot_list = InterfaceExplorer.get_Snapshot().json()["data"]["snapshots"][0]["id"]
        print(snapshot_list)

        assert snapshot_id == snapshot_list

        # 删除成功
        InterfaceExplorer.delete_Snapshot(snapshot_id)
        snapshot_list = InterfaceExplorer.get_Snapshot().json()["data"]["snapshots"][0]["id"]
        assert snapshot_id != snapshot_list

        # 注销Explorer
        InterfaceExplorer.interface_disconnect()