"""
This module provides classes and functions for working with REST channel.
"""
from enum import StrEnum

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

import datetime
import json
import logging
import threading
import time
import uuid
from threading import Thread
from typing import NamedTuple, Optional, Callable

import requests


class RestRequestType(StrEnum):
    """
    Represents a set of requests types for REST communication channel.
    """

    MESSAGE = 'message'
    """
    This request is sent to the REST channel server endpoint when one or more new messages are available for 
    the worker instance.
    """

    HEARTBEAT = 'heartbeat'
    """
    In addition to C{message} requests, the client application can send regular C{heartbeat} requests to the REST channel 
    server.These C{heartbeat} requests do not contain any significant data; their primary purpose is to prompt the server 
    to respond to previous C{message} requests from the worker instance that have accumulated on the REST channel server.
    """


class RequestMessagePayloadPart(NamedTuple):
    """
    Represents a part of a REST request payload, containing metadata and content.
    """

    payload_id: str
    """Unique identifier for the payload part."""
    sender: str
    """The entity that sends the payload (e.g., a service or user)."""
    receiver: str
    """The entity that receives the payload (e.g., a service or user)."""
    text: str
    """The content or message within the payload."""

    @classmethod
    def make(cls, text: str, sender: str, receiver: str) -> 'RequestMessagePayloadPart':
        """
        Factory method to create a new RequestMessagePayloadPart.

        @param text :
            The content of the payload.
        @param sender :
            The sender of the payload.
        @param receiver :
            The receiver of the payload.

        @return:
            A new instance of RequestMessagePayloadPart.
        """
        return cls(str(uuid.uuid4()), sender, receiver, text)


class RestChannelRequest(NamedTuple):
    """
    Represents a REST request with a list of payload parts.
    """

    req_id: str
    """Unique identifier for the request."""
    req_cmd: RestRequestType
    """Type of the request."""
    payload: list[RequestMessagePayloadPart]
    """List of payload parts attached to the request."""
    req_tstamp: str
    """Timestamp when the request was created."""

    @classmethod
    def make_message(cls, payload: list[RequestMessagePayloadPart] | RequestMessagePayloadPart) -> 'RestChannelRequest':
        """
        Factory method to create a C{message} request.

        @param payload :
            One or more payload parts to be included in the request.

        @return:
            A new C{message} request containing the provided payload.
        """
        if isinstance(payload, RequestMessagePayloadPart):
            payload = [payload]
        if not payload:
            raise ValueError('Payload cannot be empty.')

        return cls(str(uuid.uuid4()), RestRequestType.MESSAGE, payload, _utc_now_iso_format())

    @classmethod
    def make_heartbeat(cls) -> 'RestChannelRequest':
        """
        Factory method to create a C{heartbeat} request.

        @return:
            A new C{heartbeat} request with no payload.
        """
        return cls(str(uuid.uuid4()), RestRequestType.HEARTBEAT, [], _utc_now_iso_format())


class ResponseMessagePayloadPart(NamedTuple):
    """
    Represents a part of a REST response payload, linking responses to their corresponding requests.
    """

    ref_payload_id: Optional[str]
    """Unique identifier for the response payload part."""
    sender: str
    """The entity that sends the response payload."""
    receiver: str
    """The intended recipient of the response payload."""
    text: str
    """The content of the response payload."""


class RestChannelResponse(NamedTuple):
    """
    Represents a REST response containing a list of response payload parts.
    """

    resp_id: str
    """Unique identifier for the response."""
    payload: list[ResponseMessagePayloadPart]
    """List of response payload parts included in the response."""
    resp_tstamp: str
    """Timestamp when the response was created."""


def _utc_now_iso_format() -> str:
    """
    Returns the current UTC time in ISO format, truncated to milliseconds.

    @return:
        The current UTC time formatted as an ISO string.
    """
    return f'{datetime.datetime.utcnow().isoformat()[:-3]}Z'


