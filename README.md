# TPAP-auto

Nebula-auto用户测试TP+AP的接口功能。

当前只适用于 nebula graph v3.0 （待定）以上版本

主要功能：

​	使用pytest框架对TP+AP的接口进行功能测试

## 使用说明

### 环境准备

- controller 部署（具体操作见controller的部署手册）

- plato 集群部署（具体操作见plato的部署手册）

- HDFS 部署（具体自行百度）

- nebula graph环境准备

  - 部署nebula graph （具体操作见graph的使用手册）

  - 创建数据查询空间：basketballplayer，并使用importer导入数据： [basketballplayer ](https://docs-cdn.nebula-graph.com.cn/dataset/dataset.zip)

    - 创建schema

    ```
    ## 创建图空间
    nebula> CREATE SPACE dag_auto_query \
            (partition_num = 10, \
            replica_factor = 1, \
            vid_type = FIXED_STRING(30));
    
    ## 选择图空间 dag_auto_query
    nebula> USE dag_auto_query;
    
    ## 创建 Tag player
    nebula> CREATE TAG player(name string, age int);
    
    ## 创建 Tag team
    nebula> CREATE TAG team(name string);
    
    ## 创建 Edge type follow
    nebula> CREATE EDGE follow(degree int,weight double);
    
    ## 创建 Edge type serve
    nebula> CREATE EDGE serve(start_year date, end_year date,weight double);
    ```

    - schema创建成功后，使用importer导入数据： [basketballplayer ](https://docs-cdn.nebula-graph.com.cn/dataset/dataset.zip)

  - 创建结果写入空间：algo_result

    ```
    ## 创建图空间
    nebula> CREATE SPACE dag_auto_result \
            (partition_num = 10, \
            replica_factor = 1, \
            vid_type = FIXED_STRING(30));
    ```

    

- TPAP_auto 运行环境准备

  ```
  sudo apt-get install -y python3-pip python
  
  git clone https://github.com/shanlai/TPAP-auto.git
  
  cd TPAP-auto
  
  
  ```

- 将上述环境信息配置到TPAP-auto/explorer_auto/conf/conf.yaml文件，具体内容如下，请根据实际的部署情况修改「必改项」：

  ```
  # 必改项：controller的服务地址
  base_url: "http://192.168.8.88:9002"
  
  # 必改项：HDFS连接信息
  hdfs_url: http://192.168.8.88:9002
  hdfs_username: zhuang.miao
  
  # 必改项：plato集群信息
  plato_cluster: ["192.168.8.88"]
  
  # 必改项：nebula grapd连接信息
  graphd_ip: "192.168.8.168:9669"
  graphd_username: "root"
  graphd_password: "nebula"
  
  # nebula grapd：读取数据的space
  query_database: basketballplayer
  
  # nebula grapd：写入数据的space
  result_database: algo_result
  ```

  

### 使用

- smoke用例执行

  ```
  python3 -m pytest -m smoke
  ```

- 接口用例执行

  ```
  python3 -m pytest -m interface
  ```

- 算法用例用例执行

  ```
  python3 -m pytest -m algo
  ```

- 所有用例的执行

  ```
  python3 -m pytest
  ```

  
