#pragma once
#include "mlir/Dialect/EmitC/IR/EmitC.h"
#include "mlir/Dialect/Func/IR/FuncOps.h"
#include "mlir/IR/MLIRContext.h"
#include "mlir/IR/TypeUtilities.h"
#include "mlir/Support/IndentedOstream.h"
#include "mlir/Transforms/DialectConversion.h"
#include "ppl/Dialect/Ppl/IR/Dialect.h"
#include "ppl/Support/ModuleEnum.h.inc"
#include <functional>
#include <initializer_list>
#include <iostream>

using namespace mlir;
extern int PplErrorCode;

namespace mlir {
namespace ppl {
static std::unique_ptr<ModuleOp> gModule = nullptr;
static std::unique_ptr<Chip> gChip = nullptr;

template <typename U, typename V>
static inline auto
ceiling_func(U numerator, V denominator) -> decltype(numerator + denominator) {
  return (numerator + denominator - 1) / denominator;
}

template <typename U, typename V>
static inline auto align_up(U x, V a) -> decltype(x + a) {
  return ceiling_func(x, a) * a;
}

enum read_mode_t {
  BINARY = 0,
  NPY = 1,
  NPZ = 2,
};

enum mem_type_t {
  GLOBAL = 0,
  LOCAL = 1,
  CONST = 2,
  CONST_QUANT = 3,
};

enum arith_mode_t {
  ARITH_AND = 0,
  ARITH_OR = 1,
  ARITH_XOR = 2,
  ARITH_MIN = 3,
  ARITH_MAX = 4,
  ARITH_ADD = 5,
  ARITH_SUB = 6,
  ARITH_MUL = 7,
  ARITH_DIV = 8,
  ARITH_DIFF_ABS = 9,
  ARITH_MAC = 10,
};

enum comparision_mode_t {
  GREATER = 0,
  LESS = 1,
  EQUAL = 2,
  NOT_EQUAL = 3,
  GREATER_EQUAL = 4,
  LESS_EQUAL = 5,
};

enum pool_mode_t {
  FpAvgPool2D = 0,
  Fp8Int8AvgPool2D = 1,
  FpInsAvgPool2D = 2,
  Int8InsAvgPool2D = 3,
  MaxPool2D = 4,
  MinPool2D = 5,
};

enum IOType {
  PARAM = 0,
  OUTPUT = 1,
  INPUT = 2,
};

enum AlignType {
  CONTINUOUS,
  TPU_ALIGN,
  TPU_COMPACT,
  TPU_ROW_ALIGN,
  NONE_ALIGN,
};

enum InstructType {
  SYNC_INST = 0,
  TIU_DMA_INST = 1,
  SDMA_INST = 2,
  HAU_INST = 3
};

enum SyncType { TIU_DMA_SYNC = 0x1, SDMA_SYNC = 0x10, HAU_SYNC = 0x100 };

enum DataType {
  DT_NONE = 0,
  DT_FP32,
  DT_FP16,
  DT_BFP16,
  DT_FP8E5M2,
  DT_FP8E4M3,
  DT_FP20,
  DT_TF32,
  DT_INT32,
  DT_UINT32,
  DT_INT16,
  DT_UINT16,
  DT_INT8,
  DT_UINT8,
  DT_INT4,
  DT_UINT4,
  DT_INT64,
  DT_UINT64,
};

struct DataKind {
  DataKind() {}
  DataKind(DataType _dtype) : dtype(_dtype) {
    switch (_dtype) {
    case DT_FP32:
      dtype_name = "DT_FP32";
      is_fp = true;
      dtype_bits = 32;
      break;
    case DT_FP16:
      dtype_name = "DT_FP16";
    case DT_BFP16:
      dtype_name = "DT_BFP16";
      is_fp = true;
      is_f16 = true;
      dtype_bits = 16;
      break;
    case DT_FP8E5M2:
      dtype_name = "DT_FP8E5M2";
    case DT_FP8E4M3:
      dtype_name = "DT_FP8E4M3";
      is_fp = true;
      is_f8 = true;
      dtype_bits = 8;
      break;
    case DT_INT64:
      dtype_name = "DT_INT64";
      is_signed = true;
    case DT_UINT64:
      dtype_name = "DT_UINT64";
      is_unsigned = true;
      is_int = true;
      is_int64 = true;
      dtype_bits = 64;
      break;
    case DT_INT32:
      dtype_name = "DT_INT32";
      is_signed = true;
    case DT_UINT32:
      dtype_name = "DT_UINT32";
      is_unsigned = true;
      is_int = true;
      is_int32 = true;
      dtype_bits = 32;
      break;
    case DT_INT16:
      dtype_name = "DT_INT16";
      is_signed = true;
    case DT_UINT16:
      dtype_name = "DT_UINT16";
      is_unsigned = true;
      is_int = true;
      is_int16 = true;
      dtype_bits = 16;
      break;
    case DT_INT8:
      dtype_name = "DT_INT8";
      is_signed = true;
    case DT_UINT8:
      dtype_name = "DT_UINT8";
      is_unsigned = true;
      is_int = true;
      is_int8 = true;
      dtype_bits = 8;
      break;
    case DT_INT4:
      dtype_name = "DT_INT4";
      is_signed = true;
    case DT_UINT4:
      dtype_name = "DT_UINT4";
      is_unsigned = true;
      is_int = true;
      is_int4 = true;
      dtype_bits = 4;
      break;
    default:
      break;
    }
  }
  std::string dtype_name;
  DataType dtype = DT_NONE;
  int dtype_bits;
  bool is_signed = false;
  bool is_unsigned = false;
  bool is_int = false;
  bool is_int64 = false;
  bool is_int32 = false;
  bool is_int16 = false;
  bool is_int8 = false;
  bool is_int4 = false;
  bool is_fp = false;
  bool is_f16 = false;
  bool is_f8 = false;
  operator std::string() const { return dtype_name; }
};

enum RunMode {
  PioMode = 0,
  MlirMode = 1,
  TorchMode = 2,
  TorchPythonMode = 3,
};

struct TranslateOption {
  std::string file_name;
  std::string output_path;
  std::string host_func_name;
  RunMode mode = PioMode; // 0-pio 1-mlir 2-torch-cxx 3-torch-python
  bool gen_test = false;
  bool gen_kernel_wrap = false;
  bool gen_ref = false;
  bool is_test = false;
  bool no_gen_dir = false;
  bool gen_profile = false;
};


bool operator==(const DataKind &d1, const DataKind &d2);

bool operator!=(const DataKind &d1, const DataKind &d2);

inline std::ostream &operator<<(std::ostream &os, const DataKind &kind) {
  os << kind.dtype_name;
  return os;
}

//-----------------------------------------------------------------
// Helper for get/set original value
//-----------------------------------------------------------------
Value getOriValue(Value v);

//-----------------------------------------------------------------
// Helper get ModuleOp
//-----------------------------------------------------------------
ModuleOp getModuleOp(Value v);

ModuleOp getModuleOp(Operation *op);

bool isNone(Value v);

//-----------------------------------------------------------------
// Helper for interpreter
//-----------------------------------------------------------------

template <typename T>
inline std::function<T(T, T)> select_arith_operation(int mode) {
  auto min_operation = [](T lhs, T rhs) { return std::min(lhs, rhs); };
  auto max_operation = [](T lhs, T rhs) { return std::max(lhs, rhs); };
  auto and_operation = [](T lhs, T rhs) { return ((int)lhs & (int)rhs); };
  auto or_operation = [](T lhs, T rhs) { return ((int)lhs | (int)rhs); };
  auto xor_operation = [](T lhs, T rhs) { return ((int)lhs ^ (int)rhs); };
  auto add_operation = [](T lhs, T rhs) { return lhs + rhs; };
  auto sub_operation = [](T lhs, T rhs) { return lhs - rhs; };
  auto mul_operation = [](T lhs, T rhs) { return lhs * rhs; };
  auto diff_abs_operation = [](T lhs, T rhs) { return std::fabs(lhs - rhs); };
  auto none_operation = [](T lhs, T rhs) { return -1; };

  switch (mode) {
  case ARITH_MIN:
    return min_operation;
  case ARITH_MAX:
    return max_operation;
  case ARITH_AND:
    return and_operation;
  case ARITH_OR:
    return or_operation;
  case ARITH_XOR:
    return xor_operation;
  case ARITH_ADD:
    return add_operation;
  case ARITH_SUB:
    return sub_operation;
  case ARITH_MUL:
    return mul_operation;
  case ARITH_DIFF_ABS:
    return diff_abs_operation;
  default:
    std::cout << "Error: unsupported arith mode type!" << std::endl;
    std::exit(EXIT_FAILURE);
    return none_operation;
  }
}

inline std::function<float(float, float, float)>
select_cmp_operation(int mode) {
  auto equal_operation = [](float lhs, float rhs, float true_val) -> float {
    if (std::abs(lhs - rhs) < 1e-5) {
      return true_val;
    }
    return 0.0f;
  };
  auto greater_operation = [](float lhs, float rhs, float true_val) -> float {
    if (lhs > rhs) {
      return true_val;
    }
    return 0.0f;
  };
  auto less_operation = [](float lhs, float rhs, float true_val) -> float {
    if (lhs < rhs) {
      return true_val;
    }
    return 0.0f;
  };
  auto none_operation = [](float lhs, float rhs, float true_val) -> float {
    return -1.0f;
  };

  switch (mode) {
  case EQUAL:
    return equal_operation;
  case GREATER:
    return greater_operation;
  case LESS:
    return less_operation;
  default:
    std::cout << "Error: unsupported arith mode type!" << std::endl;
    std::exit(EXIT_FAILURE);
    return none_operation;
  }
}

//-----------------------------------------------------------------
// Helper for format string
// A python style string format function.
//-----------------------------------------------------------------
/**
 * @param fmt_spec format specification that use "{}" as placeholder
 * @param args values corresponding to "{}" in previous specification
 *
 * @returns new string that replace all "{}" with its corresponding value
 */
static void buildFormatString(std::ostringstream &builder,
                              const std::string &fmt_spec,
                              std::string::size_type idx) {
  builder.write(fmt_spec.data() + idx, fmt_spec.size() - idx);
}

template <typename T, typename... Types>
static void buildFormatString(std::ostringstream &builder,
                              const std::string &fmt_spec,
                              std::string::size_type idx, const T &first,
                              const Types &...args) {
  auto pos = fmt_spec.find("{}", idx);
  int nofargs = sizeof...(args);
  if (pos == std::string::npos) {
    assert(nofargs == 0 && "Too many args for format string.");
    builder.write(fmt_spec.data() + idx, fmt_spec.size() - idx);
    return;
  }
  bool is_last = fmt_spec.find("{}", pos + 2) == std::string::npos;
  if (is_last) {
    assert(nofargs == 0 && "Too many args for format string");
  } else {
    assert(nofargs != 0 && "Not enough args for format string.");
  }
  builder.write(fmt_spec.data() + idx, pos - idx);
  builder << first;
  buildFormatString(builder, fmt_spec, pos + 2, args...);
}

template <typename... Types>
static std::string formatString(const std::string &fmt_spec,
                                const Types &...args) {
  std::ostringstream builder;
  buildFormatString(builder, fmt_spec, 0, args...);
  return builder.str();
}

static std::string get_scalar_var_tpl(const std::string &type_fmt) {
  std::string var_tpl;
  if (type_fmt == "DT_INT32")
    var_tpl = "{}.s32 = {};\n";
  else if (type_fmt == "DT_INT16")
    var_tpl = "{}.s32 = {};\n";
  else if (type_fmt == "DT_INT8")
    var_tpl = "{}.s32 = {};\n";
  else if (type_fmt == "DT_UINT32")
    var_tpl = "{}.u32 = {};\n";
  else if (type_fmt == "DT_UINT16")
    var_tpl = "{}.u32 = {};\n";
  else if (type_fmt == "DT_UINT8")
    var_tpl = "{}.u32 = {};\n";
  else if (type_fmt == "DT_FP32")
    var_tpl = "{}.f32 = {};\n";
  else if (type_fmt == "DT_FP16")
    var_tpl = "{}.f32 = {};\n";
  else if (type_fmt == "DT_BFP16")
    var_tpl = "{}.f32 = {};\n";
  return var_tpl;
}

static inline std::string getPointNameOrNull(const Value &&v,
                                             const std::string &&name) {
  if (isNone(v)) {
    return "NULL";
  } else {
    return "&" + name;
  }
};

//-----------------------------------------------------------------
// Helper for chip
//-----------------------------------------------------------------
struct Attr {
  static constexpr llvm::StringRef CHIP = "module.chip";
};

void setChip(ModuleOp op, Chip chip);

Chip getChip(Operation *op);

Chip getChip(Value v);

bool isCV18xx(Chip chip);

bool isCV18xx(Operation *op);

//-----------------------------------------------------------------
// Helper for address assign
//-----------------------------------------------------------------

int64_t getAddress(Operation *op);

std::vector<Operation *> getNestedOpNoRecursive(Operation *op);

template <typename T>
int64_t calcOffset(std::vector<T> &offset, std::vector<T> &stride) {
  assert(offset.size() == stride.size());
  int64_t length = 0;
  for (size_t i = 0; i < offset.size(); ++i) {
    length += offset[i] * stride[i];
  }
  return length;
}

Type getElementType(const mlir::Value &value);

func::ReturnOp getAssumedUniqueReturnOp(func::FuncOp funcOp);

bool isEuAlign(Value v);

bool isRowAlign(Value v);

bool isCompactAlign(Value v);

int64_t getMemrefSize(const MemRefType type);

int64_t getAffineIndices(const AffineMap map);

int64_t getMemIndices(mlir::Operation::operand_range indexes);

bool isTestFunc(const func::FuncOp &op);

bool isKernelFunc(const func::FuncOp &op);

bool isAutotuneFunc(const func::FuncOp &op);

bool isDynBlockFunc(func::FuncOp &op);

bool isDim(ShapeOp &op, std::string &name);

bool isRefFunc(const func::FuncOp &op);

Value getOriTensorValue(Value v);

int getCoreNum(Operation *op);
int getCoreNum(Operation *op, int default_num);
int getBlockGroupInfo(Operation *op, std::string param_name, int default_num=1);

void setCoreNum(Operation *op, int32_t core_num);
void setBlockGroupInfo(Operation *op, std::string param_name, int32_t num);

func::FuncOp getFuncOp(func::CallOp &callOp);

std::string getFuncOriName(Operation *op);

std::string getFuncSymbol(Operation *op);

template <typename T> bool isTargetTensor(T op, TensorMode mode) {
  TensorInterface tensorOp;
  if constexpr (std::is_same_v<T, Value>) {
    tensorOp = dyn_cast<TensorInterface>(getOriValue(op).getDefiningOp());
    assert(tensorOp);
  } else if constexpr (std::is_same_v<T, Operation *>) {
    tensorOp = dyn_cast_or_null<TensorInterface>(op);
    assert(tensorOp);
  } else {
    tensorOp = dyn_cast_or_null<TensorInterface>(op.getOperation());
    assert(tensorOp);
  }
  return tensorOp.getTensorMode() == mode;
}

template <typename T> bool isLocalTensor(T op) {
  return isTargetTensor(op, TensorMode::LOCAL);
}

template <typename T> bool isL2Tensor(T op) {
  return isTargetTensor(op, TensorMode::L2);
}

template <typename T> bool isGlobalTensor(T op) {
  return isTargetTensor(op, TensorMode::GLOBAL);
}

// 0-teew 1-subtype
static std::vector<int> getTeewAndSubtype(const DataKind &dtype) {
  std::vector<int> rst(2);
  switch (dtype.dtype_bits) {
  case 8:
    rst[0] = 0;
    break;
  case 16:
    rst[0] = 1;
    break;
  case 32:
    rst[0] = 2;
    break;
  case 4:
    rst[0] = 5;
    break;
  default:
    assert(0 && "not supported dtype");
    break;
  }
  if (dtype.is_int) {
    if (dtype.is_signed) {
      rst[1] = 1;
    } else {
      rst[1] = 0;
    }
  } else {
    if (dtype.dtype == DT_BFP16) {
      rst[1] = 1;
    } else {
      rst[1] = 0;
    }
  }
  return rst;
}

#define MASK_SELECT_PRIORITY 3
#define VC_PRIORITY 2
#define HIGH_PRIORITY 1
#define LOW_PRIORITY 0
#define DELTA 25000
// #define MAX_SIGNED_VAL (llvm::APInt::getSignedMaxValue(32).getSExtValue() -
// DELTA)
#define MAX_SIGNED_VAL 3 * DELTA
using ListKey =
    std::list<std::tuple<Value, int32_t, int32_t, std::optional<AffineMap>,
                         std::optional<std::vector<Value>>>>;
using MapKey = llvm::SmallVector<ListKey, 4>;

Value getSrcGTensorOrShape(Value &src);
void recordCandidates(MapKey &candidate_list, const Value &rhs,
                      std::optional<std::vector<Value>>, int priority,
                      int start, int end);
MapKey &getCandidateList(Value v, llvm::DenseMap<Operation *, MapKey> &lists);

bool isReshapeOp(Operation *op);

bool isSubViewOp(Operation *op);

void dma_common_process(
    const Value &v, Operation *op, MapKey &candidate_list,
    const std::function<void(MapKey &, const Value &,
                             std::optional<std::vector<Value>>, int, int, int)>
        &process,
    std::optional<std::vector<Value>> in2 = std::nullopt,
    int priority = HIGH_PRIORITY, int start = 0, int end = 4);

void common_process(const Value &v, Operation *op, MapKey &candidate_list,
                    const std::function<void(MapKey &, const Value &,
                                             std::optional<std::vector<Value>>,
                                             int, int, int)> &process,
                    std::optional<std::vector<Value>> in2 = std::nullopt,
                    int priority = HIGH_PRIORITY, int start = 0, int end = 4,
                    int result_index = 0);
void poolShapeInference(Operation *op, MapKey &candidate_list);
int32_t getActualCoreNum(Operation *op);

int getConstantIntValue(Value v, int default_val);

float getConstantFloatValue(Value v, float default_val);

#define assertOpError(cond, op, msg)                                           \
  if (!(cond)) {                                                               \
    op->emitOpError(msg);                                                      \
    assert(0);                                                                 \
  }

bool checkBc(OpOperand &lhs, OpOperand &rhs, SmallVector<int64_t, 4> &lhs_bc,
             SmallVector<int64_t, 4> &rhs_bc);

int getTensorAlign(Value v);

int getTensorAlign(Operation *op);

template <typename T> bool isDefaultStride(T op) {
  TensorInterface tensorOp;
  if constexpr (std::is_same_v<T, Value>) {
    tensorOp = dyn_cast<TensorInterface>(getOriValue(op).getDefiningOp());
    assert(tensorOp);
  } else if constexpr (std::is_same_v<T, Operation *>) {
    tensorOp = dyn_cast_or_null<TensorInterface>(op);
    assert(tensorOp);
  } else {
    tensorOp = dyn_cast_or_null<TensorInterface>(op.getOperation());
    assert(tensorOp);
  }
  if (isLocalTensor(tensorOp)) {
    return tensorOp.getAlignMode() == TPU_ALIGN;
  } else {
    return tensorOp.getAlignMode() == CONTINUOUS;
  }
}

bool isNICLayout(Chip chip, Value v, const DataKind &dtype);

bool isMatrixLayout(Value v);

bool isVectorLayout(Value v);

std::vector<int> getUnsigedIdx(Operation *op);

DataKind getDataType(Value v, Operation *op = nullptr,
                     mlir::ArrayRef<int> unsignedIdx = std::vector<int>());
void findCallOpsInFuncOp(func::FuncOp funcOp,
                         std::vector<func::CallOp> &callOps);

Value createCheckTensorZero(Operation *op, std::vector<Value> &shape,
                            mlir::IRRewriter &rewriter);

bool isConstant(Value v);

} // namespace ppl
} // namespace mlir
