import requests
from lxml import etree
import re
import sys
import time

'''
在下方完善信息
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
'''
userid = '1928424***'
passwd = '*************'
passwd_jxl = '308533'
oper = '移动'
'''
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
在上方完善信息
'''
# 获取登录页面网址
def ReturnStartUrl():
    return "http://223.5.5.5"

# 警告信息
def AlartInfo(result):
    html = etree.HTML(result.text)
    error = html.xpath('//script/text()')[0]
    alert = re.findall(r'(?<=alert\(\').*(?=\')', error)[0]
    print(f'{alert}')
    input()

# 登录成功信息
def SuccessInfo(result):
    realName = etree.HTML(result.text).xpath('//input[@id="realName"]/@value')[0]
    title = etree.HTML(result.text).xpath('//title/text()')[0]
    school = re.findall(r'.*(?=校园网)', title)[0]
    print(f'{school + realName}登陆成功!')
    input()

# 是否选择登出
def islogOut():
    logOut = input(f'已经登录,请勿重复登录! \n是否登出? (yes/y or no/n)\n')
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
        sys.exit()

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
            NextUrl = response.url  # return http://10.101.2.199/portalReceiveAction.do?wlanuserip=10.104.28.190&wlanacname=HSD-BRAS-SR8808/X-2
            cookies = response.headers['Set-Cookie']    # return JSESSIONID=5EE018CF5886AF0193D6BC539E31C59C; Path=/; HttpOnly
            cookie = re.findall(r'.*(?=; Path)', cookies)[0]    # return JSESSIONID=5EE018CF5886AF0193D6BC539E31C59C
        except Exception as e:
            islogOut()
    elif location == '教学楼':
        try:
            NextUrl = re.findall(r'(?<=location.href=\").*(?=\")', response.text)[0] # retuen http://210.42.255.130/portalReceiveAction.do?wlanuserip=10.37.133.141&wlanacname=HNSFDX_H3C-S8808-X
            cookies = requests.get(NextUrl).headers['Set-Cookie']  # return JSESSIONID=5EE018CF5886AF0193D6BC539E31C59C; Path=/; HttpOnly
            cookie = re.findall(r'.*(?=; Path)', cookies)[0]  # return JSESSIONID=87F3916E17CF62EE0D69B85C23551EEB.worker1      
        except Exception as e:
            islogOut()
    else:
        islogOut()
    html = etree.HTML(requests.get(url=NextUrl).text)
    WlanacIp = html.xpath('//input[@id="wlanacIp"]/@value')[0]    # return 10.101.2.35
    wlanuserip = re.findall(r'(?<=wlanuserip=).*(?=&)', NextUrl)[0]     # return 10.104.28.190
    wlanacIp = re.findall(r'(?<=//).*(?=/po)', NextUrl)[0]  # return 10.101.2.199
    wlanacname = re.findall(r'(?<=wlanacname=).*', NextUrl)[0]  # return HSD-BRAS-SR8808/X-2    

    return NextUrl, wlanuserip, wlanacIp, cookie, wlanacname, WlanacIp, NextUrl

# 登录
def login(Location):
    login_PostURL = f'http://{GetInfo(Start_Url, location)[2]}/portalAuthAction.do'
    if Location == '宿舍':
        yys={'移动': '@yd', '联通': '@lt', '电信': '@dx'}
        operator = yys[oper]

        data = {
                'wlanuserip': GetInfo(Start_Url, location)[1],
                'wlanacname': GetInfo(Start_Url, location)[4],
                'chal_id': '',
                'chal_vector': '',
                'auth_type': 'PAP',
                'seq_id': '',
                'req_id': '',
                'wlanacIp': GetInfo(Start_Url, location)[5],
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
            'Host': GetInfo(Start_Url, location)[2],
            'Content-Length': '666',
            'Cache-Control': 'max-age = 0',
            'Upgrade-Insecure - Requests': '1',
            'Origin': f'http://{GetInfo(Start_Url, location)[2]}',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': GetInfo(Start_Url, location)[0],
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN, zh;q=0.9',
            'Cookie': GetInfo(Start_Url, location)[3],
            'Connection': 'close',
        }
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
        except:
            if IsConnected(Start_Url):
                SuccessInfo(result)
            else:
                AlartInfo(result)


    elif Location == '教学楼':

        headers = {
            'Host': GetInfo(Start_Url, location)[2],
            'Content-Length': '600',
            'Cache-Control': 'max - age = 0',
            'Upgrade-Insecure - Requests': '1',
            'Origin': f'http://{GetInfo(Start_Url, location)[2]}',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Accept': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Accept - Encoding': 'gzip, deflate',
            'Accept - Language': 'zh - CN, zh;q = 0.9',
            }

        data = {
            'wlanuserip': GetInfo(Start_Url, location)[1],
            "wlanacname": GetInfo(Start_Url, location)[4],
            'chal_id': '',
            'chal_vector': '',
            'auth_type': '',
            'seq_id': '',
            'req_id': '',
            'wlanacIp': GetInfo(Start_Url, location)[5],
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
        if '404' in response.text:
            print('登录成功')
        else:
            error = response.text
            e = re.findall(r'(?<=alert\(\').*(?=\')', error)[0]
            print(f'{e}')

if __name__ == '__main__':
    Start_Url = ReturnStartUrl()
    if IsConnected(Start_Url):
        location = ReturnLocation(Start_Url)
        if location == '':
            islogOut()
        if IsConnected(Start_Url):
            print(f'现在您正处于{location}')
            login(location)
    else:
        print(f'未连接到校园网络')
        input()
