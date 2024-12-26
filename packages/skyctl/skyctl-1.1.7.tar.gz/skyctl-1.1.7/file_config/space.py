import click
import requests
from tabulate import tabulate
from datetime import datetime


def convert_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')


def get_list(url, pat):
    headers = {
        "X-UserId": pat,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)
    # 获取 HTTP 响应状态码
    http_code = response.status_code
    if http_code == 404:
        click.echo("Code 404, this server is not alive, please login a effective server")
        return
    elif http_code != 200 and response.text == 'Invalid user ID':
        click.echo(
            f"Please check your config file `~/.skyctl/pat.ini` : \"code\": \"{str(http_code)}\", \"msg\": \"{response.text}\"")
        return
    elif http_code != 200:
        click.echo(f"Server error, \"code\": \"{str(http_code)}\", \"msg\": \"{response.text}\"")
        return
    res = response.json()
    space_list = res

    # for item in space_list:
    #     item['createTime'] = convert_timestamp(item['createTime'])
    #     item['updateTime'] = convert_timestamp(item['updateTime'])

    data_upper = [{k.upper(): v for k, v in item.items()} for item in space_list]
    click.echo(tabulate(data_upper, headers='keys', tablefmt="pipe", stralign="center", numalign="center"))


def create(url, pat, space_name: str):
    headers = {
        "X-UserId": pat,
        "Content-Type": "application/json"
    }
    params = {"namespace": space_name}

    response = requests.post(url, headers=headers, params=params)
    # 获取 HTTP 响应状态码
    http_code = response.status_code
    if http_code == 404:
        click.echo("Code 404, this server is not alive, please login a effective server")
        return
    elif http_code != 200 and response.text == 'Invalid user ID':
        click.echo(
            f"Please check your config file `~/.skyctl/pat.ini` : \"code\": \"{str(http_code)}\", \"msg\": \"{response.text}\"")
        return
    elif http_code != 200:
        click.echo(f"Server error, \"code\": \"{str(http_code)}\", \"msg\": \"{response.text}\"")
        return
    else:
        click.echo('The namespace create successful')


def space_help():
    print('Usage:  COMMAND  [Option]')
    print('Common Commands: \n'
          'list                  Display namespace list\n'
          'create [namespace]    Create a namespace and  The [namespace] represents the name you need to create\n'
          'upload [namespace]    Upload the configuration file to the specified namespace. If the [namespace] is \n'
          '                      empty,upload it to the default namespace\n'
          'exit                  Exit Skyctl terminal')
    print('\nTIP: Before using this command, you need to prepare a config file `~/.skyctl/pat.ini`')
    print('     The config file should be in the following format:')
    print('     [CREDENTIALS]')
    print('     X-UserId = your_user_id')