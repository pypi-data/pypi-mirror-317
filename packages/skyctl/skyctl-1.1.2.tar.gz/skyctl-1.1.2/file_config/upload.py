#!/usr/bin/env python3
import base64
import os
import re
import sys
import tarfile
from urllib.parse import urlparse

import click
import requests
import configparser
import yaml
import logging

from ctl.constants import *
from ctl.error import CLIError
from ctl.response_handle import handle_response

sys.path.append(os.getcwd())
from ctl.logging_config import *

home = os.path.expanduser('~').replace('\\', '/')

current_path = os.path.abspath(os.path.dirname(__file__))
upload_config = configparser.ConfigParser()
upload_config.read(current_path + '/file.ini')

aws = home + upload_config['file_path']['aws']
lam = home + upload_config['file_path']['lambda']
azure = home + upload_config['file_path']['azure']
# gcp = home + upload_config['file_path']['gcp']
ibm = home + upload_config['file_path']['ibm']
kube = home + upload_config['file_path']['kube']
oci = home + upload_config['file_path']['oci']
scp = home + upload_config['file_path']['scp']

dirs_to_tar = [aws, lam, azure, ibm, kube, oci, scp]

config_file = upload_config['file']['file_name']
kubeconfig = upload_config['file']['kubeconfig']

logger = logging.getLogger(__name__)


def execute(pat, upload_url):
    headers = {
        "X-UserId": pat
    }
    up_success_file = []
    target_path = home + config_file
    with tarfile.open(target_path, 'w') as tar:
        for dir_name in dirs_to_tar:
            base_name = os.path.basename(dir_name.rstrip('/'))
            if os.path.exists(dir_name) and os.path.isdir(dir_name):
                items = os.listdir(dir_name)
                for item in items:
                    file_path = os.path.join(dir_name, item)
                    # tar.add(file_path, arcname=os.path.basename(dir_name))
                    arcname = os.path.join(base_name, os.path.relpath(file_path, start=dir_name))
                    tar.add(file_path, arcname=arcname)
            else:
                up_success_file.append(dir_name)
    if len(up_success_file) == len(dirs_to_tar):
        logger.debug('Configuration file does not exist, upload failed')
        return

    files = {'file': open(target_path, 'rb')}
    response = requests.post(upload_url, headers=headers, files=files)
    http_code = response.status_code
    if http_code == 404:
        logger.error("Code 404, this server is not alive, please login a effective server")
        raise CLIError("server is not alive, please login a effective server", NETWORK_ERROR_CODE)
    elif http_code != 200 and response.text == 'Invalid user ID':
        logger.error(
            f"Please check your config file `~/.skyctl/pat.ini` : \"code\": \"{str(http_code)}\", \"msg\": \"{response.text}\"")
        raise CLIError("Invalid user ID", AUTHENTICATION_ERROR_CODE)
    elif http_code != 200:
        logger.error(f"Server error, \"code\": \"{str(http_code)}\", \"msg\": \"{response.text}\"")
        raise CLIError("Server error", API_ERROR_CODE)
    else:
        logger.debug('skypilot files Upload success!')
        return response.text


def get_kubeconfig(pat, api_url):
    target_path = home + kubeconfig  # ~/kubeconfig

    if os.path.exists(target_path):
        logger.debug(f"kubeconfig file exists : {target_path}")
        return target_path

    headers = {
        "X-UserId": pat
    }

    try:
        response = requests.get(api_url, headers=headers)
        handle_response(response)
        response.raise_for_status()
        response_json = response.json()
        encoded_config = response_json.get("kubeconfig")

        if not encoded_config:
            raise ValueError("No 'kubeconfig' data found, please check the interface return value.")

        kubeconfig_content = base64.b64decode(encoded_config).decode("utf-8")
        parsed_url = urlparse(api_url)
        base_url = parsed_url.hostname
        kubeconfig_content = update_kubeconfig_server_ip(kubeconfig_content, base_url)
        with open(target_path, "w") as kubeconfig_file:
            kubeconfig_file.write(kubeconfig_content)

        logger.info(f"The kubeconfig file has been generated: {target_path}")
        return target_path

    except Exception as e:
        logger.error(f"Failed to get kubeconfig: {e}")
        raise CLIError(f"Failed to get kubeconfig: {e}", API_ERROR_CODE)


def update_kubeconfig_server_ip(kubeconfig_content, target_ip):
    kubeconfig = yaml.safe_load(kubeconfig_content)

    for cluster in kubeconfig.get("clusters", []):
        server = cluster.get("cluster", {}).get("server", "")
        if re.match(r"https://(127\.0\.0\.1|localhost):\d+", server):
            new_server = re.sub(r"https://(127\.0\.0\.1|localhost):(\d+)",
                                fr"https://{target_ip}:\2", server)
            cluster["cluster"]["server"] = new_server

    updated_kubeconfig_content = yaml.dump(kubeconfig)
    return updated_kubeconfig_content
