#ifndef PPL_FE_DIALECT
#define PPL_FE_DIALECT

include "mlir/IR/OpBase.td"

def PplFe_Dialect : Dialect {
  let name = "ppl_fe";

  let cppNamespace = "::mlir::ppl::fe";

  let summary = "The PplFe IR in MLIR";

  let description = [{
    PplFe Dialect.
  }];
}


#endif // PPL_FE_DIALECT
