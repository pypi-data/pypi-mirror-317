#ifndef PPL_PASSES
#define PPL_PASSES

include "mlir/Pass/PassBase.td"

def PplLoopMemEffectMotion : Pass</*cli-arg*/"ppl-loop-mem-effect-motion", /*Op*/"mlir::ModuleOp"> {
  let summary = "loop mem effect motion pass";
  let description = [{
    loop mem effect motion pass
  }];

  let constructor = "mlir::ppl::createPplLoopMemEffectMotionPass()";

  let dependentDialects = ["mlir::ppl::PplDialect"];
}

def PplAddressAssign : Pass</*cli-arg*/"ppl-address-assign", /*Op*/"mlir::ModuleOp"> {
  let summary = "assign local address pass";
  let description = [{
    assign local address pass
  }];

  let constructor = "mlir::ppl::createPplAddressAssignPass()";

  let dependentDialects = ["mlir::ppl::PplDialect"];
  let options = [
    Option<"bank_conflict", "bank_conflict",
           "bool", /*default*/"true",
           "consider bank conflict">,
    Option<"dyn_block", "dyn_block",
           "bool", /*default*/"false",
           "support dyn_block">
  ];
}

def PplDynBlock : Pass</*cli-arg*/"ppl-dyn-block", /*Op*/"mlir::ModuleOp"> {
  let summary = "modify kernel func args for dyn block";
  let description = [{
    modify kernel func args for dyn block
  }];

  let constructor = "mlir::ppl::createPplDynBlockPass()";

  let dependentDialects = ["mlir::ppl::PplDialect"];
}

def PplPipeline : Pass<"ppl-pipeline", "mlir::ModuleOp"> {
  let summary = "pipeline";

  let description = [{
    parallel Load/Computer/Store op
  }];

  let constructor = "mlir::ppl::createPplPipelinePass()";

  let dependentDialects = ["mlir::ppl::PplDialect",
                           "mlir::scf::SCFDialect",
                           "mlir::arith::ArithDialect"];
}

def ChipAssign : Pass</*cli-arg*/"ppl-chip-assign", /*Op*/"mlir::ModuleOp"> {
  let summary = "Assign chip type";

  let constructor = "mlir::ppl::createChipAssignPass()";

  let dependentDialects = ["mlir::ppl::PplDialect"];
  let options = [
    Option<"chip", "chip", "std::string", /*default=*/"",
           "chip: cv183x/bm1684x">,
          //  "chip: cv183x/cv182x/cv186x/bm1684/bm1684x/bm1688/bm1690/mars3">,
  ];
}

def RemoveDebug : Pass</*cli-arg*/"ppl-remove-debug", /*Op*/"mlir::ModuleOp"> {
  let summary = "Remove ops relate to debug";

  let constructor = "mlir::ppl::createRemoveDebugPass()";

  let dependentDialects = ["mlir::ppl::PplDialect"];
}

def RemoveTestFunc : Pass</*cli-arg*/"ppl-remove-test-func", /*Op*/"mlir::ModuleOp"> {
  let summary = "Assign chip type";

  let constructor = "mlir::ppl::createRemoveTestFuncPass()";

  let dependentDialects = ["mlir::ppl::PplDialect"];
}

def PplCanonicalize: Pass</*cli-arg*/"ppl-canonicalize", /*Op*/"mlir::ModuleOp"> {
  let summary = "canonicalize for ppl op";

  let constructor = "mlir::ppl::createPplCanonicalizePass()";

  let dependentDialects = ["mlir::ppl::PplDialect"];
}

def PplFeConversion: Pass</*cli-arg*/"ppl-fe-conversion", /*Op*/"mlir::ModuleOp"> {
  let summary = "canonicalize for ppl op";

  let constructor = "mlir::ppl::createPplFeConversionPass()";

  let dependentDialects = ["mlir::ppl::PplDialect"];
}

def ShapeInference: Pass<"ShapeInference", "mlir::ModuleOp"> {
  let summary = "Shape Inference for ppl Op";
  let constructor = "mlir::ppl::createPplShapeInferencePass()";

  let dependentDialects = ["mlir::ppl::PplDialect", "AffineDialect", "ml_program::MLProgramDialect"];
}

def SetMemRefShape: Pass<"SetMemRefShape", "mlir::ModuleOp"> {
  let summary = "set tensor's shape for ppl Op";
  let constructor = "mlir::ppl::createPplSetMemRefShapePass()";

  let dependentDialects = ["mlir::ppl::PplDialect"];
}

def SetDynBlock: Pass<"SetDynBlock", "mlir::ModuleOp"> {
  let summary = "set FuncOp's attribute if dyn block";
  let constructor = "mlir::ppl::createPplSetDynBlockPass()";
  let dependentDialects = ["mlir::ppl::PplDialect"];
}

def ReplaceConstArg: Pass<"ReplaceConstArg", "mlir::ModuleOp"> {
  let summary = "replace const arg for jit";
  // let constructor = "mlir::ppl::createPplReplaceConstArgPass(std::string const_arg)";
  let options = [
    Option<"const_arg", "const_arg", "std::string", /*default=*/"",
           "">,
  ];

  let dependentDialects = ["mlir::ppl::PplDialect"];
}

def ReplaceConstArgAndRemoveTest: Pass<"ReplaceConstArgAndRemoveTest", "mlir::ModuleOp"> {
  let summary = "replace const arg from test and remove test";
  let constructor = "mlir::ppl::createPplReplaceConstArgAndRemoveTestPass()";
  let dependentDialects = ["mlir::ppl::PplDialect"];
}

def TensorConversion: Pass<"TensorConversion", "mlir::ModuleOp"> {
  let summary = "convert tensor to final tensor";
  let constructor = "mlir::ppl::createPplTensorConversionPass()";
  let dependentDialects = ["mlir::ppl::PplDialect"];
}

def PipelinePrior: Pass<"PipelinePrior", "mlir::ModuleOp"> {
  let summary = "set ForOp's pipeline flag";
  let constructor = "mlir::ppl::createPipelinePriorPass()";
  let dependentDialects = ["mlir::ppl::PplDialect", "mlir::scf::SCFDialect", "mlir::LLVM::LLVMDialect"];
}

def RegAlloc : Pass<"reg-alloc", "mlir::ModuleOp"> {
  let summary = "reg alloc pass";
  let description = [{
    reg alloc pass
  }];

  let constructor = "mlir::ppl::createRegAllocPass()";
  let dependentDialects = ["mlir::ppl::PplDialect"];
}

def CoreNumAssign : Pass<"ppl-corenum-assign", /*Op*/"mlir::ModuleOp"> {
  let summary = "Assign Core Num";

  let constructor = "mlir::ppl::createCoreNumAssignPass()";

  let dependentDialects = ["mlir::ppl::PplDialect"];
  let options = [
    Option<"coreNum", "core-num", "int",
           /*default=*/"1",
           "Core Number">,
  ];
}
#endif
