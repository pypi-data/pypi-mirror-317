# !/usr/bin/env python3
import configparser
import os
from typing import Optional
import re
import click
import requests
import sys
import logging
import json
from tabulate import tabulate

sys.path.append(os.getcwd())
import file_config.upload as upload_file
import file_config.space as name_space
import term.term as term_api
import dashboard.dashboard as dashboard_api
import account.account as account_api
import click.core as click_core
import app.app as app_api
from ctl.constants import *
from ctl.error import CLIError
from ctl.logging_config import *
from ctl.response_handle import handle_response

# def abort_if_false(ctx, param, value):
#     if not value:
#         ctx.abort()
str_version = '1.1.11'

login_url_path = '/skyctl/namespace/list'
upload_url_path = '/skyctl/upload'
create_url_path = '/skyctl/namespace/create'
list_url_path = '/skyctl/namespace/list'

url_config = configparser.ConfigParser()
home = os.path.expanduser('~').replace('\\', '/')
dir_path = home + '/.skyctl'
current_path = os.path.abspath(os.path.dirname(__file__))
url_config.read(current_path + '/server_config.ini')
login_url = url_config['server']['login_url']
upload_url = url_config['server']['upload_url']
list_url = url_config['server']['list_url']
create_url = url_config['server']['create_url']
upload_path = url_config['server']['upload_config']

host_ip = url_config['server']['host_ip']

# 读取 API 路径配置
term_path = url_config['server']['create_term']
account_path = url_config['server']['create_account']
app_path = url_config['server']['create_apps']
dashboard_path = url_config['server']['create_dashboard']
kubeconfig_path = url_config['server']['get_kubeconfig']

# 组装完整的 API URL
term_url = host_ip + term_path
account_url = host_ip + account_path
apps_url = host_ip + app_path
dashboard_url = host_ip + dashboard_path

logger = logging.getLogger(__name__)


def common_options(func):
    func = click.option('--sky-config',
                        default='~/.skyctl/config.yaml',
                        help='Path to config file')(func)
    func = click.option('--api-url',
                        default='http://172.16.91.17:38080',
                        help='API base URL')(func)
    func = click.option('--user-id',
                        default=None,
                        help='User ID (optional, for testing and impersonation by admin)')(func)
    func = click.option('--format',
                        default='table',
                        type=click.Choice(['json', 'table'], case_sensitive=False),
                        help='Output format: json|table')(func)
    func = click.option('--quiet',
                        is_flag=True,
                        help='Suppress output except for errors')(func)
    func = click.option('--debug',
                        is_flag=True,
                        help='Enable debug logging')(func)
    return func


def list_common_options(func):
    func = click.option('--start',
                        default=0,
                        help='Start index of the list')(func)
    func = click.option('--limit',
                        default=100,
                        help='Items per page')(func)
    func = click.option('--sort',
                        help='Sort field')(func)
    return func


@click.group()
def resource():
    """Skyctl CLI Tool"""
    pass


def common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug):
    ctx.ensure_object(dict)
    ctx.obj['config'] = term_api.load_config(sky_config)
    api = ctx.obj['config'].get('api', None)
    defaults = ctx.obj['config'].get('defaults', None)
    if ctx.get_parameter_source('quiet') == click_core.ParameterSource.COMMANDLINE:
        ctx.obj['quiet'] = quiet
    else:
        ctx.obj['quiet'] = defaults['quiet'] if defaults and 'quiet' in defaults else quiet

    if ctx.get_parameter_source('debug') == click_core.ParameterSource.COMMANDLINE:
        ctx.obj['debug'] = debug
    else:
        ctx.obj['debug'] = defaults['debug'] if defaults and 'debug' in defaults else debug

    if ctx.obj['quiet']:
        logger.setLevel(logging.ERROR)
        logging.getLogger("urllib3").setLevel(logging.ERROR)
    elif ctx.obj['debug']:
        logger.setLevel(logging.DEBUG)
        logging.getLogger("urllib3").setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        logging.getLogger("urllib3").setLevel(logging.INFO)

    if ctx.get_parameter_source('api_url') == click_core.ParameterSource.COMMANDLINE:
        ctx.obj['api_url'] = api_url
    else:
        ctx.obj['api_url'] = api['api_url'] if api and 'api_url' in api else api_url

    if ctx.obj['api_url'] is None or not validate_url(ctx.obj['api_url']):
        logger.error("Invalid API URL: %s", ctx.obj['api_url'])
        raise CLIError(f"Invalid API URL {ctx.obj['api_url']}", 2, URL_SOLUTION)

    ctx.obj['user_id'] = user_id or check_key()
    if ctx.obj['user_id'] is None:
        logger.error("User ID is required.")
        raise CLIError("User ID is required.", 2, URL_SOLUTION)

    if ctx.get_parameter_source('format') == click_core.ParameterSource.COMMANDLINE:
        ctx.obj['format'] = format
    else:
        ctx.obj['format'] = defaults['format'] if defaults and 'format' in defaults else format

    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")


