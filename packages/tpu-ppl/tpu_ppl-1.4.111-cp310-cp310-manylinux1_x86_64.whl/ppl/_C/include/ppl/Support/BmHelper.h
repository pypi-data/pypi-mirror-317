#pragma once
#include "ppl/Dialect/Ppl/IR/Dialect.h"

using namespace mlir;

//-----------------------------------------------------------------
// Helper for get/set original value
//-----------------------------------------------------------------
namespace mlir {
namespace ppl {

std::string VariableTType(const Value v);

} // namespace ppl
} // namespace mlir
