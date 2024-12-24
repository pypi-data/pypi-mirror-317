#ifndef PPL_OPS
#define PPL_OPS

include "ppl/Dialect/Ppl/IR/PplDialect.td"
include "ppl/Dialect/Ppl/IR/PplTypes.td"
include "ppl/Dialect/Ppl/IR/PplAttrDefs.td"
include "ppl/Dialect/Ppl/IR/PplInterfaces.td"
include "ppl/Dialect/Ppl/IR/PplOpInterfaces.td"
include "mlir/IR/OpBase.td"
include "mlir/Interfaces/SideEffectInterfaces.td" // Pure
include "mlir/Interfaces/ControlFlowInterfaces.td" // BranchOpInterface
include "mlir/Interfaces/InferTypeOpInterface.td" // SameOperandsAndResultType
include "mlir/Interfaces/SideEffectInterfaces.td" // Pure
include "mlir/Interfaces/CastInterfaces.td" // CastOpInterface
include "mlir/Interfaces/ViewLikeInterface.td"
include "mlir/Interfaces/InferIntRangeInterface.td"
include "mlir/IR/SymbolInterfaces.td"

include "mlir/Dialect/LLVMIR/LLVMOpBase.td"
include "mlir/Dialect/LLVMIR/LLVMInterfaces.td"

//
// Op Base
//
class PPL_Op<string mnemonic, list<Trait> traits = []> :
    Op<Ppl_Dialect, mnemonic, !listconcat(traits, [TensorSizeTrait])> {
}

//
// CastOps
//
// Use cast ops in arith:
//   bitcast
//   fptoui, fptosi, uitofp, sitofp,
//   extf, tructf,
//   extui, extsi, tructi
def PPL_IntToPtrOp : PPL_Op<"int_to_ptr", [SameOperandsAndResultShape,
                                         SameOperandsAndResultEncoding,
                                         Pure,
                                         /*DeclareOpInterfaceMethods<CastOpInterface>*/]> {
    let summary = "Cast int64 to pointer";

    let arguments = (ins PPL_I64Like:$from);

    let results = (outs PPL_PtrLike:$result);

    let assemblyFormat = "$from attr-dict `:` type($from) `->` type($result)";
}

def PPL_PtrToIntOp : PPL_Op<"ptr_to_int", [SameOperandsAndResultShape,
                                         SameOperandsAndResultEncoding,
                                         Pure,
                                         /*DeclareOpInterfaceMethods<CastOpInterface>*/]> {
    let summary = "Cast pointer to int64";

    let arguments = (ins PPL_PtrLike:$from);

    let results = (outs PPL_I64Like:$result);

    let assemblyFormat = "$from attr-dict `:` type($from) `->` type($result)";
}

// arith.bitcast doesn't support pointers
def PPL_BitcastOp : PPL_Op<"bitcast", [SameOperandsAndResultShape,
                                     SameOperandsAndResultEncoding,
                                     Pure,
                                     /*DeclareOpInterfaceMethods<CastOpInterface>*/]> {
    let summary = "Cast between types of the same bitwidth";

    let arguments = (ins PPL_Type:$from);

    let results = (outs PPL_Type:$result);

    let assemblyFormat = "$from attr-dict `:` type($from) `->` type($result)";

    // TODO: Add verifier
}

def PPL_FpToFpOp : PPL_Op<"fp_to_fp", [SameOperandsAndResultShape,
                                     SameOperandsAndResultEncoding,
                                     Pure,
                                     /*DeclareOpInterfaceMethods<CastOpInterface>*/]> {
    let summary = "Floating point casting for custom types";

    let description = [{
        Floating point casting for custom types (F8).

        F8 <-> FP16, BF16, FP32, FP64
    }];

    let arguments = (ins PPL_FloatLike:$from);

    let results = (outs PPL_FloatLike:$result);

    let assemblyFormat = "$from attr-dict `:` type($from) `->` type($result)";

    // TODO: We need a verifier here.
}

def Memref2PointerOp : PPL_Op<"memref2pointer", [Pure]> {
  let summary = "Extract and LLVM pointer from a MemRef";

  let arguments = (ins AnyMemRef : $source);
  let results = (outs PPL_PtrLike : $result);
}

def Memref2MemrefOp : PPL_Op<"memref2memref",[Pure]> {
  let summary = "cast between different types of the memref";

  let arguments = (ins AnyMemRef : $source);
  let results = (outs AnyMemRef : $result);
}

//
// Make AssertOp

def PPL_AssertOp : PPL_Op<"assert", [MemoryEffects<[MemWrite]>,
                                     DeclareOpInterfaceMethods<EmitInterface>]> {
  let summary = "tpu assert";
  let arguments = (ins PPL_Type:$condition);
  let assemblyFormat = "operands attr-dict `:` type(operands)";
  let hasCanonicalizer = 1;
}

