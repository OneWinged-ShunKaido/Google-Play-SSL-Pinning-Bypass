from typing import List, Optional


class SELinuxState:
    def __init__(self, supported: bool = False, enabled: bool = False):
        self.supported = supported
        self.enabled = enabled

    def to_dict(self) -> dict:
        return {
            'supported': self.supported,
            'enabled': self.enabled
        }


class FileState:
    def __init__(self, file_name: str = '', digest: bytes = b''):
        self.file_name = file_name
        self.digest = digest

    def to_dict(self) -> dict:
        return {
            'file_name': self.file_name,
            'digest': self.digest
        }


class SafetyNetData:
    def __init__(
        self,
        nonce: bytes = b'',
        package_name: str = '',
        signature_digest: Optional[List[bytes]] = None,
        file_digest: bytes = b'',
        gms_version_code: int = 0,
        current_time_ms: int = 0,
        google_cn: bool = False,
        se_linux_state: Optional[SELinuxState] = None,
        su_candidates: Optional[List[FileState]] = None
    ):
        self.nonce = nonce
        self.package_name = package_name
        self.signature_digest = signature_digest if signature_digest is not None else []
        self.file_digest = file_digest
        self.gms_version_code = gms_version_code
        self.current_time_ms = current_time_ms
        self.google_cn = google_cn
        self.se_linux_state = se_linux_state
        self.su_candidates = su_candidates if su_candidates is not None else []

    def to_dict(self) -> dict:
        return {
            'nonce': self.nonce,
            'package_name': self.package_name,
            'signature_digest': list(self.signature_digest),
            'file_digest': self.file_digest,
            'gms_version_code': self.gms_version_code,
            'current_time_ms': self.current_time_ms,
            'google_cn': self.google_cn,
            'se_linux_state': self.se_linux_state.to_dict() if self.se_linux_state else None,
            'su_candidates': [file_state.to_dict() for file_state in self.su_candidates]
        }


class DroidGuardResult:
    def __init__(self, result: str = ''):
        self.result = result
        self.max_length = 50

    def __str__(self):
        if len(self.result) > self.max_length:
            # Truncate the string and add ellipsis
            return f"{self.result[:self.max_length]}..."
        else:
            return self.result

    def to_dict(self) -> dict:
        return {
            'result': self.result if self.result is not None else ''
        }


class AttestRequest:
    SafetyNetData: Optional[SafetyNetData]
    DroidGuardResult: Optional[DroidGuardResult]

    def __init__(self, safety_net_data: Optional[SafetyNetData] = None,
                 droid_guard_result: Optional[DroidGuardResult] = None):
        """
        Initialize an AttestRequest instance.

        Args:
            safety_net_data (Optional[SafetyNetData]): An instance of SafetyNetData.
            droid_guard_result (Optional[DroidGuardResult]): An instance of DroidGuardResult.
        """
        self.SafetyNetData = safety_net_data
        self.DroidGuardResult = droid_guard_result

    def __str__(self) -> str:
        """
        Return a string representation of the AttestRequest instance.

        Returns:
            str: A string representation of the AttestRequest instance.
        """
        sn_data_str = str(self.SafetyNetData) if self.SafetyNetData else 'None'
        dg_result_str = str(self.DroidGuardResult) if self.DroidGuardResult else 'None'
        return f"AttestRequest(SafetyNetData={sn_data_str}, DroidGuardResult={dg_result_str})"

    def to_dict(self) -> dict:
        """
        Convert the AttestRequest instance to a dictionary.

        Returns:
            dict: A dictionary representation of the AttestRequest instance.
        """
        return dict(
            safetyNetData=self.SafetyNetData.to_dict() if self.SafetyNetData else None,
            droidGuardResult=self.DroidGuardResult.to_dict() if self.DroidGuardResult else None
        )


class AttestResponse:
    """
    message AttestResponse {
        optional string result = 2;
    }
    """
    jwt_token: str
    max_length: int = 50

    def __init__(self, jwt_token: str = ''):
        self.jwt_token = jwt_token

    def __str__(self) -> str:
        jwt_token_display = f"{self.jwt_token[:self.max_length]}..." \
            if len(self.jwt_token) > self.max_length else self.jwt_token
        return f"JWT(jwt_token={jwt_token_display})"

    def to_dict(self) -> dict:
        return {'jwt': self.jwt_token}
