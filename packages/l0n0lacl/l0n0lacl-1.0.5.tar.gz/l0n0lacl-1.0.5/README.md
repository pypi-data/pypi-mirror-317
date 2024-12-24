# 1 功能描述
由于在ascendc算子开发过程中运行算子比较复杂，为了简化算子的运行，将运行算子变成可以用python直接调用的函数。所以编写了此代码。

# 2 安装
```
pip install l0n0lacl
```

# 3 运行算子实例
## 3.1 先切换到cann环境,比如我的环境是:
```
source /home/HwHiAiUser/Ascend/ascend-toolkit/set_env.sh
```
## 3.2 先安装我们编写的算子
```
bash custom_opp_xxx_aarch64.run
```
## 3.3 创建算子运行器
```python
from l0n0lacl import *
ascendc_gelu = OpRunner("Gelu", op_path_prefix='customize')
```

## 3.4 调用算子
### 3.4.1 先看调用传参顺序
在算子工程编译后，会有代码生成，在算子工程目录:
`${算子目录}/build_out/autogen/aclnn_xxx.h`中可以找到`aclnnXXXGetWorkspaceSize`函数。以Gelu为例：
```c++
__attribute__((visibility("default")))
aclnnStatus aclnnGeluGetWorkspaceSize(
    const aclTensor *x,
    const aclTensor *out,
    uint64_t *workspaceSize,
    aclOpExecutor **executor);
```
可以看到参数为 `x`, `out`, `workspaceSize`, `executor`。其中 `workspaceSize`, `executor`不需要管。
* `aclTensor*`对应`numpy.ndarray`
* 其他参考: <a href = "https://docs.python.org/zh-cn/3/library/ctypes.html#fundamental-data-types">ctypes类型</a>
### 3.4.2 调用算子
```python
import torch
from l0n0lacl import *
ascendc_gelu = OpRunner("Gelu", op_path_prefix='customize')
target_dtype = torch.float
x = torch.empty(shape, dtype=target_dtype).uniform_(-1, 1)
y = torch.empty(shape, dtype=target_dtype).zero_()
out = ascendc_gelu(x.numpy(), y.numpy()).to_cpu()
print(out)
```

# 4. api参考
## 4.1 AclNDTensor
```python
class AclNDTensor:
    def __init__(self, np_array: np.ndarray):
        pass
    def to_cpu(self):
        pass
```
numpy ndarray与ascend nd tensor间的桥梁
### 4.1.1 `__init__`
* `np_array`: numpy的tensor
### 4.1.2 `to_cpu`
将运算结果从npu拷贝到cpu
## 4.2 OpRunner
```python
class OpRunner:
    def __init__(self, name, op_path_prefix='customize', op_path=None, device_id=0) -> None:
        pass
    def __call__(self, *args, outCout=1, argtypes=None, stream=None) -> Union[AclNDTensor, List[AclNDTensor]]:
        pass
    def sync_stream(self)->None:
        pass
```
### 4.2.1 `__init__`
* `name`:算子名称，
* `op_path_prefix`: 算子工程中**CMakePresets.json**文件中**vender_name**的值。默认是`customize`,可以不传
```json
"vendor_name": {
    "type": "STRING",
    "value": "customize"
},
```
* `op_path`: 算子`libcust_opapi.so`库的绝对位置。不传。
* `device_id`: 设备ID。默认`0`

### 4.2.2 `__call__`
* `args`: 表示传给`aclnnXXXGetWorkspaceSize`除了`workspaceSize`, `executor`的参数
* `outCout` : 表示算子的输出个数。如果输出个数为`1`,返回一个`AclNDTensor`。如果输出个数大于1,返回`List[AclNDTensor]`
* `argtypes`: 表示`aclnnXXXGetWorkspaceSize`的参数`ctypes`参数类型，对于特别复杂的算子，如果发现调用异常，可以手动指定类型。
比如(**仅用于举例，其实可以不传，自动推导就可运行。但是当发现运行异常的情况下，可以自己指定**)，对于:
```c++
__attribute__((visibility("default")))
aclnnStatus aclnnCumsumGetWorkspaceSize(
    const aclTensor *x,
    const aclTensor *axis,
    bool exclusiveOptional,
    bool reverseOptional,
    const aclTensor *out,
    uint64_t *workspaceSize,
    aclOpExecutor **executor);
```

```python
import ctypes
from l0n0lacl import *
ascendc_cumsum = OpRunner("Cumsum")
target_dtype = np.float32
data_range = (-10, 10)
shape = [100, 3, 2304]
axis_py = 1
exclusive = True
reverse = False
x = np.random.uniform(*data_range, shape).astype(target_dtype)
axis = np.array([axis_py]).astype(np.int32)
golden: np.ndarray = tf.cumsum(x, axis_py, exclusive, reverse, argtypes=[
    ctypes.c_void_p, # x
    ctypes.c_void_p, # axis
    ctypes.c_bool,   # exclusiveOptional
    ctypes.c_bool,   # reverseOptional
    ctypes.c_void_p, # out
    ctypes.c_void_p, # workspaceSize
    ctypes.c_void_p, # executor
]).numpy()
y = np.ones_like(golden, golden.dtype) * 123
ascendc_cumsum(x, axis, exclusive, reverse,  y).to_cpu()
print(y)
```
* `stream` 如果是多stream的情况下，可以自己指定stream:
例如:
```python
import numpy as np
from l0n0lacl import *
ascendc_gelu = OpRunner("Gelu", op_path_prefix='customize')
target_dtype = np.float32
shape = [10, 10]
x = np.random.uniform(-10, 10, shape).astype(target_dtype)
y = np.zeros_like(x, dtype=target_dtype)
with AclStream(0) as stream:
    out = ascendc_gelu(x, y, stream=stream).to_cpu()
print(out)
```

### 4.2.3 `sync_stream`
用于同步stream

## 4.3 verify_result
参考自：https://gitee.com/ascend/samples/blob/master/operator/AddCustomSample/KernelLaunch/AddKernelInvocationNeo/scripts/verify_result.py
```python
def verify_result(real_result:numpy.ndarray, golden:numpy.ndarray):
    pass
```
判断精度是否符合
float16: 千分之一
float32: 万分之一
int16,int32,int8: 0

## 4.4 AclArray
```python
class AclArray:
    def __init__(self, np_array: np.ndarray):
        pass
```
实例：
```c++
__attribute__((visibility("default")))
aclnnStatus aclnnEyeGetWorkspaceSize(
    aclTensor *yRef,
    int64_t numRows,
    int64_t numColumnsOptional,
    const aclIntArray *batchShapeOptional,
    int64_t dtypeOptional,
    uint64_t *workspaceSize,
    aclOpExecutor **executor);
```

```python
import tensorflow as tf
from l0n0lacl import *
ascendc_fn = OpRunner("Eye")
for i, target_dtype in enumerate([np.float16, np.float32]):
    numRows = 2
    numColumnsOptional = 3
    batchShapeOptional = 0
    dtypeOptional = 0
    shape = [numRows * numColumnsOptional]
    for value_range in [(-1, 1), (1, 10), (-1000, 1000)]:
        y = np.zeros(shape, dtype=target_dtype)
        batchShape = AclArray(np.array([1, 2, 3], dtype=np.int64))
        output = ascendc_fn(y, numRows, numColumnsOptional, batchShape, 0, outCout=5)
        output[0].to_cpu()
        golden = tf.eye(numRows, numColumnsOptional)
        print(y)
        print(golden)
        print(value_range)
        verify_result(y, golden.numpy().reshape(shape))
```