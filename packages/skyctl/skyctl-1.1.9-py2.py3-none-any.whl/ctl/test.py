#!/usr/bin/env python3
import requests
import configparser
import file_config.upload as upload
import os
import file_config.space as space

url_config = configparser.ConfigParser()
current_path = os.path.abspath(os.path.dirname(__file__))
url_config.read(current_path + '/server_config.ini')

login_url = url_config['server']['login_url']
upload_url = url_config['server']['upload_url']
list_url = url_config['server']['list_url']
create_url = url_config['server']['create_url']

login_url_path = '/skyctl/namespace/list'
upload_url_path = '/skyctl/upload'
create_url_path = '/skyctl/namespace/create'
list_url_path = '/skyctl/namespace/list'


def ctl():
    while True:
        user_id = input("please input `X-UserId` or `exit` to quit:").strip()
        if user_id == 'exit' or user_id == '':
            return
        ip = input("please input `IP` or `exit` to quit:").strip()
        if ip == 'exit':
            return
        elif ip == '':
            ip = '172.16.91.17'
            print("use default IP：172.16.91.17")
        port = input("please input `port` or `exit` to quit:").strip()
        if port == 'exit':
            return
        elif port == '':
            port = '38080'
            print("use default port：38080")
        headers = {
            "X-UserId": user_id,
            "Content-Type": "application/json"
        }
        url = "http://" + ip + ":" + port + login_url_path
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            print("login success")
            override_config(ip, port, login_url, upload_url, create_url, list_url)
            while True:
                option_other = input("please input your operation or `help` to see usage: ").strip()
                if len(option_other.split()) > 0:
                    if option_other.split()[0] == "create":
                        space.create(create_url, user_id, option_other)
                    elif option_other.split()[0] == "upload":
                        upload.execute(user_id, upload_url, option_other)
                    elif option_other == "list":
                        space.get_list(list_url, user_id)
                    elif option_other == "help":
                        space.space_help()
                    elif option_other == "exit":
                        print("Exit Skyctl")
                        return
        else:
            print('login success')


def override_config(ip, port, __login_url, __upload_url, __create_url, __list_url):
    __url_config = configparser.ConfigParser()
    # 脚本当前的绝对路径
    __current_path = os.path.abspath(os.path.dirname(__file__))
    __url_config.read(__current_path + '/server_config.ini')
    __login_url = 'http://' + ip + ':' + port + login_url_path
    __upload_url = 'http://' + ip + ':' + port + upload_url_path
    __list_url = 'http://' + ip + ':' + port + list_url_path
    __create_url = 'http://' + ip + ':' + port + create_url_path
    __url_config.set('server', 'login_url', __login_url)
    __url_config.set('server', 'upload_url', __upload_url)
    __url_config.set('server', 'create_url', __create_url)
    __url_config.set('server', 'list_url', __list_url)
    with open(__current_path + '/server_config.ini', 'w') as file:
        __url_config.write(file)


ctl()
