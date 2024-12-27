"""
This module provides utility functions for working with Humatron worker.
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

from humatron.worker.client import *


def make_default_response_payload(
    req_cmd: RequestType, req_payload_part: RequestPayloadPartBody
) -> Optional[ResponsePayloadPartBody]:
    """
    Generates a default response payload based on the request command.

    @param req_cmd :
        The command associated with the request. C{MESSAGE} and C{INTERVIEW} types are unsupported.

    @param req_payload_part :
        The request payload part for which to generate a response.

    @return:
        The generated response payload.
    """
    match req_cmd:
        case RequestType.REGISTER:
            return ResponseDataRegister.make(
                instance_id=req_payload_part.instance.id,
                ref_payload_id=req_payload_part.payload_id,
                result=True,
                reject_code=None,
                contacts=req_payload_part.contacts
            )
        case RequestType.PAUSE:
            return ResponseDataPause.make(
                instance_id=req_payload_part.instance.id,
                ref_payload_id=req_payload_part.payload_id,
                result=True,
                error_code=None,
                contacts=req_payload_part.contacts
            )
        case RequestType.RESUME:
            return ResponseDataResume(
                resp_cmd=req_cmd,
                instance_id=req_payload_part.instance.id,
                ref_payload_id=req_payload_part.payload_id,
                result=True,
                error_code=None,
                contacts=req_payload_part.contacts
            )
        case RequestType.UNREGISTER:
            return ResponseDataUnregister(
                resp_cmd=req_cmd,
                instance_id=req_payload_part.instance.id,
                ref_payload_id=req_payload_part.payload_id,
                contacts=req_payload_part.contacts
            )
        case RequestType.HEARTBEAT:
            return None
        case _:
            raise ValueError(f'Unsupported request type: {req_cmd}')