url_pattern = re.compile(
    r'^(http|https)://'  # Support both http and https
    r'((25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})\.){3}'  # Match the first three octets of the IP address
    r'(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})'  # Match the last octet of the IP address
    r':(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5][0-9]{4}|[0-9]{1,4})$'  # Valid port range (1-65535)
)


def validate_url(url):
    if url is None:
        return False
    return bool(url_pattern.match(url))


class User:
    def __init__(self, uid, username, password):
        self.uid = uid
        self.username = username
        self.password = password


_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help', '--usage'])


class _CustomClickCommand(click.Command):
    def get_help(self, ctx):
        help_str = ctx.command.help
        ctx.command.help = help_str.replace('.. code-block:: bash\n', '\b')
        return super().get_help(ctx)


@click.group()
def login():
    """SkyCtl Login CLI."""
    click.echo('SkyCtl Login CLI.')
    pass


@login.command('login', help='Login to a effective server', context_settings=_CONTEXT_SETTINGS)
@click.option('--ip',
              '-i',
              prompt=True,
              help='ip to login')
@click.option('--port',
              '-p',
              prompt=True,
              help='port to login')
def login_server(ip, port):
    pat = check_key()
    if pat is not None:
        if not validate_ip(ip):
            click.echo('Invalid value for IP!')
            return
        if not validate_port(port):
            click.echo('Invalid value for port!')
            return
        url = "http://" + ip + ":" + port + login_url_path
        headers = {
            "X-UserId": pat,
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            click.echo('Login successful!')
            override_config(ip, port)
        elif response.status_code == 500:
            click.echo('The server is exist but something is wrong!')
        else:
            click.echo('Please use a effective server!' + response.text)


@click.group()
def upload():
    """SkyCtl Upload CLI."""
    pass


@upload.command('upload',
                help='Upload skypilot configuration file',
                cls=_CustomClickCommand,
                context_settings=_CONTEXT_SETTINGS)
@click.option('--space',
              '-s',
              help='Namespace for file upload. If omitted, files will be uploaded to the default namespace.',
              default='default',
              show_default=True,
              prompt='Enter the namespace for file upload (or leave blank for default)',
              type=str)
def file(space: Optional[str]):
    # if not click.confirm(f'Are you sure want to upload to the "{space}" namespace?'):
    #     click.echo('Aborted by user.')
    #     return

    click.echo(f"Uploading files to namespace: '{space}'")
    pat = check_key()
    if pat is not None:
        upload_file.execute(pat, upload_url, space)


@click.group()
def namespace():
    """SkyCtl Namespace CLI."""
    pass


@namespace.command('namespace',
                   help='Operation of namespace',
                   context_settings=_CONTEXT_SETTINGS)
@click.option('--create',
              '-c',
              help='Create a namespace',
              type=str)
@click.option('--ls',
              '-l',
              is_flag=True,
              default=False,
              required=False,
              help='Show the namespace list')
def namespace_operation(create: Optional[str], ls: bool):
    pat = check_key()
    if pat is not None:
        if create:
            ls = False
            name_space.create(create_url, pat, create)

        if ls:
            name_space.get_list(list_url, pat)


@resource.group()  # term
@click.pass_context
def term(ctx):
    """Manage terminals"""
    pass


@term.command("create")
@click.option("--title", required=True, help="Terminal title (required)")
@click.option("--desc", required=True, help="Terminal description")
@click.option("--app-id", default=0, help="Application ID (Default: 0, skypilot)")
@click.option("--config", help="Terminal configuration string")
@click.option("--sync-skypilot", is_flag=True, help="Upload local skypilot configs to the created terminal")
@common_options
@click.pass_context
def create_term(ctx, title, desc, app_id, config, sync_skypilot, sky_config, api_url, user_id, format, quiet, debug):
    """Create a terminal"""
    global config_id
    config_id = None
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)
    api_url = ctx.obj.get('api_url') + term_path
    user_id = ctx.obj.get('user_id') or check_key()
    upload_config_url = ctx.obj.get('api_url') + upload_path
    if sync_skypilot:
        config_id = upload_file.execute(user_id, upload_config_url)

    result = term_api.create_term(api_url, user_id, title, desc, app_id, config, config_id)
    common_result_handle(ctx, result)


