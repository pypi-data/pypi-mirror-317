#pragma once
#include "mlir/Dialect/Arith/IR/Arith.h"
#include "mlir/Dialect/ControlFlow/IR/ControlFlowOps.h"
#include "mlir/Dialect/Func/IR/FuncOps.h"
#include "mlir/Dialect/SCF/IR/SCF.h"
#include "mlir/IR/BuiltinOps.h"
#include "mlir/IR/BuiltinTypes.h"
#include "mlir/IR/Dialect.h"
#include "mlir/Support/IndentedOstream.h"
#include "mlir/Transforms/DialectConversion.h"
#include "ppl/Support/RegConfigMethod.h"
#include "llvm/ADT/DenseMap.h"
#include "llvm/ADT/ScopedHashTable.h"
#include "llvm/ADT/StringExtras.h"
#include "llvm/ADT/StringMap.h"
#include "llvm/ADT/TypeSwitch.h"
#include "llvm/Support/Debug.h"
#include "llvm/Support/Format.h"
#include "llvm/Support/FormatVariadic.h"
#include <stack>

using llvm::formatv;
namespace mlir {
namespace ppl {

typedef enum {
  HOST = 0,
  HOST_HEADER,
  KERNEL,
  MAIN,
  MAIN_REF,
  DYN_HEADER,
  DYN_SRC,
  DESC_HOST,
  DESC_HOST_HEADER,
  DESC_KERNEL,
  AUTOTUNE,
  AUTOTUNE_TEST,
  HOST_MEM,
  TORCH_WRAP,
  UNSUPPORT
} file_type_t;

/// Convenience functions to produce interleaved output with functions returning
/// a LogicalResult. This is different than those in STLExtras as functions used
/// on each element doesn't return a string.
template <typename ForwardIterator, typename UnaryFunctor,
          typename NullaryFunctor>
inline LogicalResult
interleaveWithError(ForwardIterator begin, ForwardIterator end,
                    UnaryFunctor eachFn, NullaryFunctor betweenFn) {
  if (begin == end)
    return success();
  if (failed(eachFn(*begin)))
    return failure();
  ++begin;
  for (; begin != end; ++begin) {
    betweenFn();
    if (failed(eachFn(*begin)))
      return failure();
  }
  return success();
}

template <typename Container, typename UnaryFunctor, typename NullaryFunctor>
inline LogicalResult interleaveWithError(const Container &c,
                                         UnaryFunctor eachFn,
                                         NullaryFunctor betweenFn) {
  return interleaveWithError(c.begin(), c.end(), eachFn, betweenFn);
}

template <typename Container, typename UnaryFunctor>
inline LogicalResult interleaveCommaWithError(const Container &c,
                                              raw_ostream &os,
                                              UnaryFunctor eachFn) {
  return interleaveWithError(c.begin(), c.end(), eachFn, [&]() { os << ", "; });
}

/// Emitter that uses dialect specific emitters to emit C++ code.
struct CEmitter {
  explicit CEmitter(llvm::raw_fd_ostream &os, file_type_t file_type,
                    bool declareVariablesAtTop);

  /// Emits attribute or returns failure.
  LogicalResult emitAttribute(Location loc, Attribute attr);

  //   /// Emits operation 'op' with/without training semicolon or returns
  //   failure.
  // // LogicalResult emitOperation(Operation &op, EmitFunc func, bool
  // trailingSemicolon); LogicalResult emitOperation(EmitFunc func, bool
  // trailingSemicolon);

  // LogicalResult emitOperation(Operation &op, bool trailingSemicolon);

  /// Emits type 'type' or returns failure.
  LogicalResult emitType(Location loc, Type type, Value v = nullptr,
                         bool emitPoint = true, bool unsigned_flag = false);
  LogicalResult emitTorchWrapType(Location loc, Type type, bool emitPoint);
  LogicalResult emitFuncArgType(Location loc, Value v,
                                StringRef custom_type = "",
                                bool unsigned_flag = false,
                                bool is_torch_wrap = false);

  LogicalResult emitStructArgType(Location loc, Value v, StringRef argName,
                                  StringRef custom_type, bool unsigned_flag,
                                  bool is_torch_wrap = false);

  /// Emits array of types as a std::tuple of the emitted types.
  /// - emits void for an empty array;
  /// - emits the type of the only element for arrays of size one;
  /// - emits a std::tuple otherwise;
  LogicalResult emitTypes(Location loc, ArrayRef<Type> types);

  /// Emits array of types as a std::tuple of the emitted types independently of
  /// the array size.
  LogicalResult emitTupleType(Location loc, ArrayRef<Type> types);

  /// Emits an assignment for a variable which has been declared previously.
  LogicalResult emitVariableAssignment(OpResult result);

