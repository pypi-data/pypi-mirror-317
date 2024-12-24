//===-DimRangAnalysis.h - Integer range analysis -----------*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// This file declares the dataflow analysis class for integer range inference
// so that it can be used in transformations over the `arith` dialect such as
// branch elimination or signed->unsigned rewriting
//
//===----------------------------------------------------------------------===//

#pragma once
#include "mlir/Analysis/DataFlow/SparseAnalysis.h"
#include "mlir/Interfaces/InferIntRangeInterface.h"
using namespace mlir::dataflow;
namespace mlir {
namespace ppl {

/// This lattice value represents the integer range of an SSA value.
class DimValueRang {
public:
  /// Create a maximal range ([0, uint_max(t)] / [int_min(t), int_max(t)])
  /// range that is used to mark the value as unable to be analyzed further,
  /// where `t` is the type of `value`.
  static DimValueRang getMaxRange(Value value);

  /// Create an integer value range lattice value.
  DimValueRang(std::optional<ConstantIntRanges> value = std::nullopt)
      : value(std::move(value)) {}

  /// Whether the range is uninitialized. This happens when the state hasn't
  /// been set during the analysis.
  bool isUninitialized() const { return !value.has_value(); }

  /// Get the known integer value range.
  const ConstantIntRanges &getValue() const {
    assert(!isUninitialized());
    return *value;
  }

  /// Compare two ranges.
  bool operator==(const DimValueRang &rhs) const { return value == rhs.value; }

  /// Take the union of two ranges.
  static DimValueRang join(const DimValueRang &lhs, const DimValueRang &rhs) {
    if (lhs.isUninitialized())
      return rhs;
    if (rhs.isUninitialized())
      return lhs;
    return DimValueRang{lhs.getValue().rangeUnion(rhs.getValue())};
  }

  /// Print the integer value range.
  void print(raw_ostream &os) const { os << value; }

private:
  /// The known integer value range.
  std::optional<ConstantIntRanges> value;
};

/// This lattice element represents the integer value range of an SSA value.
/// When this lattice is updated, it automatically updates the constant value
/// of the SSA value (if the range can be narrowed to one).
class DimValueRangLattice : public Lattice<DimValueRang> {
public:
  using Lattice::Lattice;

  /// If the range can be narrowed to an integer constant, update the constant
  /// value of the SSA value.
  void onUpdate(DataFlowSolver *solver) const override;
  void printDependent() const {
    for (auto depend : dependents) {
      depend.first.print(llvm::errs());
    }
  }
};

/// Integer range analysis determines the integer value range of SSA values
/// using operations that define `InferIntRangeInterface` and also sets the
/// range of iteration indices of loops with known bounds.
class DimRangAnalysis : public SparseDataFlowAnalysis<DimValueRangLattice> {
public:
  using SparseDataFlowAnalysis::SparseDataFlowAnalysis;

  /// At an entry point, we cannot reason about interger value ranges.
  void setToEntryState(DimValueRangLattice *lattice) override {
    propagateIfChanged(
        lattice, lattice->join(DimValueRang::getMaxRange(lattice->getPoint())));
  }

  /// Visit an operation. Invoke the transfer function on each operation that
  /// implements `InferIntRangeInterface`.
  void visitOperation(Operation *op,
                      ArrayRef<const DimValueRangLattice *> operands,
                      ArrayRef<DimValueRangLattice *> results) override;

  /// Visit block arguments or operation results of an operation with region
  /// control-flow for which values are not defined by region control-flow.
  /// This function calls `InferIntRangeInterface` to provide values for block
  /// arguments or tries to reduce the range on loop induction variables with
  /// known bounds.
  void visitNonControlFlowArguments(Operation *op,
                                    const RegionSuccessor &successor,
                                    ArrayRef<DimValueRangLattice *> argLattices,
                                    unsigned firstIndex) override;
};

} // namespace ppl
} // end namespace mlir
