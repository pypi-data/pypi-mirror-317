## 接口自动化项目


## 目录结构
```text
--------API_Project
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
|   |   |----Email.py
|   |   |----CSV.py
|   |   |----BUG.py
|   |   |----Data.py
|   |   |----LOG.py
|   |   |----Message.py
|   |   |----Network.py
|   |
|   |----config（配置数据）
|   |   |
|   |   |----case_config.py（测试用例配置文件）
|   |   |----allure_config.py（allure配置文件）
|   |   |----bug_config.py（BUG单配置文件）
|   |   |----email_config.py（邮件配置文件）
|   |   |----host_config.py（主机域名配置文件）
|   |   |----log_config.py（日志配置文件）
|   |   |----message_config.py（消息配置文件）
|   |
|   |----bin 
|   |   |
|   |   |----allure
|   |       |----bin
|   |           |----allure.bat (allure可执行文件)
|   |           |----allure (allure可执行文件)
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
|
|----convert_ui.bat                # curl转项目的脚本
|----convert_ui.sh                 # curl转项目的脚本
|----convert_ui.py                 # curl转项目的脚本
|----init_env.bat                  # 初始化环境脚本
|----init_env.sh                   # 初始化环境脚本
|----run_apis.bat                  # 执行用例脚本
|----run_apis.sh                   # 执行用例脚本
|----run_apis.py                   # 执行用例脚本
```
----
## 环境准备
- 1、Python>=3.9.*
  - 1.1、xiaobaisaf库`pip install -U xiaobaisaf`
- 2、JDK>=8 `xiaobaiauto2Api -i jdk -v 17 -d D:\\`
- 3、Allure（已经自带）
-----

## 使用步骤

### 一、生成模板
  - 1.1 创建模板
  ```cmd
  xiaobaicmd -t api 
  ```
  
  - 1.2 初始化环境（初始化项目）
  ```cmd
  cd API_Project
  init_env.bat  或  sh init_env.sh
  ```
----
### 二、转换代码
  - 2.1 打开转换工具
  ```cmd
  convert_ui.bat  或 sh convert_ui.sh
  ```
---

### 三、执行
  - 3.1 信息配置（<b style="color:red">必须</b>）
  ```cmd
  Email(邮箱服务配置)
  API_Project>>api_project>>config>>email_config.py
  
  BUG(BUG单配置)
  API_Project>>api_project>>config>>bug_config.py
  
  message(消息配置)
  API_Project>>api_project>>config>>message_config.py
  ```
  - 3.2 执行用例，完毕后等效消息与报告
  ```cmd
  run_apis.bat  或 sh run_apis.sh  或 python run_apis.py
  ```