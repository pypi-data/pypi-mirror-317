#ifndef CAST_H
#define CAST_H

#include "common.h"
#include "fp16.h"
#include "tpu_defs.h"
#include <assert.h>
#include <limits.h>
#include <stdint.h>

#define MAX(x, y) ((x) > (y) ? (x) : (y))
#define MIN(x, y) ((x) < (y) ? (x) : (y))

static int64_t Right_Shift_Round(int64_t src, int shift_num,
                                 ROUND_MODE round_mode) {
  if (shift_num == 0)
    return src;
  if (shift_num > 63)
    shift_num = 63;
  int64_t val, res;
  val = src >> shift_num;
  res = val;
  int64_t lo_mask = (1ull << shift_num) - 1;
  int64_t mant = src & lo_mask;
  int64_t mant_0d5 = 1ull << (shift_num - 1);
  if (round_mode == ROUND_HALF_TO_EVEN) {
    if (mant == mant_0d5) {
      res = val + (val & 1);
    } else if (mant > mant_0d5) {
      res = val + 1;
    }
  } else if (round_mode == ROUND_HALF_AWAY_FROM_ZERO) {
    if (src >= 0 && mant >= mant_0d5) {
      res = val + 1;
    } else if (src < 0 && mant > mant_0d5) {
      res = val + 1;
    }
  } else if (round_mode == ROUND_TOWARDS_ZERO) {
    if (src < 0)
      res = val + (mant != 0);
  } else if (round_mode == ROUND_DOWN) {
    res = val;
  } else if (round_mode == ROUND_UP) {
    res = val + (mant != 0);
  } else if (round_mode == ROUND_HALF_UP) {
    if (mant >= mant_0d5)
      res = val + 1;
  } else if (round_mode == ROUND_HALF_DOWN) {
    if (mant > mant_0d5)
      res = val + 1;
  }
  return res;
}

static float16 fp32_to_fp16(fp32 src, ROUND_MODE round_mode, int saturate) {
  float16 dst = {.bits = 0};
  fp32 fp32val = {.bits = 0};
  int64_t temp_r, temp_l;
  if (src.format.exp == 0xFF && src.format.frac != 0) {
    dst.bits = 0x7FFF | (src.format.sign << 15);
  } else if (src.format.exp == 0xFF && src.format.frac == 0) {
    if (saturate) {
      dst.bits = 0x7bff | (src.format.sign << 15);
    } else {
      dst.bits = 0x7C00 | (src.format.sign << 15);
    }
  } else if (src.format.exp == 0 && src.format.frac == 0) {
    dst.bits = 0x0000 | (src.format.sign << 15);
  } else if (src.format.exp > 112 && src.format.exp < 255) {
    uint32_t mant = src.bits & 0x1FFF;
    if (round_mode == ROUND_DOWN) {
      if (src.format.sign == 0) {
        temp_r = (src.bits >> 13);
      } else {
        temp_r = ((src.bits >> 13) + (mant != 0));
      }
    } else if (round_mode == ROUND_UP) {
      if (src.format.sign == 0) {
        temp_r = ((src.bits >> 13) + (mant != 0));
      } else {
        temp_r = (src.bits >> 13);
      }
    } else {
      temp_r = Right_Shift_Round(src.bits, 13, round_mode);
    }
    temp_l = temp_r << 13;
    fp32val.bits = temp_l & 0xFFFFFFFF;
    const uint32_t exp = ((fp32val.bits >> 23) & 0xff) - 127 + 15;
    const uint32_t frac = fp32val.bits >> (24 - 11);
    if (fp32val.format.exp == 255 && fp32val.format.frac != 0) {
      // NAN which had been checked with IC
      dst.bits = UINT16_C(0x7FFF) | (fp32val.format.sign << 15);
    } else {
      if (exp > 0x1f || (exp == 0x1f && (frac > 0x3ff))) {
        if (saturate) {
          dst.bits = 0x7bff | (fp32val.format.sign << 15);
        } else {
          dst.bits = 0x7C00 | (fp32val.format.sign << 15);
        }
      } else {
        dst.bits = fp16_ieee_from_fp32_value(fp32val.fval);
      }
    }
  } else if (src.format.exp > 0 && src.format.exp <= 112) {
    int mant = (src.bits & 0x7FFFFF) + (1 << 23);
    mant = src.format.sign ? (0 - mant) : mant;
    int rshift_num = (113 - src.format.exp) + 13;
    mant = Right_Shift_Round(mant, rshift_num, round_mode);
    mant = src.format.sign ? (0 - mant) : mant;
    dst.bits = (mant & 0xFFFF);
    dst.format.sign = src.format.sign;
  } else {
    if (fp32val.format.exp == 255 && fp32val.format.frac != 0) {
      // NAN which had been checked with IC
      dst.bits = UINT16_C(0x7FFF) | (fp32val.format.sign << 15);
    } else {
      dst.bits = src.format.sign ? 0x8000 : 0x0000;
    }
  }
  return dst;
}

