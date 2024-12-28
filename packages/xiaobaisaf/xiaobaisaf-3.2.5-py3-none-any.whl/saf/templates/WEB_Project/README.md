## 环境准备
- 1、Python>=3.9.*
  - 1.1、xiaobaisaf库`pip install -U xiaobaisaf`
- 2、JDK>=8 `xiaobaiauto2Api -i jdk -v 17 -d D:\\`
- 3、Allure（已经自带）
-----

## 使用说明
#### 1、导出Web模板
`xiaobaicmd -t web -d D:/`

#### 2、进入模板目录
`cd Web_Project`

#### 3、初始化环境
`init_env.bat 或者 init_env.sh 或者 python init_env.py`

#### 4、运行POM工具（将网页自动生成PO模型代码）
`pomGenerator.bat`
或者
`xiaobaipom --help`

#### 5、修改配置文件（具体位置如下）
```cmd
  Email(邮箱服务配置)
  Web_Project>>web_project>>config>>email_config.py

  BUG(BUG单配置)
  Web_Project>>web_project>>config>>bug_config.py
  message(消息配置)
  Web_Project>>web_project>>config>>message_config.py
```

#### 6、修改测试用例（可选）
路径：WEB_Project>>web_project>>testcases>>*
```python
import pytest
import allure
from web_project.pageObjects.PAGE1 import page1_class   # 导入页面类，此行代码需要修改

@allure.feature("功能名称")
class TestCase:
    
    ...  # 省略其他代码
    
    @allure.story("用例名称")
    def test_case(self, driver):
        # 实例化页面
        p1 = page1_class(driver)
        # 打开p1页面
        driver.get(p1.page_url)
        # 操作p1页面的元素
        p1.send_username("admin")
        p1.send_password("123456")
        p1.click_login()
        # 断言
        assert driver.title == "xxxxx"
```

#### 7、执行用例
`main.bat 或者 main.sh 或者 python main.py`
