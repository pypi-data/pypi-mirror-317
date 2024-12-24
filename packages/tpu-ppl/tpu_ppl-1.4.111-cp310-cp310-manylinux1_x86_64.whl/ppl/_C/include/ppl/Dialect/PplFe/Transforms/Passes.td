#ifndef PPL_FE_PASSES
#define PPL_FE_PASSES

include "mlir/Pass/PassBase.td"

// for frontend
def LoopRestructure : Pass<"loop-restructure"> {
  let constructor = "mlir::ppl::fe::createLoopRestructurePass()";
  let dependentDialects = ["::mlir::scf::SCFDialect"];
}

def SCFCanonicalizeFor : Pass<"canonicalize-scf-for"> {
  let summary = "Run some additional canonicalization for scf::for";
  let constructor = "mlir::ppl::fe::createCanonicalizeForPass()";
}

def AffineCFG : Pass<"affine-cfg"> {
  let summary = "Replace scf.if and similar with affine.if";
  let constructor = "mlir::ppl::fe::replaceAffineCFGPass()";
}

def Mem2Reg : Pass<"mem2reg"> {
  let summary = "Replace scf.if and similar with affine.if";
  let constructor = "mlir::ppl::fe::createMem2RegPass()";
}

def ToPPL : Pass<"ToPPL", "ModuleOp"> {
  let summary = "convert to ppl format";
  let constructor = "mlir::ppl::fe::createToPPLPass()";
  let dependentDialects = ["::mlir::ppl::PplDialect",
                           "::mlir::ppl::fe::PplFeDialect"];
}

def AssignName : Pass<"AssignName", "ModuleOp"> {
  let summary = "assgin name to each value";
  let constructor = "mlir::ppl::fe::createAssignNamePass()";
  let dependentDialects = ["::mlir::ppl::PplDialect",
                           "::mlir::ppl::fe::PplFeDialect"];
}

def Inline: Pass<"ineline", "mlir::ModuleOp"> {
  let summary = "inline function";
  let constructor = "mlir::ppl::fe::createInlinePass()";
}
#endif
