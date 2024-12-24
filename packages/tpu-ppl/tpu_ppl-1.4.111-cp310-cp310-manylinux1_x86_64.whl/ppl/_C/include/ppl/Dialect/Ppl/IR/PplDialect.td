#ifndef PPL_DIALECT
#define PPL_DIALECT

include "mlir/IR/OpBase.td"

def Ppl_Dialect : Dialect {
  let name = "ppl";

  let cppNamespace = "::mlir::ppl";

  let summary = "The Ppl IR in MLIR";

  let description = [{
    Ppl Dialect.

    Dependent Dialects:
      * Arith:
        * addf, addi, andi, cmpf, cmpi, divf, fptosi, ...
      * Math:
        * exp, sin, cos, log, ...
      * StructuredControlFlow:
        * ForOp, IfOp, WhileOp, YieldOp, ConditionOp
  }];

  let dependentDialects = [
    "arith::ArithDialect",
    "math::MathDialect",
    "scf::SCFDialect",
    "func::FuncDialect",
    "AffineDialect"
  ];

  let extraClassDeclaration = [{
    void registerTypes();
  }];

  let hasConstantMaterializer = 1;
  let useDefaultTypePrinterParser = 1;
}

include "ppl/Dialect/Ppl/IR/PplTypes.td"


#endif // PPL_DIALECT
