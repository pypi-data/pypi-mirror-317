#! /usr/bin/env python
# -*- coding=utf-8 -*-
"""
@Author: xiaobaiTser
@Time  : 2024/1/4 22:37
@File  : MonitorBrowser.py
"""
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep, time
from argparse import ArgumentParser

"""
selenium > 4.14
"""

async_js1 = """
function getXPathForElement(element) {
    if (element && element.id !== "" && element.id !== undefined) {
        return '//' + element.tagName.toLowerCase() + '[@id="' + element.id + '"]';
    }else if (element && element.name !== "" && element.name !== undefined) {
        return '//' + element.tagName.toLowerCase() + '[@name="' + element.name + '"]';
    }else if (element && element.name !== "" && element.name !== undefined) {
        return '//' + element.tagName.toLowerCase() + '[@href="' + element.href + '"]';
    }else if (element && element.src !== "" && element.src !== undefined) {
        return '//' + element.tagName.toLowerCase() + '[@src="' + element.src + '"]';
    }else if (element && element.value !== "" && element.value !== undefined) {
        return '//' + element.tagName.toLowerCase() + '[@value="' + element.value + '"]';
    }else if (element && element.tagName.toLowerCase() === 'html' && !element.parentNode) {
        return '/html';
    }else{
        var index = 0;
        var siblings = element.parentNode.childNodes;

        for (var i = 0; i < siblings.length; i++) {
            var sibling = siblings[i];

            if (sibling === element) {
                return getXPathForElement(element.parentNode) + '/' + element.tagName + '[' + (index + 1) + ']';
            }

            if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
                index++;
            }
        }
    }
}

var callback = arguments[arguments.length - 1];
var clickedElement = null;

// 监听切换标签页window事件，返回切换的标签页句柄
window.addEventListener('message', function(event) {
    if (event.data.type === 'tabChanged') {
        var clickedElement = event.data.clickedElement;
        var iframeAncestor = event.data.iframeAncestor;
        var xpath = event.data.xpath;
        var value = {
            "iframeAncestor": iframeAncestor,
            "clickedElement": clickedElement.tagName,
            "localStorage": localStorage.getItem('XPATH'),
            "xpath": xpath
        }
        console.log(clickedElement.tagName);
        console.log(value);
        callback(value);
    }
});

// 监听点击事件，返回点击的元素的xpath表达式
window.addEventListener('click', function(event) {
    var clickedElement = event.target;
    // 获取最近的包含 iframe 的祖先元素
    var iframeAncestor = clickedElement.closest("iframe");
    // 点击元素的xpath表达式
    var xpath = getXPathForElement(clickedElement);
    // 部分元素type为submit需要存储到缓存中
    if (clickedElement && clickedElement.tagName.toLowerCase() === 'input' && clickedElement.type ==='submit') {
        localStorage.setItem('XPATH', getXPathForElement(clickedElement));
    }
    var value = {
        "iframeAncestor": iframeAncestor,
        "clickedElement": clickedElement.tagName,
        "localStorage": localStorage.getItem('XPATH'),
        "xpath": xpath
    }
    console.log(clickedElement.tagName);
    console.log(value);
    callback(value);
});
"""

async_js = """
// 用于存储操作记录的数组
let operationRecords = [];

// 缓存已计算过定位表达式的元素，减少重复计算开销
const locatorCache = new Map();

// 生成元素的定位表达式（简单示例，主要以xpath为主，可根据需求扩展更多定位方式）
function generateLocator(element) {
    if (locatorCache.has(element)) {
        return locatorCache.get(element);
    }
    if (element.tagName === 'IFRAME') {
        // 对于iframe元素，先记录切换到iframe的操作
        const iframeIndex = Array.from(document.querySelectorAll('iframe')).indexOf(element);
        operationRecords.push({
            action:'switchToIframe',
            locator: `//iframe[${iframeIndex + 1}]`,
            data: {}
        });
        return;
    }
    try {
        let xpath = "";
        let elementCopy = element;
        while (elementCopy.nodeType === Node.ELEMENT_NODE) {
            let siblingsWithSameTagName = Array.from(elementCopy.parentNode.childNodes).filter(node => node.nodeType === Node.ELEMENT_NODE && node.tagName === elementCopy.tagName);
            let position = siblingsWithSameTagName.indexOf(elementCopy) + 1;
            xpath = `/${elementCopy.tagName.toLowerCase()}[${position}]` + xpath;
            elementCopy = elementCopy.parentNode;
        }
        const result = xpath;
        locatorCache.set(element, result);
        return result;
    } catch (e) {
        console.error("生成xpath定位表达式出错:", e);
        return null;
    }
}

// 记录上一次点击的相关信息及时间戳
let lastClickInfo = null;
// 定义重复点击间隔时间（毫秒），可根据实际情况调整
const duplicateClickInterval = 500;
// 处理点击事件的函数，优化重复点击记录问题
function handleClick(event) {
    const target = event.target;
    const action = 'click';
    const locator = generateLocator(target);
    const data = {};
    if (target.id) {
        data['id'] = target.id;
    }
    if (target.className) {
        data['class'] = target.className;
    }
    const currentClickInfo = { locator, data };
    if (lastClickInfo &&
        lastClickInfo.locator === currentClickInfo.locator &&
        Date.now() - lastClickInfo.timestamp < duplicateClickInterval) {
        return; // 如果和上一次点击重复且在间隔时间内，直接返回不记录
    }
    operationRecords.push({
        action: action,
        locator: locator,
        data: data
    });
    console.log({
        action: action,
        locator: locator,
        data: data
    });
    lastClickInfo = { locator, data, timestamp: Date.now() }; // 更新上一次点击信息
}

// 使用事件委托，将点击事件监听器添加到body上，减少不必要的事件处理开销
document.body.addEventListener('click', function (event) {
    const target = event.target;
    if (target.tagName && target.tagName!== 'SCRIPT') {
        handleClick(target);
    }
});

// 标记标签页是否正在切换，避免重复记录标签页切换操作
let isTabSwitching = false;
function handleTabSwitch() {
    if (isTabSwitching) {
        return;
    }
    operationRecords.push({
        action:'switchTab',
        locator: '',
        data: {}
    });
    console.log({
        action:'switchTab',
        locator: '',
        data: {}
    });
    isTabSwitching = true;
    setTimeout(() => {
        isTabSwitching = false;
    }, 1000);
}

// 模拟浏览器的MutationObserver，当DOM变化时可能触发的逻辑（可根据实际进一步完善）
const observer = new MutationObserver(() => {
    // 这里可以添加检测DOM变化是否是由于标签页切换等相关情况导致的逻辑，然后按需调用handleTabSwitch等函数
});
observer.observe(document.documentElement, {
    childList: true,
    subtree: true,
    attributes: true,
    characterData: true
});

// 异步执行的回调函数处理，符合在selenium中异步执行js的要求
var callback = arguments[arguments.length - 1];
setTimeout(() => {
    callback(operationRecords);
}, 0);
"""