def PPL_ReadOp : PPL_Op<"read", [MemoryEffects<[MemWrite]>]> {
  let summary = "read data";
  let arguments = (ins PPL_MemRef:$dst);
  let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_CallExOp : PPL_Op<"call_ex", [MemoryEffects<[MemWrite]>,
                                      DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "call extern function";
    let arguments = (ins Variadic<AnyType>:$operands, StrAttr:$func_name);
    let results = (outs Variadic<AnyType>);
    let assemblyFormat = [{
      $func_name `(` $operands `)` attr-dict `:` functional-type($operands, results)
    }];
}

// initial random data
// new added ops for ppl
def PPL_RandFillOp : PPL_Op<"rand_fill", [MemoryEffects<[MemWrite]>]> {
    let summary = "fill memory with rand data";
    let arguments = (ins PPL_MemRef:$ptr, PPL_MemRef:$shape, PPL_MemRefOrNone:$stride,
                         PPL_MemRefOrNone:$offset, PPL_FpInt:$min_val, PPL_FpInt:$max_val);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_RandOp : PPL_Op<"rand", [MemoryEffects<[MemWrite]>]> {
    let summary = "init rand data with result";
    let arguments = (ins PPL_MemRef:$shape, PPL_MemRefOrNone:$stride,
                         PPL_MemRefOrNone:$offset, PPL_FpInt:$min_val,
                         PPL_FpInt:$max_val);
    let results = (outs PPL_MemRef:$result);
    let assemblyFormat = "operands attr-dict `:` type(operands) `->` type($result)";
}

// arith
def PPL_ArithAndOp : PPL_Op<"arith_and", [Pure,
                                         DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "c = a && b";
    let arguments = (ins PPL_IntLike:$lhs,
                         PPL_IntLike:$rhs);
    let results = (outs PPL_IntLike:$rst);
    let assemblyFormat = "operands attr-dict `:` type(operands) `->` type($rst)";
    let hasCanonicalizer = 1;
}

def PPL_ArithLogOp : PPL_Op<"arith_log", [Pure,
                                         DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "b = log(a)";
    let arguments = (ins PPL_IntLike:$input);
    let results = (outs PPL_IntLike:$rst);
    let assemblyFormat = "operands attr-dict `:` type(operands) `->` type($rst)";
    let hasCanonicalizer = 1;
}

def PPL_ArithSqrtOp : PPL_Op<"arith_sqrt", [Pure,
                                         DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "b = log(a)";
    let arguments = (ins PPL_IntLike:$input);
    let results = (outs PPL_IntLike:$rst);
    let assemblyFormat = "operands attr-dict `:` type(operands) `->` type($rst)";
    let hasCanonicalizer = 1;
}

// Get Chip Info
// new added ops for ppl
def PPL_NpuNumOp : PPL_Op<"npu_num", [Pure]> {
    let summary = "npu_num";

    // let hasCustomAssemblyFormat = 1;
    // let hasCanonicalizer = 1;
    let results = (outs /*SignlessIntegerOrFloatLike*/AnyType:$result);
    let hasCanonicalizer = 1;
}

def PPL_EuBytesOp : PPL_Op<"eu_bytes", [Pure]> {
    let summary = "eu_bytes";

    // let hasCustomAssemblyFormat = 1;
    // let hasCanonicalizer = 1;
    let results = (outs /*SignlessIntegerOrFloatLike*/AnyType:$result);
    let hasCanonicalizer = 1;
}

def PPL_CoeffLenOp : PPL_Op<"coeff_len", [Pure]> {
    let summary = "coeff_len";
    let arguments = (ins PPL_Int:$mode);

    // let hasCustomAssemblyFormat = 1;
    // let hasCanonicalizer = 1;
    let results = (outs /*SignlessIntegerOrFloatLike*/AnyType:$result);
    let hasCanonicalizer = 1;
}

// ==========================================
// ppl fe ir

def PPL_SdmaMoveOp : PPL_Op<"sdma_move", [MemoryEffects<[MemWrite]>]> {
    let summary = "l2 memory move";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src,
                         PPL_IntLikeOrNone:$port_id);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DmaMoveTransOp : PPL_Op<"dma_move_trans", [MemoryEffects<[MemWrite]>]> {
    let summary = "memory move transpose";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src,
                         PPL_Int:$trans);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DmaMoveBCOp : PPL_Op<"dma_move_broadcast", [MemoryEffects<[MemWrite]>]> {
    let summary = "memory move broadcast";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src,
                         PPL_Int:$trans);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}
// =========================================

// new added ops for ppl
def PPL_DmaLoadOp : PPL_Op<"dmaload", [MemoryEffects<[MemWrite]>,
                                       DeclareOpInterfaceMethods<DmaInterface>,
                                       DeclareOpInterfaceMethods<MemInterface>,
                                       DeclareOpInterfaceMethods<EmitInterface>,
                                       DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "dma load";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
    // let hasCustomAssemblyFormat = 1;
    // let hasCanonicalizer = 1;
}

def PPL_DmaLoadNCTransOp : PPL_Op<"dmaload_nc_trans", [MemoryEffects<[MemWrite]>,
                                  DeclareOpInterfaceMethods<DmaInterface>,
                                  DeclareOpInterfaceMethods<MemInterface>,
                                  DeclareOpInterfaceMethods<EmitInterface>,
                                  DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "dma load nc trans";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DmaStoreNCTransOp : PPL_Op<"dmastore_nc_trans", [MemoryEffects<[MemWrite]>,
                                   DeclareOpInterfaceMethods<DmaInterface>,
                                   DeclareOpInterfaceMethods<MemInterface>,
                                   DeclareOpInterfaceMethods<EmitInterface>,
                                   DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "dma store nc tanspose";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DmaLoadCWTransOp : PPL_Op<"dmaload_cw_trans", [MemoryEffects<[MemWrite]>,
                                  DeclareOpInterfaceMethods<DmaInterface>,
                                  DeclareOpInterfaceMethods<MemInterface>,
                                  DeclareOpInterfaceMethods<EmitInterface>,
                                  DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "dma load cw trans";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DmaStoreCWTransOp : PPL_Op<"dmastore_cw_trans", [MemoryEffects<[MemWrite]>,
                                   DeclareOpInterfaceMethods<DmaInterface>,
                                   DeclareOpInterfaceMethods<MemInterface>,
                                   DeclareOpInterfaceMethods<EmitInterface>,
                                   DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "dma store cw tanspose";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DmaLoadReshapeOp : PPL_Op<"dmaload_reshape", [MemoryEffects<[MemWrite]>,
                                       DeclareOpInterfaceMethods<DmaInterface>,
                                       DeclareOpInterfaceMethods<MemInterface>,
                                       DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "dma load reshape";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src);

    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DmaLoadCompactOp : PPL_Op<"load_compact", [MemoryEffects<[MemWrite]>,
                                  DeclareOpInterfaceMethods<DmaInterface>,
                                  DeclareOpInterfaceMethods<MemInterface>,
                                  DeclareOpInterfaceMethods<EmitInterface>,
                                  DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "dma load compact";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
    // let hasCustomAssemblyFormat = 1;
    // let hasCanonicalizer = 1;
}

def PPL_DmaStoreCompactOp : PPL_Op<"store_compact", [MemoryEffects<[MemWrite]>,
                                   DeclareOpInterfaceMethods<DmaInterface>,
                                   DeclareOpInterfaceMethods<MemInterface>,
                                   DeclareOpInterfaceMethods<EmitInterface>,
                                   DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "dma store compact";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}


def PPL_DmaLoadBCOp : PPL_Op<"dmaload_bc", [MemoryEffects<[MemWrite]>,
                             DeclareOpInterfaceMethods<DmaInterface>,
                             DeclareOpInterfaceMethods<MemInterface>,
                             DeclareOpInterfaceMethods<EmitInterface>,
                             DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "dma channel broad cast load";
    let arguments = (ins PPL_MemRef:$dst, PPL_MemRef:$src, PPL_Int:$num);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DmaStoreOp : PPL_Op<"dmastore", [MemoryEffects<[MemWrite]>,
                                         DeclareOpInterfaceMethods<DmaInterface>,
                                         DeclareOpInterfaceMethods<MemInterface>,
                                         DeclareOpInterfaceMethods<EmitInterface>,
                                         DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "dma store";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
    // let hasCustomAssemblyFormat = 1;
    // let hasCanonicalizer = 1;
}

def PPL_DmaStoreReshapeOp : PPL_Op<"dmastore_reshape", [MemoryEffects<[MemWrite]>,
                                       DeclareOpInterfaceMethods<DmaInterface>,
                                       DeclareOpInterfaceMethods<MemInterface>,
                                       DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "dma load reshape";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src);

    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_MatrixLoadOp : PPL_Op<"maxtrix_load", [MemoryEffects<[MemWrite]>,
                              DeclareOpInterfaceMethods<DmaInterface>,
                              DeclareOpInterfaceMethods<MemInterface>,
                              DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "matrix load";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$ptr,
                         PPL_MemRefOrNone:$offset,
                         PPL_Int:$trans);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
    // let hasCustomAssemblyFormat = 1;
    // let hasCanonicalizer = 1;
}

def PPL_MatrixStoreOp : PPL_Op<"maxtrix_store", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<DmaInterface>,
                               DeclareOpInterfaceMethods<MemInterface>,
                               DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "matrix store";
    let arguments = (ins PPL_MemRef:$ptr,
                         PPL_MemRef:$src,
                         PPL_MemRefOrNone:$offset,
                         PPL_Int:$trans);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
    // let hasCustomAssemblyFormat = 1;
    // let hasCanonicalizer = 1;
}

def PPL_TensorOp : PPL_Op<"tensorfe", [MemoryEffects<[MemAlloc]>,
                          DeclareOpInterfaceMethods<TensorInterface>]> {
    let summary = "tensor in local memory";
    let arguments = (ins PPL_IntLike:$shape,
                         PPL_AnyType:$customize_addr,
                         I64Attr:$align_mode,
                         TensorModeAttr:$mode,
                         I64Attr:$address,
                         OptionalAttr<BoolAttr>:$bc);
    let results = (outs PPL_MemRef:$result);
    let assemblyFormat = "$mode operands attr-dict `:` type(operands) `->` type($result)";
}

def PPL_BeTensorOp : PPL_Op<"tensorbe", [MemoryEffects<[MemAlloc]>,
                               DeclareOpInterfaceMethods<TensorInterface>,
                               DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "tensor in local memory";
    let arguments = (ins PPL_IntLike:$shape,
                         PPL_AnyType:$customize_addr,
                         PPL_MemRefOrNone:$stride,
                         PPL_Int:$size,
                         I64Attr:$align_mode,
                         TensorModeAttr:$mode,
                         I64Attr:$address,
                         OptionalAttr<BoolAttr>:$bc);
    let results = (outs PPL_MemRef:$result);
    let assemblyFormat = "$mode operands attr-dict `:` type(operands) `->` type($result)";
}

def PPL_SubTensorOp : PPL_Op<"sub_tensorfe",
                             [NoMemoryEffect,
                              DeclareOpInterfaceMethods<TensorInterface>]> {

    let summary = "sub set of tensor";
    let arguments = (ins PPL_MemRefOrNone:$ancestor,
                         PPL_MemRef:$parent,
                         PPL_MemRefOrNone:$shape,
                         PPL_MemRefOrNone:$offset,
                         PPL_MemRefOrNone:$stride,
                         I64Attr:$align_mode,
                         OptionalAttr<TensorModeAttr>:$mode,
                         OptionalAttr<BoolAttr>:$bc);
    let results = (outs PPL_MemRef:$result);
    let assemblyFormat = "$mode operands attr-dict `:` type(operands) `->` type($result)";
}

def PPL_BeSubTensorOp : PPL_Op<"sub_tensorbe",
                               [NoMemoryEffect,
                                DeclareOpInterfaceMethods<TensorInterface>,
                                DeclareOpInterfaceMethods<EmitInterface>]> {

    let summary = "sub set of tensor";
    let arguments = (ins PPL_MemRefOrNone:$ancestor,
                         PPL_MemRef:$parent,
                         PPL_MemRefOrNone:$shape,
                         PPL_MemRefOrNone:$stride,
                         PPL_Int:$offset,
                         PPL_Int:$size,
                         I64Attr:$align_mode,
                         OptionalAttr<TensorModeAttr>:$mode,
                         OptionalAttr<BoolAttr>:$bc);
    let results = (outs PPL_MemRef:$result);
    let assemblyFormat = "$mode operands attr-dict `:` type(operands) `->` type($result)";
}

def PPL_GlobalAllocOp : PPL_Op<"global_alloc", [MemoryEffects<[MemAlloc]>]> {
    let summary = "global alloc";
    let arguments = (ins PPL_IntLike:$shape);
    let results = (outs PPL_MemRef:$result);
    let assemblyFormat = "operands attr-dict `:` type(operands) `->` type($result)";
}
// global_free todo

def PPL_ParallelStartOp : PPL_Op<"parallel_start", [MemoryEffects<[MemWrite]>,
                                 DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "parallel start";
    let arguments = (ins BoolAttr:$loop_kernel);
    let assemblyFormat = "attr-dict";
}

def PPL_ParallelStopOp : PPL_Op<"parallel_stop", [MemoryEffects<[MemWrite]>,
                                DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "parallel stop";
    let assemblyFormat = "attr-dict";
}

def PPL_SyncOp : PPL_Op<"tpu_sync", [MemoryEffects<[MemWrite]>,
                                     DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "sync";
    let arguments = (ins DefaultValuedAttr<I64Attr, "0x111">:$sync_type, // hau|sdma|tiu+dma
                     DefaultValuedAttr<BoolAttr, "true">:$sync_all);
    let assemblyFormat = "attr-dict";
}

def PPL_ShapeOp: PPL_Op<"shape", [Pure,
                                  DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "shape";
    let arguments = (ins Variadic<PPL_Type>:$dims,
                     DefaultValuedAttr<BoolAttr, "true">:$init);

    let results = (outs PPL_MemRef:$result);
    let assemblyFormat = "operands attr-dict `:` type(operands) `->` type($result)";
}

def PPL_CoreNumOp: PPL_Op<"tpu_core_num",[MemoryEffects<[MemWrite]>,
                                          DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "get CoreNum";
    let results = (outs PPL_IntLike:$corenum);
    let assemblyFormat = "operands attr-dict `:` type($corenum)";
    let hasCanonicalizer = 1;
}

def PPL_CoreIndexOp: PPL_Op<"tpu_core_index",[MemoryEffects<[MemWrite]>,
                                          DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "get CoreIndex";
    let results = (outs PPL_IntLike:$coreindex);
    let assemblyFormat = "operands attr-dict `:` type($coreindex)";
}

def PPL_GroupNumOp: PPL_Op<"group_num",[MemoryEffects<[MemWrite]>,
                                          DeclareOpInterfaceMethods<EmitInterface, ["emitSG2260"]>]> {
    let summary = "get GroupNum";
    let results = (outs PPL_IntLike:$groupnum);
    let assemblyFormat = "operands attr-dict `:` type($groupnum)";
    let hasCanonicalizer = 1;
}

def PPL_BlockNumOp: PPL_Op<"block_num",[MemoryEffects<[MemWrite]>,
                                          DeclareOpInterfaceMethods<EmitInterface, ["emitSG2260"]>]> {
    let summary = "get BlockNum";
    let results = (outs PPL_IntLike:$blocknum);
    let assemblyFormat = "operands attr-dict `:` type($blocknum)";
    let hasCanonicalizer = 1;
}

def PPL_GroupIndexOp: PPL_Op<"group_index",[MemoryEffects<[MemWrite]>,
                                          DeclareOpInterfaceMethods<EmitInterface, ["emitSG2260"]>]> {
    let summary = "get GroupIndex";
    let results = (outs PPL_IntLike:$groupindex);
    let assemblyFormat = "operands attr-dict `:` type($groupindex)";
}

def PPL_BlockIndexOp: PPL_Op<"block_index",[MemoryEffects<[MemWrite]>,
                                          DeclareOpInterfaceMethods<EmitInterface, ["emitSG2260"]>]> {
    let summary = "get BlockIndex";
    let results = (outs PPL_IntLike:$blockindex);
    let assemblyFormat = "operands attr-dict `:` type($blockindex)";
}

def PPL_GetGlobalAddrOp : PPL_Op<"tpu_global_mem_addr", [DeclareOpInterfaceMethods<EmitInterface>,
                                                         DeclareOpInterfaceMethods<InferIntRangeInterface>
                                                         ]> {
    let summary = "get pointer from a address";
    let arguments = (ins PPL_MemRef:$src);
    let results = (outs PPL_Int : $gaddr);
    let assemblyFormat = "operands attr-dict `:` type(operands) `->` type($gaddr)";
}

def PPL_GetValueOp : PPL_Op<"get_value", [DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "get value from a pointer";
    let arguments = (ins PPL_Int:$pointer);
    let results = (outs PPL_IntLike : $value);
    let assemblyFormat = "operands attr-dict `:` type(operands) `->` type($value)";
    // let assemblyFormat = "operands attr-dict `:` type($value)";
}

def PPL_MsgSendOp : PPL_Op<"msg_send", [MemoryEffects<[MemWrite]>,
                                        DeclareOpInterfaceMethods<EmitInterface>]>{
    let summary = "message send";
    let arguments = (ins PPL_Int:$msg_idx,
                         PPL_Int:$wait_cnt,
                         PPL_Int:$is_dma);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_MsgWaitOp : PPL_Op<"msg_wait", [MemoryEffects<[MemWrite]>,
                                        DeclareOpInterfaceMethods<EmitInterface>]>{
    let summary = "message wait";
    let arguments = (ins PPL_Int:$msg_idx,
                         PPL_Int:$send_cnt,
                         PPL_Int:$is_dma);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_FenceOp : PPL_Op<"fence", [MemoryEffects<[MemWrite]>,
                                   DeclareOpInterfaceMethods<EmitInterface>]>{
    let summary = "fence";
    let arguments = (ins PPL_Int:$msg_idx,
                         PPL_Int:$send_cnt);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_LaneMaskOp : PPL_Op<"lane_mask", [MemoryEffects<[MemWrite]>,
                                          DeclareOpInterfaceMethods<EmitInterface>]>{
    let summary = "lane mask";
    let arguments = (ins PPL_Int:$mask,
                         PPL_Int:$long_valid);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_HauPollOp: PPL_Op<"hau_poll", [MemoryEffects<[MemWrite]>,
                                       DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "hau poll";
    let assemblyFormat = "attr-dict";
}

def PPL_TpuPollOp: PPL_Op<"tpu_poll", [MemoryEffects<[MemWrite]>,
                                       DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "tpu poll";
    let assemblyFormat = "attr-dict";
}

def PPL_CancelInitOp: PPL_Op<"cancel_init", [MemoryEffects<[MemWrite]>]> {
    let summary = "remove kernel emit tpu init";
    let assemblyFormat = "attr-dict";
}

def PPL_CancelPollOp: PPL_Op<"cancel_poll", [MemoryEffects<[MemWrite]>]> {
    let summary = "remove kernel emit tpu poll";
    let assemblyFormat = "attr-dict";
}

def PPL_DmaSetCOp : PPL_Op<"dma_set_C", [MemoryEffects<[MemWrite]>,
                                       DeclareOpInterfaceMethods<EmitInterface>,
                                       DeclareOpInterfaceMethods<DmaInterface>,
                                       DeclareOpInterfaceMethods<MemInterface>,
                                       DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "set system addr's contents with scaler";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_FpInt:$scalar);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_SdmaSetCOp : PPL_Op<"sdma_set_C", [MemoryEffects<[MemWrite]>,
                                       DeclareOpInterfaceMethods<EmitInterface, ["emitBM1684x", "emitSG2260"]>,
                                       DeclareOpInterfaceMethods<SdmaInterface>,
                                       DeclareOpInterfaceMethods<MemInterface>,
                                       DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "set system addr's contents with scaler";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_FpInt:$scalar);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_PrintOp : PPL_Op<"print", [MemoryEffects<[MemWrite]>,
                                   DeclareOpInterfaceMethods<EmitInterface>,
                                   IsDebugTrait]>,
  Arguments<(ins StrAttr:$format, Variadic<AnyTypeOf<[PPL_Type]>>:$args)> {
  let summary = "Device-side print, as in CUDA for debugging";
  let description = [{
    `tt.print` takes a literal string format and an arbitrary number of scalar or tensor arguments that should be printed.
    format are generated automatically from the arguments.
  }];
  let assemblyFormat = [{
    $format attr-dict `:` ($args^ `:` type($args))?
  }];
}


def PPL_ToStringOp: PPL_Op<"to_string", [MemoryEffects<[MemWrite]>,
                                         DeclareOpInterfaceMethods<EmitInterface>,
                                         DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                         IsDebugTrait]> {
    let summary = "to_string";
    let arguments = (ins PPL_MemRef:$src);
    let results = (outs PPL_MemRef:$result);
    let assemblyFormat = "operands attr-dict `:` type(operands) `->` type($result)";
}

def PPL_EmptyOp: PPL_Op<"empty", [Pure]> {
    let summary = "emtpy";
    let arguments = (ins Variadic<PPL_Type>:$dims);
    let results = (outs PPL_MemRef:$result);
    let assemblyFormat = "operands attr-dict `:` type(operands) `->` type($result)";
}

def PPL_OnesOp: PPL_Op<"ones", [Pure]> {
    let summary = "ones";
    let arguments = (ins Variadic<PPL_Type>:$dims);
    let results = (outs PPL_MemRef:$result);
    let assemblyFormat = "operands attr-dict `:` type(operands) `->` type($result)";
}

def PPL_TiuSetCOp : PPL_Op<"tiu_set_C", [MemoryEffects<[MemWrite]>,
                                         DeclareOpInterfaceMethods<TiuInterface>,
                                         DeclareOpInterfaceMethods<MemInterface>,
                                         DeclareOpInterfaceMethods<EmitInterface>,
                                         DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "set local addr's contents with scaler";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_FpInt:$scalar);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_CastOp: PPL_Op<"cast", [MemoryEffects<[MemWrite]>,
                                DeclareOpInterfaceMethods<TiuInterface>,
                                DeclareOpInterfaceMethods<MemInterface>,
                                DeclareOpInterfaceMethods<EmitInterface>,
                                DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "cast";
    let arguments = (ins PPL_MemRef:$to,
                         PPL_MemRef:$from,
                         PPL_Int:$round_mode);
    let assemblyFormat = "operands attr-dict `:` type(operands) ";
}

def PPL_AbsOp: PPL_Op<"abs", [MemoryEffects<[MemWrite]>,
                              DeclareOpInterfaceMethods<TiuInterface>,
                              DeclareOpInterfaceMethods<MemInterface>,
                              DeclareOpInterfaceMethods<EmitInterface>,
                              DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "abs";
    let arguments = (ins PPL_MemRef:$rst,
                         PPL_MemRefOrScalar:$input);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_ArangeBroadCastOp : PPL_Op<"ArangeBroadCast", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<TiuInterface>,
                               DeclareOpInterfaceMethods<MemInterface>,
                               DeclareOpInterfaceMethods<EmitInterface>,
                               DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "arithmetic sequence bcast";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_Int:$start, PPL_Int:$step,
                         PPL_Int:$num);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_MM2FpOp: PPL_Op<"fmm2", [MemoryEffects<[MemWrite]>,
                                   DeclareOpInterfaceMethods<TiuInterface>,
                                   DeclareOpInterfaceMethods<MemInterface>,
                                   DeclareOpInterfaceMethods<EmitInterface, ["emitSG2260"]>,
                                   DeclareOpInterfaceMethods<LongLivedInterface>,
                                   DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "mm2 fp";
    let arguments = (ins PPL_MemRef:$rst,
                         PPL_MemRefOrScalar:$lhs,
                         PPL_MemRefOrScalar:$rhs,
                         PPL_MemRefOrScalarOrNone:$bias,
                         PPL_Int:$ltrans,
                         PPL_Int:$rtrans,
                         PPL_Int:$rst_trans,
                         PPL_Int:$do_relu,
                         PPL_Int:$accumulate,
                         PPL_Int:$out_dtype,
                         PPL_Int:$has_bias,
                         PPL_Int:$do_saturate);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
    // let hasCanonicalizer = 1;
}

def PPL_MM2Op: PPL_Op<"mm2_int", [MemoryEffects<[MemWrite]>,
                        DeclareOpInterfaceMethods<TiuInterface>,
                        DeclareOpInterfaceMethods<MemInterface>,
                        DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                        DeclareOpInterfaceMethods<LongLivedInterface>,
                        DeclareOpInterfaceMethods<EmitInterface, ["emitSG2260", "emitBM1688"]>]> {
    let summary = "mm2 int";
    let arguments = (ins PPL_MemRef:$rst,
                         PPL_MemRefOrScalar:$lhs,
                         PPL_MemRefOrScalar:$rhs,
                         PPL_MemRefOrScalarOrNone:$bias,
                         PPL_MemRefOrScalarOrNone:$r_zp,
                         PPL_MemRefOrScalarOrNone:$requant,
                         PPL_Int:$multiplier,
                         PPL_Int:$rshift,
                         PPL_Int:$y_zp,
                         PPL_Int:$ltrans,
                         PPL_Int:$rtrans,
                         PPL_Int:$rst_trans,
                         PPL_Int:$accumulate,
                         PPL_Int:$out_dtype,
                         PPL_Int:$has_bias,
                         PPL_Int:$do_relu,
                         PPL_Int:$do_rq,
                         PPL_Int:$do_sym_saturate,
                         PPL_Int:$round_mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_MMOp: PPL_Op<"mm", [MemoryEffects<[MemWrite]>,
                              DeclareOpInterfaceMethods<TiuInterface>,
                              DeclareOpInterfaceMethods<MemInterface>,
                              DeclareOpInterfaceMethods<EmitInterface>,
                              DeclareOpInterfaceMethods<LongLivedInterface>,
                              DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "matmul op";
    let arguments = (ins PPL_MemRef:$rst,
                         PPL_MemRefOrScalar:$lhs,
                         PPL_MemRef:$rhs,
                         PPL_MemRefOrScalarOrNone:$bias,
                         PPL_Int:$ltrans,
                         PPL_Int:$rtrans,
                         PPL_Int:$accumulate,
                         PPL_Int:$lshift,
                         PPL_Int:$rshift,
                         PPL_Int:$do_relu,
                         PPL_Int:$round_mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
    // let hasCanonicalizer = 1;
}

class PPL_Pool2D_Op<string mnemonic, list<Trait> traits = []>: PPL_Op<mnemonic,
    !listconcat(traits, [MemoryEffects<[MemWrite]>,
                         DeclareOpInterfaceMethods<TiuInterface>,
                         DeclareOpInterfaceMethods<MemInterface>,
                         DeclareOpInterfaceMethods<EmitInterface>,
                         DeclareOpInterfaceMethods<ShapeInferenceOpInterface, ["inferShapes"]>])> {
    let summary = "pooling 2d fp";
    let arguments = (ins PPL_MemRef:$rst,  PPL_MemRef:$input,
                     PPL_IntLike:$kernel, PPL_IntLike:$pad,
                     PPL_IntLike:$stride, PPL_IntLike:$dilation);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}
def PPL_MaxPool2DOp:PPL_Pool2D_Op<"maxPool2D", [DeclareOpInterfaceMethods<EmitInterface>]>;
def PPL_MinPool2DOp:PPL_Pool2D_Op<"minPool2D", [DeclareOpInterfaceMethods<EmitInterface, ["emitSG2260", "emitBM1688"]>]>;

def PPL_AvgPool2DOp: PPL_Op<"ins_avgPool2D", [MemoryEffects<[MemWrite]>,
                                       DeclareOpInterfaceMethods<TiuInterface>,
                                       DeclareOpInterfaceMethods<MemInterface>,
                                       DeclareOpInterfaceMethods<EmitInterface>,
                                       DeclareOpInterfaceMethods<ShapeInferenceOpInterface, ["inferShapes"]>]> {
    let summary = "ins avgPool2D";
    let arguments = (ins PPL_MemRef:$rst,  PPL_MemRef:$input,
                     PPL_IntLike:$kernel, PPL_IntLike:$pad,
                     PPL_IntLike:$stride, PPL_IntLike:$dilation,
                     PPL_IntLikeOrNone:$ins, PPL_FpInt:$scale,
                     PPL_FpInt:$rshift);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_RoiAvgPool2DOp: PPL_Op<"roi_avgPool2D", [MemoryEffects<[MemWrite]>,
                                       DeclareOpInterfaceMethods<TiuInterface>,
                                       DeclareOpInterfaceMethods<MemInterface>,
                                       DeclareOpInterfaceMethods<EmitInterface>,
                                       DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "roi avgPool2D";
    let arguments = (ins PPL_MemRef:$output, PPL_MemRef:$input,
                     PPL_MemRef:$roi, PPL_Int:$scale,
                     PPL_IntLike:$kernel, PPL_IntLike:$stride,
                     PPL_Int:$do_relu, PPL_Int:$rounding_mode,
                     PPL_Int:$do_saturate);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_RoiMaxPool2DOp: PPL_Op<"roi_maxPool2D", [MemoryEffects<[MemWrite]>,
                                       DeclareOpInterfaceMethods<TiuInterface>,
                                       DeclareOpInterfaceMethods<MemInterface>,
                                       DeclareOpInterfaceMethods<EmitInterface>,
                                       DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "roi maxPool2D";
    let arguments = (ins PPL_MemRef:$output, PPL_MemRef:$input,
                     PPL_MemRef:$roi, PPL_IntLike:$kernel,
                     PPL_IntLike:$stride, PPL_Int:$do_relu);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_RoiMinPool2DOp: PPL_Op<"roi_minPool2D", [MemoryEffects<[MemWrite]>,
                                       DeclareOpInterfaceMethods<TiuInterface>,
                                       DeclareOpInterfaceMethods<MemInterface>,
                                       DeclareOpInterfaceMethods<EmitInterface>,
                                       DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "roi minPool2D";
    let arguments = (ins PPL_MemRef:$output, PPL_MemRef:$input,
                     PPL_MemRef:$roi, PPL_IntLike:$kernel,
                     PPL_IntLike:$stride, PPL_Int:$do_relu);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_CwTransOp: PPL_Op<"cw_trans", [MemoryEffects<[MemWrite]>,
                                       DeclareOpInterfaceMethods<TiuInterface>,
                                       DeclareOpInterfaceMethods<MemInterface>,
                                       DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                       DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "c w dim transpose";
    let arguments = (ins PPL_MemRef:$dst, PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_WcTransOp: PPL_Op<"wc_trans", [MemoryEffects<[MemWrite]>,
                                       DeclareOpInterfaceMethods<TiuInterface>,
                                       DeclareOpInterfaceMethods<MemInterface>,
                                       DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                       DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "w c dim transpose";
    let arguments = (ins PPL_MemRef:$dst, PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_TopKOp: PPL_Op<"topK", [MemoryEffects<[MemWrite]>,
                                DeclareOpInterfaceMethods<EmitInterface>,
                                DeclareOpInterfaceMethods<HauInterface>,
                                DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "topK Ops";
    let arguments = (ins PPL_MemRef:$dst, PPL_MemRefOrNone:$dst_idx,
                         PPL_MemRef:$src, PPL_MemRefOrNone:$src_idx,
                         PPL_Int:$k, PPL_Int:$descending);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_Conv2DFpOp: PPL_Op<"fp_conv2d", [MemoryEffects<[MemWrite]>,
                           DeclareOpInterfaceMethods<TiuInterface>,
                           DeclareOpInterfaceMethods<MemInterface>,
                           DeclareOpInterfaceMethods<EmitInterface>,
                           DeclareOpInterfaceMethods<LongLivedInterface>,
                           DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "conv2d_fp";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$input,
                         PPL_MemRefOrScalar:$weight,
                         PPL_MemRefOrScalarOrNone:$bias,
                         PPL_Int:$oc,
                         PPL_MemRef:$kernel,
                         PPL_MemRef:$stride,
                         PPL_MemRef:$dilation,
                         PPL_MemRef:$pad,
                         PPL_MemRefOrNone:$ins,
                         PPL_Int:$result_relu,
                         PPL_Int:$accumulate,
                         PPL_Int:$out_dtype,
                         PPL_Int:$has_bias,
                         PPL_Int:$sym_range,
                         PPL_Int:$kernel_rotate);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_Deconv2DFpOp: PPL_Op<"fp_conv2d_for_deconv2d", [MemoryEffects<[MemWrite]>,
                                      DeclareOpInterfaceMethods<TiuInterface>,
                                      DeclareOpInterfaceMethods<MemInterface>,
                                      DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                      DeclareOpInterfaceMethods<LongLivedInterface>,
                                      DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "conv2d for deconv2d fp";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$input,
                         PPL_MemRef:$weight,
                         PPL_MemRefOrNone:$bias,
                         PPL_Int:$oc,
                         PPL_MemRef:$kernel,
                         PPL_MemRef:$dilation,
                         PPL_MemRef:$pad,
                         PPL_MemRef:$ins,
                         PPL_Int:$accumulate,
                         PPL_Int:$out_dtype,
                         PPL_Int:$has_bias);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_Depthwise2DFpOp: PPL_Op<"fp_depthwise2d", [MemoryEffects<[MemWrite]>,
                                                   DeclareOpInterfaceMethods<TiuInterface>,
                                                   DeclareOpInterfaceMethods<MemInterface>,
                                                   DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                                   DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "fp_depthwise2d";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$input,
                         PPL_MemRef:$weight,
                         PPL_MemRefOrNone:$bias,
                         PPL_MemRef:$kernel,
                         PPL_MemRef:$stride,
                         PPL_MemRef:$dilation,
                         PPL_MemRef:$pad,
                         PPL_Int:$has_bias);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_Depthwise2DInt8Op: PPL_Op<"int8_depthwise2d", [MemoryEffects<[MemWrite]>,
                                                       DeclareOpInterfaceMethods<TiuInterface>,
                                                       DeclareOpInterfaceMethods<MemInterface>,
                                                       DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                                       DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "int8_depthwise2d";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$input,
                         PPL_MemRefOrScalar:$weight,
                         PPL_MemRefOrNone:$bias,
                         PPL_MemRef:$kernel,
                         PPL_MemRef:$stride,
                         PPL_MemRef:$dilation,
                         PPL_MemRef:$pad,
                         PPL_MemRefOrScalar:$pad_val,
                         PPL_Int:$result_relu,
                         PPL_Int:$out_dtype,
                         PPL_Int:$has_bias,
                         PPL_Int:$rshift,
                         PPL_Int:$rq,
                         PPL_MemRefOrScalarOrNone:$requant, /*requant_tensor(coeff_merge)*/
                         PPL_Int:$sym_range,
                         PPL_Int:$rounding_mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DepthwiseForDeconv2DFpOp: PPL_Op<"fp_depthwise_for_deconv2d", [MemoryEffects<[MemWrite]>,
                                         DeclareOpInterfaceMethods<TiuInterface>,
                                         DeclareOpInterfaceMethods<MemInterface>,
                                         DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                         DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "fp_depthwise_for_deconv2d";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$input,
                         PPL_MemRef:$weight,
                         PPL_MemRef:$bias,
                         PPL_MemRef:$kernel,
                         PPL_MemRef:$dilation,
                         PPL_MemRef:$pad,
                         PPL_MemRef:$ins,
                         PPL_Int:$out_dtype,
                         PPL_Int:$has_bias);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DepthwiseForDeconv2DInt8Op: PPL_Op<"int8_depthwise_for_deconv2d", [MemoryEffects<[MemWrite]>,
                                           DeclareOpInterfaceMethods<TiuInterface>,
                                           DeclareOpInterfaceMethods<MemInterface>,
                                           DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                           DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "int8_depthwise_for_deconv2d";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$input,
                         PPL_MemRef:$weight,
                         PPL_MemRefOrNone:$bias,
                         PPL_MemRef:$kernel,
                         PPL_MemRef:$dilation,
                         PPL_MemRef:$pad,
                         PPL_MemRef:$ins,
                         PPL_MemRefOrScalar:$pad_val,
                         PPL_Int:$result_relu,
                         PPL_Int:$out_dtype,
                         PPL_Int:$has_bias,
                         PPL_Int:$rshift,
                         PPL_Int:$rounding_mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_Conv2DOp: PPL_Op<"conv2d_int", [MemoryEffects<[MemWrite]>,
                                           DeclareOpInterfaceMethods<TiuInterface>,
                                           DeclareOpInterfaceMethods<MemInterface>,
                                           DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                           DeclareOpInterfaceMethods<LongLivedInterface>,
                                           DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "quant_conv2d_int8";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$input,
                         PPL_MemRefOrScalar:$weight,
                         PPL_MemRefOrScalarOrNone:$bias,
                         PPL_Int:$output_c,
                         PPL_MemRef:$kernel,
                         PPL_MemRef:$stride,
                         PPL_MemRef:$dilation,
                         PPL_MemRef:$pad,
                         PPL_MemRefOrNone:$ins,
                         PPL_MemRefOrScalarOrNone:$pad_val,
                         PPL_Int:$result_relu,
                         PPL_Int:$accumulate,
                         PPL_Int:$out_dtype,
                         PPL_Int:$has_bias,
                         PPL_Int:$sym,
                         PPL_MemRefOrScalar:$quant, /* when quant is Scalar, it means rshift or kzp,else it's kzp_tensor */
                         PPL_Int:$rq,
                         PPL_MemRefOrScalar:$requant, /*multiplier or requant_tensor(coeff_merge)*/
                         PPL_Int:$rshift,
                         PPL_Int:$out_zp,
                         PPL_Int:$sym_range,
                         PPL_Int:$rounding_mode,
                         PPL_Int:$kernel_rotate);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_Deconv2DOp: PPL_Op<"deconv2d_int", [MemoryEffects<[MemWrite]>,
                                           DeclareOpInterfaceMethods<TiuInterface>,
                                           DeclareOpInterfaceMethods<MemInterface>,
                                           DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                           DeclareOpInterfaceMethods<LongLivedInterface>,
                                           DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "quant_deconv2d_int8";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$input,
                         PPL_MemRef:$weight,
                         PPL_MemRefOrScalarOrNone:$bias,
                         PPL_Int:$output_c,
                         PPL_MemRef:$kernel,
                         PPL_MemRef:$dilation,
                         PPL_MemRef:$pad,
                         PPL_MemRefOrNone:$ins,
                         PPL_MemRefOrScalarOrNone:$pad_val,
                         PPL_Int:$insert_val,
                         PPL_Int:$result_relu,
                         PPL_Int:$accumulate,
                         PPL_Int:$out_dtype,
                         PPL_Int:$has_bias,
                         PPL_Int:$sym,
                         PPL_MemRefOrScalar:$quant /* when quant is Scalar, it means rshift or kzp,else it's kzp_tensor */
                         );
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_ArithOp : PPL_Op<"arith", [MemoryEffects<[MemWrite]>,
                         DeclareOpInterfaceMethods<TiuInterface>,
                         DeclareOpInterfaceMethods<MemInterface>,
                         DeclareOpInterfaceMethods<EmitInterface>,
                         DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                         ResultsBroadcastableShape]> {
    let summary = "arith op";
    let arguments = (ins PPL_MemRef:$rst, PPL_MemRefOrScalar:$lhs,
                         PPL_MemRefOrScalar:$rhs, ArithModeAttr:$mode);
    let assemblyFormat = "$mode operands attr-dict `:` type(operands)";
}

def PPL_ArithIntOp: PPL_Op<"int_arith", [MemoryEffects<[MemWrite]>,
                           DeclareOpInterfaceMethods<TiuInterface>,
                           DeclareOpInterfaceMethods<MemInterface>,
                           DeclareOpInterfaceMethods<EmitInterface>,
                           DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                           ResultsBroadcastableShape]> {
    let summary = "arith int op";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRefOrScalar:$lhs,
                         PPL_MemRefOrScalar:$rhs,
                         PPL_MemRefOrScalar:$shift,
                         PPL_Int:$round_mode,
                         PPL_Int:$saturation,
                         ArithModeAttr:$mode);
    let assemblyFormat = "$mode operands attr-dict `:` type(operands)";
}

def PPL_MacFpOp : PPL_Op<"fp_mac", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<TiuInterface>,
                               DeclareOpInterfaceMethods<MemInterface>,
                               DeclareOpInterfaceMethods<EmitInterface>,
                               DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                               ResultsBroadcastableShape]> {
    let summary = "mac fp";
    let arguments = (ins PPL_MemRef:$rst,
                         PPL_MemRefOrScalar:$lhs,
                         PPL_MemRefOrScalar:$rhs);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_VcArithOp : PPL_Op<"vc_arith",
                           [MemoryEffects<[MemWrite]>,
                           DeclareOpInterfaceMethods<TiuInterface>,
                           DeclareOpInterfaceMethods<MemInterface>,
                           DeclareOpInterfaceMethods<EmitInterface>,
                           DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "vector correlation arith";
    let arguments = (ins PPL_MemRef:$rst, PPL_MemRef:$lhs, PPL_MemRef:$rhs,
                         PPL_Int:$mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_VcArithIntOp : PPL_Op<"int_vc_arith",
                                 [MemoryEffects<[MemWrite]>,
                                  DeclareOpInterfaceMethods<TiuInterface>,
                                  DeclareOpInterfaceMethods<MemInterface>,
                                  DeclareOpInterfaceMethods<EmitInterface>,
                                  DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "vector correlation arith int";
    let arguments = (ins PPL_MemRef:$rst, PPL_MemRef:$lhs, PPL_MemRef:$rhs,
                         PPL_Int:$saturation, PPL_Int:$mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_VcDivFpOp : PPL_Op<"fp_vc_div", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<TiuInterface>,
                               DeclareOpInterfaceMethods<MemInterface>,
                               DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "vc div fp";
    let arguments = (ins PPL_MemRef:$rst, PPL_MemRef:$lhs, PPL_MemRef:$rhs);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_RoundOp : PPL_Op<"round", [MemoryEffects<[MemWrite]>,
                                   DeclareOpInterfaceMethods<TiuInterface>,
                                   DeclareOpInterfaceMethods<MemInterface>,
                                   DeclareOpInterfaceMethods<EmitInterface>,
                                   DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "round op";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$input,
                         PPL_Int:$round_mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_TiuL2LOp : PPL_Op<"tiu_l2l", [MemoryEffects<[MemWrite]>,
                         DeclareOpInterfaceMethods<TiuInterface>,
                         DeclareOpInterfaceMethods<MemInterface>,
                         DeclareOpInterfaceMethods<EmitInterface>,
                         DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "copy local to local";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DmaLoadBCL2LOp : PPL_Op<"dmaload_bc_L2L", [MemoryEffects<[MemWrite]>,
                                                   DeclareOpInterfaceMethods<DmaInterface>,
                                                   DeclareOpInterfaceMethods<MemInterface>,
                                                   DeclareOpInterfaceMethods<EmitInterface>,
                                                   DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "copy local to local with channel bcast";
    let arguments = (ins PPL_MemRef:$dst, PPL_MemRef:$src, PPL_Int:$num);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DmaMoveOp : PPL_Op<"dma_move", [MemoryEffects<[MemWrite]>,
                                      DeclareOpInterfaceMethods<DmaInterface>,
                                      DeclareOpInterfaceMethods<MemInterface>,
                                      DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                      DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "copy system memory to system memory";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DmaMoveNCTransOp : PPL_Op<"dma_move_nc_trans", [MemoryEffects<[MemWrite]>,
                                      DeclareOpInterfaceMethods<DmaInterface>,
                                      DeclareOpInterfaceMethods<MemInterface>,
                                      DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                      DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "dma move nc trans";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DmaMoveCWTransOp : PPL_Op<"dma_move_cw_trans", [MemoryEffects<[MemWrite]>,
                                      DeclareOpInterfaceMethods<DmaInterface>,
                                      DeclareOpInterfaceMethods<MemInterface>,
                                      DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                      DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "dma move cw trans";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DmaReverseOp : PPL_Op<"dma_reverse", [MemoryEffects<[MemWrite]>,
                                      DeclareOpInterfaceMethods<DmaInterface>,
                                      DeclareOpInterfaceMethods<MemInterface>,
                                      DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                      DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "Reverse the Tensor data along the _dim dimension";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src,
                         PPL_Int:$dim);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DmaSystemCpyOp : PPL_Op<"dma_system_cpy", [MemoryEffects<[MemWrite]>,
                                      DeclareOpInterfaceMethods<DmaInterface>,
                                      DeclareOpInterfaceMethods<MemInterface>,
                                      DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                      DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "copy system memory to system memory";
    let arguments = (ins PPL_MemRef:$dst, PPL_MemRef:$src, PPL_Int:$count);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_RQFpOp: PPL_Op<"rq_fp", [MemoryEffects<[MemWrite]>,
                              DeclareOpInterfaceMethods<TiuInterface>,
                              DeclareOpInterfaceMethods<MemInterface>,
                              DeclareOpInterfaceMethods<EmitInterface>,
                              DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "requant fp32";
    let arguments = (ins PPL_MemRef:$output, PPL_MemRef:$input,
                    PPL_Float:$scale, PPL_Float:$offset, PPL_Int:$output_round_mode,
                    PPL_Int:$input_round_mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_RQPCFpOp: PPL_Op<"rqpc_fp", [MemoryEffects<[MemWrite]>,
                              DeclareOpInterfaceMethods<TiuInterface>,
                              DeclareOpInterfaceMethods<MemInterface>,
                              DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                              DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "requant perchannel fp32";
    let arguments = (ins PPL_MemRef:$output, PPL_MemRef:$input,PPL_MemRef:$quant,
                     PPL_Int:$output_round_mode,
                    PPL_Int:$input_round_mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_RQIntOp: PPL_Op<"rq_int", [MemoryEffects<[MemWrite]>,
                              DeclareOpInterfaceMethods<TiuInterface>,
                              DeclareOpInterfaceMethods<MemInterface>,
                              DeclareOpInterfaceMethods<EmitInterface>,
                              DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "requant int";
    let arguments = (ins PPL_MemRef:$output, PPL_MemRef:$input,
                    PPL_Int:$multiplier, PPL_Int:$shift, PPL_Int:$offset,
                    PPL_Int:$round_mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_RQPCIntOp: PPL_Op<"rqpc_int", [MemoryEffects<[MemWrite]>,
                              DeclareOpInterfaceMethods<TiuInterface>,
                              DeclareOpInterfaceMethods<MemInterface>,
                              DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                              DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "requant perchannel int";
    let arguments = (ins PPL_MemRef:$output, PPL_MemRef:$input,PPL_MemRef:$quant,
                     PPL_Int:$round_mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DQFpOp: PPL_Op<"dq_fp", [MemoryEffects<[MemWrite]>,
                              DeclareOpInterfaceMethods<TiuInterface>,
                              DeclareOpInterfaceMethods<MemInterface>,
                              DeclareOpInterfaceMethods<EmitInterface>,
                              DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "dequant fp32";
    let arguments = (ins PPL_MemRef:$output, PPL_MemRef:$input,
                    PPL_Int:$offset, PPL_Float:$scale, PPL_Int:$round_mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DQPCFpOp: PPL_Op<"dqpc_fp", [MemoryEffects<[MemWrite]>,
                              DeclareOpInterfaceMethods<TiuInterface>,
                              DeclareOpInterfaceMethods<MemInterface>,
                              DeclareOpInterfaceMethods<EmitInterface>,
                              DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "dequant perchannel fp32";
    let arguments = (ins PPL_MemRef:$output, PPL_MemRef:$input,PPL_MemRef:$quant,
                     PPL_Int:$round_mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DQIntOp: PPL_Op<"dq_int", [MemoryEffects<[MemWrite]>,
                              DeclareOpInterfaceMethods<TiuInterface>,
                              DeclareOpInterfaceMethods<MemInterface>,
                              DeclareOpInterfaceMethods<EmitInterface>,
                              DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "dequant int";
    let arguments = (ins PPL_MemRef:$output, PPL_MemRef:$input,
                    PPL_Int:$offset, PPL_Int:$multiplier, PPL_Int:$shift,
                    PPL_Int:$round_mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DQPCIntOp: PPL_Op<"dqpc_int", [MemoryEffects<[MemWrite]>,
                              DeclareOpInterfaceMethods<TiuInterface>,
                              DeclareOpInterfaceMethods<MemInterface>,
                              DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                              DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "dequant perchannel int";
    let arguments = (ins PPL_MemRef:$output, PPL_MemRef:$input,PPL_MemRef:$quant,
                     PPL_Int:$round_mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_Dq2Op: PPL_Op<"dq2", [MemoryEffects<[MemWrite]>,
                              DeclareOpInterfaceMethods<TiuInterface>,
                              DeclareOpInterfaceMethods<MemInterface>,
                              DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                              DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "dequant 2";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$input,
                         PPL_MemRef:$offset_scale,
                         PPL_Int:$gsize);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_ShapeIndexOp: PPL_Op<"shape_index", [Pure]> {
    let summary = "shape[idx]";
    let arguments = (ins PPL_Type:$shape, PPL_Int:$idx);
    let results = (outs PPL_Type:$result);
    let assemblyFormat = "operands attr-dict `:` type(operands) `->` type($result)";
    let hasCanonicalizer = 1;
}

def PPL_NoneOp: PPL_Op<"none", [Pure]> {
    let summary = "shape";
    let results = (outs PPL_AnyType:$result);
}

def PPL_ArithShiftOp : PPL_Op<"arith_shift", [MemoryEffects<[MemWrite]>,
                              DeclareOpInterfaceMethods<TiuInterface>,
                              DeclareOpInterfaceMethods<MemInterface>,
                              DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                              DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "arith shift";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRefOrScalar:$src,
                         PPL_MemRefOrScalar:$sft,
                         PPL_Int:$rounding_mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_LogicalShiftOp : PPL_Op<"logical_shift", [MemoryEffects<[MemWrite]>,
                                DeclareOpInterfaceMethods<TiuInterface>,
                                DeclareOpInterfaceMethods<MemInterface>,
                                DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "logical shift";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRefOrScalar:$src,
                         PPL_MemRefOrScalar:$sft,
                         PPL_Int:$rounding_mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_CircularShiftOp : PPL_Op<"circular_shift", [MemoryEffects<[MemWrite]>,
                                 DeclareOpInterfaceMethods<TiuInterface>,
                                 DeclareOpInterfaceMethods<MemInterface>,
                                 DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                 DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "circular shift";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRefOrScalar:$src,
                         PPL_MemRefOrScalar:$sft,
                         PPL_Int:$rounding_mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_NpuBCastOp : PPL_Op<"npu_bcast", [MemoryEffects<[MemWrite]>,
                                DeclareOpInterfaceMethods<TiuInterface>,
                              DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                DeclareOpInterfaceMethods<MemInterface>,
                                DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "npu bcast";
    let arguments = (ins PPL_MemRef:$dst, PPL_MemRef:$src, PPL_Int:$num);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_NpuBCastStaticOp : PPL_Op<"npu_bcast_static", [MemoryEffects<[MemWrite]>,
                                DeclareOpInterfaceMethods<TiuInterface>,
                              DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                DeclareOpInterfaceMethods<MemInterface>,
                                DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "npu bcast from static";
    let arguments = (ins PPL_MemRef:$dst, PPL_Int:$npu_num, PPL_Int:$len, PPL_Int:$mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_LoadCoeffOp: PPL_Op<"load_coeff", [MemoryEffects<[MemWrite]>,
                            DeclareOpInterfaceMethods<TiuInterface>,
                            DeclareOpInterfaceMethods<MemInterface>,
                            DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "load_coeff";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_Int:$mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_HGatherOp: PPL_Op<"h_gather", [MemoryEffects<[MemWrite]>,
                                       DeclareOpInterfaceMethods<DmaInterface>,
                                       DeclareOpInterfaceMethods<MemInterface>,
                                       DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                       DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "gdma h gather";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$param,
                         PPL_MemRef:$index,
                         PPL_Type:$c,
                         PPL_Int:$index_start_pos);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_HScatterOp: PPL_Op<"h_scatter", [MemoryEffects<[MemWrite]>,
                                         DeclareOpInterfaceMethods<DmaInterface>,
                                         DeclareOpInterfaceMethods<MemInterface>,
                                         DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                         DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "gdma h scatter";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$param,
                         PPL_MemRef:$index);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_WGatherOp: PPL_Op<"w_gather", [MemoryEffects<[MemWrite]>,
                                       DeclareOpInterfaceMethods<TiuInterface>,
                                       DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                       DeclareOpInterfaceMethods<MemInterface>,
                                       DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "w gather";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$param,
                         PPL_MemRef:$index);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_WGatherExceptionOp: PPL_Op<"w_gather_exception", [MemoryEffects<[MemWrite]>,
                                   DeclareOpInterfaceMethods<TiuInterface>,
                                   DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                   DeclareOpInterfaceMethods<MemInterface>,
                                   DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "w gather exception";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$param,
                         PPL_MemRef:$index,
                         PPL_Type:$c,
                         PPL_Int:$fill_const);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_WScatterOp: PPL_Op<"w_scatter", [MemoryEffects<[MemWrite]>,
                           DeclareOpInterfaceMethods<TiuInterface>,
                           DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                           DeclareOpInterfaceMethods<MemInterface>,
                           DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "w scatter";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$param,
                         PPL_MemRef:$index);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_HWGatherOp: PPL_Op<"hw_gather", [MemoryEffects<[MemWrite]>,
                                         DeclareOpInterfaceMethods<TiuInterface>,
                                         DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                         DeclareOpInterfaceMethods<MemInterface>,
                                         DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "hw gather";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$param,
                         PPL_MemRef:$index);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_HWGatherExceptionOp: PPL_Op<"hw_gather_exception", [MemoryEffects<[MemWrite]>,
                                    DeclareOpInterfaceMethods<TiuInterface>,
                                    DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                    DeclareOpInterfaceMethods<MemInterface>,
                                    DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "hw gather exception";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$param,
                         PPL_MemRef:$index,
                         PPL_Type:$c,
                         PPL_Int:$fill_const);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_HWScatterOp: PPL_Op<"hw_scatter", [MemoryEffects<[MemWrite]>,
                            DeclareOpInterfaceMethods<TiuInterface>,
                            DeclareOpInterfaceMethods<MemInterface>,
                            DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                            DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "hw scatter";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$param,
                         PPL_MemRef:$index);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_BatchBcastHGatherOp: PPL_Op<"batch_bcast_h_gather", [MemoryEffects<[MemWrite]>,
                                    DeclareOpInterfaceMethods<TiuInterface>,
                                    DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                    DeclareOpInterfaceMethods<MemInterface>,
                                    DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "batch bcast h gather";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$param,
                         PPL_MemRef:$index,
                         PPL_Int:$is_param_repeated);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_BatchBcastHGatherExceptionOp: PPL_Op<"batch_bcast_h_gather_exception",
                                             [MemoryEffects<[MemWrite]>,
                                              DeclareOpInterfaceMethods<TiuInterface>,
                                              DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                              DeclareOpInterfaceMethods<MemInterface>,
                                              DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "batch bcast h gather exception";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$param,
                         PPL_MemRef:$index,
                         PPL_Type:$c,
                         PPL_Int:$is_param_repeated,
                         PPL_Int:$fill_const);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_BatchBcastHScatterOp: PPL_Op<"batch_bcast_h_scatter", [MemoryEffects<[MemWrite]>,
                                     DeclareOpInterfaceMethods<TiuInterface>,
                                     DeclareOpInterfaceMethods<MemInterface>,
                                     DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                     DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "batch bcast h scatter ";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$param,
                         PPL_MemRef:$index,
                         PPL_Int:$is_param_repeated);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_BatchBcastWGatherOp: PPL_Op<"batch_bcast_w_gather", [MemoryEffects<[MemWrite]>,
                                    DeclareOpInterfaceMethods<TiuInterface>,
                                    DeclareOpInterfaceMethods<MemInterface>,
                                    DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                    DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "batch bcast w gather";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$param,
                         PPL_MemRef:$index,
                         PPL_Int:$is_param_repeated);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_BatchBcastWGatherExceptionOp: PPL_Op<"batch_bcast_w_gather_exception", [MemoryEffects<[MemWrite]>,
                                             DeclareOpInterfaceMethods<TiuInterface>,
                                             DeclareOpInterfaceMethods<MemInterface>,
                                             DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                             DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "batch bcast w gather exception";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$param,
                         PPL_MemRef:$index,
                         PPL_Type:$c,
                         PPL_Int:$is_param_repeated,
                         PPL_Int:$fill_const);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_BatchBcastWScatterOp: PPL_Op<"batch_bcast_w_scatter", [MemoryEffects<[MemWrite]>,
                                     DeclareOpInterfaceMethods<TiuInterface>,
                                     DeclareOpInterfaceMethods<MemInterface>,
                                     DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                     DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "batch bcast w scatter ";
    let arguments = (ins PPL_MemRef:$output,
                         PPL_MemRef:$param,
                         PPL_MemRef:$index,
                         PPL_Int:$is_param_repeated);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_HauLineGatherOp: PPL_Op<"hau_gather_line", [MemoryEffects<[MemWrite]>,
                              DeclareOpInterfaceMethods<HauInterface>,
                              DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                              DeclareOpInterfaceMethods<EmitInterface, ["emitSG2260"]>]> {
    let summary = "hau line gather ";
    let arguments = (ins PPL_MemRef:$output, PPL_MemRef:$param,
                         PPL_MemRef:$index, PPL_FpInt:$c, PPL_Int:$start,
                         PPL_Int:$end, PPL_Int:$fill_const);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_BitwiseNotOp : PPL_Op<"bitwise_not", [MemoryEffects<[MemWrite]>,
                                DeclareOpInterfaceMethods<TiuInterface>,
                                DeclareOpInterfaceMethods<MemInterface>,
                                DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "bitwise not";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRefOrScalar:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_CmpOp : PPL_Op<"cmp", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<TiuInterface>,
                               DeclareOpInterfaceMethods<MemInterface>,
                               DeclareOpInterfaceMethods<EmitInterface>,
                               DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                               ResultsBroadcastableShape]> {
    let summary = "comparision op";
    let arguments = (ins PPL_MemRef:$rst,
                         PPL_MemRefOrScalar:$lhs,
                         PPL_MemRefOrScalar:$rhs,
                         PPL_Type:$true_val,
                         I64Attr:$mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_CmpSelectOp: PPL_Op<"cmp_select", [MemoryEffects<[MemWrite]>,
                           DeclareOpInterfaceMethods<TiuInterface>,
                           DeclareOpInterfaceMethods<MemInterface>,
                           DeclareOpInterfaceMethods<EmitInterface>,
                           DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "compare src0 and src1 then select src2 or src3";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRefOrScalar:$src0,
                         PPL_MemRefOrScalar:$src1,
                         PPL_MemRefOrScalar:$src2,
                         PPL_MemRefOrScalar:$src3,
                         I64Attr:$mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_ExtremaCmpSelectOp: PPL_Op<"extrema_cmp_select", [MemoryEffects<[MemWrite]>,
                           DeclareOpInterfaceMethods<TiuInterface>,
                           DeclareOpInterfaceMethods<MemInterface, ["getMemOutputIndex"]>,
                           DeclareOpInterfaceMethods<EmitInterface>,
                           DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "compare and select between src0 and src1 then select src2 or src3";
    let arguments = (ins PPL_MemRef:$dst0,
                         PPL_MemRef:$dst1,
                         PPL_MemRefOrScalar:$src0,
                         PPL_MemRefOrScalar:$src1,
                         PPL_MemRefOrScalar:$src2,
                         PPL_MemRefOrScalar:$src3,
                         I64Attr:$mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_VcCmpOp : PPL_Op<"vc_cmp",[MemoryEffects<[MemWrite]>,
                                   DeclareOpInterfaceMethods<TiuInterface>,
                                   DeclareOpInterfaceMethods<MemInterface>,
                                   DeclareOpInterfaceMethods<EmitInterface>,
                                   DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "vector correlation comparision";
    let arguments = (ins PPL_MemRef:$rst, PPL_MemRef:$lhs, PPL_MemRef:$rhs,
                         PPL_Type:$true_val, PPL_Int:$mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_FpScaleOp: PPL_Op<"fp_scale", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<TiuInterface>,
                               DeclareOpInterfaceMethods<MemInterface>,
                               DeclareOpInterfaceMethods<EmitInterface>,
                               DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                            ]> {
    let summary = "Fp Scale";
    let arguments = (ins PPL_MemRef:$dst,
                     PPL_MemRef:$src,
                     PPL_AnyType:$scale,
                     PPL_AnyType:$bias);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_FpAddBiasSqrOp: PPL_Op<"fp_add_bias_sqr", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<TiuInterface>,
                               DeclareOpInterfaceMethods<MemInterface>,
                               DeclareOpInterfaceMethods<EmitInterface>,
                               DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "Fp Add Bias Sqr";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRefOrScalar:$src,
                         PPL_MemRefOrScalar:$bias);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_FpSubBiasSqrOp: PPL_Op<"fp_sub_bias_sqr", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<TiuInterface>,
                               DeclareOpInterfaceMethods<MemInterface>,
                               DeclareOpInterfaceMethods<EmitInterface>,
                               DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "Fp Sub Bias Sqr";
    let arguments = (ins PPL_MemRef:$dst,
                     PPL_MemRefOrScalar:$src,
                     PPL_MemRefOrScalar:$bias);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_FpMulAddOp: PPL_Op<"fp_mul_add", [MemoryEffects<[MemWrite]>,
                           DeclareOpInterfaceMethods<TiuInterface>,
                           DeclareOpInterfaceMethods<MemInterface>,
                           DeclareOpInterfaceMethods<EmitInterface>,
                           DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "fp mul add";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRefOrScalar:$src0,
                         PPL_MemRefOrScalar:$src1,
                         PPL_MemRefOrScalar:$src2);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_FpDivOp : PPL_Op<"tunable_div", [MemoryEffects<[MemWrite]>,
                         DeclareOpInterfaceMethods<TiuInterface>,
                         DeclareOpInterfaceMethods<MemInterface>,
                         DeclareOpInterfaceMethods<EmitInterface>,
                         DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                         ResultsBroadcastableShape]> {
    let summary = "fp32 div";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRefOrScalar:$src0,
                         PPL_MemRefOrScalar:$src1,
                         PPL_Int:$numiter);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_MaskSelectOp: PPL_Op<"mask_select", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<DmaInterface>,
                               DeclareOpInterfaceMethods<MemInterface>,
                               DeclareOpInterfaceMethods<EmitInterface>,
                               DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                               ]> {
    let summary = "Mask select";
    let arguments = (
                     ins PPL_MemRef:$dst,
                     PPL_MemRef:$src,
                     PPL_MemRef:$mask
                    );
    let results = (outs PPL_Int:$filter_num);
    let assemblyFormat = "operands attr-dict `:` type(operands) `->` type($filter_num)";
}

def PPL_MaskSelectBatchBcastOp: PPL_Op<"mask_select_batch_bcast", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<MemInterface>,
                               DeclareOpInterfaceMethods<EmitInterface>,
                               DeclareOpInterfaceMethods<TiuInterface>,
                               DeclareOpInterfaceMethods<ShapeInferenceOpInterface>
                               ]> {
    let summary = "Mask select with Batch Bcast";
    let arguments = (
                     ins PPL_MemRef:$dst,
                     PPL_MemRef:$count,
                     PPL_MemRef:$src,
                     PPL_MemRef:$mask,
                     PPL_Int:$isparamrepeated
                    );
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_FpTaylorOp: PPL_Op<"fp_taylor", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<TiuInterface>,
                               DeclareOpInterfaceMethods<MemInterface>,
                               DeclareOpInterfaceMethods<EmitInterface>,
                               DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "fp taylor";
    let arguments = (
                     ins PPL_MemRef:$dst,
                     PPL_MemRef:$src,
                     PPL_MemRef:$table,
                     PPL_Int:$len
                    );
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_NormalOp: PPL_Op<"normal", [MemoryEffects<[MemWrite]>,
                                    DeclareOpInterfaceMethods<TiuInterface>,
                                    DeclareOpInterfaceMethods<MemInterface>,
                                    DeclareOpInterfaceMethods<EmitInterface>,
                                    DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "normal";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_FpExponentPartOp: PPL_Op<"fp_exponent_part", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<TiuInterface>,
                               DeclareOpInterfaceMethods<MemInterface>,
                               DeclareOpInterfaceMethods<EmitInterface>,
                               DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "fp exponent part";
    let arguments = (
                     ins PPL_MemRef:$dst, PPL_MemRef:$src
                    );
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_SinOp: PPL_Op<"sin", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<MemInterface>,
                               DeclareOpInterfaceMethods<TiuInterface>,
                               DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "sin";
    let arguments = (
                     ins PPL_MemRef:$output,
                     PPL_MemRef:$input
                    );
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_CosOp: PPL_Op<"cos", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<MemInterface>,
                               DeclareOpInterfaceMethods<TiuInterface>,
                               DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "cos";
    let arguments = (
                     ins PPL_MemRef:$output,
                     PPL_MemRef:$input
                    );
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_ArcSinOp: PPL_Op<"arcsin", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<MemInterface>,
                               DeclareOpInterfaceMethods<TiuInterface>,
                               DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "arcsin";
    let arguments = (
                     ins PPL_MemRef:$output,
                     PPL_MemRef:$input
                    );
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_ArcCosOp: PPL_Op<"arccos", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<MemInterface>,
                               DeclareOpInterfaceMethods<TiuInterface>,
                               DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "arccos";
    let arguments = (
                     ins PPL_MemRef:$output,
                     PPL_MemRef:$input
                    );
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_TanOp: PPL_Op<"tan", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<MemInterface>,
                               DeclareOpInterfaceMethods<TiuInterface>,
                               DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "tan";
    let arguments = (
                     ins PPL_MemRef:$output,
                     PPL_MemRef:$input
                    );
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_ExpOp: PPL_Op<"exp", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<MemInterface>,
                               DeclareOpInterfaceMethods<TiuInterface>,
                               DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "exp";
    let arguments = (
                     ins PPL_MemRef:$output,
                     PPL_MemRef:$input
                    );
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_MacIntOp: PPL_Op<"int8_mac", [MemoryEffects<[MemWrite]>,
                           DeclareOpInterfaceMethods<TiuInterface>,
                           DeclareOpInterfaceMethods<MemInterface>,
                           DeclareOpInterfaceMethods<EmitInterface>,
                           DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                           ResultsBroadcastableShape]> {
    let summary = "mac int8 op";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRefOrScalar:$lhs,
                         PPL_MemRefOrScalar:$rhs,
                         PPL_Int:$l_shift,
                         PPL_Int:$r_shift,
                         PPL_Int:$round_mode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_DmaNonZeroOp: PPL_Op<"dma_nonzero", [MemoryEffects<[MemWrite]>,
                                DeclareOpInterfaceMethods<DmaInterface>,
                                DeclareOpInterfaceMethods<MemInterface>,
                                DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "gdma nonzero";
    let arguments = (ins PPL_MemRef:$dst, PPL_MemRef:$src);
    let results = (outs PPL_Int:$filter_num);
    let assemblyFormat = "operands attr-dict `:` type(operands) `->` type($filter_num)";
}

def PPL_NonZeroOp: PPL_Op<"nonzero", [MemoryEffects<[MemWrite]>,
                                      DeclareOpInterfaceMethods<DmaInterface>,
                                      DeclareOpInterfaceMethods<MemInterface, ["getMemOutputIndex"]>,
                                      DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                      DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "gdma nonzero";
    let arguments = (ins PPL_MemRef:$dst_idx,
                         PPL_MemRef:$dst_cnt,
                         PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_SdmaLoadOp : PPL_Op<"sdma_load", [MemoryEffects<[MemWrite]>,
                            DeclareOpInterfaceMethods<MemInterface>,
                            DeclareOpInterfaceMethods<SdmaInterface>,
                            DeclareOpInterfaceMethods<EmitInterface, ["emitSG2260"]>,
                            DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "copy system memory to l2 memory by core index";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_VsdmaLoadOp : PPL_Op<"vsdma_load", [MemoryEffects<[MemWrite]>,
                            DeclareOpInterfaceMethods<MemInterface>,
                            DeclareOpInterfaceMethods<SdmaInterface>,
                            DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                            DeclareOpInterfaceMethods<EmitInterface, ["emitSG2260"]>]> {
    let summary = "copy system memory to l2 memory by core index";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src,
                         PPL_IntLike:$port_id);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_SdmaLoadNCTransOp : PPL_Op<"load_nc_trans", [MemoryEffects<[MemWrite]>,
                                      DeclareOpInterfaceMethods<MemInterface>,
                                      DeclareOpInterfaceMethods<SdmaInterface>,
                                      DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                      DeclareOpInterfaceMethods<EmitInterface, ["emitSG2260"]>]> {
    let summary = "sdma load nc trans to l2 memory";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_SdmaLoadCWTransOp : PPL_Op<"load_cw_trans", [MemoryEffects<[MemWrite]>,
                                      DeclareOpInterfaceMethods<MemInterface>,
                                      DeclareOpInterfaceMethods<SdmaInterface>,
                                      DeclareOpInterfaceMethods<ShapeInferenceOpInterface>,
                                      DeclareOpInterfaceMethods<EmitInterface, ["emitSG2260"]>]> {
    let summary = "sdma load cw trans to l2 memory";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_CpyCrossNpuOp: PPL_Op<"cpy_cross_npu", [MemoryEffects<[MemWrite]>,
                           DeclareOpInterfaceMethods<DmaInterface>,
                           DeclareOpInterfaceMethods<MemInterface>,
                           DeclareOpInterfaceMethods<EmitInterface, ["emitSG2260"]>,
                           DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "copy cross npu";
    let arguments = (ins PPL_MemRef:$dst, PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_Fp32SqrtOp: PPL_Op<"fp32_sqrt",
                                [MemoryEffects<[MemWrite]>,
                                DeclareOpInterfaceMethods<TiuInterface>,
                                DeclareOpInterfaceMethods<MemInterface>,
                                DeclareOpInterfaceMethods<EmitInterface, ["emitSG2260", "emitBM1688"]>,
                                DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "fp32 sqrt";
    let arguments = (ins PPL_MemRef:$dst, PPL_MemRef:$src, PPL_Int:$num_iter);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_Fp32RsqrtOp: PPL_Op<"fp32_rsqrt",
                                [MemoryEffects<[MemWrite]>,
                                DeclareOpInterfaceMethods<TiuInterface>,
                                DeclareOpInterfaceMethods<MemInterface>,
                                DeclareOpInterfaceMethods<EmitInterface, ["emitSG2260", "emitBM1688"]>,
                                DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "fp32 rsqrt";
    let arguments = (ins PPL_MemRef:$dst, PPL_MemRef:$src, PPL_Int:$num_iter);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_LogxOp: PPL_Op<"logx", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<TiuInterface>,
                               DeclareOpInterfaceMethods<MemInterface>,
                               DeclareOpInterfaceMethods<EmitInterface>,
                               DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "logx";
    let arguments = (
                     ins PPL_MemRef:$dst,
                     PPL_MemRef:$src,
                     PPL_MemRef:$work0,
                     PPL_MemRef:$coeff,
                     PPL_Float:$x
                    );
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_LogOp: PPL_Op<"loge", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<TiuInterface>,
                               DeclareOpInterfaceMethods<MemInterface>,
                               DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "ln";
    let arguments = (
                     ins PPL_MemRef:$dst,
                         PPL_MemRef:$src
                    );
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_CLZOp: PPL_Op<"count_leading_zero", [MemoryEffects<[MemWrite]>,
                      DeclareOpInterfaceMethods<TiuInterface>,
                      DeclareOpInterfaceMethods<MemInterface>,
                      DeclareOpInterfaceMethods<EmitInterface>,
                      DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "count leading zero";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRefOrScalar:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_CLOOp: PPL_Op<"count_leading_one", [MemoryEffects<[MemWrite]>,
                      DeclareOpInterfaceMethods<TiuInterface>,
                      DeclareOpInterfaceMethods<MemInterface>,
                      DeclareOpInterfaceMethods<EmitInterface>,
                      DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "count leading one";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRefOrScalar:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_SmemBcastOp : PPL_Op<"smem_bcast", [MemoryEffects<[MemWrite]>,
                             DeclareOpInterfaceMethods<EmitInterface>,
                             DeclareOpInterfaceMethods<DmaInterface>,
                             DeclareOpInterfaceMethods<MemInterface>]> {
    let summary = "bcast static mem";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_Int:$smem_offset);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_SmemDistOp : PPL_Op<"smem_dist", [MemoryEffects<[MemWrite]>,
                             DeclareOpInterfaceMethods<EmitInterface>,
                             DeclareOpInterfaceMethods<DmaInterface>,
                             DeclareOpInterfaceMethods<MemInterface>]> {
    let summary = "dist static mem";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_Int:$smem_offset);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_VectorSetOp : PPL_Op<"vector_set", [MemoryEffects<[MemWrite]>,
                             DeclareOpInterfaceMethods<EmitInterface>]> {
    let summary = "set vector register";
    let arguments = (ins PPL_Int:$e_width,
                         PPL_Int:$lmul,
                         PPL_Int:$v_len);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_VectorLoadOp : PPL_Op<"vector_load", [MemoryEffects<[MemWrite]>,
                              DeclareOpInterfaceMethods<EmitInterface>,
                              DeclareOpInterfaceMethods<DmaInterface>,
                              DeclareOpInterfaceMethods<MemInterface>]> {
    let summary = "vector register load from global mem";
    let arguments = (ins PPL_Int:$v_idx,
                         PPL_MemRef:$src_gmem);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_VectorStoreOp : PPL_Op<"vector_store", [MemoryEffects<[MemWrite]>,
                               DeclareOpInterfaceMethods<EmitInterface>,
                               DeclareOpInterfaceMethods<DmaInterface>,
                               DeclareOpInterfaceMethods<MemInterface>]> {
    let summary = "vector register store to global mem";
    let arguments = (ins PPL_MemRef:$dst_gmem,
                         PPL_Int:$v_idx);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_MoveTVOp : PPL_Op<"move_tv", [MemoryEffects<[MemWrite]>,
                                      DeclareOpInterfaceMethods<EmitInterface>,
                                      DeclareOpInterfaceMethods<DmaInterface>,
                                      DeclareOpInterfaceMethods<MemInterface>]> {
    let summary = "move data from vector register to local/static mem";
    let arguments = (ins PPL_MemRefOrScalar:$dst,
                         PPL_Int:$v_idx);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_MoveDistVOp : PPL_Op<"move_distv", [MemoryEffects<[MemWrite]>,
                             DeclareOpInterfaceMethods<EmitInterface>,
                             DeclareOpInterfaceMethods<DmaInterface>,
                             DeclareOpInterfaceMethods<MemInterface>]> {
    let summary = "move data from vector register to local mem";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_Int:$v_idx);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_MoveVVOp : PPL_Op<"move_vv", [MemoryEffects<[MemWrite]>,
                                      DeclareOpInterfaceMethods<EmitInterface>,
                                      DeclareOpInterfaceMethods<DmaInterface>,
                                      DeclareOpInterfaceMethods<MemInterface>]> {
    let summary = "move data from two vector registers to local/static mem";
    let arguments = (ins PPL_MemRefOrScalar:$dst,
                         PPL_Int:$v_idx0,
                         PPL_Int:$v_idx1);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_MoveDistVVOp : PPL_Op<"move_distvv", [MemoryEffects<[MemWrite]>,
                                              DeclareOpInterfaceMethods<EmitInterface>,
                                              DeclareOpInterfaceMethods<DmaInterface>,
                                              DeclareOpInterfaceMethods<MemInterface>]> {
    let summary = "move data from two vector registers to local mem";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_Int:$v_idx0,
                         PPL_Int:$v_idx1);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_MoveVTOp : PPL_Op<"move_vt", [MemoryEffects<[MemWrite]>,
                                      DeclareOpInterfaceMethods<EmitInterface>,
                                      DeclareOpInterfaceMethods<DmaInterface>,
                                      DeclareOpInterfaceMethods<MemInterface>]> {
    let summary = "move data from local/static mem to vector register";
    let arguments = (ins PPL_Int:$dst_v_idx,
                         PPL_MemRefOrScalar:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_MoveVCollOp : PPL_Op<"move_v_coll", [MemoryEffects<[MemWrite]>,
                                             DeclareOpInterfaceMethods<EmitInterface>,
                                             DeclareOpInterfaceMethods<DmaInterface>,
                                             DeclareOpInterfaceMethods<MemInterface>]> {
    let summary = "move data from local/static mem to vector register";
    let arguments = (ins PPL_Int:$dst_v_idx,
                         PPL_MemRef:$src);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_TiuMaskSelectOp : PPL_Op<"tiu_mask_select", [MemoryEffects<[MemWrite]>,
                                 DeclareOpInterfaceMethods<EmitInterface>,
                                 DeclareOpInterfaceMethods<DmaInterface>,
                                 DeclareOpInterfaceMethods<MemInterface, ["getMemOutputIndex"]>,
                                 DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "mask select";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$dst_cnt,
                         PPL_MemRef:$src,
                         PPL_MemRef:$mask);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_ReduceOp : PPL_Op<"dma_reduce", [MemoryEffects<[MemWrite]>,
                                 DeclareOpInterfaceMethods<EmitInterface, ["emitSG2260"]>,
                                 DeclareOpInterfaceMethods<DmaInterface>,
                                 DeclareOpInterfaceMethods<MemInterface>,
                                 DeclareOpInterfaceMethods<ShapeInferenceOpInterface>]> {
    let summary = "dma all reduce";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src,
                         PPL_Int:$psum,
                         PPL_Int:$opcode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

def PPL_SdmaReduceOp : PPL_Op<"sdma_reduce", [MemoryEffects<[MemWrite]>,
                                      DeclareOpInterfaceMethods<MemInterface>,
                                      DeclareOpInterfaceMethods<SdmaInterface>,
                                      DeclareOpInterfaceMethods<MemInterface>,
                                      DeclareOpInterfaceMethods<EmitInterface, ["emitSG2260"]>]> {
    let summary = "sdma all reduce";
    let arguments = (ins PPL_MemRef:$dst,
                         PPL_MemRef:$src,
                         PPL_Int:$psum,
                         PPL_Int:$opcode);
    let assemblyFormat = "operands attr-dict `:` type(operands)";
}

#endif // Ppl_OPS