def _post(url: str, headers: dict[str, str], req: RestChannelRequest) -> Optional[RestChannelResponse]:
    """
    Sends a POST request to the server and processes the response.

    @param url :
        The server URL to send the request to.
    @param headers :
        HTTP headers to include in the request.
    @param req :
        The request object to be sent.

    @return:
        The response from the server, or None if no response is received.

    @raise ValueError:
        If the response status code is not 200.
    """
    msg = {'req_cmd': req.req_cmd, 'req_id': req.req_id, 'req_tstamp': req.req_tstamp}

    if req.req_cmd == RestRequestType.MESSAGE:
        msg['payload'] = [r._asdict() for r in req.payload]

    res = requests.post(url, json.dumps(msg), headers=headers)

    if res.status_code != 200:
        raise ValueError(f'Unexpected response code: {res.status_code}, content={res.json()}')

    resp_js = res.json()

    if not resp_js:
        return None

    payloads = [
        ResponseMessagePayloadPart(
            ref_payload_id=p.get('ref_payload_id'),
            sender=p['sender'],
            receiver=p['receiver'],
            text=p['text']
        )
        for p in resp_js['payload']
    ]

    return RestChannelResponse(resp_js['resp_id'], payloads, resp_js['resp_tstamp'])


def _mk_headers(token: str) -> dict[str, str]:
    """
    Constructs HTTP headers required for requests.

    @param token : str
        Authorization token for the request.

    @return:
        Dictionary containing the Authorization and Content-Type headers.
    """
    return {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}


class RestChannelClient:
    """
    Synchronous REST channel client for sending requests and receiving responses.
    """

    def __init__(self, server_url: str, token: str):
        """
        Initializes the RestChannelClient with the server URL and token.

        @param server_url :
            The server URL for sending requests.
        @param token :
            Authorization token for the requests.
        """
        self._server_url = server_url
        self._headers = _mk_headers(token)

    def post(self, req: RestChannelRequest) -> Optional[RestChannelResponse]:
        """
        Sends a request to the server and returns the response.

        @param req :
            The request object to be sent.

        @return:
            The response received from the server, or None if no response is received.
        """
        return _post(self._server_url, self._headers, req)


_logger = logging.getLogger(__name__)

DFLT_HB_INTERVAL_SEC = 5
"""Default heartbeat interval, in seconds."""


class RestChannelAsyncClient:
    """
    Asynchronous REST channel client that sends requests and processes responses in the background.
    """

    def __init__(
        self,
        server_url: str,
        token: str,
        on_resp_payload: Callable[[str, ResponseMessagePayloadPart], None],
        on_heartbeat: Optional[Callable[[Optional[Exception]], None]] = None,
        hb_interval_sec: float = DFLT_HB_INTERVAL_SEC
    ):
        """
        Initializes the RestChannelAsyncClient with server details and callbacks.

        @param server_url :
            The server URL for sending requests.
        @param token :
            Authorization token for the requests.
        @param on_resp_payload :
            Callback to process each response payload part.
            The callback takes two arguments: a response ID and a payload part.
        @param on_heartbeat :
            An optional callback function to handle C{heartbeat} events.
        @param hb_interval_sec :
            Interval between C{heartbeat} requests, in seconds.
        """
        self._server_url = server_url
        self._headers = _mk_headers(token)
        self._on_resp_payload = on_resp_payload
        self._on_heartbeat = on_heartbeat
        self._hb_interval_sec = hb_interval_sec
        self._thread = Thread(target=self._hb)
        self._stopped = False
        self._sleep_event = threading.Event()
        self._lock = threading.Lock()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def start(self) -> None:
        """
        Starts the asynchronous client and the heartbeat thread.
        """
        self._thread.start()
        _logger.info('RestChannelAsyncClient started.')

    def close(self) -> None:
        """
        Stops the asynchronous client and terminates the heartbeat thread.
        """
        _logger.info('RestChannelAsyncClient closing.')
        with self._lock:
            self._stopped = True
            self._sleep_event.set()
        self._thread.join()
        _logger.info('RestChannelAsyncClient closed.')

    def post(self, req: RestChannelRequest) -> None:
        """
        Sends a request to the server asynchronously.

        @param req :
            The request to be sent to the server.
        """
        with self._lock:
            resp = _post(self._server_url, self._headers, req)
        self._on_srv_messages(resp)

    def _on_srv_messages(self, resp: Optional[RestChannelResponse]) -> None:
        """
        Processes the server messages and triggers the response callback.

        @param resp :
            The response from the server.
        """
        if resp:
            for payload in resp.payload:
                self._on_resp_payload(resp.resp_id, payload)

    def _hb(self) -> None:
        """
        The heartbeat thread function, sending regular heartbeat requests.
        """
        while not self._stopped:
            with self._lock:
                if self._stopped:
                    break
                self._sleep_event.clear()

            self._sleep_event.wait(self._hb_interval_sec)

            with self._lock:
                if self._stopped:
                    break

                try:
                    resp = _post(self._server_url, self._headers, RestChannelRequest.make_heartbeat())
                    err = None
                except Exception as e:
                    resp = None
                    err = e

            if err:
                if self._on_heartbeat:
                    self._on_heartbeat(err)
                else:
                    _logger.error(f'Error during sending heartbeat [error={err}]', exc_info=True)
            else:
                if self._on_heartbeat:
                    self._on_heartbeat(None)

            self._on_srv_messages(resp)


