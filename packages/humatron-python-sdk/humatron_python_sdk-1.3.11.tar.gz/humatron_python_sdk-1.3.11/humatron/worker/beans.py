"""
This module provides beans for working with Humatron worker, including request and response classes.
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

import json
import logging
from enum import StrEnum
from typing import Optional, Union, NamedTuple, Any


class RequestType(StrEnum):
    """
    Represents a set of requests types for system operations.
    """

    INTERVIEW = 'interview'
    """
    This request is sent to the worker endpoint when a prospective hirer (employer or hiring manager) 
    initiates the interview on Humatron website (and auto-interview is not enabled)
    """

    REGISTER = 'register'
    """
    This register request is sent to AI worker endpoint when the new instance of this AI worker is hired. 
    The AI worker implementation is assumed to be multi-tenant, i.e. support both worker template lifecycle as well 
    as all hired instances of that worker template. 
    Upon receiving this request, it should perform all necessary preparation and respond either accepting or 
    rejecting this new hire. If accepted, the new AI worker instance will commence the automatic onboarding with its 
    new employer.
    """

    UNREGISTER = 'unregister'
    """
    This request is sent to AI worker endpoint when the worker instance is terminated. 
    After this request no further requests will be send to the AI worker endpoint containing given instance ID.
    """

    PAUSE = 'pause'
    """
    This request is sent to AI worker endpoint when the worker instance is paused. 
    In this state, the instance can only be either resumed or terminated.
    """

    RESUME = 'resume'
    """This request is sent to AI worker endpoint when the worker instance is resumed."""

    HEARTBEAT = 'heartbeat'
    """
    Apart from regular requests, Humatron sends regular C{HEARTBEAT} requests to each hired AI worker. 
    These requests are sent out at least several times a minute. 
    These C{HEARTBEAT} requests do not carr y any meaningful data, their only purpose is to provide a regular ping so that 
    AI worker can react quasi-asynchronously over the synchronous HTTP protocol. 
    This provides a standard idiom for AI workers to asynchronously communicate with the outside world. 
    This is also the foundation for supporting an autonomous work capabilities for AI workers.
    """

    MESSAGE = 'message'
    """
    This request is sent to AI worker endpoint when there is one or more new messaged available for the worker instance.
    """


class Address(NamedTuple):
    """
    Represents a physical address with metadata.
    """

    street: str
    """Street address."""

    city: str
    """City name."""

    region_name: str
    """Name of the region."""

    region_abbr: Optional[str]
    """Optional abbreviation of the region."""

    postal_code: str
    """Postal or ZIP code."""

    country_name: str
    """Country name as in ISO 3166."""

    country_iso_3166: str
    """Country as ISO 3166 code."""


class ContactRecord(NamedTuple):
    """
    Represents a single contact record.
    """

    kind: str
    """Supported values: C{email}, C{slack}, C{phone}, C{REST}."""

    tstamp: str
    """Timestamp of the record creation in UTC, formatted according to ISO-8601."""

    csv_tags: Optional[str]
    """Optional list of comma separated tags."""

    properties: Any
    """Properties of the contact record. Properties content depends on the kind field."""


class Contact(NamedTuple):
    """
    Represents a contact with multiple records.
    """

    first_name: Optional[str]
    """First name of the contact."""

    last_name: Optional[str]
    """Last name of the contact."""

    full_name: str
    """Full name of the contact."""

    records: list[ContactRecord]
    """List of contact records. Order is not significant. Records are unique, as duplicates are removed."""


class Person(NamedTuple):
    """
    Represents an individual or user within the system.
    """

    first_name: str
    """First name of the person."""

    last_name: Optional[str]
    """Last name of the person."""

    email: str
    """Email address of the person."""

    suspended: bool
    """
    Indicates if the person is suspended. 
    Person can be suspended by Humatron only. Suspended person cannot sign in.
    """

    org_id: int
    """ID of the organization this person belongs to."""

    oauth_provider: Optional[str]
    """Name of the OAuth 2.0 provider from the last OAuth sing in."""

    avatar_data_uri: Optional[str]
    """
    Optional URL or data-URI for this person avatar. This avatar can only be set on Humatron website's user profile page. 
    Note that either this field, oauth_avatar_url or none can be provided for this person.
    """

    oauth_avatar_url: Optional[str]
    """User avatar URL from the last OAuth sing in."""

    primary_lang_iso_639: str
    """SO 639-2 code for the primary communication language for this person."""

    is_email_confirmed: bool
    """
    Whether or not this person email is confirmed. 
    Email must be confirmed before user can sign in at Humatron website.
    """

    phone: Optional[str]
    """Phone number of the person."""

    address: Optional[Address]
    """Address of the person."""


class File(NamedTuple):
    """
    Represents a file with associated metadata.
    """

    type: str
    """File provider type. Currently supported value is: C{AMAZON_S3}."""

    size: int
    """File size in bytes."""

    properties: Any
    """File provider related properties."""


class ChannelType(StrEnum):
    """
    Represents a set of supported channel types.
    """

    EMAIL = 'email'
    '''Email channel type.'''

    SLACK = 'slack'
    '''Slack channel type.'''

    SMS = 'SMS'
    '''SMS channel type.'''

    REST = 'REST'
    '''Rest channel type.'''

    WHATSUP = 'whatsup'
    '''Whatsup channel type.'''

    SIGNAL = 'signal'
    '''Signal channel type.'''

    VOICEMAIL = 'voicemail'
    '''Voicemail channel type.'''

    SKYPE = 'skype'
    '''Skype channel type.'''

    TELEGRAM = 'telegram'
    '''Telegram channel type.'''

    TEAMS = 'teams',
    '''Teams channel type.'''

    DROPBOX = 'dropbox'
    '''Dropbox channel type.'''

    GOOGLE_DOCS = 'google docs'
    '''Google Docs channel type.'''

    ZOOM = 'zoom'
    '''Zoom channel type.'''

    PHONE = 'phone'
    '''Phone channel type.'''

    GOOGLE_MEET = 'google meet'
    '''Google Meet channel type.'''


class Channel(NamedTuple):
    """
    Represents a communication channel with its capabilities.
    """

    type: ChannelType
    """Channel type."""

    descr: str
    """Channel description."""

    provider_name: str
    """Channel provider name."""

    capabilities_csv: str
    """Comma separated list of channel capabilities."""


class PricePlan(NamedTuple):
    """
    Represents a pricing plan for services.
    """

    trial_period_days: int
    """Number of days for the trial period. Can be zero."""

    trial_restrictions: Optional[str]
    """Restrictions during the trial period, if any."""

    service_level: str
    """
    	Description of the service level provided by this price plan. Could include response time, curation time, 
    	maximum number of request per hour, etc.
    """

    setup_fee_usd: float
    """Setup fee in USD, if any. Can be zero."""

    hourly_fee_usd: float
    """Hourly fee in USD. Cannot be zero."""

    monthly_fee_usd: float
    """Monthly fee in USD. Cannot be zero."""


class Role(NamedTuple):
    """
    Represents a role with associated permissions or responsibilities.
    """

    name: str
    """Name of the role."""

    descr: str
    """Description of the role."""


class Resource(NamedTuple):
    """
    Represents a resource within the system.
    """

    id: int
    """Resource ID."""

    channel_type: ChannelType
    """
    Type of the communication channel this resource belongs to. 
    """

    csv_tags: Optional[str]
    """Optional list of comma separated tags."""

    properties: Any
    """Properties of the resource. Properties content depends on the channel_type field."""


class Organization(NamedTuple):
    """
    Represents an organization with associated metadata.
    """

    id: int
    """Unique ID of this organization."""

    avatar_url: Optional[str]
    """URL for this organization's logo. The image will be scaled down as much as 32 pixels in height."""

    show_name: bool
    """Whether or not this organization's name should be shown in the top-right corner of the header."""

    avatar_on_right: bool
    """Whether or not this organization's logo is displayed in the top-right corner of the header."""

    name: str
    """Name of this organization."""

    formal_name: Optional[str]
    """Formal or legal name of this organization."""

    industry: Optional[str]
    """Organization industry."""

    website: str
    """Website URL of this organization. It may optionally include the protocol part 'https://'."""

    is_root: bool
    """Indicates if this organization is the root organization (i.e. Humatron AI)."""

    address: Optional[Address]
    """Address of this organization."""

    country: Optional[str]
    """Country name of this organization as in ISO 3166."""

    country_iso_3166: Optional[str]
    """ISO 3166-2 code of the country for this organization."""


