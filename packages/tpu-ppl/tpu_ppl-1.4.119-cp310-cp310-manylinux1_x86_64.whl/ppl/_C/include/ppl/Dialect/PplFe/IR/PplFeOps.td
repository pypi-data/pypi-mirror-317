#ifndef PPL_FE_OPS
#define PPL_FE_OPS

include "ppl/Dialect/PplFe/IR/PplFeDialect.td"
include "mlir/IR/OpBase.td"
include "mlir/Interfaces/InferTypeOpInterface.td" // SameOperandsAndResultType
include "mlir/Interfaces/SideEffectInterfaces.td" // Pure
include "mlir/Interfaces/CastInterfaces.td" // CastOpInterface
include "mlir/Interfaces/ViewLikeInterface.td"
include "mlir/IR/SymbolInterfaces.td"

include "mlir/Dialect/LLVMIR/LLVMOpBase.td"
include "mlir/Dialect/LLVMIR/LLVMInterfaces.td"

//
// Op Base
//
class PPL_FE_Op<string mnemonic, list<Trait> traits = []> :
    Op<PplFe_Dialect, mnemonic, !listconcat(traits, [])> {
}

def SubIndexOp : PPL_FE_Op<"subindex", [
  ViewLikeOpInterface, Pure
]> {
  let summary = "memref subview operation";

  let arguments = (ins AnyMemRef : $source, Index : $index);
  let results = (outs AnyMemRef : $result);

  let hasFolder = 1;
  let hasCanonicalizer = 1;

  let extraClassDeclaration = [{
    ::mlir::Value getViewSource() { return getSource(); }
  }];
}

def StreamToTokenOp : PPL_FE_Op<"stream2token", [
  Pure
]> {
  let summary = "Extract an async stream from a cuda stream";

  let arguments = (ins AnyType : $source);
  let results = (outs AnyType : $result);
}

def Memref2PointerOp : PPL_FE_Op<"memref2pointer", [
  ViewLikeOpInterface, Pure
]> {
  let summary = "Extract and LLVM pointer from a MemRef";

  let arguments = (ins AnyMemRef : $source);
  let results = (outs LLVM_AnyPointer : $result);

  let hasFolder = 1;
  let hasCanonicalizer = 1;

  let extraClassDeclaration = [{
    ::mlir::Value getViewSource() { return getSource(); }
  }];
}

def Pointer2MemrefOp : PPL_FE_Op<"pointer2memref", [
  ViewLikeOpInterface, Pure
]> {
  let summary = "Upgrade a pointer to a memref";

  let arguments = (ins LLVM_AnyPointer : $source);
  let results = (outs AnyMemRef : $result);

  let hasFolder = 1;
  let hasCanonicalizer = 1;

  let extraClassDeclaration = [{
    ::mlir::Value getViewSource() { return getSource(); }
  }];
}

def GetFuncOp : PPL_FE_Op<"get_func",
    [Pure, DeclareOpInterfaceMethods<SymbolUserOpInterface>]> {
  let summary = "get the pointer pointing to a function";
  let arguments = (ins FlatSymbolRefAttr:$name);
  let results = (outs LLVM_AnyPointer : $result);
  let assemblyFormat = "$name `:` type($result) attr-dict";
  let hasCanonicalizer = 1;
}

def TrivialUseOp : PPL_FE_Op<"trivialuse"> {
  let summary = "memref subview operation";

  let arguments = (ins AnyMemRef : $source);

}

def TypeSizeOp : PPL_FE_Op<"typeSize", [Pure]> {
  let summary = "Get size of type";
  let arguments = (ins TypeAttr : $source);
  let results = (outs AnyType : $result);
  let hasFolder = 1;
  let hasCanonicalizer = 1;
}

def TypeAlignOp : PPL_FE_Op<"typeAlign", [Pure]> {
  let summary = "Get alignment of type";
  let arguments = (ins TypeAttr : $source);
  let results = (outs AnyType : $result);
  let hasFolder = 1;
  let hasCanonicalizer = 1;
}
#endif // Ppl_OPS
