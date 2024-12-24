#ifndef PPL_IR_OPINTERFACES_H_
#define PPL_IR_OPINTERFACES_H_

#include "mlir/Analysis/DataFlowFramework.h"
#include "mlir/IR/OpDefinition.h"
#include "ppl/Dialect/Ppl/Transforms/Analysis/ShapeAnalysis.h"
#include <list>

namespace mlir::ppl {
enum MEM_IN_OUT { MEM_IN, MEN_OUT };

extern std::string dir;

struct Mem {
  size_t size;
  int flag;
  std::vector<uint32_t> shape;
  std::shared_ptr<std::vector<float>> data;
  void dump();
  int data_type;
};

} // namespace mlir::ppl
#include "ppl/Dialect/Ppl/IR/OpsEnums.h.inc"
#define GET_TYPEDEF_CLASSES
#include "ppl/Dialect/Ppl/IR/OpInterfaces.h.inc"
#endif // PPL_IR_OPINTERFACES_H_