class Specialist(NamedTuple):
    """
    Represents a specialist with various attributes and capabilities.
    """

    id: int
    """Unique ID of this worker template."""

    planned_live_date: Optional[str]
    """
    Planned live date of the worker template. 
    String is used only for display purpose, i.e. it does not have to be in a valid string format.'.
    """

    avatar_url: str
    """
    URL for the worker template\'s avatar. This would be the avatar shown in the marketplace for this worker as well 
    as the default avatar for worker instance when hired.
    """

    status: str
    """Status of this worker template. Supported values are: C{init}, C{dev}, C{live}, C{paused}."""

    init_setup_dur_hours: int
    """Initial technical setup duration in hours. This information is public."""

    init_setup_info: Optional[str]
    """
    General information about initial technical setup to be displayed on the resumé page. This may include additional 
    information that will be gathered, technical information, technical contacts or any other information pertaining to the 
    initial setup.
    """

    support_interview_mode: bool
    """Whether or not this worker supports interview mode."""

    auto_interview: Optional[bool]
    """
    If interview mode is supported, this flag indicates whether or not Humatron should provide auto-interview for this 
    build. In auto-interview mode Humatron will use build's resumé as a LLM context to automatically provide RAG-based 
    answers to interview questions without any communications with the build's implementation. 
    Note that this implementation is technically limited by what information is provided in build settings and its 
    external links.
    """

    interview_concurrent_sessions: Optional[int]
    """
    If interview mode is supported, this is the maximum number of the concurrent interview session supported. 
    This will be automatically enforced by Humatron.
    """

    interview_reqs_per_hour: Optional[int]
    """
    If interview mode is supported, this is the maximum number of questions that can be asked per hour in a single 
    interview session. This will be automatically enforced by Humatron.
    """

    interview_sla: Optional[str]
    """
    Optional description of SLA during the non-auto interview. Should contain any restriction or limitation 
    additionally to interview_reqs_per_hour and interview_concurrent_sessions settings.
    """

    role: str
    """
    Job title or a role of the worker, e.g. 'Sr. Software Engineer' or 'Social Content Manager'. 
    When hired, this will be a default job title.
    """

    overview: str
    """
    Overview or introduction of the worker capabilities, skills and features. 
    If the auto-interview mode is enabled, this is the main part that will be used as a RAG context for LLM answering 
    questions about this build. Text or Markdown with GitHub extensions are supported. 
    NOTE: embedded HTML is not supported.
    """

    share_summary: str
    """Short summary of the build used for sharing on social media."""

    skills_csv: str
    """
    Comma-separated list of this build main code skills. 
    It is shown on resume page and used bu auto-interview function, if enabled.
    """

    deploy_descr: str
    """Public information and necessary details about technical deployment of this build."""

    ai_stack_descr: str
    """Public information and technical details of ML/AI/GenAI stack for this build."""

    country_iso_3166_csv: Optional[str]
    """
    Comma-separated list of ISO 3166 country codes for country locations supported by this build. 
    During hiring, one of these locations will be selected.
    """

    lang_iso_639_csv: Optional[str]
    """
    Comma-separated list of ISO 639 language codes for languages supported by this worker. 
    During hiring, one of the languages will be selected as a primary language.
    """

    is_human_curated: bool
    """Whether or not this build supports human-in-the-loop curation."""

    builder_submit_person: Person
    """Person who originally submitted this build."""

    builder_support_person: Person
    """Official support person for this build. It will be used internally by Humatron only."""

    builder_org: Organization
    """Organization responsible for this build."""

    builder_descr_url: Optional[str]
    """
    Optional URL for the external description or information about this build provided by the builder. 
    If provided and auto-interview is enabled, this will be used as part of the RAG LLM context when answering 
    interview questions.
    """

    support_descr: str
    """Description of the support provided for this builds hired instances. This is a public information."""

    support_email: str
    """Public email that will be used as a support email for this build's hired instances."""

    is_private: bool
    """
    Whether or not this build is private, i.e. available for hire only for the organization that built it. 
    Non-private worker are available for hire to anyone.
    """

    api_endpoint: Optional[str]
    """Worker API endpoint for this build. Until this is set, the build will remain in C{init} status."""

    price_plan: PricePlan
    """Price plan for this build."""

    channels: list[Channel]
    """Specific channels for this specialist."""


