#ifndef PPL_DIALECT_PPL_TRANSFORMS_PASSES_H_
#define PPL_DIALECT_PPL_TRANSFORMS_PASSES_H_

#include "mlir/Pass/Pass.h"

namespace mlir {
namespace ppl {

std::unique_ptr<Pass> createCombineOpsPass();
std::unique_ptr<Pass> createPplLoopMemEffectMotionPass();
std::unique_ptr<Pass> createPplAddressAssignPass();
std::unique_ptr<Pass> createPplDynBlockPass();
std::unique_ptr<Pass> createPplPipelinePass();
std::unique_ptr<Pass> createChipAssignPass();
std::unique_ptr<Pass> createRemoveTestFuncPass();
std::unique_ptr<Pass> createRemoveDebugPass();
std::unique_ptr<Pass> createPplCanonicalizePass();
std::unique_ptr<Pass> createPplFeConversionPass();
std::unique_ptr<Pass> createPplShapeInferencePass();
std::unique_ptr<Pass> createPplSetMemRefShapePass();
std::unique_ptr<Pass> createPplSetDynBlockPass();
std::unique_ptr<Pass> createPplReplaceConstArgAndRemoveTestPass();
std::unique_ptr<Pass> createPplTensorConversionPass();
std::unique_ptr<Pass> createPipelinePriorPass();
std::unique_ptr<Pass> createRegAllocPass();
std::unique_ptr<mlir::Pass> createCoreNumAssignPass();
std::unique_ptr<mlir::Pass> createCoreNumAssignPass(int core_num);
} // namespace ppl

#define GEN_PASS_REGISTRATION
#define GEN_PASS_DECL_REPLACECONSTARG
#include "ppl/Dialect/Ppl/Transforms/Passes.h.inc"

} // namespace mlir

#endif
