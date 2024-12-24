from .utils import *
from .AclMemory import AclMemory
import math
# ACL_FUNC_VISIBILITY aclTensor * aclCreateTensor(
#     const int64_t * viewDims,
#     uint64_t viewDimsNum,
#     aclDataType dataType,
#     const int64_t * stride,
#     int64_t offset,
#     aclFormat format,
#     const int64_t * storageDims,
#     uint64_t storageDimsNum,
#     void * tensorData)
libnnopbase.aclCreateTensor.argtypes = [
    ctypes.c_void_p,  # viewDims
    ctypes.c_uint64,  # viewDimsNum
    ctypes.c_int,    # dataType
    ctypes.c_void_p,  # stride
    ctypes.c_int64,  # offset
    ctypes.c_int,    # format
    ctypes.c_void_p,  # storageDims
    ctypes.c_uint64,  # storageDimsNum
    ctypes.c_void_p,  # tensorData
]
libnnopbase.aclCreateTensor.restype = ctypes.c_void_p
libnnopbase.aclDestroyTensor.argtypes = [ctypes.c_void_p]
libnnopbase.aclDestroyTensor.restype = ctypes.c_int


class AclNDTensor:
    def __init__(self,
                 np_array: Union[np.ndarray, None] = None,
                 shape: Union[int, List[int], None] = None,
                 dtype: int = AclDtype.ACL_FLOAT16):
        self.np_array = np_array
        self.op_runner = None
        self.need_copy_to_cpu = False
        if np_array is None:
            self.shape = np.array(shape, dtype=np.int64)
            self.dtype = dtype
            self.size = np.prod(self.shape)
            self.itemsize = AclDtype.get_size(dtype)
        else:
            self.shape = np.array(np_array.shape, dtype=np.int64)
            self.dtype = numpy_dtype_2_acl_dtype(np_array.dtype)
            self.size = np_array.size
            self.itemsize = np_array.itemsize
        self.data_bytes_size = self.size * self.itemsize
        self.mem_size = int(math.ceil(self.data_bytes_size / 256) * 256) + 256
        # 分配设备内存
        self.device_memory = AclMemory(self.mem_size)
        # 拷贝数据
        if np_array is not None:
            self.device_memory.copyFromHost(
                np_array.ctypes.data, self.data_bytes_size)
        # 创建Tensor
        self.ptr = libnnopbase.aclCreateTensor(
            self.shape.ctypes.data,
            self.shape.size,
            self.dtype,
            0,
            0,
            2,
            self.shape.ctypes.data,
            self.shape.size,
            self.device_memory.device_ptr
        )
        assert (self.ptr != 0)

    def __str__(self) -> str:
        return str(self.to_cpu())

    def __del__(self):
        ret = libnnopbase.aclDestroyTensor(self.ptr)
        self.ptr = 0
        print_ret("aclDestroyTensor", ret)
        assert ret == 0

    def to_cpu(self):
        if self.op_runner is not None:
            self.op_runner.sync_stream()
        if self.need_copy_to_cpu:
            if self.np_array is None:
                self.np_array = np.zeros(
                    self.shape, dtype=acl_dtype_2_numpy_dtype(self.dtype))
            self.device_memory.copyToHost(
                self.np_array.ctypes.data, self.data_bytes_size)
            self.need_copy_to_cpu = False
        return self.np_array
