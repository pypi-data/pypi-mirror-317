import os
import acl
import ctypes
import numpy as np
import colorama
from typing import List, Union


def build_acl_lib_path(libname):
    ascend_home_path = os.environ["ASCEND_HOME_PATH"]
    lib_path = f"{ascend_home_path}/lib64/{libname}"
    return lib_path


def load_acl_lib(libname):
    return ctypes.CDLL(build_acl_lib_path(libname))


libnnopbase = load_acl_lib("libnnopbase.so")
libascendcl = load_acl_lib("libascendcl.so")
# size_t aclDataTypeSize(aclDataType dataType)
libascendcl.aclDataTypeSize.argtypes = [ctypes.c_int]
libascendcl.aclDataTypeSize.restype = ctypes.c_uint64


def print_ret(msg, ret):
    if ret == 0:
        return
    print(colorama.Fore.RED, "[错误]", msg, ret, flush=True)
    print(colorama.Style.RESET_ALL, flush=True)


class AclStreamStatus:
    # Stream上的所有任务已完成。
    ACL_STREAM_STATUS_COMPLETE = 0
    # Stream上至少有一个任务未完成。
    ACL_STREAM_STATUS_NOT_READY = 1
    # 预留。
    ACL_STREAM_STATUS_RESERVED = 0xFFFF


def stream_need_sync(stream: int):
    status, ret = acl.rt.stream_query(stream)
    if ret != 0:
        print_ret("获取stream状态错误", ret)
        return False
    return status == AclStreamStatus.ACL_STREAM_STATUS_NOT_READY


def try_sync_stream(stream: int):
    ret = acl.rt.synchronize_stream(stream)
    if ret != 0:
        print_ret("同步stream错误", ret)
        return False
    return True


def get_loss_by_type(dtype):
    loss = 0
    if dtype == np.float16:
        loss = 1 / 1000
    elif dtype == np.float32:
        loss = 1 / 10000
    return loss


def _compare(v1: np.ndarray, v2: np.ndarray):
    loss = get_loss_by_type(v1.dtype)
    return np.abs(v1 - v2) <= loss


def compare(v1: np.ndarray, v2: np.ndarray):
    return _compare(v1, v2).all()


def right_rate(v1: np.ndarray, v2: np.ndarray):
    ret = _compare(v1, v2)
    return ret.astype(np.int32).sum() / v1.size

# 参考自：https://gitee.com/ascend/samples/blob/master/operator/AddCustomSample/KernelLaunch/AddKernelInvocationNeo/scripts/verify_result.py


def verify_result(real_result, golden):
    loss = get_loss_by_type(real_result.dtype)
    minimum = 10e-10
    result = np.abs(real_result - golden)  # 计算运算结果和预期结果偏差
    deno = np.maximum(np.abs(real_result), np.abs(golden))  # 获取最大值并组成新数组
    result_atol = np.less_equal(result, loss)  # 计算绝对误差
    result_rtol = np.less_equal(result / np.add(deno, minimum), loss)  # 计算相对误差
    if not result_rtol.all() and not result_atol.all():
        if (
            np.sum(result_rtol == False) > real_result.size * loss
            and np.sum(result_atol == False) > real_result.size * loss
        ):  # 误差超出预期时返回打印错误，返回对比失败
            print(
                colorama.Fore.RED, real_result.dtype, "[ERROR] result error", flush=True
            )
            print(colorama.Style.RESET_ALL, flush=True)
            return False
    print(colorama.Fore.GREEN, real_result.dtype, "test pass", flush=True)
    print(colorama.Style.RESET_ALL, flush=True)
    return True


class AclDtype:
    ACL_DT_UNDEFINED = -1  # 未知数据类型，默认值
    ACL_FLOAT = 0
    ACL_FLOAT16 = 1
    ACL_INT8 = 2
    ACL_INT32 = 3
    ACL_UINT8 = 4
    ACL_INT16 = 6
    ACL_UINT16 = 7
    ACL_UINT32 = 8
    ACL_INT64 = 9
    ACL_UINT64 = 10
    ACL_DOUBLE = 11
    ACL_BOOL = 12
    ACL_STRING = 13
    ACL_COMPLEX64 = 16
    ACL_COMPLEX128 = 17
    ACL_BF16 = 27
    ACL_INT4 = 29
    ACL_UINT1 = 30
    ACL_COMPLEX32 = 33

    def get_size(dtype: int):
        return libascendcl.aclDataTypeSize(dtype)


class AclRunMode:
    ACL_DEVICE = 0
    ACL_HOST = 1


