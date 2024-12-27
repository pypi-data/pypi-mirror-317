"""
This module provides classes for working with Humatron worker,
including request and response handling, payload processing, and asynchronous execution.
"""
from locked_dict.locked_dict import LockedDict

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
import os
import threading
import uuid
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from typing import Callable

from humatron.worker.beans import *

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
_logger = logging.getLogger('humatron.worker.sdk')


class HumatronWorkerApi(ABC):
    """
    Abstract base class for Humatron workers responsible for handling asynchronous requests.

    This class fully represents the B{Worker API} as detailed in the
    U{Humatron documentation<https://humatron.ai/build/worker_api>}.

    This class defines the contract for processing requests, where each concrete implementation
    of this class should provide its own logic for handling a request and returning an appropriate
    response.
    """

    @abstractmethod
    def process_request(self, req: Request) -> Optional[Response]:
        """
        Posts a request asynchronously, processing its payload parts and returning a response.

        @param req :
            The request to be processed asynchronously.

        @return:
            The response after processing the request, or None if no response is available.
        """

        pass


class HumatronAsyncWorker(HumatronWorkerApi, ABC):
    """
    Asynchronous adapter for Humatron worker using a thread pool executor.

    This class extends the HumatronWorker to provide asynchronous request processing
    using a thread pool for concurrency.
    """

    def __init__(self, pool_size: Optional[int] = None):
        """
        Initializes the async adapter with a thread pool.

        @param pool_size :
            The maximum number of threads in the pool. Defaults to the number of CPUs.
        """

        if pool_size is not None and pool_size <= 0:
            raise ValueError('Pool size must be greater than 0.')

        self._max_threads = pool_size or os.cpu_count()
        self._cur_threads = 0

        self._pool = ThreadPoolExecutor(max_workers=pool_size or os.cpu_count())
        self._resp_payloads_parts_data: list[ResponsePayloadPart] = []
        self._lock = threading.Lock()
        self._storage = LockedDict()

    def close(self) -> None:
        """
        Shuts down the thread pool, ensuring all tasks are completed.
        """
        self._pool.shutdown()

    def process_request(self, req: Request) -> Optional[Response]:
        if req.req_cmd == RequestType.INTERVIEW:
            if req.storage:
                raise ValueError('Storage cannot be provided for `interview` requests.')
            elif not req.payload or len(req.payload) != 1:
                raise ValueError('Invalid payload for `interview` request.')

            pp = self.process_payload_part(
                RequestPayloadPart(req.req_cmd, req.req_id, req.req_tstamp, req.payload[0]), None
            )

            if not pp or isinstance(pp, list):
                raise ValueError(f'Unexpected response payload for `interview` request [payload={pp}]')

            return Response(_make_id(), _utc_now_iso_format(), [pp], None)

        self._storage.update(req.storage)

        with self._lock:
            storage_cp = deepcopy(self._storage)

        def fn() -> None:
            with self._lock:
                self._cur_threads += 1
                n = self._cur_threads
            _logger.debug(f'Processing request [id={req.req_id}, cur_threads={n}, max_threads={self._max_threads}]')
            try:
                res: list[ResponsePayloadPart] = []
                if req.payload:
                    for req_body in req.payload:
                        rpp = RequestPayloadPart(req.req_cmd, req.req_id, req.req_tstamp, req_body)

                        resp_bodies = self.process_payload_part(rpp, self._storage)

                        if resp_bodies is not None:
                            if not isinstance(resp_bodies, list):
                                resp_bodies = [resp_bodies]

                            resp_bodies = list(filter(lambda el: el, resp_bodies)) if resp_bodies else None

                            if resp_bodies:
                                res.extend(resp_bodies)
                    with self._lock:
                        if res:
                            self._resp_payloads_parts_data.extend(res)
            except Exception as e:
                _logger.error(f'Error during processing [error={e}]', exc_info=True)
            finally:
                with self._lock:
                    self._cur_threads -= 1
                    n = self._cur_threads
                _logger.debug(
                    f'Processing finished [id={req.req_id}, cur_threads={n}, max_threads={self._max_threads}]'
                )

        self._pool.submit(fn)

        with self._lock:
            storage, changed = (deepcopy(self._storage), True) if storage_cp != self._storage else None, False

            if not self._resp_payloads_parts_data and not changed:
                return None

            payloads = self._resp_payloads_parts_data[:] if self._resp_payloads_parts_data else None
            self._resp_payloads_parts_data.clear()

        return Response(_make_id(), _utc_now_iso_format(), payloads, storage)

    def push_response(
        self, make: Callable[[Storage], Union[list[ResponsePayloadPart], ResponsePayloadPart]]
    ) -> None:
        """
        Sends a response without an initiating request.
        This method enables the system to proactively deliver a response,
        without the need for an external request trigger.

        @param make :
            A callable that takes a C{Storage} object as input and returns a C{ResponsePayloadPart}.
            This function is responsible for preparing the response payload independently of any request,
            with the ability to modify the C{Storage} object if necessary.
            Note that the C{Storage} object is thread-safe.
        """

        resp = make(self._storage)

        with self._lock:
            if isinstance(resp, list):
                self._resp_payloads_parts_data.extend(resp)
            else:
                self._resp_payloads_parts_data.append(resp)

    @abstractmethod
    def process_payload_part(
        self, req_payload_part: RequestPayloadPart, storage: Optional[Storage]
    ) -> ResponsePayloadPart:
        """
        Abstract method to process a request payload part.
        Note that this method may run for an extended period, but you don't need to worry about its execution time.
        It is added to the execution queue and will run in a separate thread.

        @param req_payload_part :
            The request payload part to be executed.
        @param storage :
            C{storage} used to maintain state during requests processing.
            It remains empty for requests of type C{INTERVIEW}.
            Note that the C{storage} object is thread-safe.

        @return:
            The result of the execution, which could be a list of payload parts, a single payload part, or None.
        """
        pass


def _utc_now_iso_format() -> str:
    """
    Returns the current UTC time in ISO format, truncated to milliseconds.

    @return:
        The current UTC time in ISO format, truncated to milliseconds.
    """
    return f'{datetime.datetime.utcnow().isoformat()[:-3]}Z'


def _make_id() -> str:
    """
    Generates a unique ID.

    @return:
        A unique identifier string.
    """
    return str(uuid.uuid4().hex)