  /// Emits a variable declaration for a result of an operation.
  LogicalResult emitVariableDeclaration(OpResult result, bool trailingSemicolon,
                                        bool unsigend_flag = false);

  /// Emits the variable declaration and assignment prefix for 'op'.
  /// - emits separate variable followed by std::tie for multi-valued operation;
  /// - emits single type followed by variable for single result;
  /// - emits nothing if no value produced by op;
  /// Emits final '=' operator where a type is produced. Returns failure if
  /// any result type could not be converted.
  LogicalResult emitAssignPrefix(Operation &op, bool unsigend_flag = false);

  /// Emits a label for the block.
  LogicalResult emitLabel(Block &block);

  /// Emits the operands and atttributes of the operation. All operands are
  /// emitted first and then all attributes in alphabetical order.
  LogicalResult emitOperandsAndAttributes(Operation &op,
                                          ArrayRef<StringRef> exclude = {});

  /// Emits the operand of the operation.
  LogicalResult emitOperand(Value &result);

  /// Emits the operands of the operation. All operands are emitted in order.
  LogicalResult emitOperands(Operation &op);

  /// Return the existing or a new name for a Value.
  std::string getOrCreateName(Value val);

  // Emits declaration of call extern-function
  LogicalResult emitExDeclaration(func::FuncOp &func);

  /// Return the existing or a new name for tmp variable.
  std::string getOrCreateTmpVarName(Value val, std::string ext, Block *block);

  /// Return the new name for tmp variable.
  std::string getTmpVarName(Value val, std::string ext, Block *block);

  bool isTemVariableDefined(Value val, std::string ext, Block *block);

  /// Return the existing or a new label of a Block.
  StringRef getOrCreateName(Block &block);

  /// Whether to map an mlir integer to a unsigned integer in C++.
  bool shouldMapToUnsigned(IntegerType::SignednessSemantics val);

  std::string emitScalar(const Value &v, Block *block, const DataKind &dtype);

  std::string getTensorStridePointNameOrNull(const Value &v, Block *block);
  std::string getTensorBcStrideName(const Value &v, DenseI64ArrayAttr &bc,
                                    Block *block);

  std::string getTensorShapeName(const Value &v);

  std::string getTensorAddrName(const Value &v);

  std::string getVariableTName(const Value &v, Block *block,
                               const DataKind &dtype, const std::string &type);

  template <typename iterator>
  LogicalResult emitArgBase(Location loc, const std::string &addr_name,
                            const std::set<int> &unsigned_idxes,
                            iterator arg_begin, iterator arg_end, int mode,
                            bool is_torch_wrap = false) {
    // mode 0-func 1-struct
    auto eachfn = [&](BlockArgument arg) -> LogicalResult {
      bool unsigned_flag = false;
      if (unsigned_idxes.count(arg.getArgNumber())) {
        unsigned_flag = true;
      }
      if (mode == 0) {
        if (failed(emitFuncArgType(loc, arg, addr_name, unsigned_flag,
                                   is_torch_wrap)))
          return failure();
      } else if (mode == 1) {
        if (failed(emitStructArgType(loc, arg, getOrCreateName(arg), addr_name,
                                     unsigned_flag, is_torch_wrap)))
          return failure();
      } else {
        return failure();
      }
      if (mode == 0) {
        ostream() << " " << getOrCreateName(arg);
      }
      return success();
    };
    if (failed(interleaveWithError(arg_begin, arg_end, eachfn, [&]() {
          if (mode == 0) {
            os << ", ";
          } else if (mode == 1) {
            os << ";\n";
          }
        }))) {
      return failure();
    }
    return success();
  }
  template <typename iterator>
  LogicalResult emitFuncArg(Location loc, const std::string &addr_name,
                            const std::set<int> &unsigned_idxes,
                            iterator arg_begin, iterator arg_end,
                            bool is_torch_wrap = false) {
    return emitArgBase(loc, addr_name, unsigned_idxes, arg_begin, arg_end, 0,
                       is_torch_wrap);
  }
  LogicalResult emitFuncArg(Location loc, const std::string &addr_name,
                            const std::set<int> &unsigned_idxes,
                            const Region::BlockArgListType &args,
                            bool is_torch_wrap = false) {
    return emitFuncArg(loc, addr_name, unsigned_idxes, args.begin(), args.end(),
                       is_torch_wrap);
  }

  template <typename iterator>
  LogicalResult emitStructArg(Location loc, const std::string &addr_name,
                              const std::set<int> &unsigned_idxes,
                              iterator arg_begin, iterator arg_end,
                              bool is_torch_wrap = false) {
    return emitArgBase(loc, addr_name, unsigned_idxes, arg_begin, arg_end, 1,
                       is_torch_wrap);
  }
  LogicalResult emitStructArg(Location loc, const std::string &addr_name,
                              const std::set<int> &unsigned_idxes,
                              const Region::BlockArgListType &args,
                              bool is_torch_wrap = false) {
    return emitStructArg(loc, addr_name, unsigned_idxes, args.begin(),
                         args.end(), is_torch_wrap);
  }