class AclAllocPolicy:
    """
    0：ACL_MEM_MALLOC_HUGE_FIRST，当申请的内存小于等于1M时，即使使用该内存分配规则，也是申请普通页的内存。当申请的内存大于1M时，优先申请大页内存，如果大页内存不够，则使用普通页的内存。
    1：ACL_MEM_MALLOC_HUGE_ONLY，仅申请大页，如果大页内存不够，则返回错误。
    2：ACL_MEM_MALLOC_NORMAL_ONLY，仅申请普通页。
    3：ACL_MEM_MALLOC_HUGE_FIRST_P2P，仅Device之间内存复制场景下申请内存时使用该选项，表示优先申请大页内存，如果大页内存不够，则使用普通页的内存。预留选项。
    4：ACL_MEM_MALLOC_HUGE_ONLY_P2P，仅Device之间内存复制场景下申请内存时使用该选项，仅申请大页内存，如果大页内存不够，则返回错误。预留选项。
    5：ACL_MEM_MALLOC_NORMAL_ONLY_P2P，仅Device之间内存复制场景下申请内存时使用该选项，仅申请普通页的内存。预留选项。
    """
    ACL_MEM_MALLOC_HUGE_FIRST = 0
    ACL_MEM_MALLOC_HUGE_ONLY = 1
    ACL_MEM_MALLOC_NORMAL_ONLY = 2
    ACL_MEM_MALLOC_HUGE_FIRST_P2P = 3
    ACL_MEM_MALLOC_HUGE_ONLY_P2P = 4
    ACL_MEM_MALLOC_NORMAL_ONLY_P2P = 5
    ACL_MEM_TYPE_LOW_BAND_WIDTH = 0x0100
    ACL_MEM_TYPE_HIGH_BAND_WIDTH = 0x1000


class AclMemcopyKind:
    """
    0：ACL_MEMCPY_HOST_TO_HOST，Host内的内存复制。
    1：ACL_MEMCPY_HOST_TO_DEVICE，Host到Device的内存复制。
    2：ACL_MEMCPY_DEVICE_TO_HOST，Device到Host的内存复制。
    3：ACL_MEMCPY_DEVICE_TO_DEVICE，Device内的内存复制。
    """

    ACL_MEMCPY_HOST_TO_HOST = 0
    ACL_MEMCPY_HOST_TO_DEVICE = 1
    ACL_MEMCPY_DEVICE_TO_HOST = 2
    ACL_MEMCPY_DEVICE_TO_DEVICE = 3


def numpy_dtype_2_acl_dtype(numpy_dtype):
    if numpy_dtype == np.float32:
        return AclDtype.ACL_FLOAT
    if numpy_dtype == np.float16:
        return AclDtype.ACL_FLOAT16
    if numpy_dtype == np.int8:
        return AclDtype.ACL_INT8
    if numpy_dtype == np.int32:
        return AclDtype.ACL_INT32
    if numpy_dtype == np.uint8:
        return AclDtype.ACL_UINT8
    if numpy_dtype == np.int16:
        return AclDtype.ACL_INT16
    if numpy_dtype == np.uint16:
        return AclDtype.ACL_UINT16
    if numpy_dtype == np.uint32:
        return AclDtype.ACL_UINT32
    if numpy_dtype == np.int64:
        return AclDtype.ACL_INT64
    if numpy_dtype == np.uint64:
        return AclDtype.ACL_UINT64
    if numpy_dtype == np.double:
        return AclDtype.ACL_DOUBLE
    if numpy_dtype == np.bool_:
        return AclDtype.ACL_BOOL
    if numpy_dtype == np.complex64:
        return AclDtype.ACL_COMPLEX64
    if numpy_dtype == np.complex128:
        return AclDtype.ACL_COMPLEX128


def acl_dtype_2_numpy_dtype(acl_dtype):
    if acl_dtype == AclDtype.ACL_FLOAT:
        return np.float32
    if acl_dtype == AclDtype.ACL_FLOAT16:
        return np.float16
    if acl_dtype == AclDtype.ACL_INT8:
        return np.int8
    if acl_dtype == AclDtype.ACL_INT32:
        return np.int32
    if acl_dtype == AclDtype.ACL_UINT8:
        return np.uint8
    if acl_dtype == AclDtype.ACL_INT16:
        return np.int16
    if acl_dtype == AclDtype.ACL_UINT16:
        return np.uint16
    if acl_dtype == AclDtype.ACL_UINT32:
        return np.uint32
    if acl_dtype == AclDtype.ACL_INT64:
        return np.int64
    if acl_dtype == AclDtype.ACL_UINT64:
        return np.uint64
    if acl_dtype == AclDtype.ACL_DOUBLE:
        return np.float64
    if acl_dtype == AclDtype.ACL_BOOL:
        return np.bool_
    if acl_dtype == AclDtype.ACL_COMPLEX64:
        return np.complex64
    if acl_dtype == AclDtype.ACL_COMPLEX128:
        return np.complex128


def numpy_dtype_2_torch_dtype(numpy_dtype):
    import torch
    if numpy_dtype == np.float32:
        return torch.float32
    if numpy_dtype == np.float16:
        return torch.float16
    if numpy_dtype == np.int8:
        return torch.int8
    if numpy_dtype == np.int32:
        return torch.int32
    if numpy_dtype == np.uint8:
        return torch.uint8
    if numpy_dtype == np.int16:
        return torch.int16
    if numpy_dtype == np.uint16:
        return torch.int16
    if numpy_dtype == np.uint32:
        return torch.int32
    if numpy_dtype == np.int64:
        return torch.int64
    if numpy_dtype == np.uint64:
        return torch.int64
    if numpy_dtype == np.double:
        return torch.double
    if numpy_dtype == np.bool_:
        return torch.bool
    if numpy_dtype == np.complex64:
        return torch.complex64
    if numpy_dtype == np.complex128:
        return torch.complex128
    if numpy_dtype == np.complex_:
        return torch.complex32


if __name__ == "__main__":
    a = np.zeros((3, 3), dtype=np.float16)
    env = AclEnv(0)
    nd_tensor = AclNDTensor(a)
