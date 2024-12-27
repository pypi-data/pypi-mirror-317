#ifndef PPL_OPINTERFACES
#define PPL_OPINTERFACES

include "mlir/IR/OpBase.td"
include "mlir/IR/PatternBase.td"

def MemInterface : OpInterface<"MemInterface"> {
  let description = [{}];
  let cppNamespace = "::mlir::ppl";
  let methods = [
      InterfaceMethod<
        /*desc=*/[{}],
        /*retType=*/"std::vector<int64_t>",
        /*methodName=*/"getMemOperands",
        /*args=*/(ins)
      >,
      InterfaceMethod<
              /*desc=*/"Get the indexes of output mem tensors",
              /*retType=*/"std::vector<int64_t>",
              /*methodName=*/"getMemOutputIndex",
              /*args=*/(ins),
              /*methodBody=*/[{}],
              /*defaultImplementation=*/[{
                std::vector<int64_t> out_list = {0};
                return out_list;
              }]>
  ];
}

def DmaInterface : OpInterface<"DmaInterface"> {
  let description = [{}];
  let cppNamespace = "::mlir::ppl";
  let methods = [
      InterfaceMethod<
        /*desc=*/[{}],
        /*retType=*/"std::map<int64_t, std::vector<int64_t>>",
        /*methodName=*/"getBankConflictMap",
        /*args=*/(ins)
      >,
  ];
}

def TiuInterface : OpInterface<"TiuInterface"> {
  let description = [{}];
  let cppNamespace = "::mlir::ppl";
  let methods = [
      InterfaceMethod<
        /*desc=*/[{}],
        /*retType=*/"std::map<int64_t, std::vector<int64_t>>",
        /*methodName=*/"getBankConflictMap",
        /*args=*/(ins)
      >,
  ];
}

def SdmaInterface : OpInterface<"SdmaInterface"> {
  let description = [{}];
  let cppNamespace = "::mlir::ppl";
}

def HauInterface : OpInterface<"HauInterface"> {
  let description = [{}];
  let cppNamespace = "::mlir::ppl";
}

def EmitInterface : OpInterface<"EmitInterface"> {
  let description = [{}];
  let cppNamespace = "::mlir::ppl";
  let methods = [
      InterfaceMethod<
        /*desc=*/[{}],
        /*retType=*/"::mlir::LogicalResult",
        /*methodName=*/"emitBM1684x",
        /*args=*/(ins "void *":$emitter)
      >,
      InterfaceMethod<
        /*desc=*/[{}],
        /*retType=*/"::mlir::LogicalResult",
        /*methodName=*/"emitSG2260",
        /*args=*/(ins "void *":$emitter),
        [{}],
        [{
          return $_op.emitBM1684x(emitter);
        }]
      >,
      InterfaceMethod<
        /*desc=*/[{}],
        /*retType=*/"::mlir::LogicalResult",
        /*methodName=*/"emitBM1688",
        /*args=*/(ins "void *":$emitter),
        [{}],
        [{
          return $_op.emitBM1684x(emitter);
        }]
      >,
      InterfaceMethod<
        /*desc=*/[{}],
        /*retType=*/"::mlir::LogicalResult",
        /*methodName=*/"emitSG2380",
        /*args=*/(ins "void *":$emitter)
      >
  ];
}

def TensorInterface : OpInterface<"TensorInterface"> {
  let description = [{}];
  let cppNamespace = "::mlir::ppl";
  let methods = [
      InterfaceMethod<
        /*desc=*/[{}],
        /*retType=*/"mlir::Operation *",
        /*methodName=*/"getOriTensor",
        /*args=*/(ins)
      >,
      // InterfaceMethod<
      //   /*desc=*/[{}],
      //   /*retType=*/"bool",
      //   /*methodName=*/"getIsUnsigned",
      //   /*args=*/(ins),
      //   [{}],
      //   [{
      //     return $_op.getResult().getType().cast<MemRefType>().getElementType().isUnsignedInteger();
      //   }]
      // >,
      InterfaceMethod<
        /*desc=*/[{}],
        /*retType=*/"mlir::Value",
        /*methodName=*/"getShape",
        /*args=*/(ins),
        [{}],
        [{
          return $_op.getShape();
        }]
      >,
      InterfaceMethod<
        /*desc=*/[{}],
        /*retType=*/"mlir::ppl::TensorMode",
        /*methodName=*/"getTensorMode",
        /*args=*/(ins)
      >,
      InterfaceMethod<
        /*desc=*/[{}],
        /*retType=*/"int64_t",
        /*methodName=*/"getAlignMode",
        /*args=*/(ins),
        [{}],
        [{
          return $_op.getAlignMode();
        }]
      >,
  ];

}

def ShapeInferenceOpInterface : OpInterface<"ShapeInferenceOpInterface"> {
  let description = [{
    collect the output tensor's related tensor info.
  }];

  let cppNamespace = "::mlir";
  let methods = [
    InterfaceMethod<
              /*desc=*/"collect the output tensor's related tensor info.",
              /*retType=*/"void",
              /*methodName=*/"inferShapes",
              /*args=*/(ins "llvm::DenseMap<Operation *, llvm::SmallVector<std::list<std::tuple<Value, int32_t, int32_t, std::optional<AffineMap>, std::optional<std::vector<Value>>>>, 4>>  &":$lists),
              /*methodBody=*/[{}],
              /*defaultImplementation=*/[{
                  auto op =
                    ::llvm::cast<ShapeInferenceOpInterface>($_op.getOperation());
                  return op.defaultInfer(this->getOperation(), lists);
              }]>,
    InterfaceMethod<
      /*desc=*/[{}],
      /*retType=*/"mlir::LogicalResult",
      /*methodName=*/"runInferShape",
      /*args=*/(ins "mlir::ppl::InferCache &":$cache)>
  ];

  let extraClassDeclaration = [{
    void defaultInfer(mlir::Operation * op,
                     llvm::DenseMap<Operation *,
                               llvm::SmallVector<std::list<
                                  std::tuple<Value, int32_t, int32_t, std::optional<AffineMap>, std::optional<std::vector<Value>>>>, 4>>  &);
  }];
}

def LongLivedInterface : OpInterface<"LongLivedInterface"> {
  let description = [{}];
  let cppNamespace = "::mlir::ppl";
  let methods = [
      InterfaceMethod<
        /*desc=*/[{}],
        /*retType=*/"bool",
        /*methodName=*/"haveLongLiveRange",
        /*args=*/(ins),
        /*methodBody=*/[{}],
        /*defaultImplementation=*/[{
          auto op = ::llvm::cast<LongLivedInterface>($_op.getOperation());
          return op.defaultLongLive($_op.getAccumulate());
        }]
      >
  ];

  let extraClassDeclaration = [{
    bool defaultLongLive(mlir::Value val);
  }];
}

#endif // PPL_OPINTERFACES
