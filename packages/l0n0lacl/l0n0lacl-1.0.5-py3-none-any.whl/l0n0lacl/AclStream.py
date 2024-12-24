from .utils import *

class AclStream:
    def __init__(self, device_id=0):
        self.stream = None
        self.device_id = device_id
        self.set_device(device_id)

    def set_device(self, device_id):
        acl.rt.set_device(device_id)

    def __enter__(self):
        stream, ret = acl.rt.create_stream()
        print_ret("创建stream失败", ret)
        self.stream = stream
        return stream

    def __exit__(self, *args, **kwargs):
        if self.stream is None or self.stream == 0:
            return
        try_sync_stream(self.stream)
        ret = acl.rt.destroy_stream(self.stream)
        print_ret("销毁stream错误!", ret)

