"""
This module provides functions for working with REST API.
"""

"""
" ██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ████████╗██████╗  ██████╗ ███╗   ██╗
" ██║  ██║██║   ██║████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██╔═══██╗████╗  ██║
" ███████║██║   ██║██╔████╔██║███████║   ██║   ██████╔╝██║   ██║██╔██╗ ██║
" ██╔══██║██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║   ██║██║╚██╗██║
" ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║╚██████╔╝██║ ╚████║
" ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
"
"                   Copyright (C) 2023 Humatron, Inc.
"                          All rights reserved.
"""

from typing import Any

HUMATRON_RESPONSE_TOKEN = 'Humatron_Response_Token'
"""REST header name for response token."""


def check_request_token(headers: dict[str, Any], req_token: str) -> bool:
    """
    Checks if the request token in the headers matches the provided token.

    @param headers: HTTP headers to check for the request token.
    @param req_token: The expected request token.

    @return:
        True if the request token matches, False otherwise.
    """
    arr = headers.get('Authorization', '').split(' ')

    return len(arr) == 2 and arr[1] == req_token


def set_response_token(headers: dict[str, Any], resp_token: str) -> None:
    """
    Sets the response token in the headers.

    @param headers: The headers of the response.
    @param resp_token: The response token to be set.
    """
    headers[HUMATRON_RESPONSE_TOKEN] = resp_token
