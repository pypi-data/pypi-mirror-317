import requests
import json
import click.core as click_core
import logging

from ctl.constants import NETWORK_ERROR_CODE
from ctl.error import CLIError
from ctl.response_handle import handle_response
from ctl.logging_config import *

logger = logging.getLogger(__name__)


def create_dashboard(api_url, user_id, title, desc, size, url):
    """API request to create a dashboard"""
    endpoint = api_url
    headers = {"X-UserId": user_id, "Content-Type": "application/json"}
    payload = {
        "title": title,
        "description": desc,
        "size": size,
        "url": url,
        "userId": int(user_id or 0)
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        return response
    except requests.RequestException as e:
        raise CLIError(f"Request failed: {e}", NETWORK_ERROR_CODE)


def list_dashboard(api_url, user_id, start, limit, sort):
    """API request to list dashboards"""
    endpoint = f"{api_url}?_start={start}&_limit={limit}"
    if sort:
        endpoint += f"&_sort={sort}"
    headers = {"X-UserId": user_id, "Content-Type": "application/json"}

    try:
        response = requests.get(endpoint, headers=headers)
        return response
    except requests.RequestException as e:
        raise CLIError(f"Request failed: {e}", NETWORK_ERROR_CODE)


def get_dashboard(api_url, user_id, dashboard_id):
    """API request to get dashboard details"""
    endpoint = f"{api_url}/{dashboard_id}"
    headers = {"X-UserId": user_id, "Content-Type": "application/json"}

    try:
        response = requests.get(endpoint, headers=headers)
        return response
    except requests.RequestException as e:
        raise CLIError(f"Request failed: {e}", NETWORK_ERROR_CODE)


def update_dashboard(ctx, api_url, user_id, dashboard_id, title, desc, size, url):
    """API request to update a dashboard"""
    endpoint = f"{api_url}/{dashboard_id}"
    headers = {"X-UserId": user_id, "Content-Type": "application/json"}

    # First, send a GET request to fetch current dashboard data
    try:
        response = requests.get(endpoint, headers=headers)
        handle_response(response)
        current_data = response.json()
    except requests.RequestException as e:
        raise CLIError(f"Request failed: {e}", NETWORK_ERROR_CODE)

    # Prepare payload, replacing with current values if params are None or empty
    payload = {
        "title": title if ctx.get_parameter_source(
            'title') == click_core.ParameterSource.COMMANDLINE else current_data.get("title"),
        "description": desc if ctx.get_parameter_source(
            'desc') == click_core.ParameterSource.COMMANDLINE else current_data.get("description"),
        "size": size if ctx.get_parameter_source(
            'size') == click_core.ParameterSource.COMMANDLINE else current_data.get("size"),
        "url": url if ctx.get_parameter_source('url') == click_core.ParameterSource.COMMANDLINE else current_data.get(
            "url"),
        "userId": int(user_id or 0)
    }

    # Now send the PATCH request to update the dashboard
    try:
        response = requests.patch(endpoint, headers=headers, json=payload)
        return response
    except requests.RequestException as e:
        raise CLIError(f"Request failed: {e}", NETWORK_ERROR_CODE)


def delete_dashboard(api_url, user_id, dashboard_id):
    """API request to delete a dashboard"""
    endpoint = f"{api_url}/{dashboard_id}"
    headers = {"X-UserId": user_id, "Content-Type": "application/json"}

    try:
        response = requests.delete(endpoint, headers=headers)
        return response
    except requests.RequestException as e:
        raise CLIError(f"Request failed: {e}", NETWORK_ERROR_CODE)
