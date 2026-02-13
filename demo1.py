from selenium import webdriver
import os
import time
import pickle

#大麦网首页
damai_url="https://www.damai.cn/"

#登录页面
login_url="https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F"

#抢票页面
target_url="https://detail.damai.cn/item.htm?spm=a2oeg.search_category.0.0.723c4d15lc4cXL&id=1014297695248&clicktitle=2026%E4%BA%94%E7%99%BE%E9%87%8C%E9%9F%B3%E4%B9%90%E8%8A%82"


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
            print(cookie)
            self.driver.add_cookie(cookie)

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
                self.driver.get(target_url)
                # 登录一下 通过selenium传入用户信息
                self.get_cookie()

if __name__ == '__main__':
   con=Concert()
   con.login()