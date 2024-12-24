#include "mlir/Analysis/DataFlow/ConstantPropagationAnalysis.h"
#include "mlir/Analysis/DataFlow/DeadCodeAnalysis.h"
#include "mlir/Analysis/DataFlow/IntegerRangeAnalysis.h"
#include "mlir/Analysis/SliceAnalysis.h"
#include "mlir/Dialect/Affine/IR/AffineOps.h"
#include "mlir/Dialect/Affine/IR/AffineValueMap.h"
#include "mlir/Dialect/Affine/Passes.h"
#include "mlir/IR/AffineExpr.h"
#include "mlir/IR/AffineMap.h"
#pragma once
#include "mlir/Support/MathExtras.h"
#include "mlir/Transforms/FoldUtils.h"
#include <algorithm>
#include <list>
#include <set>

using namespace mlir;
using namespace mlir::dataflow;

namespace mlir {
namespace ppl {
using DimValue = std::pair<int, AffineMap>;
using ShapeValueVec = llvm::SmallVector<DimValue, 4>;
class ShapeAnalysis {
public:
  ShapeAnalysis() {}

  LogicalResult setConfig(Operation *root, MLIRContext *context,
                          std::set<int> &dyn_idxes);

  // Infer the maximum value of mlir::Value
  LogicalResult inferMaxValue(Value val, DimValue &rst);
  LogicalResult inferMinValue(Value val, DimValue &rst);

  LogicalResult init();

public:
  Operation *root;
  DataFlowSolver solver;
  MLIRContext *context;
  std::set<int> dyn_idxes;
  bool dyn_block = false;
  bool inited = false;
};

struct InferCache {
  DenseMap<Operation *, ShapeValueVec>
      tensor_cache; // save tensor & subtensor 's block shape
  DenseMap<Operation *, ShapeValueVec>
      shape_cache;                               // save ShapeOp's block shape
  DenseMap<Operation *, Value> sub_tensor_cache; // save tensor's last subtensor
  DenseSet<Operation *> uninited_tensor;
  std::unique_ptr<OperationFolder> folder;
  std::unique_ptr<OpBuilder> builder;
  std::unique_ptr<ShapeAnalysis> analysis;
  mlir::Dialect *arithDialect;
  Operation *root;
  bool dyn_block = false;

  //use RAII to manage the data container
  Value nullOp = Value{};
  std::map<int, Value> constOpMap;

  LogicalResult init(Operation *_root, MLIRContext *context,
                     std::set<int> &dyn_idxes) {
    root = _root;
    builder = std::make_unique<OpBuilder>(context);
    folder = std::make_unique<OperationFolder>(context);
    arithDialect = context->getLoadedDialect<arith::ArithDialect>();

    analysis = std::make_unique<ShapeAnalysis>();
    return analysis->setConfig(root, context, dyn_idxes);
  }
};

} // namespace ppl
} // namespace mlir
