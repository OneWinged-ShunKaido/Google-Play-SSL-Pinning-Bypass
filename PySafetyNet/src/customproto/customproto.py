


class VmInfo:
    vm_url: bytes

    def __init__(self):
        super().__init__()

    def to_dict(self) -> dict:
        return {
            'vm_url': self.vm_url
        }

















class CustomProto:
    android_check_response: AndroidCheckResponse
    AttestRequest: AttestRequest
    JWT: JWT
    safetynet_data: SafetyNetData
    droidguard_result: DroidGuardResult
    display_attest_request_data: bool = False
    display_jwt: bool = False

    def __init__(self):
        self.AttestRequest = AttestRequest()
        self.JWT = JWT()
        self.android_check_response = AndroidCheckResponse()
        super().__init__()

    def get_android_check_request(self, android_check_request: bytes):
        self.decode_android_check_request(android_check_request)

    def get_android_check_response(self, android_check_response: bytes) -> 'AndroidCheckResponse':
        self.decode_android_check_response(android_check_response)
        return self.android_check_response

    def get_attestation_request_data(self, attest_request: bytes) -> 'AttestRequest':
        self.decode_attest_request(attest_request)
        return self.AttestRequest

    def get_attestation_response_data(self, attest_response) -> 'JWT':
        return self.get_jwt(attest_response)

    def decode_android_check_request(self, binary_data: bytes):
        ...

    def decode_android_check_response(self, binary_data: bytes):
        android_check_response = androidcheck_pb2.AndroidCheckResponse()
        android_check_response.ParseFromString(binary_data)

        if android_check_response.HasField('payload'):
            payload_proto = android_check_response.payload
            self.android_check_response.payload = PayloadData()
            self.android_check_response.payload.bytecode = payload_proto.bytecode
            self.android_check_response.payload.vmChecksum = payload_proto.vmChecksum
            self.android_check_response.payload.expiry_time_secs = payload_proto.expiryTimeSecs
            self.android_check_response.payload.signature = payload_proto.signature
            self.android_check_response.payload.vmUrl = payload_proto.vmUrl

        self.android_check_response.unknown_field = android_check_response.unknownField



    def decode_attest_request(self, binary_data: bytes):
        """
        Parse the binary data into an AttestRequest object and extract fields.

        Args:
            binary_data (bytes): The binary data representing an AttestRequest.
        """
        # Parse the binary data into an AttestRequest object
        attest_request = safetynet_pb2.AttestRequest()
        attest_request.ParseFromString(binary_data)

        # Decode the SafetyNetData if it exists
        if attest_request.HasField('safetyNetData'):
            # Convert the bytes to the SafetyNetData Protobuf message
            safety_net_data_proto = safetynet_pb2.SafetyNetData()
            safety_net_data_proto.ParseFromString(attest_request.safetyNetData)

            self.safetynet_data = SafetyNetData()

            self.safetynet_data.nonce = safety_net_data_proto.nonce
            self.safetynet_data.package_name = safety_net_data_proto.packageName
            self.safetynet_data.signature_digest = list(safety_net_data_proto.signatureDigest)
            self.safetynet_data.file_digest = safety_net_data_proto.fileDigest
            self.safetynet_data.gms_version_code = safety_net_data_proto.gmsVersionCode
            self.safetynet_data.current_time_ms = safety_net_data_proto.currentTimeMs
            self.safetynet_data.google_cn = safety_net_data_proto.googleCn

            if safety_net_data_proto.HasField('seLinuxState'):
                se_linux_state_proto = safety_net_data_proto.seLinuxState
                self.safetynet_data.se_linux_state = SELinuxState()
                self.safetynet_data.se_linux_state.supported = se_linux_state_proto.supported
                self.safetynet_data.se_linux_state.enabled = se_linux_state_proto.enabled

            self.safetynet_data.su_candidates = []
            for file_state_proto in safety_net_data_proto.suCandidates:
                file_state = FileState()
                file_state.file_name = file_state_proto.fileName
                file_state.digest = file_state_proto.digest
                self.safetynet_data.su_candidates.append(file_state)

            self.AttestRequest.SafetyNetData = self.safetynet_data

        if attest_request.HasField('droidGuardResult'):
            self.droidguard_result = DroidGuardResult()
            self.droidguard_result.result = attest_request.droidGuardResult
            self.AttestRequest.DroidGuardResult = self.droidguard_result

        if self.display_attest_request_data:
            self.display_sn_attest_data()

    def get_jwt(self, gms_core_response: bytes) -> 'JWT':
        self.decode_attest_response(gms_core_response)
        return self.JWT

    def decode_attest_response(self, binary_data: bytes):
        """
        Parse the binary data into an AttestResponse object and extract fields.

        Args:
            binary_data (bytes): The binary data representing an AttestResponse.
        """
        # Parse the binary data into an AttestResponse object
        attest_response = safetynet_pb2.AttestResponse()
        attest_response.ParseFromString(binary_data)

        # Decode the AttestResponse if it exists
        if attest_response.HasField('result'):
            self.JWT.jwt_token = attest_response.result

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
        print(f"\nJWT:\n {self.JWT.jwt_token}")




