#pragma once
#include "ppl/Dialect/Ppl/IR/Dialect.h"
#include "ppl/Support/CEmitter.h"

using namespace mlir;

namespace mlir {
namespace ppl {

LogicalResult emitOperation(CEmitter *pEmitter, Operation &op,
                            bool trailingSemicolon);

LogicalResult convertToC(ModuleOp module, TranslateOption &option);

} // namespace ppl
} // namespace  mlir