# thread_lock = Lock()


# 定义一个简单的线程类
# class MyThread(Thread):
#     def __init__(self, name, target, args):
#         super().__init__()
#         self.name = name
#         self.target = target
#         self.args = args
#         self.stop_flag = False
#
#     def run(self):
#         # print(f"线程 {self.name} 启动")
#         while not self.stop_flag:
#             print(f"参数 self.args = {self.args}")
#             self.target(self.args)
#             # print(f"线程 {self.name} 正在运行")
#             sleep(0.5)
#         # print(f"线程 {self.name} 结束")
#
#     def stop(self):
#         # print(f"停止线程 {self.name}")
#         self.stop_flag = True


def addJSEventListener(browser):
    # print('正在加载js脚本...')
    # 等待所有元素加载完成
    WebDriverWait(browser, 30).until(
        EC.presence_of_all_elements_located((By.XPATH, "//*"))
    )

    try:
        # print('正在获取本地存储的xpath表达式...')
        # local_xpath = browser.execute_script("return localStorage.getItem('xpath')")
        # if local_xpath:
        #     print("您点击元素的Xpath表达式:", local_xpath)
        #     browser.execute_script("localStorage.removeItem('xpath')")
        # else:
        print('执行js脚本，等待操作中...')
        result = browser.execute_async_script(async_js)
        # 输出返回值
        print("您点击元素的Xpath表达式:", result)
    except Exception as e:
        print(e)


class MonitorBrowser(object):
    def __init__(self):
        """初始化浏览器对象"""
        self.Options = webdriver.ChromeOptions()
        self.Options.add_experimental_option(
            "useAutomationExtension", False
        )  # 去除"Chrome正在受到自动化测试软件的控制"弹出框信息
        self.Options.add_experimental_option(
            "excludeSwitches", ["--enable-automation"]
        )  # 去除"Chrome正在受到自动化测试软件的控制"弹出框信息
        self.Options.add_experimental_option("detach", True)  # 禁止自动关闭浏览器
        self.Options.add_argument("--ignore-ssl-errors")
        self.Options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )  # 隐藏Webdriver特征

    def browser_status(self):
        """关闭浏览器"""
        try:
            self.browser.title
            return True
        except Exception as e:
            return False

    def start(self, url="https://www.baidu.com"):
        """启动浏览器"""
        self.browser = webdriver.Chrome(options=self.Options)
        self.browser.implicitly_wait(30)
        # self.browser.get("https://mail.163.com/")  # iframe案例
        # self.browser.get('https://www.baidu.com/')  # type=submit案例
        self.browser.get(url)
        self.browser.set_script_timeout(120)
        _t_list = []

        while self.browser_status():
            self.browser.switch_to.default_content()
            _start_time = time()
            addJSEventListener(self.browser)
            # print(f'主页注入js耗时：{time() - _start_time}s')
            # _t_list.append(MyThread(name='page', target=addJSEventListener, args=self.browser))
            iframes = self.browser.find_elements(By.XPATH, "//iframe")
            for i, _ in enumerate(iframes):
                _start_time = time()
                self.browser.switch_to.default_content()
                self.browser.switch_to.frame(_)
                addJSEventListener(self.browser)
                # print(f'iframe_{i}注入js耗时：{time() - _start_time}s')
                # _t_list.append(MyThread(name=f'iframe_{i}', target=addJSEventListener, args=self.browser))

            # for i, t in enumerate(_t_list):
            #     self.browser.switch_to.default_content()
            #     if 0 == i:
            #         t.start()
            #     else:
            #         self.browser.switch_to.frame(iframes[i-1])
            #         t.start()

            sleep(0.2)
            # for t in _t_list:
            #     t.stop()
        self.browser.quit()

    # @property
    # def js(self):
    #     return open("getXPathInCurrentPage.js", "r", encoding="utf-8").read()

def main():
    args = ArgumentParser(
        description="浏览器监控，自动生成元素的xpath表达式",
    )
    args.add_argument('-u', '--url',
                      default='https://www.baidu.com',
                      type=str,
                      help='开始链接的url')
    user_args = args.parse_args()

    monitor = MonitorBrowser()
    monitor.start(url=user_args.url)

if __name__ == "__main__":
    main()
