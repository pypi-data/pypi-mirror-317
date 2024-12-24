#pragma once
#include "ppl/Support/utils.h"
#include <inttypes.h>
#include <memory>

namespace mlir {
namespace ppl {

template <typename T> class Singleton {
public:
  static T *GetInstance() {
    static std::once_flag s_flag;
    std::call_once(s_flag, [&]() { _instance.reset(new T()); });

    return _instance.get();
  }

protected:
  Singleton(){};
  ~Singleton(){};
  static std::unique_ptr<T> _instance;

private:
  Singleton(const Singleton &) = delete;
  Singleton &operator=(const Singleton &) = delete;
};
template <typename T> std::unique_ptr<T> Singleton<T>::_instance;
class Arch {
protected:
  Arch() {}

public:
  int64_t get_npu_num() { return npu_num; }
  int64_t get_core_num() { return core_num; }
  int64_t get_eu_bytes() { return eu_bytes; }
  int64_t get_eu_num(int64_t element_bitwidth) {
    if (element_bitwidth < 8) {
      return eu_bytes * (8 / element_bitwidth);
    }
    return eu_bytes / (element_bitwidth / 8);
  }
  int64_t get_lmem_bytes() { return lmem_bytes; }
  int64_t get_lmem_banks() { return lmem_banks; }
  int64_t get_lmem_bank_bytes() { return lmem_bank_bytes; }
  int64_t get_l2_bytes() { return l2_size; }
  int64_t get_l2_bytes_per_core() { return l2_size / core_num; }
  int64_t get_l2_start_addr() { return l2_start_addr; }

  int64_t get_tensor_size(BeTensorOp op) {
    // todo support group_conv_fc && 4N align mode (bm1684)
    if (dyn_cast_or_null<MemRefType>(op.getShape().getType())) {
      int64_t tensor_size = op.getSize()
                                .getDefiningOp<arith::ConstantOp>()
                                .getValue()
                                .dyn_cast<IntegerAttr>()
                                .getInt();
      return tensor_size;
    } else {
      auto shapeType = dyn_cast_or_null<IntegerType>(op.getShape().getType());
      assert(shapeType);
      auto constantOp =
          dyn_cast_or_null<arith::ConstantIntOp>(op.getShape().getDefiningOp());
      assert(constantOp);
      return align_up(constantOp.value(), 64);
    }
  }

protected:
  int64_t core_num;
  int64_t npu_num;
  int64_t eu_bytes;
  int64_t lmem_bytes;
  int64_t lmem_banks;
  int64_t lmem_bank_bytes;
  int64_t l2_size;
  int64_t l2_start_addr;
};

Arch *archCreator(Chip chip);

} // namespace ppl
} // namespace mlir