DFLT_HB_TIMEOUT_SEC = 60
"""Default heartbeat timeout, in seconds."""


class RestChannelSyncClient:
    """
    Synchronous REST channel client with heartbeat support for continuous communication.
    """

    def __init__(self, server_url: str, token: str, hb_interval_sec: float = DFLT_HB_INTERVAL_SEC):
        """
        Initializes the RestChannelSyncClient with server details and heartbeat configuration.

        @param server_url :
            The server URL for sending requests.
        @param token :
            Authorization token for the requests.
        @param hb_interval_sec :
            Interval between C{heartbeat} requests, in seconds.
        """
        self._server_url = server_url
        self._headers = _mk_headers(token)
        self._hb_interval_sec = hb_interval_sec

    def _get(self, req: RestChannelRequest, exp_payload_id: str) -> Optional[RestChannelResponse]:
        """
        Sends a request and checks if the expected payload is received.

        @param req :
            The request to be sent to the server.
        @param exp_payload_id :
            The expected payload ID to check in the response.

        @return:
            The response containing the expected payload, or None if not found.
        """
        resp = _post(self._server_url, self._headers, req)

        if not resp:
            return None

        for part in resp.payload:
            if part.ref_payload_id == exp_payload_id:
                return RestChannelResponse(resp.resp_id, [part], resp.resp_tstamp)
            else:
                _logger.warning(
                    f'Unexpected response [exp_payload_id={exp_payload_id}, ref_payload_id={part.ref_payload_id}]'
                )

        return None

    def post(self, req: RestChannelRequest, timeout_sec: float = DFLT_HB_TIMEOUT_SEC) -> RestChannelResponse:
        """
        Sends a request and waits for the response within the timeout period.

        @param req :
            The request object to be sent.
        @param timeout_sec :
            The maximum time to wait for a response, in seconds (default is DFLT_HB_TIMEOUT_SEC).

        @return:
            The response from the server.

        @raise ValueError:
            If the request contains more than one payload part.
        @raise TimeoutError:
            If the request times out without receiving a response.
        """
        payload = req.payload

        if len(payload) != 1:
            raise ValueError('Only single payload is supported.')

        part = payload[0]
        max_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout_sec)

        resp = self._get(req, part.payload_id)

        while not resp and datetime.datetime.now() < max_time:
            time.sleep(self._hb_interval_sec)
            resp = self._get(RestChannelRequest.make_heartbeat(), part.payload_id)

        if not resp:
            raise TimeoutError(f'Request timed out after {timeout_sec} seconds.')

        return resp
