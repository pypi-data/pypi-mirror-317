#pragma once
#include "ppl/Dialect/Ppl/IR/Dialect.h"
#include "ppl/Support/CEmitter.h"

namespace mlir {
namespace ppl {

LogicalResult emitBM1684XDescHost(CEmitter *cEmitter, func::FuncOp &functionOp,
                                  const std::string &src, mlir::ppl::Chip chip,
                                  bool gen_ref, bool is_test);
LogicalResult emitBM1684XDescHostHeader(CEmitter *cEmitter,
                                        func::FuncOp &functionOp, bool gen_ref);
} // namespace ppl
} // namespace  mlir