@term.command("list")
@list_common_options
@common_options
@click.pass_context
def list_terms(ctx, start, limit, sort, sky_config, api_url, user_id, format, quiet, debug):
    """List terminals"""
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)
    api_url = ctx.obj.get('api_url') + term_path
    user_id = ctx.obj.get('user_id') or check_key()

    result = term_api.list_terms(api_url, user_id, start, limit, sort)
    common_result_handle(ctx, result)


@term.command("get")
@click.argument("terminal-id")
@click.option("--watch", is_flag=True, help="Watch for status changes")
@common_options
@click.pass_context
def get_term(ctx, terminal_id, watch, sky_config, api_url, user_id, format, quiet, debug):
    """Get terminal details"""
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)
    api_url = ctx.obj.get('api_url') + term_path
    user_id = ctx.obj.get('user_id') or check_key()
    result = term_api.get_term(api_url, user_id, terminal_id, watch, ctx.obj.get('api_url') + kubeconfig_path)
    if not watch:
        common_result_handle(ctx, result)


@term.command("shell")
@click.argument("terminal-id")
@common_options
@click.pass_context
def shell_term(ctx, terminal_id, sky_config, api_url, user_id, format, quiet, debug):
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)
    api_url = ctx.obj.get("api_url") + term_path
    user_id = ctx.obj.get("user_id") or check_key()
    kubeconfig_url = ctx.obj.get("api_url") + kubeconfig_path

    term_api.connect_to_pod_shell(user_id, api_url, terminal_id, ctx.obj.get("api_url") + kubeconfig_path)


@term.command("update")
@click.argument("terminal-id")
@click.option("--title", help="New title")
@click.option("--desc", help="New description")
@click.option("--config", help="New configuration")
@click.option("--status", help="New status (starting|stopping)",
              type=click.Choice(['starting', 'stopping'], case_sensitive=False), default=None)
@click.option("--sync-skypilot", is_flag=True, help="Upload local skypilot configs to the created terminal")
@common_options
@click.pass_context
def update_term(ctx, terminal_id, title, desc, config, status, sync_skypilot, sky_config, api_url, user_id, format,
                quiet, debug):
    """Update a terminal"""
    global config_id
    config_id = None
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)
    api_url = ctx.obj.get('api_url') + term_path
    user_id = ctx.obj.get('user_id') or check_key()

    if sync_skypilot:
        config_id = upload_file.execute(user_id, upload_url)
    # Updating terminals
    result = term_api.update_term(ctx, api_url, user_id, terminal_id, title, desc, config, status, config_id)
    common_result_handle(ctx, result)


@term.command("delete")
@click.argument("terminal-id")
@click.option("--force", is_flag=True, help="Force deletion without confirmation")
@common_options
@click.pass_context
def delete_term(ctx, terminal_id, force, sky_config, api_url, user_id, format, quiet, debug):
    """Delete a terminal"""
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)
    api_url = ctx.obj.get('api_url') + term_path
    user_id = ctx.obj.get('user_id') or check_key()

    if not force and not click.confirm(f"Are you sure you want to delete terminal {terminal_id}?"):
        click.echo("Operation canceled.")
        return

    result = term_api.delete_term(api_url, user_id, terminal_id)
    common_result_handle(ctx, result)


@term.command("stop")
@click.argument("terminal-id")
@common_options
@click.pass_context
def stop_term(ctx, terminal_id, sky_config, api_url, user_id, format, quiet, debug):
    """Stop a terminal"""
    # Handle common options
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)

    # Get the API URL and user ID
    api_url = ctx.obj.get('api_url') + term_path
    user_id = ctx.obj.get('user_id') or check_key()

    # Call the API to stop the terminal
    result = term_api.stop_term(api_url, user_id, terminal_id)

    # Handle the result
    common_result_handle(ctx, result)


@term.command("start")
@click.argument("terminal-id")
@common_options
@click.pass_context
def start_term(ctx, terminal_id, sky_config, api_url, user_id, format, quiet, debug):
    """Start a terminal"""
    # Handle common options
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)

    # Get the API URL and user ID
    api_url = ctx.obj.get('api_url') + term_path
    user_id = ctx.obj.get('user_id') or check_key()

    # Call the API to start the terminal
    result = term_api.start_term(api_url, user_id, terminal_id)
    # Handle the result
    common_result_handle(ctx, result)


