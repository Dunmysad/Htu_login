#!/usr/bin/env python3
import requests
from lxml import etree
import webbrowser
import re
import sys
import time
import os
'''
在下方完善信息
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
'''
userid = ''   # 学号
passwd = ''   # 宿舍密码
passwd_jxl = '' # 教学楼密码
oper = '' # 手机运营商 移动 / 联通 / 电信
'''
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
在上方完善信息
'''
# 禁用requests的代理
os.environ['NO_PROXY'] = "*"

# 获取登录页面网址
def ReturnStartUrl():
    return "http://223.5.5.5"

# 警告信息
def AlartInfo(result):
    html = etree.HTML(result.text)
    error = html.xpath('//script/text()')[0]
    try:
        alert = re.findall(r'(?<=alert\(\').*(?=\')', error)[0]
    except Exception as e:
        print(e)
    print(f'{alert}')
    input()

# 宿舍登录信息
# 需要重新抓新的html中信息进行判断result.text
def SuccessInfo(result):
    if '校园黄页' in result.content.decode():
        print(f'登陆成功!')
        webbrowser.open('https://www.htu.edu.cn')
        ReConnect()
    else:
        # print(result.content.decode())
        input('未知错误')

# 是否选择登出
def islogOut():
    logOut = input(f'已经登录,请勿重复登录! \n是否登出? (yes/y or no/n)选择不登出将进入等待模式！\n ')
    if logOut in ['yes', 'y']:
        url = "http://autewifi.net/loginOut"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        } 
        response = requests.post(url=url, headers=headers)
        if IsConnected(Start_Url):
            try:
                print(response.json()['msg'], end="")
                input()
            except:
                print(f'登出失败\n{location}暂时不能登出!')
                input()
                sys.exit()
            else:
                sys.exit()
        else:
            pass
    else:
        ReConnect()

# 检测登录地
def ReturnLocation(Start_Url):
    Location = ''
    response = requests.get(Start_Url)
    if '河南师范大学校园网登录' in response.text:
        return Location + '宿舍'
    elif 'UrlPathError\n' in response.text:
        return Location
    else:
        return Location + '教学楼'

# 检测是否连接到校园网
def IsConnected(Start_Url):
    try:
        requests.get(url=Start_Url)
    except:
        return False
    else:
        return True

# 获取基本信息
def GetInfo(Start_Url,location):
    response = requests.get(url=Start_Url)
    if location == '宿舍':
        try:     
            NextUrl = response.url  
            cookies = response.headers['Set-Cookie']
            cookie = re.findall(r'.*(?=; Path)', cookies)[0]    
        except Exception as e:
            islogOut()
    elif location == '教学楼':
        try:
            NextUrl = re.findall(r'(?<=location.href=\").*(?=\")', response.text)[0] 
            cookies = requests.get(NextUrl).headers['Set-Cookie']  
            cookie = re.findall(r'.*(?=; Path)', cookies)[0]  
        except Exception as e:
            islogOut()
    else:
        islogOut()
    html = etree.HTML(requests.get(url=NextUrl).text)
    WlanacIp = html.xpath('//input[@id="wlanacIp"]/@value')[0]    
    wlanuserip = re.findall(r'(?<=wlanuserip=).*(?=&)', NextUrl)[0]     
    wlanacIp = re.findall(r'(?<=//).*(?=/po)', NextUrl)[0]  
    wlanacname = re.findall(r'(?<=wlanacname=).*', NextUrl)[0]  
    return NextUrl, wlanuserip, wlanacIp, cookie, wlanacname, WlanacIp, NextUrl

