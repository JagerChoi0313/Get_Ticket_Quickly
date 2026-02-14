from selenium import webdriver
import os
import time
import pickle

#大麦网首页
damai_url="https://www.damai.cn/"

#登录页面
login_url="https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F"

#抢票页面
target_url="https://detail.damai.cn/item.htm?spm=a2oeg.home.card_0.ditem_1.275523e1kiDZzj&id=1018231634918"


class Concert:
    """初始化加载"""
    def __init__(self):
        self.status = 0   #状态：表示当前登录执行到了哪个步骤
        self.login_method=1  # {0：模拟登录  1：cookie登录}
        self.driver=webdriver.Chrome() #初始化浏览器，自动查找驱动

    """cookies：登录网站的时候出现的，记录用户信息"""
    def set_cookies(self):
        self.driver.get(login_url)
        print("###请扫码登录###")
        time.sleep(10)
        print("###登录成功###")
        # cookie.pkl
        pickle.dump(self.driver.get_cookies(),open('cookies.pkl','wb'))
        print("###cookies保存成功")
        #抢票
        self.driver.get(target_url)


    """如果当前已经有了cookies.pkl"""
    def get_cookie(self):
        cookies = pickle.load(open('cookies.pkl','rb'))
        for cookie in cookies:
            # 使用原始的cookie信息，只移除可能导致问题的字段
            cookie_dict = cookie.copy()
            if 'expiry' in cookie_dict:
                del cookie_dict['expiry']
            # 确保domain正确
            if 'domain' in cookie_dict and cookie_dict['domain']:
                pass  # 使用原始domain
            else:
                cookie_dict['domain'] = '.damai.cn'
            self.driver.add_cookie(cookie_dict)
        print("###载入cookie成功###")


    """登录"""
    def login(self):
        #如果为0就模拟登录一下
        if self.login_method == 0:
            self.driver.get(login_url)
        elif self.login_method == 1:
            # 如果当前目录下没有cookies.pkl这个文件
            if not os.path.exists('cookies.pkl'):
                # 登录一下 登录信息记录
                self.set_cookies()
            else:
                # 先访问大麦网首页，确保域名匹配
                self.driver.get(damai_url)
                # 登录一下 通过selenium传入用户信息
                self.get_cookie()
                # 再访问目标页面
                self.driver.get(target_url)

    """打开浏览器"""
    def enter_concert(self):
        print("###打开浏览器，进入大麦网###")
        # 调用login
        self.login()
        self.driver.refresh()
        self.status=2
        print("###登录成功###")


    # 抢票并且下单
    def choose_ticket(self):
        if self.status == 2:
            print('='*30)
            print("###请开始日期选择和票价选择###")
            while self.driver.title.find("确认订单")==1:
                # 下单按钮
                buybutton=self.driver.find_element_by_class_name("buybtn").text
                if buybutton == '提交缺货登记':
                    self.driver.refresh()
                elif buybutton == '立即购票':
                    self.driver.find_element_by_class_name("buybtn").click()
                elif buybutton == '选座购买':
                    self.driver.find_element_by_class_name("buybtn").click()
                    self.status =4
                else:
                    self.status =100
                title=self.driver.title
                if title=='选座购买':
                    # 执行选座位操作
                    self.status =10
                elif title=='确认订单':
                    # 实现下单逻辑
                    while True:
                        print('###正在加载###')
                        self.check_order()
                        break

    """下单操作"""
    def check_order(self):
        print("###开始确认订单###")
        try:
            self.driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div[2]/svg').click()
        except Exception as e:
            print("###购票人信息选中失败，自行查看元素位置###")
            print(e)
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//*[@id="root"]/div/div[14]/div/div[2]/button').click()



if __name__ == '__main__':
   con=Concert()
   con.enter_concert()
   con.choose_ticket()

   # 保持浏览器窗口打开
   input("###抢票程序已启动，按回车键退出###")