class Instance(NamedTuple):
    """
    Represents an instance of a service, tied to a specialist and an organization.
    """

    id: int
    """Unique ID of this instance."""

    specialist: Specialist
    """Worker template (i.e. resume) for this worker instance."""

    org: Organization
    """Organization this worker instance was hired by."""

    status: str
    """
    Status of this instance. 
    Can be one of the following values: C{init}, C{confirmed}, C{preparing}, C{live}, C{paused}, C{terminated}.
    """

    first_name: str
    """First name or technical nickname."""

    last_name: Optional[str]
    """Optional last name."""

    avatar_url: str
    """URL for this instance avatar."""

    gender: str
    """This instance gender. This is used to resolve language grammar only. Supported values are: C{male}, C{female}."""

    age: str
    """
    Assigned age group. This is used for communication style adjustment. Supported values are: C{20-30}, C{30-40}, C{40-50+}.
    """

    country_name: str
    """Name of the country of residence as in ISO 3166."""

    country_iso_3166: str
    """Code of the country of residence as in ISO 3166-2."""

    city: str
    """City of residence. Should align with country and working time zone."""

    tz: str
    """Working time zone. Should align with country and city of residence."""

    primary_lang: str
    """Primary communication language."""

    comm_style: str
    """
    Communication style of this instance. 
    Supported values are: C{informal+}, C{informal}, C{adaptive}, C{formal}, C{formal+.}
    """

    lang_mode: str
    """Language mode of this instance. Supported values are: C{adaptive}, C{plain}."""

    work_type: str
    """Work type assigned to this instance. Supported values are: C{24/7}, C{9-to-5}."""

    workplace_persona: str
    """
    Workplace persona of this instance. 
    Supported values are: C{visionary}, C{networker}, C{builder}, C{mentor}, C{researcher}.
    """

    brevity: str
    """Brevity style of this instance. Supported values are: C{concise}, C{adaptive}, C{verbose}."""

    creativity: Optional[float]
    """Optional creativity level, specified as a number between 0 and 1."""

    job_title: str
    """Assigned job title."""

    job_descr: Optional[str]
    """Job description."""

    team: str
    """Name of team, business unit or organization this instance is part of."""

    pay_type: str
    """Payment type. Supported values: C{hourly}, C{monthly}."""

    hired_by_person: Person
    """Person who hired this worker instance."""

    reporting_to_person: Person
    """Person to whom this worker instance reports."""

    contact_person: Person
    """Employer technical contact person for this worker instance"""

    hire_ts: str
    """Timestamp of the hiring application submission, formatted in ISO-8601."""

    start_date: str
    """Start date timestamp, possible in the future, formatted in ISO-8601."""

    live_ts: Optional[str]
    """Timestamp of when this instance went live for the 1st time, formatted in ISO-8601."""

    termination_ts: Optional[str]
    """Termination timestamp, formatted in ISO-8601."""

    termination_reason: Optional[str]
    """Reason for termination."""


class RequestDataInterview(NamedTuple):
    """
    Represents the data payload for initiating an C{INTERVIEW} request.
    """

    payload_id: str
    """
    Unique ID of this payload object. Note that response payload will reference this ID in its ref_payload_id field.
    """

    ses_id: str
    """Unique ID of the interview session. Every time an new interview starts, it gets assigned a new session ID"""

    person: Person
    """Person conducting the interview."""

    org: Organization
    """Organization of the person conducting the interview."""

    specialist: Specialist
    """
    Specialist being interviewed. Note that there is no worker instance yet as the interview is conducted before hiring.
    """

    ref_resp_payload_id: Optional[str]
    """
    Optional ID of the response payload ID (see payload_id field on response payload). This field is only passed in 
    if kind field is equal to C{good_response} or C{bad_response}. In both case it references ID of the response payload 
    that user marked as "good" or "bad" accordingly in the interview chat window on Humatron website.
    """

    kind: str
    """Type of the interview request: start, stop, message, good_response, bad_response"""

    text: Optional[str]
    """Text of the user request message in interview mode. Only provided if kind field is equal to C{message}."""


