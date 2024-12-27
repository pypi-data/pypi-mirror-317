#pragma once

#include <list>
#include <set>

#include "mlir/IR/Operation.h"
#include "mlir/Support/LLVM.h"

namespace mlir {
namespace ppl {

struct TensorLive {
  uint32_t out_index; // the index of OP output
  uint32_t start = std::numeric_limits<uint32_t>::max(); // start liverange
  uint32_t end = 0;                                      // end liverange
  uint32_t tensor_size; // size of of output tensor
  TensorLive() {}
  TensorLive(uint32_t _out_index, uint32_t _start, uint32_t _end,
             uint32_t _tensor_size) {
    out_index = _out_index;
    start = _start;
    end = _end;
    tensor_size = _tensor_size;
  }
};

class GmemAllocatorMethod {
public:
  GmemAllocatorMethod(uint32_t aligment);
  virtual ~GmemAllocatorMethod();

  virtual std::string getName();

  virtual int64_t assignGaddr(std::vector<Value> &ops,
                              DenseMap<Value, TensorLive> &liveRange,
                              DenseMap<Value, int64_t> &gaddrMap,
                              bool neuronMemoryReuse, int64_t baseGaddr) = 0;

public:
protected:
  std::string name_;
  uint32_t aligment_;
};

struct OpAddr {
  Value op;
  int64_t start = 0;
  int64_t end = 0;
  uint32_t size = 0;
  uint32_t first_pos = 0;
  uint32_t end_pos = 0;

  OpAddr(Value _op, uint32_t _size, uint32_t _first_pos, uint32_t _end_pos) {
    op = _op;
    size = _size;
    first_pos = _first_pos;
    end_pos = _end_pos;
  }
};

class GmemAllocOpSizeOrder : public GmemAllocatorMethod {
public:
  // typedef std::list<std::shared_ptr<OpAddr>> LineSet;

public:
  GmemAllocOpSizeOrder(uint32_t aligment);

  int64_t assignGaddr(std::vector<Value> &ops,
                      DenseMap<Value, TensorLive> &liveRange,
                      DenseMap<Value, int64_t> &gaddrMap,
                      bool neuronMemoryReuse, int64_t baseGaddr) override;
};

class GmemAllocatorMethodFactory {
public:
  static GmemAllocatorMethod *makeMethod(std::string method_name,
                                         uint32_t aligment) {
    if (method_name == "OpSizeOrderAssign") {
      return static_cast<GmemAllocatorMethod *>(
          new GmemAllocOpSizeOrder(aligment));
    } else {
      assert(0);
      return nullptr;
    }
  }
};

class MemAllocBankConflictAware {
public:
  MemAllocBankConflictAware(int64_t bank_num, int64_t bank_size);

  bool assignAddr(std::vector<Value> &ops,
                  DenseMap<Value, TensorLive> &liveRange,
                  DenseMap<Value, DenseSet<Value>> &conflictMap,
                  DenseMap<Value, int64_t> &addrMap, int64_t &totalSize);

protected:
  void insertAddr(std::shared_ptr<OpAddr> &opAddr);

  int64_t getConflictCount(std::shared_ptr<OpAddr> &opAddr,
                           DenseMap<Value, DenseSet<Value>> &conflictMap);
  std::shared_ptr<OpAddr>
  searchAddr(Value op, DenseMap<Value, TensorLive> &liveRange, int64_t offset, int64_t end_offset);

protected:
  std::list<std::shared_ptr<OpAddr>> allocated_op_list_;
  SmallVector<SmallVector<Value>> bank_ops;
  int64_t total_consumption_;
  int64_t bank_num_;
  int64_t bank_size_;
  int64_t mem_size_;
};
} // namespace ppl
} // namespace mlir
