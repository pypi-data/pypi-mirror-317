#ifndef PPL_TYPES
#define PPL_TYPES

include "mlir/IR/AttrTypeBase.td"
include "mlir/IR/EnumAttr.td"
include "ppl/Dialect/Ppl/IR/PplDialect.td"

//
// Types
//
class PplTypeDef<string name, string _mnemonic>
    : TypeDef<Ppl_Dialect, name> {
    // Used by printer/parser
    let mnemonic = _mnemonic;
}

// Floating-point Type
def PPL_Float : AnyTypeOf<[F8E4M3FN, F8E5M2, F16, BF16, F32, F64], "floating-point">;
def PPL_FloatTensor : TensorOf<[PPL_Float]>;
def PPL_FloatMemRef : MemRefOf<[PPL_Float]>;
def PPL_FloatLike : AnyTypeOf<[PPL_Float, PPL_FloatTensor, PPL_FloatMemRef]>;

// Boolean Type
// PPL_Bool -> I1
def PPL_BoolTensor : TensorOf<[I1]>;
def PPL_BoolLike : AnyTypeOf<[I1, PPL_BoolTensor]>;

// I4 UI4
def I4 : I<4>;
def UI4 : UI<4>;

// Integer Type
def PPL_Int : AnyTypeOf<[I1, I4, I8, I16, I32, I64, UI1, UI4, UI8, UI16, UI32, UI64], "integer">;
def PPL_IntTensor : TensorOf<[PPL_Int]>;
def PPL_IntMemRef : MemRefOf<[PPL_Int]>;
def PPL_IntLike : AnyTypeOf<[PPL_Int, PPL_IntTensor, PPL_IntMemRef]>;
def PPL_IntLikeOrNone : AnyTypeOf<[PPL_Int, PPL_IntTensor, PPL_IntMemRef, NoneType]>;
// Unsigned Integer Type
def PPL_UInt : AnyTypeOf<[UI1, UI4, UI8, UI16, UI32, UI64], "unsigned integer">;
def PPL_UIntTensor : TensorOf<[PPL_UInt]>;
def PPL_UIntMemRef : MemRefOf<[PPL_UInt]>;
def PPL_UIntLike : AnyTypeOf<[PPL_UInt, PPL_UIntTensor, PPL_UIntMemRef]>;

// I32 Type
// PPL_I32 -> I32
// PPL_I32Tensor -> I32Tensor
def PPL_I32Like: AnyTypeOf<[I32, I32Tensor]>;

// I64 Type
// PPL_I64 -> I64
// PPL_I64Tensor -> I64Tensor
def PPL_I64Like: AnyTypeOf<[I64, I64Tensor]>;

// UI64 Type
// PPL_UI64 -> UI64
// PPL_UI64Tensor -> UI64Tensor
def UI64Tensor  : TensorOf<[UI64]>;
def UPPL_UI64Like: AnyTypeOf<[UI64, UI64Tensor]>;

// Pointer Type
def PPL_Ptr : PplTypeDef<"Pointer", "ptr"> {
    let summary = "pointer type";

    let description = [{
        Ppl PointerType
    }];

    let parameters = (ins "Type":$pointeeType, "int":$addressSpace);

    let builders = [
        TypeBuilderWithInferredContext<(ins
            "Type":$pointeeType,
            "int":$addressSpace
        ), [{
            return $_get(pointeeType.getContext(), pointeeType, addressSpace);
        }]>
    ];

    let hasCustomAssemblyFormat = 1;
    let skipDefaultBuilders = 1;
}

def PPL_PtrTensor : TensorOf<[PPL_Ptr]>;
def PPL_PtrLike : AnyTypeOf<[PPL_Ptr, PPL_PtrTensor]>;

// matrix
def PPL_Matrix : PplTypeDef<"Matrix", "matrix"> {
    let summary = "matrix type";

    let description = [{
        Ppl MatrixType
    }];
    let parameters = (ins "Type":$MatrixType, "int":$addressSpace);
    let builders = [
        TypeBuilderWithInferredContext<(ins
            "Type":$MatrixType,
            "int":$addressSpace
        ), [{
            return $_get(MatrixType.getContext(), MatrixType, addressSpace);
        }]>
    ];

    let hasCustomAssemblyFormat = 1;
    let skipDefaultBuilders = 1;
}
def PPL_MatrixTensor : TensorOf<[PPL_Matrix]>;

def PPL_FpInt : AnyTypeOf<[PPL_Int, PPL_Float]>;
def PPL_FpIntTensor : AnyTypeOf<[PPL_FloatTensor, PPL_IntTensor, PPL_UIntTensor]>;
def PPL_FpIntMemRef : AnyTypeOf<[PPL_FloatMemRef, PPL_IntMemRef, PPL_UIntMemRef]>;
def PPL_Tensor : AnyTypeOf<[PPL_FpIntTensor, PPL_PtrTensor, PPL_MatrixTensor]>;
def PPL_MemRef : AnyTypeOf<[PPL_FpIntMemRef]>;
def PPL_TensorOrNone : AnyTypeOf<[PPL_FpIntTensor, PPL_PtrTensor, PPL_MatrixTensor, NoneType]>;
def PPL_MemRefOrNone : AnyTypeOf<[PPL_FpIntMemRef, NoneType]>;
def PPL_IntMemRefOrNone : AnyTypeOf<[PPL_IntMemRef, NoneType]>;

def PPL_Type : AnyTypeOf<[PPL_FloatLike, PPL_IntLike, PPL_UIntLike, PPL_PtrLike]>;
def PPL_AnyType : AnyTypeOf<[PPL_FloatLike, PPL_BoolLike, PPL_IntLike, PPL_UIntLike, NoneType]>;
def PPL_MemRefOrTensor : AnyTypeOf<[PPL_Tensor, PPL_MemRef]>;
def PPL_Scalar : AnyTypeOf<[PPL_FpInt, PPL_UInt]>;
def PPL_MemRefOrScalar : AnyTypeOf<[PPL_MemRef, PPL_Scalar]>;
def PPL_MemRefOrScalarOrNone : AnyTypeOf<[PPL_MemRef, PPL_Scalar, NoneType]>;
def PPL_FpIntOrNone : AnyTypeOf<[PPL_FpInt, NoneType]>;


def TensorModeAttr: I64EnumAttr<"TensorMode", "Tensor Mode",[
      I64EnumAttrCase<"LOCAL",  0>,
      I64EnumAttrCase<"L2", 1>,
      I64EnumAttrCase<"GLOBAL",  2>,
    ]> {
  let cppNamespace = "::mlir::ppl";
}

def ArithModeAttr: I64EnumAttr<"ArithMode", "Arith Mode",[
      I64EnumAttrCase<"AND",  0>,
      I64EnumAttrCase<"OR", 1>,
      I64EnumAttrCase<"XOR",  2>,
      I64EnumAttrCase<"MIN",  3>,
      I64EnumAttrCase<"MAX",  4>,
      I64EnumAttrCase<"ADD",  5>,
      I64EnumAttrCase<"SUB",  6>,
      I64EnumAttrCase<"MUL",  7>,
      I64EnumAttrCase<"DIV",  8>,
      I64EnumAttrCase<"DIFF_ABS",  9>,
      I64EnumAttrCase<"MAC",  10>,
    ]> {
  let cppNamespace = "::mlir::ppl";
}

#endif
