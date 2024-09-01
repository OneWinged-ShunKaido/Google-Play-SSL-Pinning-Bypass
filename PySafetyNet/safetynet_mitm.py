#   mitmdump --listen-port 9998 -s safetynet_mitm.py -q

import logging
from colorama import Fore, Style, init
from src.protodecoder import ProtoDecoder
from mitmproxy import http

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()


class SafetyNetBypass(ProtoDecoder):
    safetynet_host = "www.googleapis.com"
    play_integrity_host = ""
    android_check_api = "androidcheck/v1/attestations"
    anti_abuse_api = "androidantiabuse/v1/x"
    integrity_api = ""
    action_allowed_hosts = [safetynet_host, play_integrity_host]

    def __init__(self):
        super().__init__()

    def request(self, flow: http.HTTPFlow) -> None:
        req = flow.request
        if req.host not in self.action_allowed_hosts:
            return

        self.state = self.check_request_state(request=req, r_type="request", response=flow.response)
        self._on_state()

    def response(self, flow: http.HTTPFlow) -> None:
        req = flow.request
        if req.host not in self.action_allowed_hosts:
            return

        self.state = self.check_request_state(request=req, r_type="response", response=flow.response)
        self._on_state()

    def check_request_state(self, request: http.HTTPRequest, r_type: str = "request",
                            response: http.HTTPResponse = None) -> dict:
        """Check and return the request state, including device user-agent and action type."""
        user_agent = request.headers.get("user-agent", "")
        action = None
        if request.host == self.safetynet_host:

            if self.android_check_api in request.path:
                #   [SN] -> DroidGuard Result request
                action = "android_check"

            elif self.anti_abuse_api in request.path:
                #   [SN/PI?] -> VM & bytecode download
                action = "anti_abuse"

        elif request.host == self.play_integrity_host:
            #   [PI] -> DroidGuard Result request
            if self.integrity_api in request:
                action = "integrity"

        content = response.content if response else request.content

        return dict(user_agent=user_agent, action=action, r_type=r_type, content=content)

    """def _on_message(self, message: bytes, message_state: dict = None):
        if not message_state:
            return False"""


addons = [SafetyNetBypass()]
