#pragma once
#include "mlir/Dialect/Arith/IR/Arith.h"
#include "mlir/Dialect/ControlFlow/IR/ControlFlowOps.h"
#include "mlir/Dialect/Func/IR/FuncOps.h"
#include "mlir/Dialect/SCF/IR/SCF.h"
#include "mlir/IR/BuiltinOps.h"
#include "mlir/IR/BuiltinTypes.h"
#include "mlir/IR/Dialect.h"
#include "mlir/IR/Operation.h"
#include "mlir/Support/IndentedOstream.h"
#include "ppl/Dialect/Ppl/IR/Dialect.h"
#include "ppl/Support/CEmitter.h"

#define EMITWITHCALLEE(OP, CALLEE)                                             \
  LogicalResult emitCommon(void *emitter, OP##Op op,                           \
                           StringRef funcName = #CALLEE);
#define EMITWITHOUTCALLEE(OP)                                                  \
  LogicalResult emitCommon(void *emitter, OP##Op op);
#define GetMacro(_1, _2, NAME, ...) NAME
#define EMITCOMMON(...)                                                        \
  GetMacro(__VA_ARGS__, EMITWITHCALLEE, EMITWITHOUTCALLEE, ...)(__VA_ARGS__)
namespace mlir {
namespace ppl {

EMITCOMMON(arith::Constant)
EMITCOMMON(arith::AddI)
EMITCOMMON(arith::OrI)
EMITCOMMON(arith::AddF)
EMITCOMMON(arith::AndI)
EMITCOMMON(arith::CmpI)
EMITCOMMON(arith::DivSI)
EMITCOMMON(arith::DivUI)
EMITCOMMON(arith::DivF)
EMITCOMMON(arith::ExtSI)
EMITCOMMON(arith::ExtUI)
EMITCOMMON(arith::TruncI)
EMITCOMMON(arith::TruncF)
EMITCOMMON(arith::IndexCast)
EMITCOMMON(arith::MinSI, MIN)
EMITCOMMON(arith::MaxSI, MAX)
EMITCOMMON(arith::MulI)
EMITCOMMON(arith::MulF)
EMITCOMMON(arith::RemSI)
EMITCOMMON(arith::SIToFP)
EMITCOMMON(arith::SubI)
EMITCOMMON(arith::SubF)
EMITCOMMON(arith::Select)
EMITCOMMON(arith::XOrI)
EMITCOMMON(arith::FPToSI)
EMITCOMMON(cf::Branch)
EMITCOMMON(cf::CondBranch)
EMITCOMMON(func::Call)
EMITCOMMON(func::Constant)
// EMITCOMMON(func::Func)
EMITCOMMON(func::Return)
EMITCOMMON(Module)
EMITCOMMON(scf::For)
EMITCOMMON(scf::If)
EMITCOMMON(scf::Yield)
EMITCOMMON(AffineLoad)
// EMITCOMMON(memref::Alloca)
// EMITCOMMON(AffineStore)

LogicalResult emitCommon(void *emitter, std::vector<func::FuncOp> &func_ops,
                         const std::string &file_path,
                         const std::string &file_base_name = "",
                         RunMode mode = PioMode, bool isTest = false);

LogicalResult emitHostHeader(const std::vector<func::FuncOp> &func_ops,
                             const std::string &file_path,
                             const std::string &file_base_name,
                             const char *chip, RunMode mode);

LogicalResult emitHost(std::vector<func::FuncOp> &func_ops,
                       const std::string &file_path,
                       const std::string &file_base_name, mlir::ppl::Chip chip,
                       RunMode mode, bool is_test);

LogicalResult emitMain(const std::vector<func::FuncOp> &func_ops,
                       const std::string &file_path,
                       const std::string &file_base_name, Chip chip,
                       const char *chip_str, bool gen_ref, bool is_desc,
                       bool autotune = false);

LogicalResult emitKernel(std::vector<func::FuncOp> &func_ops,
                         const std::string &file_path,
                         const std::string &file_base_name, Chip chip,
                         RunMode mode, bool is_test = false);

LogicalResult emitAutotuneTest(const std::vector<func::FuncOp> &func_ops,
                               const std::string &file_path,
                               const std::string &file_base_name);

LogicalResult emitTorchHostMem(std::vector<func::FuncOp> &func_ops,
                               const std::string &file_path,
                               const std::string &file_base_name,
                               mlir::ppl::Chip chip);
LogicalResult emitPyBind(std::vector<func::FuncOp> &func_ops,
                               const std::string &file_path,
                               const std::string &file_base_name,
                               mlir::ppl::Chip chip);
} // namespace ppl
} // namespace mlir
