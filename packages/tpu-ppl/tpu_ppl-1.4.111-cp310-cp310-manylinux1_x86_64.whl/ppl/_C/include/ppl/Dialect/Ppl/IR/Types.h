#ifndef PPL_IR_TYPES_H_
#define PPL_IR_TYPES_H_

#include "mlir/IR/BuiltinTypes.h"
#include "mlir/IR/TypeSupport.h"
#include "mlir/IR/Types.h"

#define GET_TYPEDEF_CLASSES
#include "ppl/Dialect/Ppl/IR/Types.h.inc"

namespace mlir {

unsigned getPointeeBitWidth(RankedTensorType tensorTy);

}

#endif // PPL_IR_TYPES_H_