class ResponseDataInterview(NamedTuple):
    """
    Represents the data payload for responding to an C{INTERVIEW} request.
    """

    resp_cmd: RequestType
    """Supported value: C{interview}."""

    ses_id: str
    """ID of the interview session as it was passed in the request payload."""

    payload_id: str
    """
    Unique ID of this payload. This ID may be referenced (see ref_resp_payload_id field on request payload) 
    by the future interview requests with kind field equal to either C{good_response} or C{bad_response}
    """

    ref_payload_id: str
    """ID of the interview request payload object this response is responding to."""

    text: Optional[str]
    """
    Interview response message. It is only required if the request's kind field is equal to C{start} or C{message}. 
    Text or Markdown with GitHub extensions are supported. NOTE: embedded HTML is not supported.
    """

    @classmethod
    def make(
        cls,
        ses_id: str,
        payload_id: str,
        ref_payload_id: str,
        text: Optional[str] = None
    ) -> 'ResponseDataInterview':
        """Factory method to create a `ResponseDataInterview` object."""
        return cls(RequestType.INTERVIEW, ses_id, payload_id, ref_payload_id, text)


class RequestDataHeartbeat(NamedTuple):
    """
    Represents the data payload for a C{HEARTBEAT} request to keep the instance active.
    """

    payload_id: str
    """Unique ID of this payload object. Note that some response payload may reference this ID."""

    instance: Instance
    """Current worker instance."""

    contacts: list[Contact]
    """List of contacts available for worker instance."""

    resources: list[Resource]
    """List of resources assigned to worker instance."""


class RequestDataRegister(NamedTuple):
    """
    Represents the data payload for a C{REGISTER} request used to register an instance.
    """

    payload_id: str
    """Unique ID of this payload object. Note that some response payload may reference this ID. """

    instance: Instance
    """Current worker instance."""

    contacts: list[Contact]
    """List of contacts available for worker instance."""

    resources: list[Resource]
    """List of resources assigned to worker instance."""


class ResponseDataRegister(NamedTuple):
    """
    Represents the data payload for the response to a C{REGISTRATION} request.
    """

    resp_cmd: RequestType
    """Supported value: C{register}."""

    instance_id: int
    """Worker instance ID."""

    ref_payload_id: str
    """ID of the register request payload object this response is responding to."""

    result: bool
    """C{true} if successfully registered, C{false} if not."""

    reject_code: Optional[int]
    """Provided if result is false. Supported values are: 
     - C{100} - Undefined reason.
     - C{200} - Legal or contractual reason.
     - C{300} - System or technical reason.
     """

    contacts: Optional[list[Contact]]
    """
    List of contact objects. If provided, these contacts will override all existing instance contacts. 
    Order is not important. Duplicate records will be skipped.
    """

    @classmethod
    def make(
        cls,
        instance_id: int,
        ref_payload_id: str,
        result: bool = True,
        reject_code: Optional[int] = None,
        contacts: Optional[list[Contact]] = None
    ) -> 'ResponseDataRegister':
        """Factory method to create a `ResponseDataRegister` object."""
        return cls(RequestType.REGISTER, instance_id, ref_payload_id, result, reject_code, contacts)


class RequestDataUnregister(NamedTuple):
    """
    Represents the data payload for an C{UNREGISTER} request, used to deregister an instance.
    """

    payload_id: str
    """Unique ID of this payload object. Note that some response payload may reference this ID. """

    instance: Instance
    """Current worker instance."""

    contacts: list[Contact]
    """List of contacts available for worker instance."""

    resources: list[Resource]
    """List of resources assigned to worker instance."""


class ResponseDataUnregister(NamedTuple):
    """
    Represents the data payload for the response to an C{UNREGISTER} request.
    """

    resp_cmd: RequestType
    """Supported value: C{unregister}."""

    instance_id: int
    """Worker Instance ID."""

    ref_payload_id: str
    """ID of the unregister request payload object this response is responding to."""

    contacts: Optional[list[Contact]]
    """
    List of contact objects. If provided, these contacts will override all existing instance contacts. 
    Order is not important. Not unique records will be skipped.
    """

    @classmethod
    def make(
        cls,
        instance_id: int,
        ref_payload_id: str,
        contacts: Optional[list[Contact]] = None
    ) -> 'ResponseDataUnregister':
        """Factory method to create a `ResponseDataUnregister` object."""
        return cls(RequestType.UNREGISTER, instance_id, ref_payload_id, contacts)


class RequestDataPause(NamedTuple):
    """
    Represents the data payload for a C{PAUSE} request, used to pause an instance.
    """

    payload_id: str
    """Unique ID of this payload object. Note that some response payload may reference this ID."""

    instance: Instance
    """Current worker instance."""

    contacts: list[Contact]
    """List of contacts available for worker instance."""

    resources: list[Resource]
    """List of resources assigned to worker instance."""


class ResponseDataPause(NamedTuple):
    """
    Represents the data payload for the response to a C{PAUSE} request.
    """

    resp_cmd: RequestType
    """Supported value: C{pause}."""

    instance_id: int
    """Instance ID."""

    ref_payload_id: str
    """ID of the pause request payload object."""

    result: bool
    """C{true} if successfully paused, C{false} if not."""

    error_code: Optional[int]
    """
    Provided if result is false. Supported values are:
    - C{100} - Undefined reason.
    - C{200} - Legal or contractual reason.
    - C{300} - System or technical reason.
    """

    contacts: Optional[list[Contact]]
    """
    List of contact objects. If provided, these contacts will override all existing instance contacts. 
    Order is not important. Duplicate records will be skipped.
    """

    @classmethod
    def make(
        cls,
        instance_id: int,
        ref_payload_id: str,
        result: bool = True,
        error_code: Optional[int] = None,
        contacts: Optional[list[Contact]] = None
    ) -> 'ResponseDataPause':
        """Factory method to create a `ResponseDataPause` object."""
        return cls(RequestType.PAUSE, instance_id, ref_payload_id, result, error_code, contacts)


