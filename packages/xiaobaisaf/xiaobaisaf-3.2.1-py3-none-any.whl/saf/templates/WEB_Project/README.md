## 使用说明
### 0、环境准备
```cmd
1、安装JDK（安装命令：xiaobaiauto2Api -i jdk -v 17 -d D:\）
2、python -m venv venv
3、venv\Scripts\activate.bat(windows) 
   或 
   source venv/bin/activate(mac、linux)
```
### 1、生成POM代码
```cmd
修改并执行：
pomGenerator.bat
```
### 2、生成测试用例
```cmd
1、自行编写测试用例
或
2、使用Selenium IDE生成测试用例
```
### 3、修改用例文件
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
### 4、执行用例
```cmd
python main.py
或
main.bat            # Windows系统执行文件
或
sh main.sh          # 非Windows系统执行文件
```