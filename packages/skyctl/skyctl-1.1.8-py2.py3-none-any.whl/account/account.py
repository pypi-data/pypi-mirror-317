import requests
import click.core as click_core
import logging

from ctl.response_handle import handle_response
from ctl.logging_config import *



def create_account(api_url, user_id, title, desc, host, type, username, password):
    payload = {
        "title": title,
        "description": desc,
        "host": host,
        "type": type,
        "username": username,
        "password": password,
        "userId": int(user_id or 0)
    }
    headers = {"X-UserId": user_id, "Content-Type": "application/json"}
    response = requests.post(f"{api_url}", json=payload, headers=headers)
    return response


def get_account_details(api_url, user_id, account_id):
    headers = {"X-UserId": user_id}
    response = requests.get(f"{api_url}/{account_id}", headers=headers)
    return response


def update_account(ctx, api_url, user_id, account_id, title, desc, host, type, username, password):
    # Get existing account details
    response = get_account_details(api_url, user_id, account_id)
    handle_response(response)
    existing_account = response.json()
    # If no existing data, use provided values directly
    if not existing_account:
        return f"No existing account found. Using provided values."

    # Prepare payload, prioritizing provided values
    payload = {
        "title": title if ctx.get_parameter_source(
            'title') == click_core.ParameterSource.COMMANDLINE else existing_account.get("title"),
        "description": desc if ctx.get_parameter_source(
            'desc') == click_core.ParameterSource.COMMANDLINE else existing_account.get("description"),
        "host": host if ctx.get_parameter_source(
            'title') == click_core.ParameterSource.COMMANDLINE else existing_account.get("host"),
        "type": type if ctx.get_parameter_source(
            'type') == click_core.ParameterSource.COMMANDLINE else existing_account.get("type"),
        "username": username if ctx.get_parameter_source(
            'username') == click_core.ParameterSource.COMMANDLINE else existing_account.get("username"),
        "password": password if ctx.get_parameter_source(
            'password') == click_core.ParameterSource.COMMANDLINE else existing_account.get("password"),
        "userId": int(user_id or 0)
    }

    headers = {"X-UserId": user_id, "Content-Type": "application/json"}
    response = requests.patch(f"{api_url}/{account_id}", json=payload, headers=headers)

    return response


def delete_account(api_url, user_id, account_id, force=False):
    headers = {"X-UserId": user_id}
    response = requests.delete(f"{api_url}/{account_id}", headers=headers)
    return response


def list_accounts(api_url, user_id, start, limit, sort):
    headers = {"X-UserId": user_id}
    endpoint = f"{api_url}?_start={start}&_limit={limit}"
    if sort:
        endpoint += f"&_sort={sort}"
    response = requests.get(endpoint, headers=headers)
    return response
