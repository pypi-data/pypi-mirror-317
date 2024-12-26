import requests
from tabulate import tabulate
from datetime import datetime


def convert_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')


data = {'userId': 8}
response = requests.post('http://172.16.91.17:48080/app-api/uc/space/list', data=data)
res = response.json()
print('res = ', res)
data = res['data']
print('data = ', data)

for item in data:
    item['createTime'] = convert_timestamp(item['createTime'])
    item['updateTime'] = convert_timestamp(item['updateTime'])


data_capitalized = [{k.upper(): v for k, v in item.items()} for item in data]
print(tabulate(data_capitalized, headers='keys', tablefmt="pipe", stralign="center", numalign="center"))
