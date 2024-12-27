#ifndef PPL_DIALECT_PPL_IR_DIALECT_H_
#define PPL_DIALECT_PPL_IR_DIALECT_H_

#include "mlir/Dialect/Arith/IR/Arith.h"
#include "mlir/Dialect/ControlFlow/IR/ControlFlow.h"
#include "mlir/Dialect/Func/IR/FuncOps.h"
#include "mlir/Dialect/Math/IR/Math.h"
#include "mlir/Dialect/MemRef/IR/MemRef.h"
#include "mlir/Dialect/SCF/IR/SCF.h"
#include "mlir/Dialect/Tensor/IR/Tensor.h"
#include "mlir/Dialect/LLVMIR/LLVMDialect.h"
#include "mlir/Dialect/Affine/IR/AffineOps.h"
#include "mlir/Dialect/MLProgram/IR/MLProgram.h"
#include "mlir/Dialect/Traits.h"
// #include "ppl/Support/ModuleInterpreter.h"

#include "mlir/IR/BuiltinOps.h"
#include "mlir/IR/Dialect.h"
#include "mlir/Interfaces/ControlFlowInterfaces.h"
#include "ppl/Dialect/Ppl/IR/Dialect.h.inc"
#include "ppl/Dialect/Ppl/IR/OpInterfaces.h"
#include "ppl/Dialect/Ppl/IR/Traits.h"
#include "ppl/Dialect/Ppl/IR/Types.h"

#define GET_OP_CLASSES
#include "ppl/Dialect/Ppl/IR/Ops.h.inc"

namespace mlir {
namespace ppl {


} // namespace ppl
} // namespace mlir

#endif // PPL_IR_DIALECT_H_
