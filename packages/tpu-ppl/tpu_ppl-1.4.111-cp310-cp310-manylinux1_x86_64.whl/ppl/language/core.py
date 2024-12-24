from __future__ import annotations

from contextlib import contextmanager
from enum import Enum
from functools import wraps
from typing import Callable, List, Sequence, TypeVar

from .._C.libppl.ppl import ir
from ..runtime.jit import jit
from . import math, semantic
import inspect
import os
T = TypeVar('T')

PPL_MAX_TENSOR_NUMEL = 10000000000#131072

PPL_BUILTIN = "__ppl_builtin__"
def get_npu_num() ->int:
    arch = os.getenv("CHIP", default="bm1684x")
    npu_num = 64
    if arch == "bm1684x":
        npu_num = 64
    elif arch == "bm1688":
        npu_num = 32
    return npu_num

def builtin(fn: T) -> T:
    """Mark a function as a builtin."""
    assert callable(fn)

    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "_builder" not in kwargs or kwargs["_builder"] is None:
            raise ValueError(
                "Did you forget to add @ppl.jit ? "
                "(`_builder` argument must be provided outside of JIT functions.)"
            )
        return fn(*args, **kwargs)

    setattr(wrapper, PPL_BUILTIN, True)

    return wrapper

def _tensor_member_fn(fn: T) -> T:
    """Decorator that adds this free function as a member fn on class tensor.

    When called as a member function on class tensor, the first argument to `fn`
    is `self`, i.e. the tensor object.

    If there are multiple decorators on a function, you probably want this one
    to be the highest one (i.e. furthest from the function's `def`), so it's
    applied last.

    Unfortunately you still need to add a type stub to the body of class tensor
    in order for pytype to know about it.
    """
    assert callable(fn)
    orig_sig = inspect.signature(fn)
    # Does fn take args other than _builder, _generator, and the tensor itself?
    has_args = len(orig_sig.parameters.keys() - {"_builder", "_generator"}) > 1

    if not fn.__doc__:
        fn.__doc__ = ""
    fn.__doc__ += f"""
    This function can also be called as a member function on :py:class:`tensor`,
    as :code:`x.{fn.__name__}({"..." if has_args else ""})` instead of
    :code:`{fn.__name__}(x{", ..." if has_args else ""})`.
    """

    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    # Match the signature of `fn`, but change the first arg to `self` so the
    # docs are a little less weird.
    new_params = list(orig_sig.parameters.values())
    new_params[0] = new_params[0].replace(name='self')
    new_sig = orig_sig.replace(parameters=new_params)
    wrapper.__signature__ = new_sig
    wrapper.__doc__ = f"Forwards to :py:func:`{fn.__name__}` free function"
    # If fn is a builtin, mark the wrapper as a builtin too.
    if is_builtin(fn):
        setattr(wrapper, PPL_BUILTIN, True)

    setattr(tensor, fn.__name__, wrapper)
    return fn

def is_builtin(fn) -> bool:
    """Is this a registered ppl builtin function?"""
    return getattr(fn, PPL_BUILTIN, False)


def _to_tensor(x, builder):
    if isinstance(x, bool):
        return tensor(builder.get_int1(x), int1)
    # Note: compile-time const integers are represented by unsigned values
    elif isinstance(x, int):
        if -2**31 <= x < 2**31:
            return tensor(builder.get_int32(x), int32)
        elif 2**31 <= x < 2**32:
            return tensor(builder.get_int32(x), uint32)
        elif -2**63 <= x < 2**63:
            return tensor(builder.get_int64(x), int64)
        elif 2**63 <= x < 2**64:
            return tensor(builder.get_int64(x), uint64)
        else:
            raise RuntimeError(f'Nonrepresentable integer {x}.')
    elif isinstance(x, float):
        min_float32 = 2 ** -126
        max_float32 = (2 - 2**-23) * 2**127
        abs_x = __builtins__['abs'](x)
        if abs_x == float("inf") or\
           abs_x == 0.0 or \
           x != x or \
           min_float32 <= abs_x <= max_float32:
            return tensor(builder.get_fp32(x), float32)
        else:
            return tensor(builder.get_fp64(x), float64)

    elif isinstance(x, constexpr):
        return _to_tensor(x.value, builder)
    if isinstance(x, tensor):
        return x
    elif isinstance(x, gtensor):
        return x.create(builder)
    elif isinstance(x, ctensor):
        return x
    elif x is None:
        return tensor(builder.get_none_value(), void)
    assert False, f"cannot convert {x} of type {type(x)} to tensor"

class mtype:
    def __init__(self, name):
        self.name = name

    # def to_ir(self, builder: ir.builder):
    #   if self.name == "GLOBAL":
    #     return builder.get_tensor_mode_ty(2)
    #   if self.name == "L2":
    #     return builder.get_tensor_mode_ty(1)

    def val(self):
        if self.name == "GLOBAL":
            return int(2)
        if self.name == "L2":
            return int(1)
        if self.name == 'LOCAL':
            return int(0)

    def __str__(self):
        return f'mtype<{self.name}>'

    def __repr__(self):
        return self.__str__()

    @property
    def scalar(self):
        return self

class round_mode:
    def __init__(self, name):
        self.name = name

    def val(self):
        if self.name == "RM_HALF_TO_EVEN":
            return int(0)
        elif self.name == "RM_HALF_AWAY_FROM_ZERO":
            return int(1)
        elif self.name == "RM_TOWARDS_ZERO":
            return int(2)
        elif self.name == "RM_DOWN":
            return int(3)
        elif self.name == "RM_UP":
            return int(4)
        elif self.name == "RM_HALF_UP":
            return int(5)
        elif self.name == "RM_HALF_DOWN":
            return int(6)

    def __str__(self):
        return f'round_mode<{self.name}>'

    def __repr__(self):
        return self.__str__()

    @property
    def scalar(self):
        return self

class coeff_table_mode:
    def __init__(self, name):
        self.name = name

    def val(self):
        if self.name == "EXP":
            return int(0)
        elif self.name == "LOG":
            return int(1)
        elif self.name == "SIN":
            return int(2)
        elif self.name == "COS":
            return int(3)
        elif self.name == "TAN":
            return int(4)
        elif self.name == "ARCSIN":
            return int(5)
        elif self.name == "ERF_TAYLOR":
            return int(6)

    def __str__(self):
        return f'coeff_table_mode<{self.name}>'

    def __repr__(self):
        return self.__str__()

class align_mode:
    def __init__(self, name):
        self.name = name

    def val(self):
        if self.name == "CONTINUOUS":
            return int(0)
        elif self.name == "TPU_ALIGN":
            return int(1)
        elif self.name == "TPU_COMPACT":
            return int(2)
        elif self.name == "TPU_ROW_ALIGN":
            return int(3)
        elif self.name == "NONE_ALIGN":
            return int(4)

    def __str__(self):
        return f'align_mode<{self.name}>'

    def __repr__(self):
        return self.__str__()

    @property
    def scalar(self):
        return self

class transpose_mode:
    def __init__(self, name):
        self.name = name

    def val(self):
        if self.name == "NC_TRANS":
            return int(0)
        elif self.name == "CW_TRANS":
            return int(1)

    def __str__(self):
        return f'transpose_mode<{self.name}>'

    def __repr__(self):
        return self.__str__()

    @property
    def scalar(self):
        return self

