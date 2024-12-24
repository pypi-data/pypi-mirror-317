#ifndef SOPHGO_TPU_UTIL
#define SOPHGO_TPU_UTIL

#include <stdint.h>
#include <stdio.h>

#define asm __asm__
#define CFG_LOCAL_TENSOR(ta_id, n, c, h, w, addr, teew, subtype, layout,       \
                         stride_n, stride_c, stride_h, stride_w)               \
  do {                                                                         \
    uint64_t val = (uint64_t)addr & 0xffffffff;                                \
    val |= ((uint64_t)layout & 0x0f) << 52;                                    \
    val |= ((uint64_t)subtype & 0x01) << 59;                                   \
    val |= ((uint64_t)teew & 0xffffffff) << 60;                                \
    asm volatile("sg.cfgtr ta" #ta_id ", %0\n" : : "r"(val));                  \
    val = (uint64_t)w;                                                         \
    val |= ((uint64_t)h & 0xffff) << 16;                                       \
    val |= ((uint64_t)c & 0xffff) << 32;                                       \
    val |= ((uint64_t)n & 0xffff) << 48;                                       \
    asm volatile("sg.cfgtr.shape ta" #ta_id ", %0\n" : : "r"(val));            \
    if (layout == 3) {                                                         \
      val = (uint64_t)stride_w;                                                \
      val |= (uint64_t)stride_h << 32;                                         \
      asm volatile("sg.cfgtr.hwstride ta" #ta_id ", %0\n" : : "r"(val));       \
      val = (uint64_t)stride_c;                                                \
      val |= (uint64_t)stride_n << 32;                                         \
      asm volatile("sg.cfgtr.ncstride ta" #ta_id ", %0\n" : : "r"(val));       \
    }                                                                          \
  } while (0)

#define CFG_GLOBAL_TENSOR(ga_id, n, c, h, w, addr, teew, subtype, layout,      \
                          stride_n, stride_c, stride_h, stride_w)              \
  do {                                                                         \
    uint64_t val = (uint64_t)addr & 0x1ffffffffffful;                          \
    val |= ((uint64_t)layout & 0x0f) << 52;                                    \
    val |= ((uint64_t)subtype & 0x01) << 59;                                   \
    val |= ((uint64_t)teew & 0xffffffff) << 60;                                \
    asm volatile("sg.cfggr ga" #ga_id ", %0\n" : : "r"(val));                  \
    val = (uint64_t)w;                                                         \
    val |= ((uint64_t)h & 0xffff) << 16;                                       \
    val |= ((uint64_t)c & 0xffff) << 32;                                       \
    val |= ((uint64_t)n & 0xffff) << 48;                                       \
    asm volatile("sg.cfggr.shape ga" #ga_id ", %0\n" : : "r"(val));            \
    if (layout == 3) {                                                         \
      val = (uint64_t)stride_w;                                                \
      val |= (uint64_t)stride_h << 32;                                         \
      asm volatile("sg.cfggr.hwstride ga" #ga_id ", %0\n" : : "r"(val));       \
      val = (uint64_t)stride_c;                                                \
      val |= (uint64_t)stride_n << 32;                                         \
      asm volatile("sg.cfggr.ncstride ga" #ga_id ", %0\n" : : "r"(val));       \
    }                                                                          \
  } while (0)

#define CFG_GLOBAL_TENSOR_CONTINOUS(ga_id, n, c, h, w, addr, teew, subtype)    \
  CFG_GLOBAL_TENSOR(ga_id, n, c, h, w, addr, teew, subtype, 1, 0, 0, 0, 0)

#define CFG_GLOBAL_TENSOR_FREE(ga_id, n, c, h, w, addr, teew, subtype,         \
                               stride_n, stride_c, stride_h, stride_w)         \
  CFG_GLOBAL_TENSOR(ga_id, n, c, h, w, addr, teew, subtype, 3, stride_n,       \
                    stride_c, stride_h, stride_w)

#define CFG_LOCAL_TENSOR_HW_ALIGN(ta_id, n, c, h, w, addr, teew, subtype)      \
  CFG_LOCAL_TENSOR(ta_id, n, c, h, w, addr, teew, subtype, 0, 0, 0, 0, 0)

#define CFG_LOCAL_TENSOR_CONTINOUS(ta_id, n, c, h, w, addr, teew, subtype)     \
  CFG_LOCAL_TENSOR(ta_id, n, c, h, w, addr, teew, subtype, 1, 0, 0, 0, 0)

#define CFG_LOCAL_TENSOR_ROW_ALIGN(ta_id, n, c, h, w, addr, teew, subtype)     \
  CFG_LOCAL_TENSOR(ta_id, n, c, h, w, addr, teew, subtype, 2, 0, 0, 0, 0)

#define CFG_LOCAL_TENSOR_FREE(ta_id, n, c, h, w, addr, teew, subtype,          \
                              stride_n, stride_c, stride_h, stride_w)          \
  CFG_LOCAL_TENSOR(ta_id, n, c, h, w, addr, teew, subtype, 3, stride_n,        \
                   stride_c, stride_h, stride_w)

#define CFG_CONSTANT(ca_id, addr, teew, subtype)                               \
  do {                                                                         \
    uint64_t val = ((uint64_t)teew & 0x0f) << 60;                              \
    val |= ((uint64_t)subtype & 0x01) << 59;                                   \
    uint64_t tmp = 0;                                                          \
    typeof(addr) tmp_addr = addr;                                              \
    switch (teew) {                                                            \
    case 0:                                                                    \
      tmp = (uint64_t)(*(uint8_t *)(&(tmp_addr)));                             \
      break;                                                                   \
    case 1:                                                                    \
      tmp = (uint64_t)(*(uint16_t *)(&(tmp_addr)));                            \
      break;                                                                   \
    case 2:                                                                    \
      tmp = (uint64_t)(*(uint32_t *)(&(tmp_addr)));                            \
      break;                                                                   \
    default:                                                                   \
      assert(0);                                                               \
      break;                                                                   \
    }                                                                          \
    val |= (tmp & 0x00ffffffffffffff);                                         \
    asm volatile("sg.cfgcr ca" #ca_id ", %0\n" : : "r"(val));                  \
  } while (0);

#define CFG_CONST_QUANT(ca_id, multiplier, shift, yzp, teew, subtype)          \
  do {                                                                         \
    uint64_t val = (uint64_t)((uint32_t)multiplier);                           \
    val |= (uint64_t)((uint8_t)shift) << 32;                                   \
    val |= (uint64_t)((uint16_t)yzp) << 40;                                    \
    val |= ((uint64_t)subtype & 0x1) << 59;                                    \
    val |= ((uint64_t)teew & 0xf) << 60;                                       \
    asm volatile("sg.cfgcr ca" #ca_id ", %0\n" : : "r"(val));                  \
  } while (0);

#define CFG_QUANT_CA(ca_id)                                                    \
  do {                                                                         \
    asm volatile("sg.cfg.quant ca" #ca_id "\n");                               \
  } while (0);

#define CFG_QUANT_TA(ta_id)                                                    \
  do {                                                                         \
    asm volatile("sg.cfg.quant ta" #ta_id "\n");                               \
  } while (0);

#define CFG_KZP_CA(ca_id)                                                      \
  do {                                                                         \
    asm volatile("sg.cfg.kzp ca" #ca_id "\n");                                 \
  } while (0);

#define CFG_KZP_TA(ta_id)                                                      \
  do {                                                                         \
    asm volatile("sg.cfg.kzp ta" #ta_id "\n");                                 \
  } while (0);

#define CFG_SATURATE(staturate, sym_saturate)                                  \
  do {                                                                         \
    uint64_t val = (uint64_t)staturate & 0x1;                                  \
    val |= ((uint64_t)sym_saturate & 0x1) << 1;                                \
    asm volatile("sg.cfg.satu %0\n" : : "r"(val));                             \
  } while (0)

#define CFG_ROUND_MODE(round_mode)                                             \
  do {                                                                         \
    uint64_t val = (uint64_t)round_mode & 0xf;                                 \
    asm volatile("sg.cfg.round_mode  %0\n" : : "r"(val));                      \
  } while (0)

#define CFG_DMA_IDX(const_val, start_pos)                                      \
  do {                                                                         \
    uint64_t val = (uint64_t)const_val & 0xffffffff;                           \
    val |= ((uint64_t)start_pos & 0xffff) << 32;                               \
    asm volatile("sg.cfg.dmaidx %0" : : "r"(val));                             \
  } while (0)

#define CFG_PADDING(pad_val, up_pad, dn_pad, lf_pad, rt_pad, pad_mode)         \
  do {                                                                         \
    uint64_t val = (uint64_t)pad_val & 0xffffffff;                             \
    val |= ((uint64_t)up_pad & 0xf) << 32;                                     \
    val |= ((uint64_t)dn_pad & 0xf) << 36;                                     \
    val |= ((uint64_t)lf_pad & 0xf) << 40;                                     \
    val |= ((uint64_t)rt_pad & 0xf) << 44;                                     \
    val |= ((uint64_t)pad_mode & 0xf) << 48;                                   \
    asm volatile("sg.cfg.pad %0\n" : : "r"(val));                              \
  } while (0)

#define CFG_INSERT(insert_val, ins_kh, ins_kw, ins_ih, ins_iw)                 \
  do {                                                                         \
    uint64_t val = (uint64_t)insert_val & 0xffffffff;                          \
    val |= ((uint64_t)ins_iw & 0xf) << 32;                                     \
    val |= ((uint64_t)ins_ih & 0xf) << 36;                                     \
    val |= ((uint64_t)ins_kw & 0xf) << 40;                                     \
    val |= ((uint64_t)ins_kh & 0xf) << 44;                                     \
    asm volatile("sg.cfg.insrt %0\n" : : "r"(val));                            \
  } while (0)

#define CFG_STENCIL(kh, kw, stride_h, stride_w, kr, do_relu)                   \
  do {                                                                         \
    uint64_t val = (uint64_t)kw & 0xffff;                                      \
    val |= ((uint64_t)kh & 0xffff) << 16;                                      \
    val |= ((uint64_t)stride_w & 0xff) << 32;                                  \
    val |= ((uint64_t)stride_h & 0xff) << 40;                                  \
    val |= ((uint64_t)kr & 0x1) << 62;                                         \
    val |= ((uint64_t)do_relu & 0x1) << 63;                                    \
    asm volatile("sg.cfg.stencil %0\n" : : "r"(val));                          \
  } while (0)

#endif /* SOPHGO_TPU_UTIL */
