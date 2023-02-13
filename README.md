
 ### 使用
 
 - 前置条件 安装所用到的依赖

  ```
  pip install -r requirements.txt
  pip3 install -r requirements.txt
  ```

 - 所有用例执行

  ```
  pytest
  ```

- login登录用例执行

  ```
  pytest -m login
  ```

- 上传文件测试用例执行

  ```
  pytest -m files
  ```
  
- 快照测试用例执行

  ```
  pytest -m snapshot
  ```

- 模板测试用例执行

  ```
  pytest -m template
  ```

- 自定义增强测试用例执行

  ```
  pytest -m icons
  ```

- workflow测试用例执行

  ```
  pytest -m workflow
  ```
  
