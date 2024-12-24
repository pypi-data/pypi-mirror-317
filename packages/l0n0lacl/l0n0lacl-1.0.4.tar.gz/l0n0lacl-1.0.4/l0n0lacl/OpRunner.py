from .AclNDTensor import *
from .AclArray import AclArray
from .AclMemory import AclMemory


def build_op_api_lib_path(prefix='customize'):
    ascend_home_path = os.environ["ASCEND_HOME_PATH"]
    op_path = f"{ascend_home_path}/opp/vendors/{prefix}/op_api/lib/libcust_opapi.so"
    return op_path


class OpRunner:
    default_stream = None

    def __init__(self, name, op_path_prefix='customize', op_path=None, device_id=0) -> None:
        op_path = op_path or build_op_api_lib_path(op_path_prefix)
        self.op_lib = ctypes.CDLL(op_path)
        self.get_workspace_size = getattr(
            self.op_lib, f"aclnn{name}GetWorkspaceSize")
        self.run = getattr(self.op_lib, f"aclnn{name}")
        self.run.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint64,
            ctypes.c_void_p,
            ctypes.c_void_p,
        ]
        self.executor = np.array([0], dtype=np.uint64)
        self.temp_args = None
        self.workspace_memory = None

    def __call__(self, *args, outCout=1, argtypes=None, stream=None) -> Union[AclNDTensor, List[AclNDTensor]]:
        stream = stream or OpRunner.default_stream
        self.stream = stream
        temp_args = []
        for arg in args:
            if isinstance(arg, np.ndarray):
                acl_tensor = AclNDTensor(arg)
                acl_tensor.op_runner = self
                acl_tensor.need_copy_to_cpu = True
                temp_args.append(acl_tensor)
            elif isinstance(arg, AclNDTensor):
                arg.op_runner = self
                arg.need_copy_to_cpu = True
                temp_args.append(arg)
            else:
                temp_args.append(arg)
        self.temp_args = temp_args
        real_args = []
        run_argtypes = argtypes or []
        for arg in temp_args:
            if isinstance(arg, AclNDTensor):
                real_args.append(arg.ptr)
                if argtypes is None:
                    run_argtypes.append(ctypes.c_void_p)
            elif isinstance(arg, bool):
                real_args.append(arg)
                if argtypes is None:
                    run_argtypes.append(ctypes.c_bool)
            elif isinstance(arg, int):
                real_args.append(arg)
                if argtypes is None:
                    int32_info = np.iinfo(np.int32)
                    if arg > int32_info.max or arg < int32_info.min:
                        run_argtypes.append(ctypes.c_int64)
                    else:
                        run_argtypes.append(ctypes.c_int32)
            elif isinstance(arg, float):
                real_args.append(arg)
                if argtypes is None:
                    float32_info = np.finfo(np.float32)
                    if arg > float32_info.max or arg < float32_info.min:
                        run_argtypes.append(ctypes.c_double)
                    else:
                        run_argtypes.append(ctypes.c_float)
            elif isinstance(arg, bytes):
                real_args.append(arg)
                if argtypes is None:
                    run_argtypes.append(ctypes.c_char_p)
            elif isinstance(arg, AclArray):
                real_args.append(arg.ptr)
                if argtypes is None:
                    run_argtypes.append(ctypes.c_void_p)
            elif isinstance(arg, ctypes.c_int16):
                real_args.append(arg.value)
                if argtypes is None:
                    run_argtypes.append(ctypes.c_int16)
            elif isinstance(arg, ctypes.c_int32):
                real_args.append(arg.value)
                if argtypes is None:
                    run_argtypes.append(ctypes.c_int32)
            elif isinstance(arg, ctypes.c_int64):
                real_args.append(arg.value)
                if argtypes is None:
                    run_argtypes.append(ctypes.c_int64)
            elif isinstance(arg, ctypes.c_double):
                real_args.append(arg.value)
                if argtypes is None:
                    run_argtypes.append(ctypes.c_double)

        workspace = np.zeros([1], dtype=np.uint64)
        real_args.append(workspace.ctypes.data)
        real_args.append(self.executor.ctypes.data)
        run_argtypes.append(ctypes.c_void_p)
        run_argtypes.append(ctypes.c_void_p)
        self.get_workspace_size.argtypes = run_argtypes
        self.get_workspace_size(*real_args)
        workspace_ptr = 0
        workspace_size = int(workspace[0])
        if workspace_size > 0:
            self.workspace_memory = AclMemory(workspace_size)
            workspace_ptr = self.workspace_memory.device_ptr
        self.run(workspace_ptr, workspace_size, int(self.executor[0]), stream)
        if outCout == 1:
            return temp_args[-1]
        return temp_args[-outCout:]

    def sync_stream(self):
        if self.stream is not None and stream_need_sync(self.stream):
            try_sync_stream(self.stream)
        self.temp_args = None
        self.workspace_memory = None