static bfloat16 fp32_to_bf16(fp32 src, ROUND_MODE round_mode, int saturate) {
  bfloat16 dst;
  fp32 fp32val;
  long long temp_r, temp_l;
  if (src.format.exp > 0 && src.format.exp < 255) {
    uint32_t mant = src.bits & 0xFFFF;
    if (round_mode == ROUND_DOWN) {
      if (src.format.sign == 0) {
        temp_r = (src.bits >> 16);
      } else {
        temp_r = ((src.bits >> 16) + (mant != 0));
      }
    } else if (round_mode == ROUND_UP) {
      if (src.format.sign == 0) {
        temp_r = ((src.bits >> 16) + (mant != 0));
      } else {
        temp_r = (src.bits >> 16);
      }
    } else {
      temp_r = Right_Shift_Round(src.bits, 16, round_mode);
    }
    temp_l = temp_r << 16;
    fp32val.bits = temp_l & 0xFFFFFFFF;
    if (fp32val.format.exp == 255) {
      if (fp32val.format.frac != 0) {
        // NAN which had been checked with IC
        dst.bits = 0x7FFFU | (fp32val.format.sign << 15);
      } else {
        // INF
        dst.bits = (uint16_t)(fp32val.bits >> 16);
      }
    } else if (fp32val.format.exp == 0) {
      // zero
      dst.bits = 0x0;
      dst.format.sign = fp32val.format.sign;
    } else {
      const uint16_t sign_exp = (fp32val.bits & UINT32_C(0xFF800000)) >> 16;
      const uint32_t mantissa = fp32val.bits & UINT32_C(0x7FFFFF);
      // Use CPU FP32 add to do mantissa >> 16 and rounding
      float base = fp32_from_bits(UINT32_C(0x48000000));
      base = fp32_from_bits(UINT32_C(0x40000000) | mantissa) + base;
      // Get new mantissa
      uint16_t bf16_mantissa = fp32_to_bits(base) & UINT32_C(0X1FF);
      bf16_mantissa = bf16_mantissa - UINT16_C(0x80);
      // Get bf16 bits
      dst.bits = sign_exp + bf16_mantissa;
    }
  } else if (src.format.exp == 0xff && src.format.frac != 0) {
    dst.bits = 0x7fff | (src.format.sign << 15);
  } else if (src.format.exp == 0xff && src.format.frac == 0) {
    dst.bits = 0x7f80 | (src.format.sign << 15);
  } else {
    dst.bits = 0x0000 | (src.format.sign << 15);
  }
  if (dst.bits == 0x7f80) {
    dst.bits = saturate ? 0x7f7f : 0x7f80;
  } else if (dst.bits == 0xff80) {
    dst.bits = saturate ? 0xff7f : 0xff80;
  }
  return dst;
}

static fp32 fp16_to_fp32(float16 half) {
  fp32 res;
  if (half.format.exp == 31 && half.format.frac != 0) {
    res.bits = UINT32_C(0x7fffffff) | (half.format.sign << 31);
    return res;
  }
  res.bits = fp16_ieee_to_fp32_bits(half.bits);
  return res;
}

static fp32 bf16_to_fp32(bfloat16 half) {
  fp32 res;
  res.bits = (uint32_t)(half.bits) << 16;
  return res;
}

scalar_t tpu_fp_cast(scalar_t src, data_type_t dst_type, data_type_t src_type,
                     ROUND_MODE round_mode) {
  if (dst_type == DT_FP16) {
    assert(src_type != DT_BFP16);
  }
  if (dst_type == DT_BFP16) {
    assert(src_type != DT_BFP16);
  }
  scalar_t dst = {.u32 = 0};
  if (src_type == DT_FP32) {
    if (dst_type == DT_FP16) {
      fp32 f32 = {.fval = src.f32};
      dst.f16.bits = fp32_to_fp16(f32, round_mode, 0).bits;
    } else if (dst_type == DT_BFP16) {
      fp32 f32 = {.fval = src.f32};
      dst.bf16.bits = fp32_to_bf16(f32, round_mode, 0).bits;
    } else {
      dst = src;
    }
  } else if (src_type == DT_FP16) {
    if (dst_type == DT_FP32) {
      float16 f16 = {.bits = src.f16.bits};
      dst.f32 = fp16_to_fp32(f16).fval;
    } else {
      dst = src;
    }
  } else if (src_type == DT_BFP16) {
    if (dst_type == DT_FP32) {
      bfloat16 bf16 = {.bits = src.bf16.bits};
      dst.f32 = bf16_to_fp32(bf16).fval;
    } else {
      dst = src;
    }
  }
  return dst;
}