# 登录
def login(Location):
    NextUrl, wlanuserip, wlanacIp, cookie, wlanacname, WlanacIp, NextUrl = GetInfo(Start_Url, location)
    login_PostURL = f'http://{wlanacIp}/portalAuthAction.do'

    # 宿舍登陆
    if Location == '宿舍':
        yys={'移动': '@yd', '联通': '@lt', '电信': '@dx'}
        operator = yys[oper]
        data = {
                'wlanuserip': wlanuserip,
                'wlanacname': wlanacname,
                'chal_id': '',
                'chal_vector': '',
                'auth_type': 'PAP',
                'seq_id': '',
                'req_id': '',
                'wlanacIp': WlanacIp,
                'ssid': '',
                'vlan': '',
                'mac': '',
                'message': '',
                'bank_acct': '',
                'isCookies': '',
                'version': '0',
                'authkey': '88----89',
                'url': '',
                'usertime': '0',
                'listpasscode': '0',
                'listgetpass': '0',
                'getpasstype': '0',
                'randstr': '7462',
                'domain': '',
                'isRadiusProxy': 'true',
                'usertype': '0',
                'isHaveNotice': '0',
                'times': '12',
                'weizhi': '0',
                'smsid': '1',
                'freeuser': '',
                'freepasswd': '',
                'listwxauth': '0',
                'templatetype': '1',
                'tname': 'shida_pc_portal_mubiao_V2.1',
                'logintype': '0',
                'act': '',
                'is189': 'false',
                'terminalType': '',
                'checkterminal': 'true',
                'portalpageid': '261',
                'listfreeauth': '0',
                'viewlogin': '1',
                'userid': userid + operator,
                'authGroupId': '',
                'userName': userid + operator,
                'passwd': passwd,
                'useridtemp': userid + operator,
                'operator': operator
               }
        headers = {
            'Host': wlanacIp,
            'Content-Length': '666',
            'Cache-Control': 'max-age = 0',
            'Upgrade-Insecure - Requests': '1',
            'Origin': f'http://{wlanacIp}',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': NextUrl,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN, zh;q=0.9',
            'Cookie': cookie,
            'Connection': 'close',
        }

        # 宿舍登陆处理
        try:   
            while True:
                    result = requests.post(url=login_PostURL, data=data, headers=headers)
                    if '此帐号已在其它设备登录' in result.text:
                        error = etree.HTML(result.text)
                        e = error.xpath('//script/text()')[1]
                        alert = re.findall(r'(?<=alert\(\").*(?=\"\))', e)[0]
                        print(f'{alert} \n正在重新登录')
                        time.sleep(2)
                        continue
                    elif '5' in result.text:
                        if IsConnected(Start_Url):
                            SuccessInfo(result)
                            break
                        else:
                            print(f'正在等待，5s后再次登录')
                            time.sleep(6)
                            continue 
                    else:
                        AlartInfo(result)
                        input()
        except:
            AlartInfo(result)
            input()

    # 教学楼登陆
    elif Location == '教学楼':
        headers = {
            'Host': wlanacIp,
            'Content-Length': '600',
            'Cache-Control': 'max - age = 0',
            'Upgrade-Insecure - Requests': '1',
            'Origin': f'http://{wlanacIp}',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Accept': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Accept - Encoding': 'gzip, deflate',
            'Accept - Language': 'zh - CN, zh;q = 0.9',
            }
        data = {
            'wlanuserip': wlanuserip,
            "wlanacname": wlanacname,
            'chal_id': '',
            'chal_vector': '',
            'auth_type': '',
            'seq_id': '',
            'req_id': '',
            'wlanacIp': WlanacIp,
            'ssid': '',
            'vlan': '',
            'mac': '',
            'message': '',
            'bank_acct': '',
            'isCookies': '',
            'version': '0',
            'authkey': '88 ----89',
            'url': '',
            'usertime': '0',
            'listpasscode': '0',
            'listgetpass': '0',
            'getpasstype': '0',
            'randstr': '4687',
            'domain': '',
            'isRadiusProxy': 'false',
            'usertype': '0',
            'isHaveNotice': '0',
            'times': '12',
            'weizhi': '0',
            'smsid': '',
            'freeuser': '',
            'freepasswd': '',
            'listwxauth': '0',
            'templatetype': '1',
            'tname': 'shida_pc_portal',
            'logintype': '0',
            'act': '',
            'is189': 'false',
            'terminalType': '',
            'checkterminal': 'true',
            'portalpageid': '101',
            'listfreeauth': '0',
            'viewlogin': '1',
            'userid': userid,
            'authGroupId': '',
            'useridtemp': userid,
            'passwd': passwd_jxl
            }
        response = requests.post(url=login_PostURL, data=data, headers=headers)
        # print(response.text)

        # 教学楼登录信息
        if '百度' in requests.get('https://www.baidu.com').content.decode():
            print('登录成功')
        else:
            error = response.text
            try:
                e = re.findall(r'(?<=alert\(\').*(?=\')', error)[0]
                print(f'{e}')
                input()
            except Exception as e:
                print(f'{e}')
                input()

# 等待模式            
def ReConnect():
    print("程序进入等待模式")
    T1 = time.perf_counter()
    while True:
        try:
            '百度' in requests.get('http://www.baidu.com').content.decode()
            T2 = time.perf_counter()
            print(f'\r    time wait : {round(T2 - T1)} s ', end='')
        except(ValueError, ArithmeticError):
            print(f'\n网络于 {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} 断开')
            print('\n3 s 后重新连接校园网')
            time.sleep(3)
            print(f'\n网络于 {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} 尝试连接')
            os.system('python login.py')

# 检测信息是否为空
def checkInfo(Location):
    info = [userid, passwd, passwd_jxl, oper]
    info_name = ['userid', 'passwd', 'passwd_jxl', 'oper']
    if '' in info:
        input(f"请确保 {info_name[info.index('')]} 不为空")
        sys.exit()

if __name__ == '__main__':
    Start_Url = ReturnStartUrl()
    if IsConnected(Start_Url):
        location = ReturnLocation(Start_Url)
        checkInfo(location)
        if location == '':
            islogOut()
        if IsConnected(Start_Url):
            print(f'现在您正处于{location}')
            login(location)
            ReConnect()
    else:
        input(f'未连接到校园网络')