class RequestDataResume(NamedTuple):
    """
    Represents the data payload for a C{RESUME} request, used to resume an instance.
    """

    payload_id: str
    """Unique ID of this payload object. Note that some response payload may reference this ID."""

    instance: Instance
    """Current worker instance."""

    contacts: list[Contact]
    """List of contacts available for worker instance."""

    resources: list[Resource]
    """List of resources assigned to worker instance."""


class ResponseDataResume(NamedTuple):
    """
    Represents the data payload for the response to a C{RESUME} request.
    """

    resp_cmd: RequestType
    """Supported value: C{resume}."""

    instance_id: int
    """Instance ID."""

    ref_payload_id: str
    """ID of the resumé request payload object this response is responding to."""

    result: bool
    """C{true} if successfully resumed, C{false} if not."""

    error_code: Optional[int]
    """
    Provided if result is false. Supported values are:
    - C{100} - Undefined reason.
    - C{200} - Legal or contractual reason.
    - C{300} - System or technical reason.
    """

    contacts: Optional[list[Contact]]
    """
    List of contact objects. If provided, these contacts will override all existing instance contacts. 
    Order is not important. Duplicate records will be skipped.
    """

    @classmethod
    def make(
        cls,
        instance_id: int,
        ref_payload_id: str,
        result: bool = True,
        error_code: Optional[int] = None,
        contacts: Optional[list[Contact]] = None
    ) -> 'ResponseDataResume':
        """Factory method to create a `ResponseDataResume` object."""
        return cls(RequestType.RESUME, instance_id, ref_payload_id, result, error_code, contacts)


class RequestMessageSlack(NamedTuple):
    """
    Represents the data payload for a C{slack} C{MESSAGE} request.
    """

    body: Any
    """
    Slack C{message} event body. 
    See more at U{Slack Events API body<https://api.slack.com/apis/connections/events-api>}.
    """

    conversation: Any
    """
    C{channel} property from Slack C{conversations.info} method call result. 
    See more at U{Slack Conversations Request<https://api.slack.com/methods/conversations.info>}.
    """

    conversation_users: list[Any]
    """
    List of C{user} property objects from Slack C{users.info} method call results. 
    See more at U{Slack Users Request<https://api.slack.com/methods/users.info>}. 
    """

    files: Optional[list[File]]
    """Files transferred with the message."""


class RequestMessageEmail(NamedTuple):
    """
    Represents the data payload for an C{email} C{MESSAGE} request.
    """

    sender: str
    """Sender email address."""

    to: str
    """Comma separated list of recipient email addresses."""

    reply_to: Optional[str]
    """Comma separated list of reply-to email addresses."""

    subj: Optional[str]
    """Email subject."""

    cc: Optional[str]
    """Comma separated list of CC email addresses."""

    bcc: Optional[str]
    """Comma separated list of BCC email addresses."""

    html: Optional[str]
    """HTML email content. Has higher priority than plain text content. Either text or html field should be set."""

    text: Optional[str]
    """Plain text email content. Either text or html field should be set."""

    files: Optional[list[File]]
    """List of attached files. Order is not important. Records should be unique, duplicates will be skipped."""


class RequestMessageSms(NamedTuple):
    """
    Represents the data payload for an C{SMS} C{MESSAGE} request.
    """

    sender: str
    """Sender phone number."""

    receiver: str
    """Receiver phone number."""

    text: str
    """Plain text content of the SMS."""


class RequestMessageRest(NamedTuple):
    """
    Represents the data payload for a C{REST} channel C{MESSAGE} request.
    """

    sender: str
    """The sender of the C{REST} channel message."""

    receiver: str
    """The receiver of the C{REST} channel message."""

    text: str
    """The text content of the C{REST} channel message."""


RequestMessage = Union[RequestMessageSlack, RequestMessageEmail, RequestMessageSms, RequestMessageRest]
"""Request message alias."""


class RequestDataMessage(NamedTuple):
    """
    Represents the data payload for sending a C{MESSAGE} request: C{slack}, C{email}, C{SMS} or C{rest}.
    """

    payload_id: str
    """Unique ID of this payload object. Note that some response payload may reference this ID."""

    instance: Instance
    """Current worker instance."""

    contacts: list[Contact]
    """List of contacts available for worker instance."""

    resources: list[Resource]
    """List of resources assigned to worker instance."""

    resource_id: int
    """ID of the resource that delivered this message."""

    message: RequestMessage
    """
    Structure of this object depends on channel_type property of the resource that delivered this message. 
    ID of the resource that delivered this message is in resource_id field. 
    All resources assigned to this worker instance are available in resources field.
    """


class ResponseMessageSlack(NamedTuple):
    """
    Represents the data payload for the response to a C{slack} C{MESSAGE} request.
    """

    channel: str
    """Slack channel ID."""

    text: Optional[str]
    """Slack message text."""

    thread_ts: Optional[str]
    """Slack thread timestamp field. It is used for thread replies."""

    files: Optional[list[File]]
    """List of attached files. Order is not important. Not unique records will be skipped."""

    @classmethod
    def make(
        cls,
        channel: str,
        text: Optional[str] = None,
        thread_ts: Optional[str] = None,
        files: Optional[list[File]] = None
    ) -> 'ResponseMessageSlack':
        """Factory method to create a `ResponseDataSlack` object."""
        if not text and not files:
            raise ValueError('Either text or files must be provided.')
        return cls(channel, text, thread_ts, files)