@resource.group()  # app
def app():
    """Manage Apps"""
    pass


@app.command("create")
@click.option("--title", required=True, help="App title (required)")
@click.option("--desc", required=True, help="App description")
@click.option("--repo", required=True, help="Repository URL (required)")
@click.option("--version", help="Version string")
@click.option("--config", help="Configuration string")
@click.option("--acct-id", default=0, help="Account ID for private repositories")
@common_options
@click.pass_context
def create_app(ctx, title, desc, repo, version, config, acct_id, sky_config, api_url, user_id, format, quiet, debug):
    """Create an app definition"""
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)
    api_url = ctx.obj.get('api_url') + app_path
    user_id = ctx.obj.get('user_id') or check_key()
    result = app_api.create_app(api_url, user_id, title, desc, repo, version, config, acct_id)
    common_result_handle(ctx, result)


@app.command("list")
@list_common_options
@common_options
@click.pass_context
def list_apps(ctx, start, limit, sort, sky_config, api_url, user_id, format, quiet, debug):
    """List apps"""
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)
    api_url = ctx.obj.get('api_url') + app_path
    user_id = ctx.obj.get('user_id') or check_key()
    result = app_api.list_apps(api_url, user_id, start, limit, sort)
    common_result_handle(ctx, result)


@app.command("delete")
@click.argument("app-id", required=True)
@click.option("--force", is_flag=True, help="Force deletion without confirmation")
@common_options
@click.pass_context
def delete_app(ctx, app_id, force, sky_config, api_url, user_id, format, quiet, debug):
    """Delete an app"""
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)
    api_url = ctx.obj.get('api_url') + app_path
    user_id = ctx.obj.get('user_id') or check_key()
    if not force:
        if not click.confirm(f"Are you sure you want to delete app {app_id}?"):
            click.echo("Operation cancelled.")
            return
    result = app_api.delete_app(api_url, user_id, app_id, force)
    common_result_handle(ctx, result)


@app.command("get")
@click.argument("app-id", required=True)
@common_options
@click.pass_context
def get_app(ctx, app_id, sky_config, api_url, user_id, format, quiet, debug):
    """Get app details"""
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)
    api_url = ctx.obj.get('api_url') + app_path
    user_id = ctx.obj.get('user_id') or check_key()
    result = app_api.get_app(api_url, user_id, app_id)
    common_result_handle(ctx, result)


@app.command("update")
@click.argument("app-id", required=True)
@click.option("--title", help="New title")
@click.option("--desc", help="New description")
@click.option("--repo", help="New repository URL")
@click.option("--acct-id", help="New account ID")
@click.option("--config", help="New configuration string")
@click.option("--version", help="Version string")
@common_options
@click.pass_context
def update_app(ctx, app_id, title, desc, repo, acct_id, sky_config, config, api_url, user_id, format, quiet, debug,
               version):
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)
    api_url = ctx.obj.get('api_url') + app_path
    user_id = ctx.obj.get('user_id') or check_key()
    result = app_api.update_app(ctx, api_url, user_id, app_id, title, desc, repo, acct_id, config, version)
    common_result_handle(ctx, result)


@resource.group()  # account
def account():
    """Manage Accounts"""
    pass


@account.command("create")
@click.option("--title", required=True, help="Account title (required)")
@click.option("--desc", help="Account description")
@click.option("--host", required=True, help="Host URL (required)")
@click.option("--type", required=True, type=click.Choice(["oci", "helm", "git"]), help="Account type: oci|helm|git")
@click.option("--username", required=True, help="Username (required)")
@click.option("--password", required=True, help="Password (required)")
@common_options
@click.pass_context
def create_account(ctx, title, desc, host, type, username, password, sky_config, api_url, user_id, format, quiet,
                   debug):
    """Create an account"""
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)

    api_url = ctx.obj.get('api_url') + account_path
    user_id = ctx.obj.get('user_id') or check_key()

    # 调用 API 创建账户
    result = account_api.create_account(api_url, user_id, title, desc, host, type, username, password)

    common_result_handle(ctx, result)


