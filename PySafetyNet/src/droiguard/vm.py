class VirtualMachine:
    vm_url: str
    vm_checksum: str
    bytecode: bytes = b''
    expiryTimeSecs: int
    the_apk_folder: str
    the_apk: str
    vm_lib_path: str

    def __init__(self):
        ...

    def read_vm_path(self) -> str:
        open(f"./{self}")
        return ''

