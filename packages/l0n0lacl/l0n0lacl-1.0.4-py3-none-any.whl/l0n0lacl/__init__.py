import atexit
from .utils import *
from .AclNDTensor import AclNDTensor
from .OpRunner import OpRunner
from .AclStream import AclStream
from .AclArray import AclArray

# 初始化acl
acl.init()
acl.rt.set_device(0)
OpRunner.default_stream, ret = acl.rt.create_stream()
print_ret("创建_defualt_stream失败", ret)

@atexit.register
def finalize():
    global default_stream
    if OpRunner.default_stream is not None and OpRunner.default_stream != 0:
        if stream_need_sync(OpRunner.default_stream):
            try_sync_stream(OpRunner.default_stream)
        acl.rt.destroy_stream(OpRunner.default_stream)
        OpRunner.default_stream = None
    print_ret("销毁stream错误!", ret)
    acl.finalize()