@account.command("get")
@click.argument("account_id")
@common_options
@click.pass_context
def get_account(ctx, account_id, sky_config, api_url, user_id, format, quiet, debug):
    """Get account details"""
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)
    api_url = ctx.obj.get('api_url') + account_path
    user_id = ctx.obj.get('user_id')
    # 调用 API 获取账户详情
    result = account_api.get_account_details(api_url, user_id, account_id)
    common_result_handle(ctx, result)


@account.command("update")
@click.argument("account_id")
@click.option("--title", help="New title")
@click.option("--desc", help="New description")
@click.option("--host", help="New host URL")
@click.option("--type", type=click.Choice(["oci", "helm", "git"]), help="New account type")
@click.option("--username", help="New username")
@click.option("--password", help="New password")
@common_options
@click.pass_context
def update_account(ctx, account_id, title, desc, host, type, username, password, sky_config, api_url, user_id, format,
                   quiet, debug):
    """Update an account"""
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)
    api_url = ctx.obj.get('api_url') + account_path
    user_id = ctx.obj.get('user_id')
    result = account_api.update_account(ctx, api_url, user_id, account_id, title, desc, host, type, username, password)

    common_result_handle(ctx, result)


@account.command("delete")
@click.argument("account_id")
@click.option("--force", is_flag=True, help="Force deletion without confirmation")
@common_options
@click.pass_context
def delete_account(ctx, account_id, force, sky_config, api_url, user_id, format, quiet, debug):
    """Delete an account"""
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)

    api_url = ctx.obj.get('api_url') + account_path
    user_id = ctx.obj.get('user_id')
    if not force:
        if not click.confirm(f"Are you sure you want to delete account {account_id}?"):
            click.echo("Operation cancelled.")
            return
    result = account_api.delete_account(api_url, user_id, account_id)

    common_result_handle(ctx, result)


# 列出所有账户命令
@account.command("list")
@list_common_options
@common_options
@click.pass_context
def list_accounts(ctx, start, limit, sort, sky_config, api_url, user_id, format, quiet, debug):
    """List all accounts"""
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)

    api_url = ctx.obj.get('api_url') + account_path
    user_id = ctx.obj.get('user_id')
    result = account_api.list_accounts(api_url, user_id, start, limit, sort)

    # 根据输出格式返回结果
    common_result_handle(ctx, result)


@resource.group()  # dashboard
def dashboard():
    """Manage Dashboards"""
    pass


@dashboard.command("create")
@click.option("--title", required=True, help="Dashboard title (required)")
@click.option("--desc", required=True, help="Dashboard description")
@click.option("--size", required=True, type=click.Choice(["small", "medium", "large"]), help="Dashboard size")
@click.option("--url", required=True, help="Dashboard URL")
@common_options
@click.pass_context
def create_dashboard(ctx, title, desc, size, url, sky_config, api_url, user_id, format, quiet, debug):
    """Create a dashboard"""
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)
    api_url = ctx.obj.get('api_url') + dashboard_path
    user_id = ctx.obj.get('user_id') or check_key()

    result = dashboard_api.create_dashboard(api_url, user_id, title, desc, size, url)
    common_result_handle(ctx, result)


@dashboard.command("list")
@list_common_options
@common_options
@click.pass_context
def list_dashboards(ctx, start, limit, sort, sky_config, api_url, user_id, format, quiet, debug):
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)
    api_url = ctx.obj.get('api_url') + dashboard_path
    user_id = ctx.obj.get('user_id') or check_key()

    result = dashboard_api.list_dashboard(api_url, user_id, start, limit, sort)
    common_result_handle(ctx, result)


@dashboard.command("get")
@click.argument("dashboard_id", type=int)
@common_options
@click.pass_context
def get_dashboard(ctx, dashboard_id, sky_config, api_url, user_id, format, quiet, debug):
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)
    api_url = ctx.obj.get('api_url') + dashboard_path
    user_id = ctx.obj.get('user_id') or check_key()
    result = dashboard_api.get_dashboard(api_url, user_id, dashboard_id)
    common_result_handle(ctx, result)


@dashboard.command("update")
@click.argument("dashboard_id", type=int)
@click.option("--title", help="New title")
@click.option("--desc", help="New description")
@click.option("--size", type=click.Choice(["small", "medium", "large"]), help="New size")
@click.option("--url", help="New URL")
@common_options
@click.pass_context
def update_dashboard(ctx, dashboard_id, title, desc, size, url, sky_config, api_url, user_id, format, quiet, debug):
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)
    api_url = ctx.obj.get('api_url') + dashboard_path
    user_id = ctx.obj.get('user_id') or check_key()
    result = dashboard_api.update_dashboard(ctx, api_url, user_id, dashboard_id, title, desc, size, url)
    click.echo(result)


