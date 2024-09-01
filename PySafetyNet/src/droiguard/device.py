import struct


class CodedObject:
    def serialize(self):
        raise NotImplementedError

    @classmethod
    def deserialize(cls, stream):
        raise NotImplementedError


class CommandAndPackageNameObject(CodedObject):
    def __init__(self, command=None, package_name=None):
        self.command = command
        self.package_name = package_name

    def serialize(self):
        result = b''
        if self.command:
            result += struct.pack('B', 10) + self.command.encode('utf-8')
        if self.package_name:
            result += struct.pack('B', 18) + self.package_name.encode('utf-8')
        return result

    @classmethod
    def deserialize(cls, stream):
        command = None
        package_name = None
        while True:
            tag = struct.unpack('B', stream.read(1))[0]
            if tag == 0:
                break
            elif tag == 10:
                command = stream.read(1).decode('utf-8')
            elif tag == 18:
                package_name = stream.read(1).decode('utf-8')
        return cls(command, package_name)


class StringKeyValueCodedObject(CodedObject):
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value

    def serialize(self):
        result = b''
        if self.key:
            result += struct.pack('B', 26) + self.key.encode('utf-8')
        if self.value:
            result += struct.pack('B', 34) + self.value.encode('utf-8')
        return result

    @classmethod
    def deserialize(cls, stream):
        key = None
        value = None
        while True:
            tag = struct.unpack('B', stream.read(1))[0]
            if tag == 0:
                break
            elif tag == 26:
                key = stream.read(1).decode('utf-8')
            elif tag == 34:
                value = stream.read(1).decode('utf-8')
        return cls(key, value)


class AntiabuseRequestData(CodedObject):
    def __init__(self):
        self.a = False
        self.b = None
        self.c = []
        self.d = False
        self.e = ""
        self.f = -1

    def add_key_value(self, obj):
        if not isinstance(obj, StringKeyValueCodedObject):
            raise TypeError("Expected instance of StringKeyValueCodedObject")
        self.c.append(obj)

    def set_command_and_package_name(self, obj):
        if not isinstance(obj, CommandAndPackageNameObject):
            raise TypeError("Expected instance of CommandAndPackageNameObject")
        self.a = True
        self.b = obj

    def set_string(self, e):
        self.d = True
        self.e = e

    def serialize(self):
        result = b''
        if self.a and self.b:
            result += struct.pack('B', 1) + self.b.serialize()
        for obj in self.c:
            result += struct.pack('B', 2) + obj.serialize()
        if self.d:
            result += struct.pack('B', 3) + self.e.encode('utf-8')
        return result

    @classmethod
    def deserialize(cls, stream):
        obj = cls()
        while True:
            tag = struct.unpack('B', stream.read(1))[0]
            if tag == 0:
                break
            elif tag == 1:
                obj.b = CommandAndPackageNameObject.deserialize(stream)
                obj.a = True
            elif tag == 2:
                obj.add_key_value(StringKeyValueCodedObject.deserialize(stream))
            elif tag == 3:
                obj.set_string(stream.read().decode('utf-8'))
        return obj

    def __eq__(self, other):
        if not isinstance(other, AntiabuseRequestData):
            return False
        return (self.a == other.a and
                self.d == other.d and
                self.f == other.f and
                self.e == other.e and
                self.b == other.b and
                self.c == other.c)


class Build:
    BOARD = "board_value"
    BOOTLOADER = "bootloader_value"
    BRAND = "brand_value"
    CPU_ABI = "cpu_abi_value"
    CPU_ABI2 = "cpu_abi2_value"
    DEVICE = "device_value"
    DISPLAY = "display_value"
    FINGERPRINT = "fingerprint_value"
    HARDWARE = "hardware_value"
    HOST = "host_value"
    ID = "id_value"
    MANUFACTURER = "manufacturer_value"
    MODEL = "model_value"
    PRODUCT = "product_value"
    RADIO = "radio_value"
    SERIAL = "serial_value"
    TAGS = "tags_value"
    TIME = 1234567890
    TYPE = "type_value"
    USER = "user_value"
    VERSION = {
        'CODENAME': "codename_value",
        'INCREMENTAL': "incremental_value",
        'RELEASE': "release_value",
        'SDK': "sdk_value",
        'SDK_INT': 30
    }


def create_protobuf_request_data(command):
    antiabuse_request = AntiabuseRequestData()
    command_and_package_name = CommandAndPackageNameObject(command, "com.google.android.gms")
    antiabuse_request.set_command_and_package_name(command_and_package_name)
    antiabuse_request.set_string("4.0.33 (910055-30)")

    for key, value in Build.__dict__.items():
        if not key.startswith('__'):
            antiabuse_request.add_key_value(StringKeyValueCodedObject(key, str(value)))

    return antiabuse_request


# Usage example
