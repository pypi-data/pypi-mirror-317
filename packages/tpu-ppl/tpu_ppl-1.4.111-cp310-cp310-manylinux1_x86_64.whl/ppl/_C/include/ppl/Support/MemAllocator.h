#pragma once

#include <list>
#include <set>

#include "MemAllocatorMethod.h"
#include "mlir/IR/Operation.h"
#include "mlir/Support/LLVM.h"

namespace mlir {
namespace ppl {

class GmemAllocator {
public:
  GmemAllocator(uint32_t alignment = 16);
  void registerMethod(std::string method_name, bool reuse);
  void registerAllMethod();
  int64_t assignGaddr(std::vector<Value> &ops,
                      DenseMap<Value, TensorLive> &liveRange,
                      DenseMap<Value, int64_t> &gaddrMap,
                      bool neuronMemoryReuse, int64_t baseGaddr);
  static void sortOpByLiveStart(std::vector<Value> &ops,
                                DenseMap<Value, TensorLive> &liveRange);

  uint32_t alignment;

private:
  std::vector<std::string> reuse_methods_;
  std::vector<std::string> methods_;
};

} // namespace ppl
} // namespace mlir
