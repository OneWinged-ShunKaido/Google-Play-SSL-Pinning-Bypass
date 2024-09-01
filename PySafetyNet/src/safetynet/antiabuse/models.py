class VmInfo:
    def __init__(self, vm_url: bytes = b''):
        self.vm_url = vm_url

    def to_dict(self) -> dict:
        return {
            'vm_url': self.vm_url
        }


class PayloadData:
    def __init__(self, bytecode: bytes = b'', vm_url: str = '', vm_checksum: bytes = b'',
                 expiry_time_secs: int = 0, signature: bytes = b'', vm_info: bytes = None):
        self.bytecode = bytecode
        self.vm_url = vm_url
        self.vm_info = vm_info if vm_info else VmInfo()  # Initialize VmInfo if not provided
        self.vm_checksum = self.process_string(vm_checksum, False)
        self.expiry_time_secs = expiry_time_secs
        self.signature = signature

    def to_dict(self) -> dict:
        return {
            'bytecode': self.bytecode,
            'vm_url': self.vm_url,
            'vm_checksum': self.vm_checksum,
            'expiry_time_secs': self.expiry_time_secs,
            'signature': self.signature,
        }

    @staticmethod
    def process_string(byte_array: bytes, exclude_trailing_zero: bool) -> str:
        hex_chars = '0123456789ABCDEF'
        result = []

        for i, byte in enumerate(byte_array):
            if not exclude_trailing_zero or (i != len(byte_array) - 1 or byte != 0):
                result.append(hex_chars[byte >> 4])
                result.append(hex_chars[byte & 0x0F])

        return ''.join(result)


class AntiAbuseResponse:
    def __init__(self, payload: PayloadData = None, unknown_field: bytes = b''):
        self.payload = payload if payload else PayloadData()  # Initialize PayloadData if not provided
        self.unknown_field = unknown_field

    def to_dict(self) -> dict:
        return {
            'payload': self.payload.to_dict() if self.payload else None,
            'unknown_field': self.unknown_field
        }

