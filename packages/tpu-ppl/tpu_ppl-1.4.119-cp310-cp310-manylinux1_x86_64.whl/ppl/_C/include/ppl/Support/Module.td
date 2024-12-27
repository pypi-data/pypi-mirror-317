#ifndef PPL_MODULE_ATTR
#define PPL_MODULE_ATTR

include "mlir/IR/AttrTypeBase.td"
include "mlir/IR/EnumAttr.td"
include "mlir/IR/BuiltinDialect.td"

def Module_Chip: I32EnumAttr<"Chip", "module chip",[
      I32EnumAttrCase<"ALL", 0>,
      I32EnumAttrCase<"BM1684",  1000, "bm1684">,
      I32EnumAttrCase<"BM1684X", 1001, "bm1684x">,
      I32EnumAttrCase<"BM1688",  1002, "bm1688">,
      I32EnumAttrCase<"CV186X",  1003, "cv186x">,
      I32EnumAttrCase<"SG2260",  1004, "bm1690">,
      I32EnumAttrCase<"MARS3",  1005, "mars3">,
      I32EnumAttrCase<"SG2380",  1006, "sg2380">,
      I32EnumAttrCase<"CV180x",  2000, "cv180x">,
      I32EnumAttrCase<"CV181x",  2001, "cv181x">,
      I32EnumAttrCase<"CV182x",  2002, "cv182x">,
      I32EnumAttrCase<"CV183x",  2003, "cv183x">
    ]> {
  let genSpecializedAttr = 0;
  let cppNamespace = "::mlir::ppl";
}

def Module_Mode: I32EnumAttr<"Mode", "module mode",[
      I32EnumAttrCase<"INT8",  0>,
      I32EnumAttrCase<"UINT8", 1>,
      I32EnumAttrCase<"INT4",  2>,
      I32EnumAttrCase<"BF16",  3>,
      I32EnumAttrCase<"F16",   4>,
      I32EnumAttrCase<"F32",   5>
    ]> {
  let genSpecializedAttr = 0;
  let cppNamespace = "::mlir::ppl";
}


#endif // PPL_MODULE_ATTR
