import requests
import click.core as click_core
import logging
from ctl.response_handle import handle_response
from ctl.logging_config import *


def create_app(api_url, user_id, title, desc, repo, version, config, acct_id):
    payload = {
        "title": title,
        "description": desc,
        "repo": repo,
        "version": version,
        "config": config,
        "acctId": int(acct_id or 0),
        "userId": int(user_id or 0)
    }
    headers = {"X-UserId": user_id, "Content-Type": "application/json"}
    response = requests.post(f"{api_url}", json=payload, headers=headers)
    return response


def update_app(ctx, api_url, user_id, app_id, title, desc, repo, acct_id, config, version):
    headers = {"X-UserId": user_id, "Content-Type": "application/json"}
    response = requests.get(f"{api_url}/{app_id}", headers=headers)

    handle_response(response)
    existing_data = response.json()
    payload = {
        "title": title if ctx.get_parameter_source(
            'title') == click_core.ParameterSource.COMMANDLINE else existing_data.get("title"),
        "description": desc if ctx.get_parameter_source(
            'desc') == click_core.ParameterSource.COMMANDLINE else existing_data.get("description"),
        "repo": repo if ctx.get_parameter_source(
            'repo') == click_core.ParameterSource.COMMANDLINE else existing_data.get("repo"),
        "acctId": int(acct_id or 0) if ctx.get_parameter_source(
            'acct_id') == click_core.ParameterSource.COMMANDLINE else existing_data.get("acct_id"),
        "version": version if ctx.get_parameter_source(
            'version') == click_core.ParameterSource.COMMANDLINE else existing_data.get("version"),
        "config": config if ctx.get_parameter_source(
            'config') == click_core.ParameterSource.COMMANDLINE else existing_data.get("config"),
        "userId": int(user_id or 0)
    }
    response = requests.patch(f"{api_url}/{app_id}", json=payload, headers=headers)
    return response


def delete_app(api_url, user_id, app_id, force):
    headers = {"X-UserId": user_id, "Content-Type": "application/json"}
    response = requests.delete(f"{api_url}/{app_id}", headers=headers)
    return response


def get_app(api_url, user_id, app_id):
    """获取 App 详情"""
    headers = {"X-UserId": str(user_id), "Content-Type": "application/json"}
    response = requests.get(f"{api_url}/{app_id}", headers=headers)
    return response


def list_apps(api_url, user_id, start, limit, sort):
    endpoint = f"{api_url}?_start={start}&_limit={limit}"
    if sort:
        endpoint += f"&_sort={sort}"
    headers = {"X-UserId": str(user_id), "Content-Type": "application/json"}

    response = requests.get(endpoint, headers=headers)
    return response