@dashboard.command("delete")
@click.argument("dashboard_id", type=int)
@click.option("--force", is_flag=True, help="Force deletion without confirmation")
@common_options
@click.pass_context
def delete_dashboard(ctx, dashboard_id, force, sky_config, api_url, user_id, format, quiet, debug):
    common_options_handle(ctx, sky_config, api_url, user_id, format, quiet, debug)
    api_url = ctx.obj.get('api_url') + dashboard_path
    user_id = ctx.obj.get('user_id') or check_key()
    if not force:
        if not click.confirm(f"Are you sure you want to delete dashboard {dashboard_id}?"):
            click.echo("Operation cancelled.")
            return
    result = dashboard_api.delete_dashboard(api_url, user_id, dashboard_id)
    click.echo(result)


@click.group()
def version():
    pass


@version.command('version',
                 help='check version',
                 context_settings=_CONTEXT_SETTINGS)
def check_version():
    click.echo('SkyCtl Version: ' + str_version)


def check_key():
    file_path = dir_path + '/pat.ini'
    if not os.path.exists(file_path):
        click.echo('No user authentication profile detected! Creating one...')
        os.makedirs(dir_path, exist_ok=True)
        config = configparser.ConfigParser()
        config['CREDENTIALS'] = {'X-UserId': '99'}
        with open(file_path, 'w') as configfile:
            config.write(configfile)
        return '19'
    try:
        config = configparser.ConfigParser()
        # read `pat.ini`
        config.read(file_path)
        pat = config['CREDENTIALS']['X-UserId']

    except:
        click.echo('User profile error, please check and log in again!')
    else:
        return pat


def override_config(ip, port):
    __url_config = configparser.ConfigParser()
    __current_path = os.path.abspath(os.path.dirname(__file__))
    __url_config.read(__current_path + '/server_config.ini')
    __login_url = 'http://' + ip + ':' + port + login_url_path
    __upload_url = 'http://' + ip + ':' + port + upload_url_path
    __list_url = 'http://' + ip + ':' + port + list_url_path
    __create_url = 'http://' + ip + ':' + port + create_url_path
    __host_ip = 'http://' + ip + ':' + port
    __url_config.set('server', 'login_url', __login_url)
    __url_config.set('server', 'upload_url', __upload_url)
    __url_config.set('server', 'create_url', __create_url)
    __url_config.set('server', 'list_url', __list_url)
    __url_config.set('server', 'host_ip', __host_ip)
    with open(__current_path + '/server_config.ini', 'w') as file:
        __url_config.write(file)


def validate_ip(ip):
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    if not ip_pattern.match(ip):
        return False
    parts = ip.split('.')
    return all(0 <= int(part) <= 255 for part in parts)


def validate_port(port):
    port_pattern = re.compile(r'^\d+$')
    if not port_pattern.match(port):
        return False
    port_int = int(port)
    return 0 <= port_int <= 65535


def common_result_handle(ctx, response):
    handle_response(response)
    result = response.json()
    if ctx.obj.get('format') == 'table' and isinstance(result, (dict, list)):
        if isinstance(result, list):
            table = tabulate(result, headers="keys", tablefmt="grid")
        else:
            table = tabulate([result], headers="keys", tablefmt="grid")
        click.echo(table)
    else:
        click.echo(json.dumps(result, indent=4))


cli = click.CommandCollection(sources=[login, upload, namespace, version, resource])
cli.help = """
     *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *\n
     *  SkyCtl CLI Tool.                                                        *\n
\n
     *  This is the main entry point for the SkyCtl command line interface.     *\n
     *  It provides a set of commands to interact with the Skybackend server.   *\n
\n
     *  Before using any of the commands, you need to prepare a config file     *\n
     *  at `~/.skyctl/pat.ini` with the following format:                       *\n
     *      [CREDENTIALS]                                                       *\n
     *      X-UserId = your_user_id                                             *\n
\n
     *  You can find more information in the official github documentation.     *\n
     *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
    """

if __name__ == '__main__':
    try:
        cli()
    except CLIError as e:
        e.show()
        sys.exit(e.code)
    except Exception as e:
        cli_error = CLIError(str(e), GENERAL_ERROR_CODE)
        cli_error.show()
        sys.exit(cli_error.code)
