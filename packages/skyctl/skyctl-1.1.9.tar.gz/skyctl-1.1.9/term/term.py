import sys
import threading
import time
# import tty

import click
import requests
import os

import select
import yaml
import logging

from kubernetes.client import ApiException
from kubernetes.stream import stream
from kubernetes.stream.ws_client import STDOUT_CHANNEL

import file_config.upload as upload_file
from kubernetes import client, config, watch
import click.core as click_core

from ctl.constants import *
from ctl.error import CLIError
from ctl.response_handle import handle_response
from ctl.logging_config import *

# import termios

logger = logging.getLogger(__name__)


def load_config(config_path):
    """加载配置文件"""
    try:
        with open(os.path.expanduser(config_path), 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Config file not found: {config_path}")
        return {}
    except yaml.YAMLError as e:
        logger.error(f"Error reading config file: {e}")
        return {}


def create_term(api_url, user_id, title, desc, app_id, config, config_id):
    payload = {
        "title": title,
        "description": desc,
        "config": config,
        "userId": int(user_id or 0),
        "skyConf": int(config_id or 0)
    }
    headers = {"X-UserId": user_id, "Content-Type": "application/json"}
    response = requests.post(f"{api_url}", json=payload, headers=headers)
    return response


def get_term(api_url, user_id, terminal_id, watch, kubeconfig_url):
    headers = {"X-UserId": user_id}
    response = requests.get(f"{api_url}/{terminal_id}", headers=headers)
    handle_response(response)
    if watch:
        get_k8s_client(user_id, kubeconfig_url)
        pod_name = get_pod_name(response.json().get("title"), f'sky-{user_id}')
        if not pod_name:
            raise CLIError("Pod not found", API_ERROR_CODE)
        watch_pods(pod_name, f'sky-{user_id}', response.json().get("title"))
    return response


def get_pod_name(container_name, namespace):
    match_labels = None
    if not container_name:
        logger.error("Container name not found in response")
        return None

    logger.info(f"Container name: {container_name}")
    apps_v1 = client.AppsV1Api()
    core_v1 = client.CoreV1Api()

    try_count = 0
    max_retries = 10
    sleep_duration = 3
    logger.info(f"try to get deployment,wait a few seconds")
    key = 0
    while try_count < max_retries:
        try:
            # Get the Deployment
            deployment = apps_v1.read_namespaced_deployment(container_name, namespace)
            replicas = deployment.spec.replicas or 0

            if replicas == 0:
                logger.warning(f"Deployment '{container_name}' has 0 replicas. Retrying...")
                try_count += 1
                time.sleep(sleep_duration)
                continue
            match_labels = deployment.spec.selector.match_labels
            key = 1
            break
        except ApiException as e:
            try_count += 1
            logger.debug(f"Attempt {try_count}/{max_retries} - Error fetching deployment: {e}")
            if try_count < max_retries:
                time.sleep(sleep_duration)
            else:
                logger.error("Max retries reached. Deployment could not be fetched.")
                return None
    if key == 0:
        logger.error("Max retries reached. Deployment could not be fetched.")
        return None
    # Retry logic to find the running pod
    max_retries = 15
    retry_count = 0
    pod_name = None
    logger.info(f"try to get podName,wait a few seconds")
    while retry_count < max_retries:
        try:
            pod_list = core_v1.list_namespaced_pod(
                namespace,
                label_selector=",".join([f"{k}={v}" for k, v in match_labels.items()])
            )

            for pod in pod_list.items:
                if pod.metadata.deletion_timestamp is None:
                    pod_name = pod.metadata.name
                    logger.info(f"Pod found: {pod_name}")
                    return pod_name
        except ApiException as e:
            logger.error(f"Error listing pods: {e}")
            return None

        logger.debug("Pod not found, sleep 5s ,retrying...")
        time.sleep(5)
        retry_count += 1

    logger.error("Failed to find a running pod after retries")
    return None
    pass


def connect_to_pod_shell(user_id, api_url, terminal_id, kubeconfig_url):
    headers = {"X-UserId": user_id}
    response = requests.get(f"{api_url}/{terminal_id}", headers=headers)
    print("response" + str(response))
    print(" " + user_id + " " + api_url + " " + terminal_id + " " + kubeconfig_url)
    handle_response(response)
    get_k8s_client(user_id, kubeconfig_url)
    title = response.json().get('title')
    pod_name = get_pod_name(title, f'sky-{user_id}')
    if not pod_name:
        raise CLIError("Pod not found", API_ERROR_CODE)
    interactive_exec1(pod_name, f'sky-{user_id}', "bash")
    return response.json()


def update_term(ctx, api_url, user_id, terminal_id, title, desc, config, status, config_id):
    headers = {"X-UserId": user_id, "Content-Type": "application/json"}
    response = requests.get(f"{api_url}/{terminal_id}", headers=headers)
    handle_response(response)
    existing_data = response.json()
    updated_payload = {
        "userId": int(user_id or 0),
        "appId": int(existing_data.get("appId") or 0),
        "svc": existing_data.get("svc")
    }
    # Check and update each field based on the source of the parameter
    if ctx.get_parameter_source('title') == click_core.ParameterSource.COMMANDLINE:
        updated_payload["title"] = title
    elif existing_data.get("title"):
        updated_payload["title"] = existing_data.get("title")

    if ctx.get_parameter_source('desc') == click_core.ParameterSource.COMMANDLINE:
        updated_payload["description"] = desc
    elif existing_data.get("description"):
        updated_payload["description"] = existing_data.get("description")

    if ctx.get_parameter_source('config') == click_core.ParameterSource.COMMANDLINE:
        updated_payload["config"] = config
    elif existing_data.get("config"):
        updated_payload["config"] = existing_data.get("config")

    if status == 'starting':
        updated_payload["status"] = 2
    elif status == 'stopping':
        updated_payload["status"] = 5

    if ctx.get_parameter_source('sync_skypilot') == click_core.ParameterSource.COMMANDLINE:
        updated_payload["skyConf"] = int(config_id or 0)
    elif existing_data.get("skyConf"):
        updated_payload["skyConf"] = existing_data.get("skyConf")

    if not updated_payload:
        return "No updates needed"
    response = requests.patch(f"{api_url}/{terminal_id}", json=updated_payload, headers=headers)

    return response


def stop_term(api_url, user_id, terminal_id):
    headers = {"X-UserId": user_id}

    # Send request to stop the terminal
    response = requests.get(f"{api_url}/stop/{terminal_id}", headers=headers)

    return response


def start_term(api_url, user_id, terminal_id):
    headers = {"X-UserId": user_id}

    # Send request to start the terminal
    response = requests.get(f"{api_url}/run/{terminal_id}", headers=headers)

    return response


def delete_term(api_url, user_id, terminal_id):
    headers = {"X-UserId": user_id}
    response = requests.delete(f"{api_url}/{terminal_id}", headers=headers)
    return response


def list_terms(api_url, user_id, start, limit, sort):
    endpoint = f"{api_url}?_start={start}&_limit={limit}"
    if sort:
        endpoint += f"&_sort={sort}"
    headers = {"X-UserId": str(user_id), "Content-Type": "application/json"}
    try:
        response = requests.get(endpoint, headers=headers)
        return response
    except requests.RequestException as e:
        raise CLIError(f"Error fetching terminals: {e}", GENERAL_ERROR_CODE)


def get_k8s_client(user_id, api_url):
    kubeconfig_path = upload_file.get_kubeconfig(user_id, api_url)
    try:
        # Load configuration from kubeconfig file
        config.load_kube_config(config_file=kubeconfig_path)
        logger.debug("load kubeconfig successfully")

    except Exception as e:
        raise CLIError(f"Error loading kubeconfig: {e}", GENERAL_ERROR_CODE)


def watch_pods(pod_nam, namespace, container_name):
    v1 = client.CoreV1Api()

    # Creating a watch object
    w = watch.Watch()

    logger.debug(f"Watching Pods in namespace: {namespace}...")
    try:
        for event in w.stream(v1.list_namespaced_pod, namespace=namespace):
            event_type = event['type']
            pod_name = event['object'].metadata.name
            pod_status = event['object'].status.phase
            if pod_nam == pod_name:
                logger.info(f"Event: {event_type} - Pod: {pod_name} - Status: {pod_status}")
            if event_type == 'DELETED' and pod_nam == pod_name:
                logger.info("the old pod is deleted, finding the new pod")
                pod_nam = get_pod_name(container_name, namespace)
                if not pod_nam:
                    raise CLIError("Pod not found", API_ERROR_CODE)
                else:
                    logger.info(f"new pod is created, watching the new pod {pod_nam}")
    except KeyboardInterrupt:
        logger.debug("Watch interrupted by user.")
    finally:
        w.stop()


def exec_in_pod(pod_name, namespace):
    # 获取 API 客户端
    v1 = client.CoreV1Api()

    # 修改命令来启动 bash shell
    exec_command = [
        "bash"  # 只启动 bash shell，不传入额外命令
    ]
    result = None
    print(namespace)
    try:
        # 使用 Kubernetes Python 客户端执行命令
        ws = stream(
            v1.connect_get_namespaced_pod_exec,
            pod_name,
            namespace,
            command=exec_command,
            container=None,  # 如果 Pod 中有多个容器，请指定容器名称
            stderr=True,
            stdin=True,
            stdout=True,
            tty=True,
            _preload_content=False  # 必须设置为 False
        )

        # 设置输入输出流
        print("result" + str(ws))
        return ws

    except Exception as e:
        print(f"Error executing command: {e}")


def interactive_exec(pod_name, namespace, command):
    # Create an API instance
    v1 = client.CoreV1Api()

    # Establish a WebSocket connection to the Pod
    ws = stream(
        v1.connect_get_namespaced_pod_exec,
        pod_name,
        namespace,
        command=command,
        stderr=True,
        stdin=True,
        stdout=True,
        tty=True,
        _preload_content=False,  # Enable raw WebSocket handling
    )

    def read_user_input():
        """Reads user input and sends it to the WebSocket."""
        try:
            while True:
                user_input = os.read(sys.stdin.fileno(), 1024)  # Read raw input
                if not user_input:
                    break
                ws.write_stdin(user_input.decode('utf-8'))
        except Exception as e:
            print(f"Error reading user input: {e}")
        finally:
            ws.close()

    def read_pod_output():
        """Reads Pod output from the WebSocket and displays it."""
        try:
            # 使用 select 来阻塞直到有数据可读
            rlist, _, _ = select.select([ws], [], [], None)
            if rlist:
                output = ws.read_stdout()
                if output:
                    sys.stdout.write(output)
                    sys.stdout.flush()
        except Exception as e:
            print(f"Error reading stdout: {e}")

    # Save terminal settings
    old_settings = termios.tcgetattr(sys.stdin)
    print("2222")
    try:
        tty.setraw(sys.stdin.fileno())  # Set terminal to raw mode

        # Start threads for input and output
        input_thread = threading.Thread(target=read_user_input, daemon=True)
        input_thread.start()

        read_pod_output()  # Main thread handles output
    except KeyboardInterrupt:
        print("\nExiting interactive mode.")
    finally:
        # Restore terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        ws.close()


def interactive_exec1(pod_name, namespace, command):
    v1 = client.CoreV1Api()
    ws = stream(
        v1.connect_get_namespaced_pod_exec,
        pod_name,
        namespace,
        command=command,  # Start a shell session
        stderr=True,
        stdin=True,
        stdout=True,
        tty=True,
        _preload_content=False,  # Enable raw WebSocket handling
    )

    def read_pod_output():
        while True:
            try:
                pod_output = ws.read_stdout(timeout=10)  # Wait for Pod output
                if pod_output:
                    sys.stdout.write(pod_output)
                    sys.stdout.flush()
            except Exception as e:
                print(f"\nError reading output: {e}")
                break

    output_thread = threading.Thread(target=read_pod_output, daemon=True)
    output_thread.start()

    try:
        print("Connected to Pod. Type commands below:\n")
        while True:
            user_input = input().strip()
            if not user_input:
                continue
            ws.write_stdin(user_input + "\n")
            if not ws.is_open():
                print("\nConnection closed by Pod.")
                break

    except KeyboardInterrupt:
        print("\nExiting interactive mode.")
    finally:
        ws.close()

# def interactive_shell(ws):
#     """
#     Handle interactive shell input and output using tty for a realistic experience.
#     """
#     old_settings = termios.tcgetattr(sys.stdin)  # Save the terminal's original settings
#     try:
#         tty.setraw(sys.stdin.fileno())  # Set the terminal to raw mode
#
#         def send_input():
#             """Send user input to the WebSocket."""
#             try:
#                 while True:
#                     user_input = os.read(sys.stdin.fileno(), 1024)  # Read raw input
#                     if not user_input:
#                         break
#                     ws.stdin.write(user_input)  # Send input to the WebSocket
#                     ws.stdin.flush()
#             except KeyboardInterrupt:
#                 ws.close()
#
#         input_thread = threading.Thread(target=send_input, daemon=True)
#         input_thread.start()
#
#         # Receive output from the WebSocket and display it
#         try:
#             while True:
#                 output = ws.stdout.read(1024)  # Read output from the pod
#                 if not output:
#                     break
#                 sys.stdout.write(output.decode())  # Write output to terminal
#                 sys.stdout.flush()
#         except KeyboardInterrupt:
#             ws.close()
#     finally:
#         termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)  # Restore terminal settings
