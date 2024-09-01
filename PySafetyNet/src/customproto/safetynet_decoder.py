from src.safetynet.proto import safetynet_pb2, antiabuse_pb2
from src.safetynet.antiabuse.models import PayloadData, AntiAbuseResponse
from src.safetynet.androidcheck.models import AttestRequest, SafetyNetData, AttestResponse, DroidGuardResult, \
    SELinuxState, FileState


class SafetyNetDecoder:
    anti_abuse_response: AntiAbuseResponse
    payload_data: PayloadData
    safetynet_data: SafetyNetData
    droidguard_result: DroidGuardResult

    def __init__(self):
        self.message = b''
        self.state = {}
        self.safetynet_action = ["anti_abuse", "android_check"]
        self.attest_request: AttestRequest = AttestRequest()
        self.attest_response: AttestResponse = AttestResponse()
        self.display_attest_request_data = False
        self.display_jwt = False

    def perform_sn_action(self):
        content_type = self.state.get("r_type")
        content = self.state.get("content")
        action = self.state.get("action")

        if action == "anti_abuse":
            if content_type == "request":
                # self.decode_anti_abuse_request(content)
                pass
            elif content_type == "response":
                self.decode_anti_abuse_response(content)

        elif action == "android_check":
            if content_type == "request":
                self.decode_android_check_request(content)
                print(self.get_attest_request())

            elif content_type == "response":
                self.decode_android_check_response(content)

    def decode_anti_abuse_request(self, message: bytes):
        #   Not Implement yet too boring
        ...

    def decode_anti_abuse_response(self, message: bytes):
        response = antiabuse_pb2.AntiAbuseResponse()
        response.ParseFromString(message)

        # Map ProtoBuf AntiAbuseResponse to internal model
        if response.HasField('payload'):
            payload = response.payload
            self.payload_data = PayloadData(
                bytecode=payload.bytecode,
                vm_url=payload.vmUrl,  # Assuming vmUrl is a string; adjust if needed
                vm_checksum=payload.vmChecksum,
                expiry_time_secs=payload.expiryTimeSecs,
                signature=payload.signature
            )

        self.anti_abuse_response = AntiAbuseResponse(
            payload=self.payload_data if response.HasField('payload') else None,
            unknown_field=response.unknownField  # Handle unknown fields as bytes
        )

    def decode_android_check_request(self, message: bytes):
        request = safetynet_pb2.AttestRequest()
        request.ParseFromString(message)

        # Decode SafetyNetData if it exists
        if request.HasField('safetyNetData'):
            safety_net_data_proto = safetynet_pb2.SafetyNetData()
            safety_net_data_proto.ParseFromString(request.safetyNetData)

            self.safetynet_data = SafetyNetData(
                nonce=safety_net_data_proto.nonce,
                package_name=safety_net_data_proto.packageName,
                signature_digest=list(safety_net_data_proto.signatureDigest),
                file_digest=safety_net_data_proto.fileDigest,
                gms_version_code=safety_net_data_proto.gmsVersionCode,
                current_time_ms=safety_net_data_proto.currentTimeMs,
                google_cn=safety_net_data_proto.googleCn,
                se_linux_state=SELinuxState(
                    supported=safety_net_data_proto.seLinuxState.supported if safety_net_data_proto.HasField(
                        'seLinuxState') else None,
                    enabled=safety_net_data_proto.seLinuxState.enabled if safety_net_data_proto.HasField(
                        'seLinuxState') else None
                ) if safety_net_data_proto.HasField('seLinuxState') else None,
                su_candidates=[
                    FileState(file_name=file_state_proto.fileName, digest=file_state_proto.digest)
                    for file_state_proto in safety_net_data_proto.suCandidates
                ]
            )

        # Decode DroidGuardResult if it exists
        if request.HasField('droidGuardResult'):
            self.droidguard_result = DroidGuardResult(result=request.droidGuardResult)

        # Update the attest_request
        self.attest_request = AttestRequest(
            safety_net_data=self.safetynet_data,
            droid_guard_result=self.droidguard_result
        )

        # Optionally display the data if required
        if self.display_attest_request_data:
            self.display_sn_attest_data()

    def decode_android_check_response(self, message: bytes):
        response = safetynet_pb2.AttestResponse()
        response.ParseFromString(message)

        # Decode the result field
        self.attest_response = AttestResponse(jwt_token=response.result)

        # Optionally display the result if required
        if self.display_jwt:
            self.display_jwt_token()

    def display_sn_attest_data(self):
        print("SafetyNetData:")
        print(f"  Nonce: {self.safetynet_data.nonce}")
        print(f"  PackageName: {self.safetynet_data.package_name}")
        print(f"  SignatureDigest: {self.safetynet_data.signature_digest}")
        print(f"  FileDigest: {self.safetynet_data.file_digest}")
        print(f"  GMS Version Code: {self.safetynet_data.gms_version_code}")
        print(f"  CurrentTimeMs: {self.safetynet_data.current_time_ms}")
        print(f"  Google CN: {self.safetynet_data.google_cn}")

        if self.safetynet_data.se_linux_state:
            print("  SELinuxState:")
            print(f"    Supported: {self.safetynet_data.se_linux_state.supported}")
            print(f"    Enabled: {self.safetynet_data.se_linux_state.enabled}")

        for file_state in self.safetynet_data.su_candidates:
            print("  FileState:")
            print(f"    FileName: {file_state.file_name}")
            print(f"    Digest: {file_state.digest}")

        if self.droidguard_result:
            print(f"DroidGuardResult: {self.droidguard_result.result}")

    def display_jwt_token(self):
        print(f"\nJWT:\n {self.attest_response.jwt_token}")

    def get_payload_data(self) -> PayloadData:
        return self.payload_data

    def get_anti_abuse_response(self) -> AntiAbuseResponse:
        return self.anti_abuse_response

    def get_attest_request(self) -> AttestRequest:
        return self.attest_request

    def get_attest_response(self) -> AttestResponse:
        return self.attest_response

    def get_safetynet_data(self) -> SafetyNetData:
        return self.safetynet_data

    def get_droidguard_result(self) -> DroidGuardResult:
        return self.droidguard_result
