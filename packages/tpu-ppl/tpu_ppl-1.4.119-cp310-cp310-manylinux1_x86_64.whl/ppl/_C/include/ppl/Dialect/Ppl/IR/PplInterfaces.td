#ifndef PPL_INTERFACES
#define PPL_INTERFACES

include "mlir/IR/OpBase.td"

def TensorSizeTrait : NativeOpTrait<"TensorSizeTrait">;
def IsDebugTrait: NativeOpTrait<"IsDebugTrait">;
def SameOperandsAndResultEncoding : NativeOpTrait<"SameOperandsAndResultEncoding">;
def SameOperandsEncoding : NativeOpTrait<"SameOperandsEncoding">;
#endif // PPL_INTERFACES
