import time
import random
import pytest
from explorer_auto.common.yaml_util import read_yaml_by_key
from explorer_auto.action.action_explorer import ActionExplorer
from explorer_auto.interface.interface_explorer import InterfaceExplorer

class Testtemplate:

    @pytest.mark.template
    def test_template(self):
        # 循环创建模板
        template_data = [
            {"name":"查询语句模板(match)","space":"demo_basketballplayer","content":"match (v) return v limit 100","result":"match (v) return v limit 100","marks":[]},
            {"name":"非查询语句模板(insert)","space":"demo_basketballplayer","content":"INSERT VERTEX player (name, age) VALUES \"11\":(\"n1\", 12);","result":"INSERT VERTEX player (name, age) VALUES \"11\":(\"n1\", 12);","marks":[]},
            {"name":"int类型空间模板(sf1)","space":"sf1","content":"match (v) return v limit 100","result":"match (v) return v limit 100","marks":[]},
            {"name":"重复名称","space":"demo_basketballplayer","description":"Go语句","content":"go 1 to 2 steps from \"player114\" over * yield dst(edge),src(edge)","result":"go 1 to 2 steps from \"player114\" over * yield dst(edge),src(edge)","marks":[]},
            {"name":"重复名称","space":"demo_basketballplayer","description":"FIND PATH语句","content":"FIND SHORTEST PATH FROM \"player102\" TO \"team204\" OVER * YIELD path AS p;","result":"FIND SHORTEST PATH FROM \"player102\" TO \"team204\" OVER * YIELD path AS p;","marks":[]},
            {"name":"特殊字符（~！@#￥%……&*）汉字字母ABC","space":"demo_basketballplayer","description":"LOOKUP","content":"LOOKUP ON follow WHERE follow.degree == 60 YIELD dst(edge) AS DstVID, properties(edge).degree AS Degree | GO FROM $-.DstVID OVER serve YIELD $-.DstVID, properties(edge).start_year, properties(edge).end_year, properties($$).name;","result":"LOOKUP ON follow WHERE follow.degree == 60 YIELD dst(edge) AS DstVID, properties(edge).degree AS Degree | GO FROM $-.DstVID OVER serve YIELD $-.DstVID, properties(edge).start_year, properties(edge).end_year, properties($$).name;","marks":[]},
            {"name":"多条语句","space":"demo_basketballplayer","description":"Go + Match","content":"match (v) return v limit 100;\ngo 1 to 2 steps from \"player101\" over * yield dst(edge),src(edge);","result":"match (v) return v limit 100;\ngo 1 to 2 steps from \"player101\" over * yield dst(edge),src(edge);","marks":[]},
            {"name":"多个input","space":"demo_basketballplayer","content":"MATCH (m)-[]->(n) WHERE id(m)==\"player100\" OPTIONAL MATCH (n)-[]->(l) WHERE id(n)==\"player125\" RETURN id(m),id(n),id(l);","result":"MATCH (m)-[]->(n) WHERE id(m)==\"${VID_1}\" OPTIONAL MATCH (n)-[]->(l) WHERE id(n)==\"${VID_2}\" RETURN id(m),id(n),id(l);","marks":[{"name":"VID_1","sample":"player100","position":{"start":{"line":0,"ch":32},"end":{"line":0,"ch":41}}},{"name":"VID_2","sample":"player125","position":{"start":{"line":0,"ch":84},"end":{"line":0,"ch":93}}}]},
            {"name":"不存在spaces","space":"不存在","content":"match (v) return v limit 100","result":"match (v) return v limit 100","marks":[]}
        ]
        for data in template_data:
            code = InterfaceExplorer.add_template(data).json()["code"]
            assert 0 == code

        # 创建gql、参数为空、缺少参数的模板 并判断code为4004001
        template_data = [
            {"name":"ngql为空","space":"demo_basketballplayer","content":"","result":"","marks":[]},
            {"name":"缺少参数","content":"","result":"","marks":[]},
            {"name":"","space":"","content":"","result":"","marks":[]},
        ]
        for data in template_data:
            code = InterfaceExplorer.add_template(data).json()["code"]
            assert 40004001 == code

        # 获取列表判断添加成功
        json_data = InterfaceExplorer.get_template().json()["data"]
        assert '不存在spaces' == json_data["items"][0]["name"]
        assert '多个input' == json_data["items"][1]["name"]
        assert '多条语句' == json_data["items"][2]["name"]
        assert '特殊字符（~！@#￥%……&*）汉字字母ABC' == json_data["items"][3]["name"]
        assert '重复名称' == json_data["items"][4]["name"]
        assert '重复名称' == json_data["items"][5]["name"]
        assert 'int类型空间模板(sf1)' == json_data["items"][6]["name"]
        assert '非查询语句模板(insert)' == json_data["items"][7]["name"]
        assert '查询语句模板(match)' == json_data["items"][8]["name"]

        # 循环更新模板
        Update_data = [
            {"name":"更新名称","space":"demo_basketballplayer","description":"","content":"MATCH (m)-[]->(n) WHERE id(m)==\"player100\" OPTIONAL MATCH (n)-[]->(l) WHERE id(n)==\"player125\" RETURN id(m),id(n),id(l);","result":"MATCH (m)-[]->(n) WHERE id(m)==\"${VID_1}\" OPTIONAL MATCH (n)-[]->(l) WHERE id(n)==\"${VID_2}\" RETURN id(m),id(n),id(l);","marks":[{"description":"","name":"VID_1","sample":"player100","position":{"start":{"line":0,"ch":32},"end":{"line":0,"ch":41}}},{"description":"","name":"VID_2","sample":"player125","position":{"start":{"line":0,"ch":84},"end":{"line":0,"ch":93}}}]},
            {"name":"更新空间","space":"sf1","description":"","content":"MATCH (m)-[]->(n) WHERE id(m)==\"player100\" OPTIONAL MATCH (n)-[]->(l) WHERE id(n)==\"player125\" RETURN id(m),id(n),id(l);","result":"MATCH (m)-[]->(n) WHERE id(m)==\"${VID_1}\" OPTIONAL MATCH (n)-[]->(l) WHERE id(n)==\"${VID_2}\" RETURN id(m),id(n),id(l);","marks":[{"description":"","name":"VID_1","sample":"player100","position":{"start":{"line":0,"ch":32},"end":{"line":0,"ch":41}}},{"description":"","name":"VID_2","sample":"player125","position":{"start":{"line":0,"ch":84},"end":{"line":0,"ch":93}}}]},
            {"name":"更新input","space":"sf1","description":"","content":"MATCH (m)-[]->(n) WHERE id(m)==\"player100\" OPTIONAL MATCH (n)-[]->(l) WHERE id(n)==\"player125\" RETURN id(m),id(n),id(l);","result":"MATCH (m)-[]->(n) WHERE id(m)==\"player100\" OPTIONAL MATCH (n)-[]->(l) WHERE id(n)==\"${VID_2}\" RETURN id(m),id(n),id(l);","marks":[{"description":"","name":"VID_2","sample":"player125","position":{"start":{"line":0,"ch":84},"end":{"line":0,"ch":93}}}]},
            {"name":"更新描述","space":"sf1","description":"QA","content":"MATCH (m)-[]->(n) WHERE id(m)==\"player100\" OPTIONAL MATCH (n)-[]->(l) WHERE id(n)==\"player125\" RETURN id(m),id(n),id(l);","result":"MATCH (m)-[]->(n) WHERE id(m)==\"player100\" OPTIONAL MATCH (n)-[]->(l) WHERE id(n)==\"${VID_2}\" RETURN id(m),id(n),id(l);","marks":[{"description":"","name":"VID_2","sample":"player125","position":{"start":{"line":0,"ch":84},"end":{"line":0,"ch":93}}}]},
            {"name":"更新ngql","space":"sf1","description":"QA","content":"match (v) return v limit 100","result":"match (v) return v limit 100","marks":[]},
            {"name":"不存在的spaces","space":"不存在的spaces","description":"","content":"MATCH (m)-[]->(n) WHERE id(m)==\"player100\" OPTIONAL MATCH (n)-[]->(l) WHERE id(n)==\"player125\" RETURN id(m),id(n),id(l);","result":"MATCH (m)-[]->(n) WHERE id(m)==\"${VID_1}\" OPTIONAL MATCH (n)-[]->(l) WHERE id(n)==\"${VID_2}\" RETURN id(m),id(n),id(l);","marks":[{"description":"","name":"VID_1","sample":"player100","position":{"start":{"line":0,"ch":32},"end":{"line":0,"ch":41}}},{"description":"","name":"VID_2","sample":"player125","position":{"start":{"line":0,"ch":84},"end":{"line":0,"ch":93}}}]},
            {"name":"不存在的模板","space":"sf1","description":"","content":"MATCH (m)-[]->(n) WHERE id(m)==\"player100\" OPTIONAL MATCH (n)-[]->(l) WHERE id(n)==\"player125\" RETURN id(m),id(n),id(l);","result":"MATCH (m)-[]->(n) WHERE id(m)==\"${VID_1}\" OPTIONAL MATCH (n)-[]->(l) WHERE id(n)==\"${VID_2}\" RETURN id(m),id(n),id(l);","marks":[{"description":"","name":"VID_1","sample":"player100","position":{"start":{"line":0,"ch":32},"end":{"line":0,"ch":41}}},{"description":"","name":"VID_2","sample":"player125","position":{"start":{"line":0,"ch":84},"end":{"line":0,"ch":93}}}]}
        ]
        template_id = json_data["items"][1]["id"]
        for data in Update_data:
            code = InterfaceExplorer.put_template(template_id,data).json()["code"]
            assert 0 == code

        # 更新缺少参数的模板
        data = {"name":"缺少参数","description":"","content":"MATCH (m)-[]->(n) WHERE id(m)==\"player100\" OPTIONAL MATCH (n)-[]->(l) WHERE id(n)==\"player125\" RETURN id(m),id(n),id(l);","result":"MATCH (m)-[]->(n) WHERE id(m)==\"player100\" OPTIONAL MATCH (n)-[]->(l) WHERE id(n)==\"${VID_2}\" RETURN id(m),id(n),id(l);","marks":[{"description":"","name":"VID_2","sample":"player125","position":{"start":{"line":0,"ch":84},"end":{"line":0,"ch":93}}}]}
        code = InterfaceExplorer.put_template(template_id,data).json()["code"]
        assert 40004001 == code

        # 获取模板列表判断更新成功
        json_data = InterfaceExplorer.get_template().json()["data"]
        assert "不存在的模板" ==  json_data["items"][1]["name"]

        # 循环删除模板、不存在的模板、已删除的模板
        id = [9,8,7,6,5,4,3,2,1,123456,9]
        for delete_template in id:
            code = InterfaceExplorer.delete_template(delete_template).json()["code"]
            assert 0 == code

        # 获取模板列表判断删除成功
        json_data = InterfaceExplorer.get_template().json()["data"]
        assert [] == json_data["items"]