class dtype:
    SINT_TYPES = ['int4', 'int8', 'int16', 'int32', 'int64']
    UINT_TYPES = ['int1', 'uint4', 'uint8', 'uint16', 'uint32', 'uint64']
    FP_TYPES = ['fp8e4b15', 'fp8e4', 'fp8e5', 'fp16', 'bf16', 'fp32', 'fp64']
    STANDARD_FP_TYPES = ['fp16', 'bf16', 'fp32', 'fp64']
    OTHER_TYPES = ['void']

    class SIGNEDNESS(Enum):
        SIGNED = 0
        UNSIGNED = 1

    def __init__(self, name):
        self.name = name
        self.allow_ir_unsigned = False
        assert name in dtype.SINT_TYPES + dtype.UINT_TYPES + dtype.FP_TYPES + dtype.OTHER_TYPES, name
        if name in dtype.SINT_TYPES:
            self.int_signedness = dtype.SIGNEDNESS.SIGNED
            self.int_bitwidth = int(name.split('int')[-1])
            self.primitive_bitwidth = self.int_bitwidth
        elif name in dtype.UINT_TYPES:
            self.int_signedness = dtype.SIGNEDNESS.UNSIGNED
            self.int_bitwidth = int(name.split('int')[-1])
            self.primitive_bitwidth = self.int_bitwidth
        elif name in dtype.FP_TYPES:
            if name == 'fp8e4b15':
                self.fp_mantissa_width = 3
                self.primitive_bitwidth = 8
                self.exponent_bias = 15
            elif name == 'fp8e4':
                self.fp_mantissa_width = 3
                self.primitive_bitwidth = 8
                self.exponent_bias = 7
            elif name == 'fp8e5':
                self.fp_mantissa_width = 2
                self.primitive_bitwidth = 8
                self.exponent_bias = 15
            elif name == 'fp16':
                self.fp_mantissa_width = 10
                self.primitive_bitwidth = 16
                self.exponent_bias = 15
            elif name == 'bf16':
                self.fp_mantissa_width = 7
                self.primitive_bitwidth = 16
                self.exponent_bias = 127
            elif name == 'fp32':
                self.fp_mantissa_width = 23
                self.primitive_bitwidth = 32
                self.exponent_bias = 127
            elif name == 'fp64':
                self.fp_mantissa_width = 53
                self.primitive_bitwidth = 64
                self.exponent_bias = 1023
            else:
                raise RuntimeError(f'Unsupported floating-point type {name}')
        elif name == 'void':
            self.primitive_bitwidth = 0

    def is_fp8(self):
        return 'fp8' in self.name

    def is_fp8e4(self):
        return self.name == 'fp8e4'

    def is_fp8e5(self):
        return self.name == 'fp8e5'

    def is_fp8e4b15(self):
        return self.name == 'fp8e4b15'

    def is_fp16(self):
        return self.name == 'fp16'

    def is_bf16(self):
        return self.name == 'bf16'

    def is_fp32(self):
        return self.name == 'fp32'

    def is_fp64(self):
        return self.name == 'fp64'

    def is_int1(self):
        return self.name == 'int1'

    def is_int4(self):
        return self.name == 'int4'

    def is_int8(self):
        return self.name == 'int8'

    def is_int16(self):
        return self.name == 'int16'

    def is_int32(self):
        return self.name == 'int32'

    def is_int64(self):
        return self.name == 'int64'

    def is_uint4(self):
        return self.name == 'uint4'

    def is_uint8(self):
        return self.name == 'uint8'

    def is_uint16(self):
        return self.name == 'uint16'

    def is_uint32(self):
        return self.name == 'uint32'

    def is_uint64(self):
        return self.name == 'uint64'

    def is_floating(self):
        return self.name in dtype.FP_TYPES

    def is_standard_floating(self):
        return self.name in dtype.STANDARD_FP_TYPES

    def is_int_signed(self):
        return self.name in dtype.SINT_TYPES

    def is_int_unsigned(self):
        return self.name in dtype.UINT_TYPES

    def is_int(self):
        return self.name in dtype.SINT_TYPES + dtype.UINT_TYPES

    def is_bool(self):
        return self.is_int1()

    @staticmethod
    def is_void():
        raise RuntimeError("Not implemented")

    @staticmethod
    def is_block():
        return False

    @staticmethod
    def is_ptr():
        return False

    def __eq__(self, other: dtype):
        if not isinstance(other, dtype):
            return False
        return self.name == other.name

    def __ne__(self, other: dtype):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.name,))

    @property
    def scalar(self):
        return self

    def to_ir(self, builder: ir.builder) -> ir.type:
        if self.name == 'void':
            return builder.get_void_ty()
        elif self.name == 'int1':
            return builder.get_int1_ty()
        elif self.name in 'int4':
            return builder.get_int4_ty()
        elif self.name in 'uint4':
            if self.allow_ir_unsigned:
                return builder.get_uint4_ty()
            else:
                return builder.get_int4_ty()
        elif self.name in 'int8':
            return builder.get_int8_ty()
        elif self.name in 'uint8':
            if self.allow_ir_unsigned:
                return builder.get_uint8_ty()
            else:
                return builder.get_int8_ty()
        elif self.name in 'int16':
            return builder.get_int16_ty()
        elif self.name in 'uint16':
            if self.allow_ir_unsigned:
                return builder.get_uint16_ty()
            else:
                return builder.get_int16_ty()
        elif self.name in 'int32':
            return builder.get_int32_ty()
        elif self.name in 'uint32':
            if self.allow_ir_unsigned:
                return builder.get_uint32_ty()
            else:
                return builder.get_int32_ty()
        elif self.name in 'int64':
            return builder.get_int64_ty()
        elif self.name in 'uint64':
            if self.allow_ir_unsigned:
                return builder.get_uint64_ty()
            else:
                return builder.get_int64_ty()
        elif self.name == 'fp8e5':
            return builder.get_fp8e5_ty()
        elif self.name == 'fp8e4':
            return builder.get_fp8e4_ty()
        elif self.name == 'fp8e4b15':
            return builder.get_fp8e4b15_ty()
        elif self.name == 'fp16':
            return builder.get_half_ty()
        elif self.name == 'bf16':
            return builder.get_bf16_ty()
        elif self.name == 'fp32':
            return builder.get_float_ty()
        elif self.name == 'fp64':
            return builder.get_double_ty()
        raise ValueError(f'fail to convert {self} to ir type')

    def __str__(self):
        return self.name

    @property
    def cache_key_part(self) -> str:
        """See cache_key_part() in ppl.cc."""
        return self.name

    def __repr__(self):
        return f'ppl.language.{self.name}'


class pointer_type(dtype):
    def __init__(self, element_ty: dtype, address_space: int = 1):
        if not isinstance(element_ty, dtype):
            raise TypeError('element_ty is a {type(element_ty).__name__}.')
        self.element_ty = element_ty
        self.address_space = address_space

        self.name = self.__str__()

    def to_ir(self, builder: ir.builder) -> ir.pointer_type:
        return builder.get_ptr_ty(self.element_ty.to_ir(builder), 1)

    def __str__(self):
        return f'pointer<{self.element_ty}>'

    def __repr__(self):
        return self.__str__()

    def is_ptr(self):
        return True

    def __eq__(self, other: pointer_type) -> bool:
        if not isinstance(other, pointer_type):
            return False
        return self.element_ty == other.element_ty and self.address_space == other.address_space

    def __ne__(self, other: pointer_type) -> bool:
        return not self.__eq__(other)

    @property
    def scalar(self):
        return self


class block_type(dtype):
    def __init__(self, element_ty: dtype, shape: List):
        self.element_ty = element_ty

        # Note that block_type's shape is a list of int
        # while tensor's shape is a list of constexpr.

        # shape can be empty ([]) when an input is a 0D tensor.
        if not shape:
            raise TypeError('0d block_type is forbidden')
        if isinstance(shape[0], constexpr):
            shape = [s.value for s in shape]

        self.shape = shape
        self.numel = 1
        for s in self.shape:
            self.numel *= s
        if self.numel > PPL_MAX_TENSOR_NUMEL:
            raise ValueError(f"numel ({self.numel}) exceeds ppl maximum tensor numel ({PPL_MAX_TENSOR_NUMEL})")

        self.name = self.__str__()

    def to_ir(self, builder: ir.builder) -> ir.block_type:
        return builder.get_block_ty(self.element_ty.to_ir(builder), self.shape)

    def __str__(self):
        return f'<{self.shape}, {self.element_ty}>'

    def __repr__(self):
        return self.__str__()

    def is_block(self):
        return True

    def get_block_shapes(self) -> List[int]:
        return self.shape

    def __eq__(self, other: block_type) -> bool:
        if not isinstance(other, block_type):
            return False
        return self.element_ty == other.element_ty and self.shape == other.shape

    def __ne__(self, other: block_type) -> bool:
        return not self.__eq__(other)

    @property
    def scalar(self):
        return self.element_ty


class function_type(dtype):
    def __init__(self, ret_types: List[dtype], param_types: List[dtype]) -> None:
        self.ret_types = ret_types
        self.param_types = param_types

    def __str__(self):
        return f'fn ({self.param_types}) -> {self.ret_types}'

    def to_ir(self, builder: ir.builder):
        ir_param_types = [ty.to_ir(builder) for ty in self.param_types]
        ret_types = [ret_type.to_ir(builder) for ret_type in self.ret_types]
        return builder.get_function_ty(ir_param_types, ret_types)


# scalar types
void = dtype('void')
int1 = dtype('int1')
int4 = dtype('int4')
int8 = dtype('int8')
int16 = dtype('int16')
int32 = dtype('int32')
int64 = dtype('int64')
uint4 = dtype('uint4')
uint8 = dtype('uint8')
uint16 = dtype('uint16')
uint32 = dtype('uint32')
uint64 = dtype('uint64')
float8e5 = dtype('fp8e5')
float8e4 = dtype('fp8e4')
float8e4b15 = dtype('fp8e4b15')
float16 = dtype('fp16')
bfloat16 = dtype('bf16')
float32 = dtype('fp32')
float64 = dtype('fp64')
# pointer types
pvoid_t = pointer_type(void)
pi1_t = pointer_type(int1)
pi4_t = pointer_type(int4)
pi8_t = pointer_type(int8)
pi16_t = pointer_type(int16)
pi32_t = pointer_type(int32)
pi64_t = pointer_type(int64)
pu4_t = pointer_type(uint4)
pu8_t = pointer_type(uint8)
pu16_t = pointer_type(uint16)
pu32_t = pointer_type(uint32)
pu64_t = pointer_type(uint64)
pfp8e4_t = pointer_type(float8e4)
pfp8e5_t = pointer_type(float8e5)
pfp8e4b15_t = pointer_type(float8e4b15)
pfp16_t = pointer_type(float16)
pbf16_t = pointer_type(bfloat16)
pfp32_t = pointer_type(float32)
pfp64_t = pointer_type(float64)
# mtype
GLOBAL = mtype('GLOBAL')
L2 = mtype('L2')
LOCAL = mtype('LOCAL')
RM_HALF_TO_EVEN = round_mode('RM_HALF_TO_EVEN')
RM_HALF_AWAY_FROM_ZERO = round_mode('RM_HALF_AWAY_FROM_ZERO')
RM_TOWARDS_ZERO = round_mode('RM_TOWARDS_ZERO')
RM_DOWN = round_mode('RM_DOWN')
RM_UP = round_mode('RM_UP')
RM_HALF_UP = round_mode('RM_HALF_UP')
RM_HALF_DOWN = round_mode('RM_HALF_DOWN')
CONTINUOUS = align_mode('CONTINUOUS')
TPU_ALIGN = align_mode('TPU_ALIGN')
TPU_COMPACT = align_mode('TPU_COMPACT')
TPU_ROW_ALIGN = align_mode('TPU_ROW_ALIGN')
NONE_ALIGN = align_mode('NONE_ALIGN')
EXP = coeff_table_mode('EXP')
LOG = coeff_table_mode('LOG')
SIN = coeff_table_mode('SIN')
COS = coeff_table_mode('COS')
TAN = coeff_table_mode('TAN')
ARCSIN = coeff_table_mode('ARCSIN')
ERF_TAYLOR = coeff_table_mode('ERF_TAYLOR')
NC_TRANS=transpose_mode('NC_TRANS')
CW_TRANS=transpose_mode('CW_TRANS')
# -----------------------
# constexpr
# -----------------------


