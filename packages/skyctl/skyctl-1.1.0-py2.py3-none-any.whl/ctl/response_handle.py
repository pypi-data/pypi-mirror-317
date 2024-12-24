import logging
from ctl.error import CLIError
from ctl.constants import *
from ctl.logging_config import *

logger = logging.getLogger(__name__)


def handle_response(response):
    if response.status_code == 404:
        logger.error('404 Not Found')
        raise CLIError(f'404 Not Found {response.url} {response.text}', NETWORK_ERROR_CODE)
    if response.status_code == 401:
        logger.error('401 Unauthorized')
        raise CLIError('401 Unauthorized', AUTHENTICATION_ERROR_CODE)
    if response.status_code == 400:
        logger.error('400 Bad Request')
        raise CLIError(f'400 Bad Request {response.text}', API_ERROR_CODE)