class ResponseMessageEmail(NamedTuple):
    """
    Represents the data payload for the response to an C{email} C{MESSAGE} request.
    """

    sender: str
    """Sender email address. It is configured resource email."""

    to: str
    """Comma separated list of recipient email addresses."""

    reply_to: Optional[str]
    """Comma separated list of reply-to email addresses."""

    subj: Optional[str]
    """Subject of the email."""

    cc: Optional[str]
    """Comma separated list of CC email addresses."""

    bcc: Optional[str]
    """Comma separated list of BCC email addresses."""

    html: Optional[str]
    """
    HTML email content. Either text or HTML content must be provided. 
    HTML content has higher priority than plain text if both are provided.
    """

    text: Optional[str]
    """Plain text email content. Either text or HTML content must be provided."""

    files: Optional[list[File]]
    """List of attached files. Order is not important. Not unique records will be skipped."""

    @classmethod
    def make(
        cls,
        sender: str,
        to: str,
        reply_to: Optional[str] = None,
        subj: Optional[str] = None,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
        html: Optional[str] = None,
        text: Optional[str] = None,
        files: Optional[list[File]] = None
    ) -> 'ResponseMessageEmail':
        """Factory method to create a `ResponseDataEmail` object."""
        if not text and not html and not files:
            raise ValueError('Either text, html or files must be provided.')
        return cls(sender, to, reply_to, subj, cc, bcc, html, text, files)


class ResponseMessageSms(NamedTuple):
    """
    Represents the data payload for the response to an C{SMS} C{MESSAGE} request.
    """

    sender: str
    """Sender phone number."""

    receiver: str
    """Receiver phone number."""

    text: str
    """Plain text SMS content."""

    @classmethod
    def make(
        cls,
        sender: str,
        receiver: str,
        text: str
    ) -> 'ResponseMessageSms':
        """Factory method to create a `ResponseDataSms` object."""
        return cls(sender, receiver, text)


class ResponseMessageRest(NamedTuple):
    """
    Represents the data payload for the response to a C{REST} channel C{MESSAGE} request.
    """

    sender: str
    """The sender of the C{REST} channel message."""

    receiver: str
    """The receiver of the C{REST} channel message."""

    text: str
    """The text content of the C{REST} channel message."""

    @classmethod
    def make(
        cls,
        sender: str,
        receiver: str,
        text: str
    ) -> 'ResponseMessageRest':
        """Factory method to create a `ResponseDataRest` object."""
        return cls(sender, receiver, text)


ResponseMessage = Union[ResponseMessageSlack, ResponseMessageEmail, ResponseMessageSms, ResponseMessageRest]
"""Response message alias."""


class ResponseDataMessage(NamedTuple):
    """
    Represents the data payload for the response to a C{MESSAGE} request (C{slack}, C{email}, C{SMS} or C{rest}).
    """

    resp_cmd: RequestType
    """Supported value: C{message}."""

    instance_id: int
    """Instance ID."""

    resource_id: int
    """ID of the resource that should be used to deliver the message in this payload."""

    message: ResponseMessage
    """
    Content depends on channel_type field value of the resource object specified in this payload. 
    The resource is provided by its ID in resource_id field.
    """

    ref_payload_id: Optional[str]
    """
    Optional ID of the message request payload object this response is responding to. Note that new messages from worker 
    instance may be unrelated to any previous request payloads, hence this field is optional. This is an essence 
    of autonomous work capabilities when AI worker can communicate with the outside world spontaneously "on its own".
    """

    translate_lang: Optional[str]
    """
    Optional language to translate the message to. Language should be specified as ISO 3166-2 code and 
    be one of the supported by the worker.
    """

    tone_shifting: Optional[str]
    """
    Default value is C{true}. Message will be rewritten according on the overall social and communication preferences 
    for this worker instance. Various social and communication properties are available via instance object. 
    Note that all social and communication preferences in combination play a role in how message will be rewritten. 
    Some of them have a short-term impact, some provide an effect during a long conversation only, and some, 
    like gender, only affect the language grammar.
    """

    contacts: Optional[list[Contact]]
    """
    List of contact objects. If provided, these contacts will override all existing instance contacts. 
    Order is not important. Not unique records will be skipped.
    """

    @classmethod
    def make(
        cls,
        instance_id: int,
        resource_id: int,
        message: ResponseMessage,
        ref_payload_id: Optional[str] = None,
        translate_lang: Optional[str] = None,
        tone_shifting: Optional[str] = None,
        contacts: Optional[list[Contact]] = None
    ) -> 'ResponseDataMessage':
        """Factory method to create a `ResponseDataMessage` object."""
        return cls(
            RequestType.MESSAGE, instance_id, resource_id, message, ref_payload_id, translate_lang, tone_shifting,
            contacts
        )


RequestPayloadPartBody = Union[
    RequestDataInterview,
    RequestDataHeartbeat,
    RequestDataRegister,
    RequestDataUnregister,
    RequestDataPause,
    RequestDataResume,
    RequestDataMessage
]
"""Request payload part body type alias."""

ResponsePayloadPartBody = Union[
    ResponseDataInterview,
    ResponseDataRegister,
    ResponseDataUnregister,
    ResponseDataPause,
    ResponseDataResume,
    ResponseDataMessage
]
"""Response payload part body type alias."""

