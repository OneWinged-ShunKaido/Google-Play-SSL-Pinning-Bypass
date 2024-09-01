from os import makedirs
from src.droiguard.api import AntiAbuseApi


class DroidGuard(AntiAbuseApi):

    def __init__(self):
        super().__init__()

    def generate_attestation(self, antiabuse_content: bytes):
        self.request_droidguard_vm(antiabuse_content)

    def download_vm(self, vm_checksum: str = None):
        if vm_checksum:
            self.vm_checksum = vm_checksum

        self.download_droidguard_vm()


