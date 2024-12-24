from .utils import *

# aclIntArray *aclCreateIntArray(const int64_t *value, uint64_t size)
libnnopbase.aclCreateIntArray.argtypes = [ctypes.c_void_p, ctypes.c_uint64]
libnnopbase.aclCreateIntArray.restype = ctypes.c_void_p
# aclnnStatus aclDestroyIntArray(const aclIntArray *array)
libnnopbase.aclDestroyIntArray.argtypes = [ctypes.c_void_p]
libnnopbase.aclDestroyIntArray.restype = ctypes.c_int

# aclFloatArray *aclCreateFloatArray(const float *value, uint64_t size)
libnnopbase.aclCreateFloatArray.argtypes = [ctypes.c_void_p, ctypes.c_uint64]
libnnopbase.aclCreateFloatArray.restype = ctypes.c_void_p
# aclnnStatus aclDestroyFloatArray(const aclFloatArray *array)
libnnopbase.aclDestroyFloatArray.argtypes = [ctypes.c_void_p]
libnnopbase.aclDestroyFloatArray.restype = ctypes.c_int

# aclBoolArray *aclCreateBoolArray(const bool *value, uint64_t size)
libnnopbase.aclCreateBoolArray.argtypes = [ctypes.c_void_p, ctypes.c_uint64]
libnnopbase.aclCreateBoolArray.restype = ctypes.c_void_p
# aclnnStatus aclDestroyBoolArray(const aclBoolArray *array)
libnnopbase.aclDestroyBoolArray.argtypes = [ctypes.c_void_p]
libnnopbase.aclDestroyBoolArray.restype = ctypes.c_int


class AclArray:
    def __init__(self, np_array: np.ndarray):
        self.np_array = np_array
        if np_array.dtype == np.int64:
            self.ptr = libnnopbase.aclCreateIntArray(
                np_array.ctypes.data, np_array.size)
        elif np_array.dtype == np.float32:
            self.ptr = libnnopbase.aclCreateFloatArray(
                np_array.ctypes.data, np_array.size)
        elif np_array.dtype == np.bool:
            self.ptr = libnnopbase.aclCreateBoolArray(
                np_array.ctypes.data, np_array.size)
        else:
            raise Exception(
                "np_array的类型必须是[numpy.int64, numpy.float32, numpy.bool] 的一种, 提供的类型为:" + str(np_array.dtype))

    def __del__(self) -> str:
        if self.np_array.dtype == np.int64:
            ret = libnnopbase.aclDestroyIntArray(self.ptr)
        elif self.np_array.dtype == np.float32:
            ret = libnnopbase.aclDestroyFloatArray(self.ptr)
        elif self.np_array.dtype == np.bool:
            ret = libnnopbase.aclDestroyBoolArray(self.ptr)
        assert (ret == 0)
