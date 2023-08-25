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
    def test_Query(self):
        # Explorer所用到的查询语句 并取出返回结果个数进行判断
        ngql = [
            'show spaces',
            'use nba',
            'match (v) return v limit 5',
            'MATCH (n) WHERE id(n) IN ["Spurs", "Carmelo Anthony", "Danny Green", "Dejounte Murray","Dwight Howard"] RETURN n',
            'SHOW TAG INDEXES',
            'LOOKUP ON  `player` WHERE  `player`.`age` == 31     yield vertex as `vertex_` | LIMIT 1',
            'GET SUBGRAPH 1 STEPS FROM "Danny Green" BOTH `like`, `serve`, `teammate`  YIELD VERTICES AS `vertices_`, EDGES AS `edges_`',
            'MATCH (n) WHERE id(n) IN ["Danny Green", "Tim Duncan", "Cavaliers", "Raptors", "Spurs", "Dejounte Murray", "Marco Belinelli", "LeBron James"] RETURN n	',
            'fetch prop on `teammate` "Tim Duncan"->"Danny Green"@0 YIELD edge as `edge_`',
            'fetch prop on `like` "Dejounte Murray"->"Danny Green"@0, "Marco Belinelli"->"Danny Green"@0, "Danny Green"->"LeBron James"@0, "Danny Green"->"Marco Belinelli"@0, "Danny Green"->"Tim Duncan"@0, "Marco Belinelli"->"Tim Duncan"@0, "Dejounte Murray"->"LeBron James"@0, "Dejounte Murray"->"Marco Belinelli"@0, "Dejounte Murray"->"Tim Duncan"@0 YIELD edge as `edge_`',
            'MATCH p=(v)-[e:`like`|:`serve`|:`teammate`*1]->(v2) WHERE id(v) IN ["Dejounte Murray"] AND ALL(l IN e WHERE  l.likeness == 99) RETURN p LIMIT 100',
            'MATCH (n) WHERE id(n) IN ["Dejounte Murray", "Kyle Anderson", "Russell Westbrook", "Tony Parker", "James Harden", "Kevin Durant", "Danny Green", "Chris Paul", "LeBron James", "Tim Duncan", "Manu Ginobili", "Marco Belinelli"] RETURN n',
            'fetch prop on `like` "Dejounte Murray"->"Kyle Anderson"@0, "Dejounte Murray"->"Russell Westbrook"@0, "Dejounte Murray"->"Tony Parker"@0, "Dejounte Murray"->"James Harden"@0, "Dejounte Murray"->"Kevin Durant"@0, "Dejounte Murray"->"Danny Green"@0, "Dejounte Murray"->"Chris Paul"@0, "Dejounte Murray"->"LeBron James"@0, "Dejounte Murray"->"Tim Duncan"@0, "Dejounte Murray"->"Manu Ginobili"@0, "Dejounte Murray"->"Marco Belinelli"@0 YIELD edge as `edge_`',
            'MATCH p=(v)<-[e:`like`|:`serve`|:`teammate`*1]-(v2) WHERE id(v) IN ["Tim Duncan"] AND ALL(l IN e WHERE  l.likeness == 90) RETURN p LIMIT 100',
            'MATCH (n) WHERE id(n) IN ["Manu Ginobili", "Tim Duncan"] RETURN n',
            'fetch prop on `like` "Manu Ginobili"->"Tim Duncan"@0 YIELD edge as `edge_`',
            'MATCH p=(v)-[e:`like`|:`serve`|:`teammate`*1]-(v2) WHERE id(v) IN ["Tim Duncan"] RETURN p LIMIT 5',
            'MATCH (n) WHERE id(n) IN ["Tony Parker", "Tim Duncan", "Tiago Splitter", "James Harden", "Marco Belinelli", "Manu Ginobili", "Boris Diaw", "Aron Baynes", "Spurs", "Danny Green", "Dejounte Murray", "LaMarcus Aldridge"] RETURN n	',
            'fetch prop on `like` "LaMarcus Aldridge"->"Tim Duncan"@0, "Dejounte Murray"->"Tim Duncan"@0, "Danny Green"->"Tim Duncan"@0, "Aron Baynes"->"Tim Duncan"@0, "Boris Diaw"->"Tim Duncan"@0 YIELD edge as `edge_`',
            '(GO FROM "Dejounte Murray" OVER *  YIELD dst(edge) as id  UNION GO FROM "Dejounte Murray"  OVER * REVERSELY YIELD src(edge) as id) INTERSECT(GO FROM "Danny Green" OVER *  YIELD dst(edge) as id  UNION GO FROM "Danny Green"  OVER * REVERSELY YIELD src(edge) as id)',
            'FIND ALL PATH FROM "Spurs", "Tim Duncan", "Marco Belinelli", "LeBron James" TO "Dejounte Murray", "Danny Green" OVER *  BIDIRECT UPTO 1 STEPS YIELD path as p | limit 5',
            'MATCH (n) WHERE id(n) IN ["Danny Green", "Tim Duncan", "Spurs", "LeBron James", "Marco Belinelli", "Dejounte Murray"] RETURN n',
            'fetch prop on `teammate` "Tim Duncan"->"Danny Green"@0 YIELD edge as `edge_`',
            'FIND ALL PATH FROM "Dejounte Murray" TO "Danny Green" over `like`, `serve`, `teammate`  UPTO 5 STEPS yield path as `_path` | LIMIT 5',
            'MATCH (n) WHERE id(n) IN ["Dejounte Murray", "Danny Green", "Tim Duncan", "Marco Belinelli"] RETURN n',
            'fetch prop on `teammate` "Tim Duncan"->"Danny Green"@0, "Tim Duncan"->"Danny Green"@0 YIELD edge as `edge_`',
            'fetch prop on `like` "Dejounte Murray"->"Danny Green"@0 YIELD edge as `edge_`',
            'fetch prop on `like` "Dejounte Murray"->"Danny Green"@0, "Dejounte Murray"->"Tim Duncan"@0, "Dejounte Murray"->"Marco Belinelli"@0, "Marco Belinelli"->"Danny Green"@0, "Dejounte Murray"->"Manu Ginobili"@0, "Manu Ginobili"->"Tim Duncan"@0, "Dejounte Murray"->"Manu Ginobili"@0 YIELD edge as `edge_`',
            'MATCH (v) RETURN id(v) as vid,tags(v) as tagsName limit 10	',
            'MATCH ()<-[e]-() RETURN src(e) as src, dst(e) as dst , rank(e) as rank limit 10'
        ]
        space = "nba"
        Length_assert = [8,0,5,5,4,1,2,8,1,9,11,12,11,1,2,1,5,12,5,4,5,6,1,5,4,2,1,7,10,10]
        for i in range(len(ngql)):
            Length = len(asyncio.run(InterfaceExplorer.test_WebSocket_ngql(ngql[i],space)).json()["body"]["content"]["data"]["tables"])
            assert Length_assert[i] == Length

    @pytest.mark.ngql
    def test_Schema(self):
        # Explorer中所用到的非查询语句
        ngql = [
            'CREATE SPACE `test_schema` (partition_num = 1, replica_factor = 1, vid_type = FIXED_STRING(30))',
            'use `test_schema`',
            'CREATE tag `test_Tag@@##--  __` (`string->int@@##  --` string NULL)',
            'ALTER tag `test_Tag@@##--  __` ADD (`string__##@@ **` string NULL)',
            'ALTER tag `test_Tag@@##--  __` ADD (`int_( )!@#$ $%` int NULL)',
            'CREATE edge `test_edge##$$ ()^*` (`int->string!@#$ *&!@$` int NULL )',
            'ALTER edge `test_edge##$$ ()^*` ADD (`string!@#$ *&!@$` string NULL)',
            'ALTER edge `test_edge##$$ ()^*` ADD (`int_!@#$ *&!@$` int NULL)',
            'CREATE TAG INDEX `test_index` on `test_Tag@@##--  __`(`string__##@@ **`(10), `int_( )!@#$ $%`)',
            'DROP tag INDEX `test_index`',
            'ALTER edge `test_edge##$$ ()^*` DROP (`int->string!@#$ *&!@$`)',
            'DROP EDGE `test_edge##$$ ()^*`',
            'ALTER tag `test_Tag@@##--  __` DROP (`string->int@@##  --`)',
            'DROP TAG `test_Tag@@##--  __`',
            'DROP SPACE `test_schema`'
        ]
        Status_assert = 'Success'
        for ngql in ngql:
            if ngql == 'use `test_schema`':
                print('新建spaces需要心跳,请等待')
                time.sleep(20)

            Status = asyncio.run(InterfaceExplorer.test_WebSocket_ngql(ngql)).json()["body"]["content"]["message"]
            assert Status_assert == Status