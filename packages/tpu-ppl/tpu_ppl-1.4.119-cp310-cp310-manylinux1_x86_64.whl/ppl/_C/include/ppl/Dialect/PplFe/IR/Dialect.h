#ifndef PPL_FE_DIALECT_PPL_IR_DIALECT_H_
#define PPL_FE_DIALECT_PPL_IR_DIALECT_H_


#include "mlir/Dialect/Arith/IR/Arith.h"
#include "mlir/Dialect/ControlFlow/IR/ControlFlow.h"
#include "mlir/Dialect/Func/IR/FuncOps.h"
#include "mlir/Dialect/Math/IR/Math.h"
#include "mlir/Dialect/SCF/IR/SCF.h"
#include "mlir/Dialect/Tensor/IR/Tensor.h"
#include "mlir/Dialect/LLVMIR/LLVMDialect.h"

#include "mlir/IR/BuiltinOps.h"
#include "mlir/IR/Dialect.h"
#include "mlir/Interfaces/ControlFlowInterfaces.h"
#include "ppl/Dialect/Ppl/IR/Dialect.h"
#include "ppl/Dialect/PplFe/IR/Dialect.h.inc"

#define GET_OP_CLASSES
#include "ppl/Dialect/PplFe/IR/Ops.h.inc"


#endif // PPL_IR_DIALECT_H_
