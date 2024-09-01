from os.path import isfile


class DroidGuardUtils:
    save_bytecode: bool = True
    save_vm: bool = True
    default_sn_bytecode_path: str = ""
    default_vm_apk_path: str = ""

    def __init__(self):
        super().__init__()

    def compare_vm(self):
        if not isfile(self.default_sn_bytecode_path):
            return False

    def save_safetynet_bytecode_to(self, vm_bytecode: bytes, path: str):
        self.save_safetynet_bytecode_to(vm_bytecode, path)

    def save_safetynet_bytecode(self, vm_bytecode: bytes, to: str = None):
        fn = self.default_sn_bytecode_path if not to else to
        open(fn, "wb").write(vm_bytecode)

    def save_vm_apk_to(self, apk_content: bytes, fn):
        self.save_vm_apk(apk_content, fn)

    def save_vm_apk(self, apk_content: bytes, to: str = None):
        fn = self.default_sn_bytecode_path if not to else to
        open(fn, "wb").write(apk_content)
