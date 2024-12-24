#ifndef __PPL_FE_OPS_H__
#define __PPL_FE_OPS_H__
#include "mlir/Dialect/Affine/IR/AffineOps.h"
#include "mlir/Dialect/LLVMIR/LLVMDialect.h"
#include "mlir/IR/BuiltinTypes.h"
#include "mlir/IR/Dialect.h"
#include "mlir/IR/OpDefinition.h"
#include "mlir/IR/PatternMatch.h"
#include "mlir/Interfaces/SideEffectInterfaces.h"
#include "mlir/Interfaces/ViewLikeInterface.h"
#include "llvm/Support/CommandLine.h"

#include "mlir/Dialect/Affine/IR/AffineOps.h"
#include "mlir/IR/Matchers.h"
#include "mlir/IR/PatternMatch.h"
#include "llvm/Support/CommandLine.h"

namespace mlir {
namespace ppl {
namespace fe {

bool collectEffects(
    mlir::Operation *op,
    llvm::SmallVectorImpl<mlir::MemoryEffects::EffectInstance> &effects,
    bool ignoreBarriers);

bool getEffectsBefore(
    mlir::Operation *op,
    llvm::SmallVectorImpl<mlir::MemoryEffects::EffectInstance> &effects,
    bool stopAtBarrier);

bool getEffectsAfter(
    mlir::Operation *op,
    llvm::SmallVectorImpl<mlir::MemoryEffects::EffectInstance> &effects,
    bool stopAtBarrier);

bool isReadOnly(mlir::Operation *);
bool isReadNone(mlir::Operation *);

bool mayReadFrom(mlir::Operation *, mlir::Value);
bool mayWriteTo(mlir::Operation *, mlir::Value, bool ignoreBarrier = false);

bool mayAlias(mlir::MemoryEffects::EffectInstance a,
              mlir::MemoryEffects::EffectInstance b);

bool mayAlias(mlir::MemoryEffects::EffectInstance a, mlir::Value b);
struct ValueOrInt {
  bool isValue;
  mlir::Value v_val;
  int64_t i_val;
  ValueOrInt(mlir::Value v) { initValue(v); }
  void initValue(mlir::Value v) {
    using namespace mlir;
    if (v) {
      IntegerAttr iattr;
      if (matchPattern(v, m_Constant(&iattr))) {
        i_val = iattr.getValue().getSExtValue();
        v_val = nullptr;
        isValue = false;
        return;
      }
    }
    isValue = true;
    v_val = v;
  }

  ValueOrInt(size_t i) : isValue(false), v_val(), i_val(i) {}

  bool operator>=(int64_t v) {
    if (isValue)
      return false;
    return i_val >= v;
  }
  bool operator>(int64_t v) {
    if (isValue)
      return false;
    return i_val > v;
  }
  bool operator==(int64_t v) {
    if (isValue)
      return false;
    return i_val == v;
  }
  bool operator<(int64_t v) {
    if (isValue)
      return false;
    return i_val < v;
  }
  bool operator<=(int64_t v) {
    if (isValue)
      return false;
    return i_val <= v;
  }
  bool operator>=(llvm::APInt v) {
    if (isValue)
      return false;
    return i_val >= v.getSExtValue();
  }
  bool operator>(llvm::APInt v) {
    if (isValue)
      return false;
    return i_val > v.getSExtValue();
  }
  bool operator==(llvm::APInt v) {
    if (isValue)
      return false;
    return i_val == v.getSExtValue();
  }
  bool operator<(llvm::APInt v) {
    if (isValue)
      return false;
    return i_val < v.getSExtValue();
  }
  bool operator<=(llvm::APInt v) {
    if (isValue)
      return false;
    return i_val <= v.getSExtValue();
  }
};
enum class Cmp { EQ, LT, LE, GT, GE };

bool valueCmp(Cmp cmp, mlir::AffineExpr expr, size_t numDim,
              mlir::ValueRange operands, ValueOrInt val);

bool valueCmp(Cmp cmp, mlir::Value bval, ValueOrInt val);
} // namespace fe
} // namespace ppl
} // namespace mlir
#endif