class constexpr:
    """
    This class is used to store a value that is known at compile-time.
    """

    def __init__(self, value):
        if isinstance(value, constexpr):
            self.value = value.value
        else:
            self.value = value

    def __repr__(self) -> str:
        return f"constexpr[{self.value}]"

    def __index__(self):
        return self.value

    def __add__(self, other):
        return constexpr(self.value + other.value)

    def __radd__(self, other):
        return constexpr(other.value + self.value)

    def __sub__(self, other):
        return constexpr(self.value - other.value)

    def __rsub__(self, other):
        return constexpr(other.value - self.value)

    def __mul__(self, other):
        return constexpr(self.value * other.value)

    def __mod__(self, other):
        return constexpr(self.value % other.value)

    def __rmul__(self, other):
        return constexpr(other.value * self.value)

    def __truediv__(self, other):
        return constexpr(self.value / other.value)

    def __rtruediv__(self, other):
        return constexpr(other.value / self.value)

    def __floordiv__(self, other):
        return constexpr(self.value // other.value)

    def __rfloordiv__(self, other):
        return constexpr(other.value // self.value)

    def __gt__(self, other):
        return constexpr(self.value > other.value)

    def __rgt__(self, other):
        return constexpr(other.value > self.value)

    def __ge__(self, other):
        return constexpr(self.value >= other.value)

    def __rge__(self, other):
        return constexpr(other.value >= self.value)

    def __lt__(self, other):
        return constexpr(self.value < other.value)

    def __rlt__(self, other):
        return constexpr(other.value < self.value)

    def __le__(self, other):
        return constexpr(self.value <= other.value)

    def __rle__(self, other):
        return constexpr(other.value <= self.value)

    def __eq__(self, other):
        return constexpr(self.value == other.value)

    def __ne__(self, other):
        return constexpr(self.value != other.value)

    def __bool__(self):
        return bool(self.value)

    def __neg__(self):
        return constexpr(-self.value)

    def __and__(self, other):
        return constexpr(self.value & other.value)

    def logical_and(self, other):
        return constexpr(self.value and other.value)

    def __or__(self, other):
        return constexpr(self.value | other.value)

    def __xor__(self, other):
        return constexpr(self.value ^ other.value)

    def logical_or(self, other):
        return constexpr(self.value or other.value)

    def __pos__(self):
        return constexpr(+self.value)

    def __invert__(self):
        return constexpr(~self.value)

    def __pow__(self, other):
        return constexpr(self.value ** other.value)

    def __rshift__(self, other):
        return constexpr(self.value >> other.value)

    def __lshift__(self, other):
        return constexpr(self.value << other.value)

    def __not__(self):
        return constexpr(not self.value)

    def __call__(self, *args, **kwds):
        return self.value(*args, **kwds)

class gtensor:
    def __init__(self, shape, mem: mtype, ptr=None, dtype=int32):
        # IR handle
        # self.handle = handle
        self.shape = shape
        # Block shape
        # self.shape = (1, )
        # if type.is_block():
        #     self.shape = type.shape
        self.mem = mem
        if ptr is None or isinstance(ptr, constexpr):
            self.dtype = semantic.get_scalar_dtype(dtype)
        else:
            #self.dtype = ptr.type.element_ty
            self.dtype = semantic.get_scalar_dtype(ptr.type)
        self.dtype.allow_ir_unsigned = True
        # self.type = ptr.type  # Tensor type (can be block_type)
        # Following the practice in pytorch, dtype is scalar type
        # self.shape = [constexpr(s) for s in self.shape]
        self.ptr = ptr

    def __str__(self) -> str:
        # ex. "float32[3,4]"
        return str(self.dtype) + '[' + ','.join(str(s) for s in self.shape) + ']'

    @property
    def T(self):
        assert False, "Transposition must be created by the AST Visitor"

    def create(self, _builder=None):
        return semantic.make_gtensor(self, _to_tensor(self.ptr, _builder), self.dtype.is_int_unsigned(), _builder)

    def sub_view(self, shape, offset, stride=None, _builder=None):
        return semantic.sub_view(self, shape, offset, stride, _builder)

class tensor:
    """Represents an N-dimensional array of values or pointers.

    :code:`tensor` is the fundamental data structure in ppl programs.  Most
    functions in :py:mod:`ppl.language` operate on and return tensors.

    :code:`tensor` also defines most of the magic/dunder methods, so you can
    write :code:`x+y`, :code:`x << 2`, etc.

    .. rubric:: Constructors
    ..
       For some reason Sphinx includes __init__ before printing the full table
       of methods.  Not what I want, but I can't figure out how to fix it.  Give
       it its own section so it looks intentional. :)
    """
    def __init__(self, handle, type: dtype):
        """Not called by user code."""
        # IR handle
        self.handle = handle
        # Block shape
        self.shape = (1, )
        if type.is_block():
            self.shape = type.shape
        self.numel = 1
        for s in self.shape:
            self.numel *= s
        self.numel = constexpr(self.numel)
        self.type = type  # Tensor type (can be block_type)
        # Following the practice in pytorch, dtype is scalar type
        self.dtype = type.scalar
        self.shape = [constexpr(s) for s in self.shape]
        self.dtype.allow_ir_unsigned = True

    def __str__(self) -> str:
        # ex. "float32[3,4]"
        return str(self.dtype) + '[' + ','.join(str(s) for s in self.shape) + ']'

    def sub_view(self, shape, offset, stride=None, _builder=None):
        return semantic.sub_view(self, shape, offset, stride, _builder)

    def view(self, shape, _builder=None):
        return semantic.view(self, shape, _builder)

    def set_dtype(self, type: dtype, _builder=None):
        assert self.type.is_ptr(), "just support pointer_type"
        assert type.is_ptr(), "just support pointer_type"
        self.type = type
        self.dtype = type.scalar

    @builtin
    def __add__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.add(None, self, other,
                            _to_tensor(0, _builder),
                            _to_tensor(_constexpr_to_value(RM_HALF_TO_EVEN).val(), _builder),
                            _to_tensor(False, _builder),
                            _builder)

    def __radd__(self, other, _builder=None):
        return self.__add__(other, _builder=_builder)

    @builtin
    def __sub__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.sub(None, self, other,
                            _to_tensor(0, _builder),
                            _to_tensor(_constexpr_to_value(RM_HALF_TO_EVEN).val(), _builder),
                            _to_tensor(False, _builder),
                            _builder)

    def __rsub__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.sub(None, other, self,
                            _to_tensor(0, _builder),
                            _to_tensor(_constexpr_to_value(RM_HALF_TO_EVEN).val(), _builder),
                            _to_tensor(False, _builder),
                            _builder)

    @builtin
    def __mul__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.mul(None, self, other,
                            _to_tensor(0, _builder),
                            _to_tensor(_constexpr_to_value(RM_HALF_TO_EVEN).val(), _builder),
                            _to_tensor(False, _builder),
                            _builder)

    def __rmul__(self, other, _builder=None):
        return self.__mul__(other, _builder=_builder)

    @builtin
    def __truediv__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.truediv(None, self, other, 3, _builder)

    def __rtruediv__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.truediv(None, other, self, 3, _builder)

    @builtin
    def __floordiv__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.floordiv(self, other, _builder)

    @builtin
    def __rfloordiv__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.floordiv(other, self, _builder)

    @builtin
    def __mod__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.mod(self, other, _builder)

    @builtin
    def __rmod__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.mod(other, self, _builder)

    # unary operators
    @builtin
    def __neg__(self, _builder=None):
        return semantic.minus(None, self, _builder)

    @builtin
    def __invert__(self, _builder=None):
        return semantic.invert(None, self, _builder)

    # bitwise operators

    @builtin
    def __and__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.and_(None, self, other, _builder)

    @builtin
    def __rand__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.and_(None, other, self, _builder)

    @builtin
    def __or__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.or_(None, self, other, _builder)

    @builtin
    def __ror__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.or_(None, other, self, _builder)

    @builtin
    def __xor__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.xor_(None, self, other, _builder)

    @builtin
    def __rxor__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.xor_(None, other, self, _builder)

    @builtin
    def __lshift__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.shift(None, self, other,
                             _to_tensor(_constexpr_to_value(RM_HALF_TO_EVEN).val(), _builder),
                             True, _builder)

    @builtin
    def __rshift__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.shift(None, self, other,
                             _to_tensor(_constexpr_to_value(RM_TOWARDS_ZERO).val(), _builder), False, _builder)

    # comparison operators

    # >
    @builtin
    def __gt__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.greater_than(None, self, other, _to_tensor(1, _builder), _builder)

    @builtin
    def __rgt__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.greater_than(None, other, self, _to_tensor(1, _builder), _builder)

    # >=
    @builtin
    def __ge__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.greater_equal(self, other, _builder)

    @builtin
    def __rge__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.greater_equal(other, self, _builder)

    # <
    @builtin
    def __lt__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.less_than(None, self, other, _to_tensor(1, _builder), _builder)

    @builtin
    def __rlt__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.less_than(None, other, self,  _to_tensor(1, _builder), _builder)

    # <=
    @builtin
    def __le__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.less_equal(self, other, _builder)

    @builtin
    def __rle__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.less_equal(other, self, _builder)

    # ==
    @builtin
    def __eq__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.equal(None, self, other,
                    _to_tensor(1, _builder), _builder)

    @builtin
    def __ne__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.not_equal(self, other, _builder)

    @builtin
    def logical_and(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.logical_and(self, other, _builder)

    @builtin
    def logical_or(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.logical_or(self, other, _builder)

    # note: __not__ isn't actually a magic method in python
    # but it's ok because our ASTVisitor handles it
    @builtin
    def __not__(self, _builder=None):
        return semantic.not_(None, self, _builder)

    def __get_dim__(self, dim: int, _builder):
        return semantic.get_dim(self, dim, _builder)

    @builtin
    def __getitem__(self, slices, _builder=None):
        if isinstance(slices, slice):
            slices = [slices]
        shape = []
        offset = []
        stride = None
        for dim, sl in enumerate(slices):
            if isinstance(sl, slice) and sl.start is None and sl.stop is None and sl.step is None:
                offset.append(0)
                shape.append(self.__get_dim__(dim, _builder))
            elif isinstance(sl, slice) and not sl.start is None and not sl.stop is None and sl.step is None:
                offset.append(sl.start)
                stop = _to_tensor(sl.stop, _builder)
                start = _to_tensor(sl.start, _builder)
                size = semantic.sub(None, stop, start,
                                    _to_tensor(0, _builder),
                                    _to_tensor(_constexpr_to_value(RM_HALF_TO_EVEN).val(), _builder),
                                    _to_tensor(False, _builder),
                                    _builder)
                shape.append(size)
        return semantic.sub_view(self, shape, offset, stride, _builder)

    @property
    def T(self):
        assert False, "Transposition must be created by the AST Visitor"

    @builtin
    def to(self, dtype, bitcast=False, _builder=None):
        if isinstance(bitcast, constexpr):
            bitcast = bitcast.value
        if bitcast:
            return semantic.bitcast(self, dtype, _builder)
        return semantic.cast(self, dtype, _builder)

class ctensor:
    def __init__(self, handle, type: dtype):
        # IR handle
        self.handle = handle
        # Block shape
        self.shape = (1, )
        if type.is_block():
            self.shape = type.shape
        self.numel = 1
        for s in self.shape:
            self.numel *= s
        self.numel = constexpr(self.numel)
        self.type = type  # Tensor type (can be block_type)
        # Following the practice in pytorch, dtype is scalar type
        self.dtype = type.scalar
        self.shape = [constexpr(s) for s in self.shape]

    def __str__(self) -> str:
        # ex. "float32[3,4]"
        return str(self.dtype) + '[' + ','.join(str(s) for s in self.shape) + ']'

    @builtin
    def __add__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.add(None, self, other, _to_tensor(0, _builder),
                            _to_tensor(_constexpr_to_value(RM_HALF_TO_EVEN).val(), _builder),
                            _to_tensor(False, _builder),
                            _builder)

    def __radd__(self, other, _builder=None):
        return self.__add__(other, _builder=_builder)

    @builtin
    def __sub__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.sub(None, self, other,
                            _to_tensor(0, _builder),
                            _to_tensor(_constexpr_to_value(RM_HALF_TO_EVEN).val(), _builder),
                            _to_tensor(False, _builder),
                            _builder)

    def __rsub__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.sub(None, other, self,
                            _to_tensor(0, _builder),
                            _to_tensor(_constexpr_to_value(RM_HALF_TO_EVEN).val(), _builder),
                            _to_tensor(False, _builder),
                            _builder)

    @builtin
    def __mul__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.mul(None, self, other,
                            _to_tensor(0, _builder),
                            _to_tensor(_constexpr_to_value(RM_HALF_TO_EVEN).val(), _builder),
                            _to_tensor(False, _builder),
                            _builder)

    def __rmul__(self, other, _builder=None):
        return self.__mul__(other, _builder=_builder)

    @builtin
    def __truediv__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.truediv(None, self, other, 3, _builder)

    def __rtruediv__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.truediv(None, other, self, 3, _builder)

    @builtin
    def __floordiv__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.floordiv(self, other, _builder)

    @builtin
    def __rfloordiv__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.floordiv(other, self, _builder)

    @builtin
    def __mod__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.mod(self, other, _builder)

    @builtin
    def __rmod__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.mod(other, self, _builder)

    # unary operators
    @builtin
    def __neg__(self, _builder=None):
        return semantic.minus(None, self, _builder)

    @builtin
    def __invert__(self, _builder=None):
        return semantic.invert(None, self, _builder)

    # bitwise operators

    @builtin
    def __and__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.and_(None, self, other, _builder)

    @builtin
    def __rand__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.and_(None, other, self, _builder)

    @builtin
    def __or__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.or_(None, self, other, _builder)

    @builtin
    def __ror__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.or_(None, other, self, _builder)

    @builtin
    def __xor__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.xor_(None, self, other, _builder)

    @builtin
    def __rxor__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.xor_(None, other, self, _builder)

    @builtin
    def __lshift__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.shift(None, self, other,
                            _to_tensor(_constexpr_to_value(RM_HALF_TO_EVEN).val(), _builder),
                            True, _builder)

    @builtin
    def __rshift__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.shift(None, self, other,
                            _to_tensor(_constexpr_to_value(RM_TOWARDS_ZERO).val(), _builder),
                            False, _builder)

    # comparison operators

    # >
    @builtin
    def __gt__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.greater_than(None, self, other, _to_tensor(1, _builder), _builder)

    @builtin
    def __rgt__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.greater_than(None, other, self, _to_tensor(1, _builder), _builder)

    # >=
    @builtin
    def __ge__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.greater_equal(self, other, _builder)

    @builtin
    def __rge__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.greater_equal(other, self, _builder)

    # <
    @builtin
    def __lt__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.less_than(None, self, other,  _to_tensor(1, _builder), _builder)

    @builtin
    def __rlt__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.less_than(None, other, self,  _to_tensor(1, _builder), _builder)

    # <=
    @builtin
    def __le__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.less_equal(self, other, _builder)

    @builtin
    def __rle__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.less_equal(other, self, _builder)

    # ==
    @builtin
    def __eq__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.equal(None, self, other,
                   _to_tensor(1, _builder), _builder)

    @builtin
    def __ne__(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.not_equal(self, other, _builder)

    @builtin
    def logical_and(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.logical_and(self, other, _builder)

    @builtin
    def logical_or(self, other, _builder=None):
        other = _to_tensor(other, _builder)
        return semantic.logical_or(self, other, _builder)

    # note: __not__ isn't actually a magic method in python
    # but it's ok because our ASTVisitor handles it
    @builtin
    def __not__(self, _builder=None):
        return semantic.not_(None, self, _builder)

    @builtin
    def __getitem__(self, slices, _builder=None):
        if isinstance(slices, slice):
            slices = [slices]
        ret = self
        for dim, sl in enumerate(slices):
            if isinstance(sl, constexpr) and sl.value is None:
                ret = semantic.expand_dims(ret, dim, _builder)
            elif isinstance(sl, slice) and sl.start is None and sl.stop is None and sl.step is None:
                pass
            else:
                assert False, f"unsupported tensor index: {sl}"
        return ret

    @property
    def T(self):
        assert False, "Transposition must be created by the AST Visitor"

    @builtin
    def to(self, dtype, bitcast=False, _builder=None):
        if isinstance(bitcast, constexpr):
            bitcast = bitcast.value
        if bitcast:
            return semantic.bitcast(self, dtype, _builder)
        return semantic.cast(self, dtype, _builder)


# -----------------------
# SPMD Programming Model
# -----------------------
def _constexpr_to_value(v):
    if isinstance(v, constexpr):
        return v.value
    return v

@builtin
def get_core_index(_builder=None):
    """
    在 kernel 函数中获取当前程序所运行核的索引,通常与 get_core_num 和 get_core_index 两个指令配合使用。

      .. code-block:: python

        index = get_core_index()
    """
    return semantic.get_core_index(_builder)

@builtin
def get_group_index(_builder=None):
    """
    在 kernel 函数中获取当前程序所运行group的索引,通常与 set_group_num 和 get_group_num 两个指令配合使用。

      .. code-block:: python

        index = get_group_index()
    """
    return semantic.get_group_index(_builder)

@builtin
def get_block_index(_builder=None):
    """
    在 kernel 函数中获取当前程序所运行block的索引,通常与 set_block_num 和 get_block_num 两个指令配合使用。

      .. code-block:: python

        index = get_block_index()
    """
    return semantic.get_block_index(_builder)


# -----------------------
# Non-Atomic Memory Operations
# -----------------------

@builtin
def num_programs(axis, _builder=None):
    """
    Returns the number of program instances launched along the given :code:`axis`.

    :param axis: The axis of the 3D launch grid. Has to be either 0, 1 or 2.
    :type axis: int
    """
    axis = _constexpr_to_value(axis)
    return semantic.num_programs(axis, _builder)


# -----------------------
# Block Initialization
# -----------------------


@builtin
def arange(start, end, _builder=None):
    """
    Returns contiguous values within the left-closed and right-open interval [:code:`start`, :code:`end`). \
    End - Start must be less than or equal to PPL_MAX_TENSOR_NUMEL = 131072

    :param start: Start of the interval. Must be a power of two.
    :type start: int32
    :param end: End of the interval. Must be a power of two > start.
    :type end: int32
    """
    start = _constexpr_to_value(start)
    end = _constexpr_to_value(end)
    return semantic.arange(start, end, _builder)


def _shape_check_impl(shape):
    shape = _constexpr_to_value(shape)
    for i, d in enumerate(shape):
        if not isinstance(d, constexpr):
            raise TypeError(f"Shape element {i} must have type `constexpr`")
        if not isinstance(d.value, int):
            raise TypeError(f"Shape element {i} must have type `constexpr[int]`, got `constexpr[{type(d.value)}]")
    return [_constexpr_to_value(x) for x in shape]

# -----------------------
# Shape Manipulation
# -----------------------


@builtin
def broadcast(input, other, _builder=None):
    """
    Tries to broadcast the two given blocks to a common compatible shape.

    :param input: The first input tensor.
    :type input: Block
    :param other: The second input tensor.
    :type other: Block
    """
    return semantic.broadcast_impl_value(input, other, _builder)


@builtin
def broadcast_to(input, shape, _builder=None):
    """
    Tries to broadcast the given tensor to a new :code:`shape`.

    :param input: The input tensor.
    :type input: Block
    :param shape: The desired shape.
    :type shape: Tuple[int]
    """
    shape = _shape_check_impl(shape)
    return semantic.broadcast_impl_shape(input, shape, _builder)


@builtin
def trans(input, _builder=None):
    return semantic.trans(input, _builder)


@builtin
def cat(input, other, can_reorder=False, _builder=None):
    """
    Concatenate the given blocks

    :param input: The first input tensor.
    :type input:
    :param other: The second input tensor.
    :type other:
    :param reorder: Compiler hint. If true, the compiler is
    allowed to reorder elements while concatenating inputs.
    Only use if the order does not matter (e.g., result is
    only used in reduction ops)
    """
    return semantic.cat(input, other, can_reorder, _builder)


@builtin
def view(input, shape, _builder=None):
    """
    Returns a tensor with the same elements as `input` but a different shape.
    The order of the elements may not be preserved.

    :param input: The input tensor.
    :type input:
    :param shape: The desired shape.
    :type shape: Tuple[int]

    """
    #shape = _shape_check_impl(shape)
    return semantic.view(input, shape, _builder)


@builtin
def reshape(input, shape, _builder=None):
    shape = _shape_check_impl(shape)
    return semantic.reshape(input, shape, _builder)


def _wrap_axis(axis, ndim):
    if not (-ndim <= axis < ndim):
        raise ValueError(f"invalid axis {axis}. Expected {-ndim} <= axis < {ndim}")

    return axis if axis >= 0 else axis + ndim


@builtin
def expand_dims(input, axis, _builder=None):
    """
    Expand the shape of a tensor, by inserting new length-1 dimensions.

    Axis indices are with respect to the resulting tensor, so
    ``result.shape[axis]`` will be 1 for each axis.

    :param input: The input tensor.
    :type input: pl.tensor
    :param axis: The indices to add new axes
    :type axis: int | Sequence[int]

    """
    axis = _constexpr_to_value(axis)
    axes = list(axis) if isinstance(axis, Sequence) else [axis]
    new_ndim = len(input.shape) + len(axes)
    axes = [_wrap_axis(_constexpr_to_value(d), new_ndim) for d in axes]

    if len(set(axes)) != len(axes):
        raise ValueError(f"expand_dims recieved duplicate axes, normalized axes = {axes}")

    ret = input
    for a in sorted(axes):
        ret = semantic.expand_dims(ret, a, _builder)
    return ret


@builtin
def make_block_ptr(base: tensor, shape, strides, offsets, block_shape, order, _builder=None):
    """
    Returns a pointer to a block in a parent tensor

    :param base: The base pointer to the parent tensor
    :param shape: The shape of the parent tensor
    :param strides: The strides of the parent tensor
    :param offsets: The offsets to the block
    :param block_shape: The shape of the block
    :param order: The order of the original data format
    """
    return semantic.make_block_ptr(base, shape, strides, offsets, block_shape, order, _builder)


@builtin
def advance(base: tensor, offsets, _builder=None):
    """
    Advance a block pointer

    :param base: the block pointer to advance
    :param offsets: the offsets to advance, a tuple by dimension
    """
    return semantic.advance(base, offsets, _builder)

# -----------------------
# Atomic Memory Operations
# -----------------------


def _add_atomic_docstr(name: str) -> Callable[[T], T]:

    def _decorator(func: T) -> T:
        docstr = """
    Performs an atomic {name} at the memory location specified by :code:`pointer`.

    Return the data stored at :code:`pointer` before the atomic operation.

    :param pointer: The memory locations to compare-and-swap.
    :type pointer: Block of dtype=ppl.PointerDType
    :param cmp: The values expected to be found in the atomic object
    :type cmp: Block of dtype=`pointer.dtype.element_ty`
    :param val: The values to copy in case the expected value matches the contained value.
    :type val: Block of dtype=`pointer.dtype.element_ty`
    """
        func.__doc__ = docstr.format(name=name)
        return func

    return _decorator


@builtin
@_add_atomic_docstr("compare-and-swap")
def atomic_cas(pointer, cmp, val, sem=None, _builder=None):
    cmp = _to_tensor(cmp, _builder)
    val = _to_tensor(val, _builder)
    sem = _constexpr_to_value(sem)
    return semantic.atomic_cas(pointer, cmp, val, sem, _builder)


@builtin
@_add_atomic_docstr("exchange")
def atomic_xchg(pointer, val, mask=None, sem=None, _builder=None):
    val = _to_tensor(val, _builder)
    sem = _constexpr_to_value(sem)
    return semantic.atomic_xchg(pointer, val, mask, sem, _builder)


@builtin
@_add_atomic_docstr("add")
def atomic_add(pointer, val, mask=None, sem=None, _builder=None):
    val = _to_tensor(val, _builder)
    sem = _constexpr_to_value(sem)
    return semantic.atomic_add(pointer, val, mask, sem, _builder)


@builtin
@_add_atomic_docstr("max")
def atomic_max(pointer, val, mask=None, sem=None, _builder=None):
    val = _to_tensor(val, _builder)
    sem = _constexpr_to_value(sem)
    return semantic.atomic_max(pointer, val, mask, sem, _builder)


@builtin
@_add_atomic_docstr("min")
def atomic_min(pointer, val, mask=None, sem=None, _builder=None):
    val = _to_tensor(val, _builder)
    sem = _constexpr_to_value(sem)
    return semantic.atomic_min(pointer, val, mask, sem, _builder)


@builtin
@_add_atomic_docstr("logical and")
def atomic_and(pointer, val, mask=None, sem=None, _builder=None):
    val = _to_tensor(val, _builder)
    sem = _constexpr_to_value(sem)
    return semantic.atomic_and(pointer, val, mask, sem, _builder)


@builtin
@_add_atomic_docstr("logical or")
def atomic_or(pointer, val, mask=None, sem=None, _builder=None):
    val = _to_tensor(val, _builder)
    sem = _constexpr_to_value(sem)
    return semantic.atomic_or(pointer, val, mask, sem, _builder)


@builtin
@_add_atomic_docstr("logical xor")
def atomic_xor(pointer, val, mask=None, sem=None, _builder=None):
    val = _to_tensor(val, _builder)
    sem = _constexpr_to_value(sem)
    return semantic.atomic_xor(pointer, val, mask, sem, _builder)


# -----------------------
# Conditioning
# -----------------------

@builtin
def where(condition, x, y, _builder=None):
    """
    Returns a tensor of elements from either :code:`x` or :code:`y`, depending on :code:`condition`.

    Note that :code:`x` and :code:`y` are always evaluated regardless of the value of :code:`condition`.

    If you want to avoid unintended memory operations, use the :code:`mask` arguments in `ppl.load` and `ppl.store` instead.

    The shape of :code:`x` and :code:`y` are both broadcast to the shape of :code:`condition`.
    :code:`x` and :code:`y` must have the same data type.

    :param condition: When True (nonzero), yield x, otherwise yield y.
    :type condition: Block of ppl.bool
    :param x: values selected at indices where condition is True.
    :param y: values selected at indices where condition is False.
    """
    condition = _to_tensor(condition, _builder)
    x = _to_tensor(x, _builder)
    y = _to_tensor(y, _builder)
    return semantic.where(condition, x, y, _builder)


# -----------------------
# Math
# -----------------------

@builtin
def umulhi(x, y, _builder=None):
    x = _to_tensor(x, _builder)
    y = _to_tensor(y, _builder)
    return semantic.umulhi(x, y, _builder)


def _add_math_1arg_docstr(name: str) -> Callable[[T], T]:

    def _decorator(func: T) -> T:
        docstr = """
    Computes the element-wise {name} of :code:`x`.

    :param x: the input values
    :type x: Block
    """
        func.__doc__ = docstr.format(name=name)
        return func

    return _decorator


@builtin
@_add_math_1arg_docstr("exponential")
def exp(x, _builder=None):
    return semantic.exp(x, _builder)


@builtin
@_add_math_1arg_docstr("natural logarithm")
def log(x, _builder=None):
    return semantic.log(x, _builder)


@builtin
@_add_math_1arg_docstr("cosine")
def cos(x, _builder=None):
    return semantic.cos(x, _builder)


@builtin
@_add_math_1arg_docstr("sine")
def sin(x, _builder=None):
    return semantic.sin(x, _builder)


@builtin
@_add_math_1arg_docstr("square root")
def sqrt(x, _builder=None):
    return semantic.sqrt(x, _builder)

# -----------------------
# Reductions
# -----------------------

def _add_reduction_docstr(name: str, return_indices_arg: str = None, tie_break_arg: str = None) -> Callable[[T], T]:

    def _decorator(func: T) -> T:
        docstr = """
    Returns the {name} of all elements in the :code:`input` tensor along the provided :code:`axis`

    :param input: the input values
    :param axis: the dimension along which the reduction should be done"""
        if return_indices_arg is not None:
            docstr += f"""
    :param {return_indices_arg}: if true, return index corresponding to the {name} value"""
        if tie_break_arg is not None:
            docstr += f"""
    :param {tie_break_arg}: if true, return the left-most indices in case of ties for values that aren't NaN"""

        func.__doc__ = docstr.format(name=name)
        return func

    return _decorator


@contextmanager
def _insertion_guard(builder):
    ip = builder.get_insertion_point()
    yield
    builder.restore_insertion_point(ip)


@builtin
def reduce(input, axis, combine_fn, _builder=None, _generator=None):
    """Applies the combine_fn to all elements in :code:`input` tensors along the provided :code:`axis`

    :param input: the input tensor, or tuple of tensors
    :param axis: the dimension along which the reduction should be done
    :param combine_fn: a function to combine two groups of scalar tensors (must be marked with @ppl.jit)

    """
    if isinstance(input, tensor):
        return reduce((input,), axis, combine_fn,
                      _builder=_builder, _generator=_generator)[0]

    def make_combine_region(reduce_op):
        in_scalar_tys = [t.type.scalar for t in input]
        prototype = function_type(in_scalar_tys, in_scalar_tys * 2)

        region = reduce_op.get_region(0)
        with _insertion_guard(_builder):
            param_types = [ty.to_ir(_builder) for ty in prototype.param_types]
            block = _builder.create_block_with_parent(region, param_types)
            args = [tensor(block.arg(i), ty)
                    for i, ty in enumerate(prototype.param_types)]
            results = _generator.call_JitFunction(combine_fn, args, kwargs={})
            if isinstance(results, tensor):
                handles = [results.handle]
            else:
                handles = [r.handle for r in results]
            _builder.create_reduce_ret(*handles)
    if axis is not None:
        axis = _constexpr_to_value(axis)
    return semantic.reduction(input, axis, make_combine_region, _builder)


@builtin
def _promote_reduction_input(t, _builder=None):
    scalar_ty = t.type.scalar
    # input is extended to 32-bits if necessary
    # this increases numerical accuracy and can be done pretty much for free
    # on GPUs
    if scalar_ty.is_int() and scalar_ty.int_bitwidth < 32:
        return t.to(int32, _builder=_builder)

    # hardware doesn't support FMAX, FMIN, CMP for bfloat16
    if scalar_ty is bfloat16:
        return t.to(float32, _builder=_builder)

    return t


@builtin
def _reduce_with_indices(input, axis, combine_fn, _builder=None, _generator=None):
    axis = _constexpr_to_value(axis)
    n = input.shape[axis]
    index = arange(0, n, _builder=_builder)

    if len(input.shape) > 1:
        # Broadcast index across the non-reduced axes
        axes_to_expand = [constexpr(d) for d in range(len(input.shape))]
        del axes_to_expand[axis]
        index = expand_dims(index, axes_to_expand, _builder=_builder)
        index = broadcast_to(index, input.shape, _builder=_builder)

    rvalue, rindices = reduce((input, index), axis, combine_fn,
                              _builder=_builder, _generator=_generator)
    return rvalue, rindices
'''
@jit
def minimum(x, y):
    """
    Computes the element-wise minimum of :code:`x` and :code:`y`.

    :param input: the first input tensor
    :type input: Block
    :param other: the second input tensor
    :type other: Block
    """
    return where(x < y, x, y)

@jit
def maximum(x, y):
    """
    Computes the element-wise maximum of :code:`x` and :code:`y`.

    :param input: the first input tensor
    :type input: Block
    :param other: the second input tensor
    :type other: Block
    """
    return where(x > y, x, y)
'''
# max and argmax


@jit
def _argmax_combine(value1, index1, value2, index2, tie_break_left):
    if tie_break_left:
        tie = value1 == value2 and index1 < index2
    else:
        tie = False
    gt = value1 > value2 or tie
    v_ret = where(gt, value1, value2)
    i_ret = where(gt, index1, index2)
    return v_ret, i_ret


@jit
def _argmax_combine_tie_break_left(value1, index1, value2, index2):
    return _argmax_combine(value1, index1, value2, index2, True)


@jit
def _argmax_combine_tie_break_fast(value1, index1, value2, index2):
    return _argmax_combine(value1, index1, value2, index2, False)


@jit
def _fast_max(x, y):
    return math.max(x, y)

'''
@jit
@_add_reduction_docstr("maximum",
                       return_indices_arg="return_indices",
                       tie_break_arg="return_indices_tie_break_left")
def max(input, axis=None, return_indices=False, return_indices_tie_break_left=True):
    input = _promote_reduction_input(input)
    if return_indices:
        if return_indices_tie_break_left:
            return _reduce_with_indices(input, axis, _argmax_combine_tie_break_left)
        else:
            return _reduce_with_indices(input, axis, _argmax_combine_tie_break_fast)
    else:
        if constexpr(input.dtype.primitive_bitwidth) < 32:
            if constexpr(input.dtype.is_floating()):
                input = input.to(float32)
            else:
                assert input.dtype.is_integer_type()
                input = input.to(int32)
        return reduce(input, axis, _fast_max)
'''

@jit
@_add_reduction_docstr("maximum index", tie_break_arg="tie_break_left")
def argmax(input, axis, tie_break_left=True):
    (_, ret) = max(input, axis, return_indices=True, return_indices_tie_break_left=tie_break_left)
    return ret

# min and argmin


@jit
def _argmin_combine(value1, index1, value2, index2, tie_break_left):
    if tie_break_left:
        tie = value1 == value2 and index1 < index2
    else:
        tie = False
    lt = value1 < value2 or tie
    value_ret = where(lt, value1, value2)
    index_ret = where(lt, index1, index2)
    return value_ret, index_ret


@jit
def _argmin_combine_tie_break_left(value1, index1, value2, index2):
    return _argmin_combine(value1, index1, value2, index2, True)


@jit
def _argmin_combine_tie_break_fast(value1, index1, value2, index2):
    return _argmin_combine(value1, index1, value2, index2, False)


@jit
def _fast_min(x, y):
    return math.min(x, y)

'''
@jit
@_add_reduction_docstr("minimum",
                       return_indices_arg="return_indices",
                       tie_break_arg="return_indices_tie_break_left")
def min(input, axis=None, return_indices=False, return_indices_tie_break_left=True):
    input = _promote_reduction_input(input)
    if return_indices:
        if return_indices_tie_break_left:
            return _reduce_with_indices(input, axis, _argmin_combine_tie_break_left)
        else:
            return _reduce_with_indices(input, axis, _argmin_combine_tie_break_fast)
    else:
        if constexpr(input.dtype.primitive_bitwidth) < 32:
            if constexpr(input.dtype.is_floating()):
                input = input.to(float32)
            else:
                assert input.dtype.is_integer_type()
                input = input.to(int32)
        return reduce(input, axis, _fast_min)
'''

@jit
@_add_reduction_docstr("minimum index",
                       tie_break_arg="tie_break_left")
def argmin(input, axis, tie_break_left=True):
    _, ret = min(input, axis, return_indices=True, return_indices_tie_break_left=tie_break_left)
    return ret


@jit
def _sum_combine(a, b):
    return a + b

# sum


@jit
@_add_reduction_docstr("sum")
def sum(input, axis=None):
    input = _promote_reduction_input(input)
    return reduce(input, axis, _sum_combine)


@jit
def _xor_combine(a, b):
    return a ^ b


# xor sum

@builtin
@_add_reduction_docstr("xor sum")
def xor_sum(input, axis=None, _builder=None, _generator=None):
    scalar_ty = input.type.scalar
    if not scalar_ty.is_int():
        raise ValueError("xor_sum only supported for integers")

    input = _promote_reduction_input(input, _builder=_builder)
    return reduce(input, axis, _xor_combine,
                  _builder=_builder, _generator=_generator)


# -----------------------
# Scans
# -----------------------

def _add_scan_docstr(name: str, return_indices_arg: str = None, tie_break_arg: str = None) -> Callable[[T], T]:

    def _decorator(func: T) -> T:
        docstr = """
    Returns the {name} of all elements in the :code:`input` tensor along the provided :code:`axis`

    :param input: the input values
    :param axis: the dimension along which the scan should be done"""
        func.__doc__ = docstr.format(name=name)
        return func

    return _decorator


@builtin
def associative_scan(input, axis, combine_fn, _builder=None, _generator=None):
    """Applies the combine_fn to each elements with a carry in :code:`input` tensors along the provided :code:`axis` and update the carry

    :param input: the input tensor, or tuple of tensors
    :param axis: the dimension along which the reduction should be done
    :param combine_fn: a function to combine two groups of scalar tensors (must be marked with @ppl.jit)

    """
    if isinstance(input, tensor):
        return associative_scan((input,), axis, combine_fn,
                                _builder=_builder, _generator=_generator)[0]

    def make_combine_region(scan_op):
        in_scalar_tys = [t.type.scalar for t in input]
        prototype = function_type(in_scalar_tys, in_scalar_tys * 2)

        region = scan_op.get_region(0)
        with _insertion_guard(_builder):
            param_types = [ty.to_ir(_builder) for ty in prototype.param_types]
            block = _builder.create_block_with_parent(region, param_types)
            args = [tensor(block.arg(i), ty)
                    for i, ty in enumerate(prototype.param_types)]
            results = _generator.call_JitFunction(combine_fn, args, kwargs={})
            if isinstance(results, tensor):
                handles = [results.handle]
            else:
                handles = [r.handle for r in results]
            _builder.create_scan_ret(*handles)
    axis = _constexpr_to_value(axis)
    return semantic.associative_scan(input, axis, make_combine_region, _builder)

# cumsum


@jit
@_add_scan_docstr("cumsum")
def cumsum(input, axis=0):
    # todo rename this to a generic function name
    input = _promote_reduction_input(input)
    return associative_scan(input, axis, _sum_combine)

# cumprod


@jit
def _prod_combine(a, b):
    return a * b


@jit
@_add_scan_docstr("cumprod")
def cumprod(input, axis=0):
    # todo rename this to a generic function name
    input = _promote_reduction_input(input)
    return associative_scan(input, axis, _prod_combine)

# -----------------------
# Compiler Hint Ops
# -----------------------


@builtin
def debug_barrier(_builder=None):
    '''
    Insert a barrier to synchronize all threads in a block.
    '''
    return semantic.debug_barrier(_builder)


@builtin
def multiple_of(input, values, _builder=None):
    """
    Let the compiler knows that the values in :code:`input` are all multiples of :code:`value`.
    """
    if isinstance(values, constexpr):
        values = [values]
    for i, d in enumerate(values):
        if not isinstance(d, constexpr):
            raise TypeError(f"values element {i} must have type `constexpr`")
        if not isinstance(d.value, int):
            raise TypeError(f"values element {i} must have type `constexpr[int]`, got `constexpr[{type(d.value)}]")
    values = [x.value for x in values]
    return semantic.multiple_of(input, values)


@builtin
def max_contiguous(input, values, _builder=None):
    """
    Let the compiler knows that the `value` first values in :code:`input` are contiguous.
    """
    if isinstance(values, constexpr):
        values = [values]
    for i, d in enumerate(values):
        if not isinstance(d, constexpr):
            raise TypeError(f"values element {i} must have type `constexpr`")
        if not isinstance(d.value, int):
            raise TypeError(f"values element {i} must have type `constexpr[int]`, got `constexpr[{type(d.value)}]")
    values = [x.value for x in values]
    return semantic.max_contiguous(input, values)


@builtin
def max_constancy(input, values, _builder=None):
    """
    Let the compiler knows that the `value` first values in :code:`input` are constant.

    e.g. if :code:`values` is [4], then each group of 4 values in :code:`input` should all be equal,
    for example [0, 0, 0, 0, 1, 1, 1, 1].
    """
    if isinstance(values, constexpr):
        values = [values]
    for i, d in enumerate(values):
        if not isinstance(d, constexpr):
            raise TypeError(f"values element {i} must have type `constexpr`")
        if not isinstance(d.value, int):
            raise TypeError(f"values element {i} must have type `constexpr[int]`, got `constexpr[{type(d.value)}]")
    values = [x.value for x in values]
    return semantic.max_constancy(input, values)
# -----------------------
# Debugging functions
# -----------------------


@builtin
def static_print(*values, sep: str = " ", end: str = "\n", file=None, flush=False, _builder=None):
    '''
    Print the values at compile time.  The parameters are the same as the builtin :code:`print`.

    NOTE: Calling the Python builtin :code:`print` is not the same as calling this, it instead maps to :code:`device_print`,
    which has special requirements for the arguments.

    .. highlight:: python
    .. code-block:: python

        pl.static_print(f"{BLOCK_SIZE=}")
    '''
    pass


@builtin
def static_assert(cond, msg="", _builder=None):
    '''
    Assert the condition at compile time.  Does not require that the :code:`PPL_DEBUG` environment variable
    is set.

    .. highlight:: python
    .. code-block:: python

        pl.static_assert(BLOCK_SIZE == 1024)
    '''
    pass


@builtin
def device_print(prefix, *args, _builder=None):
    '''
    Print the values at runtime from the device.  String formatting does not work for runtime values, so you should
    provide the values you want to print as arguments.  The first value must be a string, all following values must
    be scalars or tensors.

    Calling the Python builtin :code:`print` is the same as calling this function, and the requirements for the arguments will match
    this function (not the normal requirements for :code:`print`).

    .. highlight:: python
    .. code-block:: python

        pl.device_print("pid", pid)
        print("pid", pid)

    :param prefix: a prefix to print before the values. This is required to be a string literal.
    :param args: the values to print. They can be any tensor or scalar.
    '''
    import string
    prefix = _constexpr_to_value(prefix)
    assert isinstance(prefix, str), f"{prefix} is not string"
    b_ascii = True
    for ch in prefix:
        if ch not in string.printable:
            b_ascii = False
            break
    assert b_ascii, f"{prefix} is not an ascii string"
    new_args = []
    for arg in args:
        new_args.append(_to_tensor(arg, _builder))
    return semantic.device_print(prefix, new_args, _builder)


@builtin
def device_assert(cond, msg="", _builder=None):
    '''
    Assert the condition at runtime from the device.  Requires that the environment variable :code:`PPL_DEBUG`
    is set to a value besides :code:`0` in order for this to have any effect.

    Using the Python :code:`assert` statement is the same as calling this function, except that the second argument
    must be provided and must be a string, e.g. :code:`assert pid == 0, "pid != 0"`.  The environment variable must
    be set for this :code:`assert` statement to have any effect.

    .. highlight:: python
    .. code-block:: python

        pl.device_assert(pid == 0)
        assert pid == 0, f"pid != 0"

    :param cond: the condition to assert. This is required to be a boolean tensor.
    :param msg: the message to print if the assertion fails. This is required to be a string literal.
    '''
    msg = _constexpr_to_value(msg)
    import inspect
    frame = inspect.currentframe()
    module = inspect.getmodule(frame)
    # The ppl function module doesn't have the name attribute.
    # We use this trick to find the caller.
    while hasattr(module, "__name__"):
        frame = frame.f_back
        module = inspect.getmodule(frame)
    lineno = 0
    func_name = 'unknown'
    file_name = 'unknown'
    if frame is not None:
        func_name = frame.f_code.co_name
        file_name = frame.f_back.f_code.co_filename
        # TODO: The line number currently indicates the line
        # where the ppl function is called but not where the
        # device_assert is called. Need to enhance this.
        lineno = frame.f_back.f_lineno
    return semantic.device_assert(_to_tensor(cond, _builder), msg, file_name, func_name, lineno, _builder)


# -----------------------
# Iterators
# -----------------------


class static_range:

    """
    Iterator that counts upward forever.

    .. highlight:: python
    .. code-block:: python

        @ppl.jit
        def kernel(...):
            for i in pl.static_range(10):
                ...
    :note: This is a special iterator used to implement similar semantics to Python's :code:`range` in the context of
        :code:`ppl.jit` functions. In addition, it also guides the compiler to unroll the loop aggressively.
    :param arg1: the start value.
    :param arg2: the end value.
    :param step: the step value.
    """

    def __init__(self, arg1, arg2=None, step=None):
        assert isinstance(arg1, constexpr)
        if step is None:
            self.step = constexpr(1)
        else:
            assert isinstance(step, constexpr)
            self.step = step
        if arg2 is None:
            self.start = constexpr(0)
            self.end = arg1
        else:
            assert isinstance(arg2, constexpr)
            self.start = arg1
            self.end = arg2

    def __iter__(self):
        raise RuntimeError("static_range can only be used in @ppl.jit'd functions")

    def __next__(self):
        raise RuntimeError("static_range can only be used in @ppl.jit'd functions")


# -----------------------
# Extern functions
# -----------------------

def dispatch(func, lib_name: str, lib_path: str, args: list, arg_type_symbol_dict: dict, ret_shape: tuple, is_pure: bool, _builder=None):
    '''
        Dispatch a function to a library
        :param func: the function to dispatch
        :param lib_name: the name of the library
        :param lib_path: the path of the library
        :param args: the arguments of the function
        :param arg_type_symbol_dict: the type of the arguments
        :param ret_shape: the shape of the return value
        :param _builder: the builder
        :return: the return value of the function
    '''
    if len(arg_type_symbol_dict) == 0:
        raise ValueError("arg_type_symbol_dict is empty")

    num_args = len(list(arg_type_symbol_dict.keys())[0])
    if len(args) != num_args:
        raise ValueError(f"length of input args does not match."
                         f"Expect {len(args)}, got {num_args}")

    arg_types = []
    arg_list = []
    for arg in args:
        if isinstance(arg, tensor):
            arg_types.append(arg.dtype)
            arg_list.append(arg.handle)
        else:
            arg_types.append(type(arg))
            arg_list.append(arg)
    arg_types = tuple(arg_types)

    if arg_types not in arg_type_symbol_dict:
        raise ValueError(f"input arg type does not match."
                         f"Expect one of {arg_type_symbol_dict.keys()}, got {arg_types}")
    else:
        symbol = arg_type_symbol_dict[arg_types][0]
        ret_type = arg_type_symbol_dict[arg_types][1]
        if ret_shape:
            ret_type = block_type(ret_type, ret_shape)
        return tensor(func(lib_name, lib_path, symbol, arg_list, ret_type.to_ir(_builder), is_pure), ret_type)


def extern_elementwise(lib_name: str, lib_path: str, args: list, arg_type_symbol_dict: dict, is_pure: bool, _builder=None):
    '''
        Dispatch an elementwise function to a library
        :param lib_name: the name of the library
        :param lib_path: the path of the library
        :param args: the arguments of the function
        :param arg_type_symbol_dict: the type of the arguments
        :param is_pure: whether the function is pure
        :param _builder: the builder
        :return: the return value of the function
    '''
    dispatch_args = args.copy()
    all_scalar = True
    ret_shape = None
    arg_types = []
    for i in range(len(dispatch_args)):
        dispatch_args[i] = _to_tensor(dispatch_args[i], _builder)
        arg_types.append(dispatch_args[i].dtype)
        if dispatch_args[i].type.is_block():
            all_scalar = False
    if len(arg_types) > 0:
        arg_types = tuple(arg_types)
        arithmetic_check = True
        # If there's a type tuple that is not supported by the library, we will do arithmetic check
        if arg_types in arg_type_symbol_dict:
            arithmetic_check = False
        broadcast_arg = dispatch_args[0]
        # Get the broadcast shape over all the arguments
        for i, item in enumerate(dispatch_args):
            _, broadcast_arg = semantic.binary_op_type_checking_impl(
                item, broadcast_arg, _builder, arithmetic_check=arithmetic_check)
        # Change the shape of each argument based on the broadcast shape
        for i in range(len(dispatch_args)):
            dispatch_args[i], _ = semantic.binary_op_type_checking_impl(
                dispatch_args[i], broadcast_arg, _builder, arithmetic_check=arithmetic_check)
        if not all_scalar:
            ret_shape = broadcast_arg.shape
    func = getattr(_builder, "create_extern_elementwise")
    return dispatch(func, lib_name, lib_path, dispatch_args, arg_type_symbol_dict, ret_shape, is_pure, _builder)


def extern(fn):
    """A decorator for external functions."""
    return builtin(fn)

@builtin
def make_tensor(mem_shape, dtype, tensor_shape=None, align_mode=TPU_ALIGN, _builder=None):
    """
    主要作用是创建一个 tensor, 然后可以对tensor执行view或sub_view等操作

        .. code-block:: python

            dst = make_tensor(mem_shape, dtype, tensor_shape, align_mode)

    参数:
        - ``mem_shape`` (`dim4`):  tensor的memory shape

        - ``dtype`` (`pl.dtype`): 张量元素的数据类型

        - ``tensor_shape`` (`dim4或None`):  tensor的实际shape

        - ``align_mode`` (`pl.align_mode`):  数据排布方式, 默认为TPU_ALIGN
    返回值:
        - ``dst`` (`ppl.language.tensor`):  dst在local memory上的张量

    注意事项:
        无
    """
    dtype = semantic.get_scalar_dtype(dtype)
    mem_shape = _constexpr_to_value(mem_shape)
    tensor_shape = _constexpr_to_value(tensor_shape)
    align_mode = _constexpr_to_value(align_mode).val()
    return semantic.make_tensor(mem_shape, tensor_shape, dtype, dtype.is_int_unsigned(), align_mode, _builder)

@builtin
def make_gtensor_permute(mem_shape, mem_stride, dtype, addr, order, mode=GLOBAL, _builder=None):
    """
    根据 order 的设定顺序,修改 mem_shape,并根据修改后的 shape 生成 global/L2 mem 上的 tensor;
    order 默认 mem_shape 不变

        .. code-block:: python

            dst = make_gtensor_permute(mem_shape, mem_stride, dtype, addr, order, mode)

    参数:
        - ``mem_shape`` (`dim4`):  tensor的memory shape

        - ``mem_stride`` (`dim4`):  memory shape的stride

        - ``dtype`` (`pl.dtype`): 张量元素的数据类型

        - ``addr`` (`pl.pointer_type`): 在global/L2上数据的地址

        - ``order`` (`dim4`):  permute的order

        - ``mode`` (`pl.mtype`):  Global或L2

    返回值:
        - ``dst`` (`ppl.language.tensor`):  dst在global memory上的张量

    注意事项:
        无
    """
    dtype = semantic.get_scalar_dtype(dtype)
    assert(len(mem_shape) == 4)
    assert(len(order) == 4)
    stride_permute = []
    for i, item in enumerate(mem_shape):
        mem_shape[i] = _to_tensor(item, _builder)

    stride_permute.append(mem_stride[order[0]])
    stride_permute.append(mem_stride[order[1]])
    stride_permute.append(mem_stride[order[2]])
    stride_permute.append(mem_stride[order[3]])
    shape_permute=[]
    shape_permute.append(mem_shape[order[0]])
    shape_permute.append(mem_shape[order[1]])
    shape_permute.append(mem_shape[order[2]])
    shape_permute.append(mem_shape[order[3]])
    g_tensor = gtensor(shape_permute, mode, addr).create(_builder)
    return g_tensor.sub_view(shape_permute, None, stride_permute, _builder)

@builtin
def get_eu_num(type:pl.dtype, _builder=None):
    """
    获取当前数据类型 (pl.dtype) 所对应的 eu 数

        .. code-block:: python

            num = get_eu_num(type)

    参数:
        - ``type`` (`pl.dtype`): pl.dtype数据类型

    返回值:
        eu数
    """
    return semantic.get_eu_num(type, _builder)

@builtin
def get_nic(type:pl.dtype, _builder=None):
    """
    获取当前数据类型 (pl.dtype) 应该对齐的 ic 数

        .. code-block:: python

            num = get_nic(type)

    参数:
        - ``type`` (`pl.dtype`): pl.dtype数据类型

    返回值:
        对齐的 ic数
    """
    dtype = semantic.get_scalar_dtype(type)
    nic = 1
    if dtype.is_fp32() or dtype.is_int32() or dtype.is_uint32():
        nic = 1
    elif dtype.is_bf16() or dtype.is_fp16() or dtype.is_int16() or dtype.is_uint16():
        other = _to_tensor(2, _builder)
        nic = semantic.floordiv(semantic.lane_num(_builder), other, _builder)
    elif dtype.is_int8() or dtype.is_uint8() or dtype.is_fp8():
        nic = semantic.lane_num(_builder)
    elif dtype.is_int4() or dtype.is_uint4():
        arch = os.getenv("CHIP", default="bm1684x")
        if arch == "bm1688":
            other = _to_tensor(2, _builder)
            nic = semantic.mul(None, semantic.lane_num(_builder), other,
                            _to_tensor(0, _builder),
                            _to_tensor(_constexpr_to_value(RM_HALF_TO_EVEN).val(), _builder),
                            _to_tensor(False, _builder),
                            _builder)
        else:
            assert False, "don't support int4 conv"
    else:
        other = _to_tensor(2, _builder)
        nic = semantic.mul(None, semantic.lane_num(_builder), other,
                            _to_tensor(0, _builder),
                            _to_tensor(_constexpr_to_value(RM_HALF_TO_EVEN).val(), _builder),
                            _to_tensor(False, _builder),
                            _builder)
    return _to_tensor(nic, _builder)

@builtin
def lane_num(_builder=None):
    """
    获取当前芯片的lane个数

        .. code-block:: python

            num = lane_num()

    参数:
        无

    返回值:
        lane个数
    """
    return semantic.lane_num(_builder)

lane_num.alias = 'LANE_NUM'
globals()[lane_num.alias] = lane_num

@builtin
def enable_pipeline(_builder=None):
    """
    开启 ppl 流水优化的指令,写在需要进行流水优化的 for 循环内部

        .. code-block:: python

            enable_pipeline()
    """
    return semantic.enable_pipeline(_builder)

@builtin
def set_core_num(core_num:int,
                _builder=None):
    """
    设置在 num 个核上并行运行 kernel 函数, 通常与 get_core_num 和 get_core_index 两个指令配合使用

      .. code-block:: python

        set_core_num(core_num)
    """
    return semantic.set_core_num(core_num,
                                _builder)

@builtin
def get_core_num(_builder=None):
    """
    在 kernel 函数中获取使用了多少个核, 通常与 set_core_num 和 get_core_index 两个指令配合使用

      .. code-block:: python

        num = get_core_num()
    """
    return semantic.get_core_num(_builder)

@builtin
def set_group_num(group_num:int,
                _builder=None):
    """
    设置在 num 个group上并行运行 kernel 函数, 通常与 get_group_num 和 get_group_index 两个指令配合使用

      .. code-block:: python

        set_core_num(core_num)
    """
    return semantic.set_group_num(group_num, _builder)

@builtin
def get_group_num(_builder=None):
    """
    在 kernel 函数中获取使用了多少个group, 通常与 set_group_num 和 get_group_index 两个指令配合使用

      .. code-block:: python

        num = get_group_num()
    """
    return semantic.get_group_num(_builder)

@builtin
def set_block_num(block_num:int,
                _builder=None):
    """
    设置在 num 个block上并行运行 kernel 函数, 通常与 get_block_num 和 get_block_index 两个指令配合使用

      .. code-block:: python

        set_block_num(core_num)
    """
    return semantic.set_block_num(block_num, _builder)

@builtin
def get_block_num(_builder=None):
    """
    在 kernel 函数中获取在当前group中使用了多少个block, 通常与 set_block_num 和 get_block_index 两个指令配合使用

      .. code-block:: python

        num = get_block_num()
    """
    return semantic.get_block_num(_builder)
'''
@builtin
def tpu_sync_core(_builder=None):
    return semantic.tpu_sync_core(_builder)
'''
@builtin
def sync(_builder=None):
    """
    同步所有设备

      .. code-block:: python

         sync()
    """
    return semantic.sync(_builder)

@builtin
def hau_poll(_builder=None):
    """
    阻塞设备,直至该语句之前的 hau 操作结束

      .. code-block:: python

         hau_poll()
    """
    return semantic.hau_poll(_builder)

@builtin
def tpu_poll(_builder=None):
    """
    阻塞设备,直至该语句之前的所有操作结束

      .. code-block:: python

         tpu_poll()
    """
    return semantic.tpu_poll(_builder)

@builtin
def msg_send(msg_idx:int,
             wait_cnt:int,
             is_dma:bool,
            _builder=None):
    """
    通过消息同步机制进行多核间的同步操作

        .. code-block:: python

            msg_send(msg_idx, wait_cnt, is_dma)

    参数:
        - ``msg_idx`` (`int`): message index

        - ``wait_cnt`` (`int`): 等待该 message index 的操作个数

        - ``is_dma`` (`int`): 是否应用于 dma

    返回值:
        无

    注意事项:
        该指令仅支持 SG2380
    """
    return semantic.msg_send(_to_tensor(_constexpr_to_value(msg_idx), _builder),
                            _to_tensor(_constexpr_to_value(wait_cnt), _builder),
                            _to_tensor(_constexpr_to_value(is_dma), _builder),
                            _builder)

@builtin
def msg_wait(msg_idx:int,
            send_cnt:int,
            is_dma:bool,
            _builder=None):
    """
    通过消息同步机制进行多核间的同步操作

        .. code-block:: python

            msg_wait(msg_idx, send_cnt, is_dma)

    参数:
        - ``msg_idx`` (`int`): message index

        - ``send_cnt`` (`int`): 需要等待该 message index 发送的次数

        - ``is_dma`` (`int`): 是否应用于 dma

    返回值:
        无

    注意事项:
        该指令仅支持 SG2380
    """
    return semantic.msg_wait(_to_tensor(_constexpr_to_value(msg_idx), _builder),
                            _to_tensor(_constexpr_to_value(send_cnt), _builder),
                            _to_tensor(_constexpr_to_value(is_dma), _builder),
                            _builder)

@builtin
def fence(_builder=None):
    """
    用于保证该指令前序所有 MOV 读写指令(load/store/cache)比该指令后序所有 MOV 读写指令更早被观察到

        .. code-block:: python

            fence()
    参数:
        无

    返回值:
        无

    注意事项:
        该指令仅支持 SG2380
    """
    return semantic.fence(_builder)

@builtin
def lane_mask(mask:int,
            long_valid:bool,
            _builder=None):
    """
    TIU LANE 写屏蔽指令,mask 每个 bit 代表 1 个 Lane,当 bit 为 0 时则屏蔽 TIU 写对应的 Lane;
    long_valid 为 1 则,mask 将影响后续所有的 TIU 指令;
    如果为 0 则只影响后续的第一条 TIU 指令

        .. code-block:: python

            lane_mask(mask, long_valid)
    参数:
        - ``mask`` (`int`): 写屏蔽mask

        - ``long_valid`` (`bool`): 影响后续所有的 TIU 指令的标志

    返回值:
        无

    注意事项:
        该指令仅支持 SG2380
    """
    return semantic.lane_mask(_to_tensor(_constexpr_to_value(mask), _builder),
                            _to_tensor(_constexpr_to_value(long_valid), _builder),
                            _builder)

@builtin
def vset(v_idx:int,
        lmul:int,
        v_len:int,
        _builder=None):
    """
    设置 vector 寄存器的使用状态

        .. code-block:: python

            vset(v_idx, lmul, v_len)
    参数:
        - ``v_idx`` (`int`): vector 寄存器中储存的数据的位数

        - ``lmul`` (`int`): 绑定使用的 vector 寄存器个数

        - ``v_len`` (`int`): 每个 vector 寄存器上存储的元素个数

    返回值:
        无

    注意事项:
        a.该指令仅支持 SG2380
        b.v_idx 的可取值为 8、16、32。
        c.使用 vector 寄存器时,其索引必须是 vset 设置中 lmul 的整数倍
    """
    return semantic.vset(_to_tensor(_constexpr_to_value(v_idx), _builder),
                        _to_tensor(_constexpr_to_value(lmul), _builder),
                         _to_tensor(_constexpr_to_value(v_len), _builder),
                        _builder)

@builtin
def get_scalar_dtype(dtype:pl.dtype, _builder=None):
    """
    获取张量或pointer_type中元素的标量数据类型

        .. code-block:: python

            scalar_type = get_scalar_dtype(dtype)
    参数:
        - ``dtype`` (`pl.dtype`): 张量类型或pointer_type

    返回值:
        - ``scalar_type`` (`pl.dtype`): 张量或pointer_type中元素的标量数据类型

    注意事项:
        无
    """
    return semantic.get_scalar_dtype(dtype)