Storage = dict[Any, Any]
"""Storage type alias."""


class Request(NamedTuple):
    """
    Represents a Humatron worker request.
    """

    req_cmd: RequestType
    """The command associated with the request."""
    req_id: str
    """The unique identifier for the request."""
    req_tstamp: str
    """The timestamp when the request was created in ISO format."""
    payload: list[RequestPayloadPartBody]
    """A list of payload parts containing the data for the request."""
    storage: Optional[Storage]
    """
    C{storage} used to maintain state during requests processing. 
    It remains empty for requests of type C{INTERVIEW}.
    """

    @classmethod
    def from_json(cls, js: str, skip_unknown_fields: bool = True) -> 'Request':
        """
        Creates a Request instance from a JSON string.

        @param js :
            The JSON string representing the request.
        @param skip_unknown_fields :
            A flag that determines whether unknown fields should be skipped or trigger an error.

        @return:
            A new Request instance.

        @raise ValueError:
            Raised if expected fields are missing or contain invalid values,
            or if unknown fields are present and  C{skip_unknown_fields} is set to C{True}.
        """
        return cls.from_dict(json.loads(js), skip_unknown_fields)

    @classmethod
    def from_dict(cls, d: dict[Any, Any], skip_unknown_fields: bool = True) -> 'Request':
        """
        Creates a Request instance from a dictionary.

        @param d :
            A dictionary containing the request data.
        @param skip_unknown_fields :
            A flag that determines whether unknown fields should be skipped or trigger an error.

        @return:
            A new Request instance.

        @raise ValueError:
            Raised if expected fields are missing or contain invalid values,
            or if unknown fields are present and  C{skip_unknown_fields} is set to C{True}.
        """
        return _deserialize_request(d, skip_unknown_fields)


class Response(NamedTuple):
    """
    Represents a Humatron worker response.
    """

    resp_id: str
    """The unique identifier for the response."""
    resp_tstamp: str
    """The timestamp when the response was created in ISO format."""
    payload: Optional[list[ResponsePayloadPartBody]]
    """An optional list of payload parts containing the response data."""
    storage: Optional[Storage]
    """Optional storage for maintaining state during response processing."""

    def to_json(self) -> str:
        """
        Converts the Response instance to a JSON string.

        @return:
            A JSON string representing the Response instance.
        """
        return json.dumps(self.to_dict())

    def to_dict(self) -> dict[Any, Any]:
        """
        Converts the Response instance to a dictionary.

        @return:
            A dictionary representing the Response instance.
        """
        return _serialize(self)


class RequestPayloadPart(NamedTuple):
    """
    Represents a part of the request payload.
    """

    req_cmd: RequestType
    """The command associated with the payload part."""
    req_id: str
    """The unique identifier for the request."""
    req_tstamp: str
    """The timestamp of the request."""
    body: RequestPayloadPartBody
    """An object representing a part body of the request payload."""


ResponsePayloadPart = Union[list[ResponsePayloadPartBody], ResponsePayloadPartBody, None]
"""Response payload part alias."""

_logger = logging.getLogger('humatron.worker.sdk.beans')


def _serialize(obj: Any) -> Any:
    from datetime import datetime, date, time
    import collections

    if obj is None:
        return None

    def recurse(x):
        return map(_serialize, x)

    def obj_is(x):
        return isinstance(obj, x)

    # namedtuple
    if obj_is(tuple) and hasattr(obj, '_fields'):
        # noinspection PyProtectedMember
        d = dict(zip(obj._fields, recurse(obj)))
        return {k: v for k, v in d.items() if v is not None}
    elif obj_is(collections.abc.Mapping):
        return type(obj)(zip(obj.keys(), recurse(obj.values())))
    elif obj_is(collections.abc.Iterable) and not obj_is(str):
        return type(obj)(recurse(obj))
    elif obj_is(datetime) or obj_is(date) or obj_is(time):
        return str(obj)
    elif obj_is(StrEnum):
        return str(obj)

    return obj


def _deserialize_request(src: Any, skip_unknown_fields: bool) -> Request:
    _check_keys('request', src, skip_unknown_fields, {'req_cmd', 'req_id', 'req_tstamp', 'payload', 'storage'})

    req_cmd = _extract_enum_opt(RequestType, src['req_cmd'], skip_unknown_fields)

    return Request(
        req_cmd=req_cmd,
        req_id=src['req_id'],
        req_tstamp=src['req_tstamp'],
        payload=[
            pp for pp in
            [_deserialize_payload_part(p, req_cmd, skip_unknown_fields) for p in _opt_dflt(src, 'payload', [])]
            if pp
        ],
        storage=src['storage'] if 'storage' in src else None
    ) if req_cmd else None


