## 接口自动化项目


## 目录结构
```text
--------project
| 
|----api_project
|   |
|   |----apis（接口封装）
|   |   |
|   |   |----Client.py
|   |
|   |----testcases（测试用例脚本）
|   |   |
|   |   |----test_*.py
|   |   |----test_*.py
|   |
|   |----case_data_files（测试用例数据）
|   |   |
|   |   |----*_CASE_DATA.csv
|   |
|   |----common（公共方法）
|   |   |
|   |   |----ENV.py
|   |   |----csvUtils.py
|   |   |----jsonUtils.py
|   |   |----yamlUtils.py
|   |   |----emailService.py
|   |
|   |----config（配置数据）
|   |   |
|   |   |----case_config.py（测试用例配置文件）
|   |   |----config.py
|   |   |----email_config.py（邮件配置文件）
|   |   |----host_config.py（主机域名配置文件）
|   |   |----log_config.py（日志配置文件）
|   |
|   |----data（测试数据）
|   |   |
|   |   |----*
|   |
|   |----log（日志文件）
|   |   |
|   |   |----*.log
|   |
|   |----report（pytest测试报告）
|   |   |
|   |   |----（默认为空，执行前清空文件等内容）
|   |
|   |----allure_report（allure测试报告）
|   |   |
|   |   |----index.html
|   |   |----*
|   |
|----run_apis.py
```
----
## 使用前提
- Python>=3.9.*
  - xiaobaisaf库
  安装命令：`pip install -U xiaobaisaf`
- JDK>=8 
  
  `xiaobaiauto2Api -i jdk -v 17 -d D:\\`

- Allure

  `xiaobaiauto2Api -i allure -d D:\\`
-----

## 使用模板步骤

- 一、环境准备（<b style="color:red">必须</b>）
  - 1.1 （<b style="color:red">必须</b>）
  ```cmd
  1、cd API_Project                         # 进入项目
  2、init_env.bat 
     或 
     sh init_env.sh        # 执行脚本
  ```
----
- 二、一键生成/手动编写代码
  - 2.1 一键生成代码（即为：一键将curl命令转为python代码）
  ```cmd
  convert_ui.bat              # Windows系统执行文件
  或
  sh convert_ui.sh            # 非Windows系统执行文件
  ```
  - 2.2 手动编写代码（模仿一键生成方法即可，测试用例脚本、测试用例数据文件、用例配置文件）
---

- 三、执行
  - 3.1 信息配置（<b style="color:red">必须</b>）
  ```cmd
  # Email(邮箱配置)
  路径：API_Project>>api_project>>config>>email_config.py
  
  # BUG(BUG单配置)
  路径：API_Project>>api_project>>config>>bug_config.py
  
  # message(消息配置)
  路径：API_Project>>api_project>>config>>message_config.py
  ```
  - 3.2 执行用例，完毕后等效消息与报告
  ```cmd
  python run_apis.py
  ```