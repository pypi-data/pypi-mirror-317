#pragma once

#include <map>

#include "mlir/IR/Operation.h"

#include "ppl/Support/utils.h"

namespace mlir {
namespace ppl {

/// register configure method for sg2380
class RegConfigger {
public:
  bool needReset(Value&);
  int getValueSerialNum(Value &val,
                        mem_type_t tensor_mode);
};

} // namespace ppl
} // namespace mlir