scalar_t tpu_int_cast(scalar_t src, data_type_t dst_dtype,
                      data_type_t src_dtype) {
  long long val = 0;
  if (src_dtype == DT_UINT32)
    val = src.u32;
  else if (src_dtype == DT_INT32)
    val = src.s32;
  else if (src_dtype == DT_UINT16)
    val = src.u16;
  else if (src_dtype == DT_INT16)
    val = src.s16;
  else if (src_dtype == DT_UINT8)
    val = src.u8;
  else if (src_dtype == DT_INT8)
    val = src.s8;
  scalar_t dst = {.u32 = 0};
  if (dst_dtype == DT_UINT32)
    dst.u32 = MIN(MAX(val, 0), UINT_MAX);
  else if (dst_dtype == DT_INT32)
    dst.s32 = MIN(MAX(val, INT_MIN), INT_MAX);
  else if (dst_dtype == DT_UINT16)
    dst.u16 = MIN(MAX(val, 0), USHRT_MAX);
  else if (dst_dtype == DT_INT16)
    dst.s16 = MIN(MAX(val, SHRT_MIN), SHRT_MAX);
  else if (dst_dtype == DT_UINT8)
    dst.u8 = MIN(MAX(val, 0), UCHAR_MAX);
  else if (dst_dtype == DT_INT8)
    dst.s8 = MIN(MAX(val, -128), 127);
  return dst;
}
ROUND_MODE convertRoundingMode(rounding_mode_t mode) {
  ROUND_MODE convertedMode = ROUND_HALF_TO_EVEN;

  switch (mode) {
  case RM_HALF_TO_EVEN:
    convertedMode = ROUND_HALF_TO_EVEN;
    break;
  case RM_HALF_AWAY_FROM_ZERO:
    convertedMode = ROUND_HALF_AWAY_FROM_ZERO;
    break;
  case RM_TOWARDS_ZERO:
    convertedMode = ROUND_TOWARDS_ZERO;
    break;
  case RM_DOWN:
    convertedMode = ROUND_DOWN;
    break;
  case RM_UP:
    convertedMode = ROUND_UP;
    break;
  case RM_HALF_UP:
    convertedMode = ROUND_HALF_UP;
    break;
  case RM_HALF_DOWN:
    convertedMode = ROUND_HALF_DOWN;
    break;
  default:
    break;
  }

  return convertedMode;
}

bool tpu_is_data_type_int4(data_type_t dtype) {
  return dtype == DT_INT4 || dtype == DT_UINT4;
}

bool tpu_is_data_type_int8(data_type_t dtype) {
  return dtype == DT_INT8 || dtype == DT_UINT8;
}

bool tpu_is_data_type_int16(data_type_t dtype) {
  return dtype == DT_INT16 || dtype == DT_UINT16;
}

bool tpu_is_data_type_int32(data_type_t dtype) {
  return dtype == DT_INT32 || dtype == DT_UINT32;
}

bool tpu_is_data_type_int(data_type_t dtype) {
  return tpu_is_data_type_int4(dtype) || tpu_is_data_type_int8(dtype) ||
         tpu_is_data_type_int16(dtype) || tpu_is_data_type_int32(dtype);
}

scalar_t tpu_cast(scalar_t src, data_type_t dst_dtype, data_type_t src_dtype,
                  rounding_mode_t mode) {
  bool is_dst_int = tpu_is_data_type_int(dst_dtype);
  bool is_src_int = tpu_is_data_type_int(src_dtype);
  ROUND_MODE convert_mode = convertRoundingMode(mode);
  if (is_dst_int && is_src_int)
    return tpu_int_cast(src, dst_dtype, src_dtype);
  else
    return tpu_fp_cast(src, dst_dtype, src_dtype, convert_mode);
  // else if (is_dst_int && !is_src_int)
  //     return tpu_fp_to_int_cast(src, dst_dtype, src_dtype, convert_mode);
  // else /* if (!is_dst_int && is_src_int) */
  //     return tpu_int_to_fp_cast(src, dst_dtype, src_dtype, convert_mode);
}

#endif /* CAST_H*/