  /// RAII helper function to manage entering/exiting C++ scopes.
  struct Scope {
    Scope(CEmitter &emitter)
        : valueMapperScope(emitter.valueMapper),
          blockMapperScope(emitter.blockMapper), emitter(emitter) {
      emitter.valueInScopeCount.push(emitter.valueInScopeCount.top());
      emitter.labelInScopeCount.push(emitter.labelInScopeCount.top());
    }
    ~Scope() {
      emitter.valueInScopeCount.pop();
      emitter.labelInScopeCount.pop();
    }

  private:
    llvm::ScopedHashTableScope<Value, std::string> valueMapperScope;
    llvm::ScopedHashTableScope<Block *, std::string> blockMapperScope;
    CEmitter &emitter;
  };

  /// Returns wether the Value is assigned to a C++ variable in the scope.
  bool hasValueInScope(Value val);

  // Returns whether a label is assigned to the block.
  bool hasBlockLabel(Block &block);

  /// Returns the output stream.
  raw_indented_ostream &ostream() { return this->os; };

  /// Returns if all variables for op results and basic block arguments need
  /// to be declared at the beginning of a function.
  bool shouldDeclareVariablesAtTop() { return declareVariablesAtTop; };

  file_type_t file_type;

  /// Boolean to record if need gen autotune_test in call emmiter
  bool autotune;

  /// emit the mem or const of sg2380(0-gmem 1-lmem 2-const)
  /// emit the mem or const of sg2380(0-gmem 1-lmem 2-const)
  int emitMem(Value &val, mem_type_t tensor_mode, raw_indented_ostream &os,
              Block *block, int need_reset, DenseI64ArrayAttr bc = {},
              DataKind dtype = DataKind(), int multiplier = 0, int shift = 0,
              int yzp = 0);

  int emitValueSerialNum(Value &val, mem_type_t tensor_mode) {
    return regConfigger.getValueSerialNum(val, tensor_mode);
  }

  /// emit the scalar or mem of sg2380
  int emitScalarOrMem(Value &val, std::string &func_name,
                      std::vector<std::string> &check_shape,
                      raw_indented_ostream &os, Block *block,
                      bool is_final_operand, int need_reset,
                      DenseI64ArrayAttr bc = {}, DataKind dtype = DataKind());

  bool needReset(Value &val);

  std::string emitAccumulateOutType(Value &v, Block *block,
                                    const DataKind &dtype);

  void constantOpEmitDone(bool done);

  bool isConstantOpDone();

  void emitScalar(Operation *);

private:
  using ValueMapper = llvm::ScopedHashTable<Value, std::string>;
  using BlockMapper = llvm::ScopedHashTable<Block *, std::string>;
  using TmpVarMapper = std::map<Block *, std::vector<std::string>>;

  /// Output stream to emit to.
  raw_indented_ostream os;

  /// Boolean to enforce that all variables for op results and block
  /// arguments are declared at the beginning of the function. This also
  /// includes results from ops located in nested regions.
  bool declareVariablesAtTop;

  /// Map from value to name of C++ variable that contain the name.
  ValueMapper valueMapper;

  /// Map from block to name of C++ label.
  BlockMapper blockMapper;

  /// record temp variables name.
  TmpVarMapper tempVarMapper;

  /// Configure register for 2380.
  RegConfigger regConfigger;

  // emit constantOp done flag for 2380
  bool constant_emit_done;
  /// The number of values in the current scope. This is used to declare the
  /// names of values in a scope.
  std::stack<int64_t> valueInScopeCount;
  std::stack<int64_t> labelInScopeCount;
};

bool emitRand(CEmitter *cEmitter, mlir::Operation *op,
              std::stringstream &mem_rand, std::string dataType, int mem_idx);

void emitRand(CEmitter *cEmitter, mlir::ppl::RandOp randOp,
              std::stringstream &mem_rand, std::string dataType, int mem_idx);

bool emitRead(CEmitter *cEmitter, mlir::Operation *op,
              std::stringstream &mem_read, std::string dataType, int mem_idx,
              int index);

template <typename OsType, typename OpsType>
static void emitWithShapeCheck(OsType &os, const OpsType &op_fmt,
                               const llvm::ArrayRef<std::string> inputs) {
  std::string os_str = "if (";
  for (int i = 0; i < inputs.size(); ++i) {
    auto input = inputs[i];
    if (i > 0 && i < inputs.size()) {
      os_str += " && ";
    }
    os_str += formatString("{}.size", input);
  }
  os_str += ") {\n  ";
  os << os_str << op_fmt << ";\n}";
}

} // namespace ppl
} // namespace mlir