def _deserialize_payload_part(src: Any, req_cmd: RequestType, skip_unknown_fields: bool) -> RequestPayloadPartBody:
    match req_cmd:
        case RequestType.INTERVIEW:
            _check_keys(
                'interview_data',
                src,
                skip_unknown_fields,
                {'payload_id', 'ses_id', 'person', 'org', 'specialist', 'ref_resp_payload_id', 'kind', 'text'}
            )
            return _deserialize_tuple(RequestDataInterview, src, skip_unknown_fields)
        case RequestType.REGISTER:
            _check_keys('register_data', src, skip_unknown_fields, {'payload_id', 'instance', 'contacts', 'resources'})
            return _deserialize_tuple(RequestDataRegister, src, skip_unknown_fields)
        case RequestType.UNREGISTER:
            _check_keys(
                'unregister_data', src, skip_unknown_fields, {'payload_id', 'instance', 'contacts', 'resources'}
            )
            return _deserialize_tuple(RequestDataUnregister, src, skip_unknown_fields)
        case RequestType.PAUSE:
            _check_keys('pause_data', src, skip_unknown_fields, {'payload_id', 'instance', 'contacts', 'resources'})
            return _deserialize_tuple(RequestDataPause, src, skip_unknown_fields)
        case RequestType.RESUME:
            _check_keys('resume_data', src, skip_unknown_fields, {'payload_id', 'instance', 'contacts', 'resources'})
            return _deserialize_tuple(RequestDataResume, src, skip_unknown_fields)
        case RequestType.MESSAGE:
            _check_keys(
                'message_data', src, skip_unknown_fields,
                {'payload_id', 'instance', 'contacts', 'resources', 'resource_id', 'message'}
            )
            resources = _deserialize_list(Resource, _opt_dflt(src, 'resources', []), skip_unknown_fields, [])
            resource_id = src['resource_id']
            rs = list(filter(lambda r: r.id == resource_id, resources))
            if len(rs) != 1:
                raise ValueError(f'Resource not found: {resource_id}')
            channel_type = _extract_enum_opt(ChannelType, rs[0].channel_type, skip_unknown_fields)
            return RequestDataMessage(
                payload_id=src['payload_id'],
                instance=_deserialize_tuple(Instance, src['instance'], skip_unknown_fields),
                contacts=_deserialize_list(Contact, _opt_dflt(src, 'contacts', []), skip_unknown_fields, []),
                resources=resources,
                resource_id=resource_id,
                message=_deserialize_message(src['message'], channel_type, skip_unknown_fields)
            ) if channel_type else None
        case RequestType.HEARTBEAT:
            _check_keys('heartbeat_data', src, skip_unknown_fields, {'payload_id', 'instance', 'contacts', 'resources'})
            return _deserialize_tuple(RequestDataHeartbeat, src, skip_unknown_fields)
        case _:
            raise ValueError(f'Unknown request type: {req_cmd}')


def _deserialize_message(src: Any, channel_type: ChannelType, skip_unknown_fields: bool) -> RequestMessage:
    match channel_type:
        case ChannelType.EMAIL:
            _check_keys(
                'email_message_data',
                src, skip_unknown_fields,
                {'sender', 'to', 'reply_to', 'subj', 'cc', 'bcc', 'html', 'text', 'files'}
            )
            return _deserialize_tuple(RequestMessageEmail, src, skip_unknown_fields)
        case ChannelType.SLACK:
            _check_keys(
                'slack_message_data', src, skip_unknown_fields, {'body', 'conversation', 'conversation_users', 'files'}
            )
            return _deserialize_tuple(RequestMessageSlack, src, skip_unknown_fields)
        case ChannelType.SMS:
            _check_keys('sms_message_data', src, skip_unknown_fields, {'sender', 'receiver', 'text'})
            return _deserialize_tuple(RequestMessageSms, src, skip_unknown_fields)
        case ChannelType.REST:
            _check_keys('rest_message_data', src, skip_unknown_fields, {'sender', 'receiver', 'text'})
            return _deserialize_tuple(RequestMessageRest, src, skip_unknown_fields)
        case _:
            raise ValueError(f'Unknown channel type: {channel_type}')


def _deserialize_tuple(factory: Any, src: Any, skip_unknown_fields: bool) -> Any:
    if src is None:
        return None

    if not hasattr(factory, '_fields'):
        if factory == Any:
            return src
        try:
            return factory(src)
        except ValueError as e:
            if skip_unknown_fields and issubclass(factory, StrEnum):
                return None
            raise e

    arg = {}

    for name, claxx in factory.__annotations__.items():
        val = src[name] if name in src else None

        if claxx.__name__ == Optional.__name__:
            claxx = claxx.__args__[0]

        if val is not None:
            if hasattr(claxx, '__annotations__'):
                v = _deserialize_tuple(claxx, val, skip_unknown_fields)
            elif isinstance(val, list):
                v = [_deserialize_tuple(claxx.__args__[0], v, skip_unknown_fields) for v in val]
            else:
                v = val
        else:
            v = None
        arg[name] = v

    _check_keys(f'tuple_{factory}', src, skip_unknown_fields, {k for k in arg.keys()})

    return factory(**arg)


def _deserialize_list(factory_obj: Any, src: Any, skip_unknown_fields: bool, dflt: list[Any]) -> list[Any]:
    return [_deserialize_tuple(factory_obj, v, skip_unknown_fields) for v in src] if src is not None else dflt


def _opt_dflt(src: Any, key: str, dflt: Any) -> Any:
    return src[key] if key in src else dflt


def _extract_enum_opt(factory: Any, src: Any, skip_unknown_fields: bool) -> Optional[Any]:
    try:
        return factory(src)
    except ValueError as e:
        if skip_unknown_fields:
            _logger.warning(f'Unknown enum value [factory={factory}, src={src}]')
            return None
        raise e


def _check_keys(name: str, src: Any, skip_unknown_fields: bool, expected: set[str]) -> None:
    if (
        (not skip_unknown_fields or _logger.isEnabledFor(logging.WARNING)) and
        src and
        hasattr(src, 'keys') and
        callable(src.keys) and
        not set(src.keys()).issubset(expected)
    ):
        err = f"Unknown keys [name={name}, src={src}, unexpected-keys={','.join(set(src.keys()) - expected)}]"
        if not skip_unknown_fields:
            raise ValueError(err)
        _logger.warning(err)
