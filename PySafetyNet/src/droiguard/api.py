from os import makedirs
from hashlib import md5
from typing import Union
from zipfile import ZipFile
from src.droiguard.utils.customproto import CustomProto
from src.droiguard.vm import VirtualMachine
from requests import Session


class AntiAbuseApi(CustomProto, VirtualMachine):

    droidguard_session: Session
    antiabuse_api = "www.googleapis.com/androidantiabuse/v1/x/create?"
    google_static_api = "www.gstatic.com/droidguard"
    key = "AIzaSyBofcZsgLSS7BOnBjZPEkk4rYwzOIz-lTI"
    alt = "PROTO"
    url: str
    payload: bytes
    response: bytes
    save_bytecode: bool = True
    save_vm: bool = True
    vm_extract: bool = True
    vm_apk_path: str
    verify: bool = True
    cert_path = "./chls.pem"

    def __init__(self):
        super().__init__()
        self.droidguard_session = Session()
        self.set_headers()
        if self.verify:
            self.droidguard_session.verify = "./"

    def request_droidguard_vm(self, data: bytes):
        self.url = self.antiabuse_api + f'alt={self.alt}&key={self.key}'
        self.payload = data
        self.payload = open("./request", "rb").read()

        self.send_request()

    def download_droidguard_vm(self):
        self.url = self.google_static_api + f'/{self.vm_checksum}'
        """if self.vm_url and self.vm_url != self.url:
            ..."""
        self.reset_headers()
        with self.droidguard_session.get(
                f"https://{self.url}",
                verify=True if not self.verify else self.cert_path
        ) as r:
            self.the_apk_folder = f"./vm_{self.vm_checksum}"
            self.vm_apk_path = f"{self.the_apk_folder}/vm"
            makedirs(self.vm_apk_path, exist_ok=True)
            if self.save_vm and r.status_code == 200:
                self.the_apk = f"{self.the_apk_folder}/{self.vm_checksum}.apk"
                open(self.the_apk, "wb").write(r.content)
                if self.vm_extract:
                    self.extract_vm()

            if self.save_bytecode:
                open(f"{self.the_apk_folder}/{md5(self.bytecode).hexdigest()}.bytecode", "wb").write(self.bytecode)

    def extract_vm(self):
        with ZipFile(self.the_apk, "r") as zp:
            zp.extractall(self.vm_apk_path)

    def send_request(self):
        with self.droidguard_session.post(
                f"https://{self.url}", data=self.payload,
                verify=True if not self.verify else self.cert_path
        ) as r:
            self.response = r.content
            self.handle_response()

    def handle_response(self):
        print(self.response == open("./response", "rb").read())

    def set_headers(self):
        self.droidguard_session.headers = {
            "Content-Type": "application/x-protobuf",
            "User-Agent": "DroidGuard/213314000",
            "Host": "www.googleapis.com",
            "Accept-Encoding": "gzip"
        }

    def reset_headers(self):
        self.droidguard_session.headers = {
            "accept-encoding": "gzip, deflate, br, zstd",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }



