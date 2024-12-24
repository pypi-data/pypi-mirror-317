from .utils import *


class AclMemory:
    def __init__(self, size: int):
        self.size = size
        self.device_ptr, ret = acl.rt.malloc(size, 0)
        print_ret("AclMemory malloc", ret)
        assert ret == 0

    def __del__(self):
        acl.rt.free(self.device_ptr)

    def copyFromHost(self, hostPtr: int, size: int):
        size = int(min(size, self.size))
        ret = acl.rt.memcpy(
            self.device_ptr,
            size,
            hostPtr,
            size,
            AclMemcopyKind.ACL_MEMCPY_HOST_TO_DEVICE,
        )
        print_ret("AclMemory memcpy", ret)
        assert ret == 0

    def copyToHost(self, hostPtr: int, size: int):
        size = int(min(size, self.size))
        ret = acl.rt.memcpy(
            hostPtr,
            size,
            self.device_ptr,
            size,
            AclMemcopyKind.ACL_MEMCPY_DEVICE_TO_HOST,
        )
        print_ret("AclMemory memcpy", ret)
        assert ret == 0

    def copyFromDevice(self, devicePtr: int, size: int):
        size = int(min(size, self.size))
        ret = acl.rt.memcpy(
            self.device_ptr,
            size,
            devicePtr,
            size,
            AclMemcopyKind.ACL_MEMCPY_DEVICE_TO_DEVICE,
        )
        print_ret("AclMemory memcpy", ret)
        assert ret == 0

    def copyToDevice(self, devicePtr: int, size: int):
        size = int(min(size, self.size))
        ret = acl.rt.memcpy(
            devicePtr,
            size,
            self.device_ptr,
            size,
            AclMemcopyKind.ACL_MEMCPY_DEVICE_TO_DEVICE,
        )
        print_ret("AclMemory memcpy", ret)
        assert ret == 0
