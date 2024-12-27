#ifndef CAST_H_
#define CAST_H_

#include "common.h"
// #include "math.h"
#include "fp16.h"
// #include "base_def.h"
#include "limits.h"
#include <string>

#ifdef __cplusplus
extern "C" {
#endif
static long long get_first_zero(long long src, PREC prec) {
    u32 len;
    long long val;
    if (prec == INT8 ) len = 8;
    if (prec == INT16) len = 16;
    if (prec == INT32) len = 32;
    for (u32 i = 0; i <= len; i++) {
        if (i == len) return len;
        val = src >> (len-1-i);
        val &= 0x1;
        if (val == 0) return i;
    }
    return len;
}
static long long Right_Shift_Round(long long src, int shift_num, int round_mode)
{
  if (shift_num == 0) return src;
  if (shift_num > 63) shift_num = 63;
  long long val, res;
  val = src >> shift_num;
  res = val;
  long long lo_mask = (1ull << shift_num) - 1;
  long long mant = src & lo_mask;
  long long mant_0d5 = 1ull << (shift_num - 1);
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
    if (src < 0) res = val + (mant != 0);
  } else if (round_mode == ROUND_DOWN) {
    res = val;
  } else if (round_mode == ROUND_UP) {
    res = val + (mant != 0);
  } else if (round_mode == ROUND_HALF_UP) {
    if (mant >= mant_0d5) res = val + 1;
  } else if (round_mode == ROUND_HALF_DOWN) {
    if (mant > mant_0d5) res = val + 1;
  }
  return res;
}
static uint8_t fp32_to_fp8(const fp32 single, bool is_e5m2, bool saturate, ROUND_MODE rd_mode) {
  uint8_t res = 0;

  uint32_t FP8_EXP_BIAS = 0;
  uint32_t FP8_EXP_MASK = 0;
  uint32_t FP8_SIGNIFICAND_BITS = 0;
  uint32_t FP8_MAXNORM = 0;
  uint32_t FP8_MANTISSA_MASK = 0;
  if (is_e5m2) {
    FP8_EXP_BIAS = 15;
    FP8_EXP_MASK = 0x1f;
    FP8_SIGNIFICAND_BITS = 3;
    FP8_MAXNORM = 0x7b;
    FP8_MANTISSA_MASK = 0x3;
  } else {
    FP8_EXP_BIAS = 7;
    FP8_EXP_MASK = 0xf;
    FP8_SIGNIFICAND_BITS = 4;
    FP8_MAXNORM = 0x7e;
    FP8_MANTISSA_MASK = 0x7;
  }

  if (single.format.exp > (127 - FP8_EXP_BIAS) && single.format.exp < 0xff) {
   const uint32_t mantissa = single.format.frac;
    const int32_t shift_num = 24 - FP8_SIGNIFICAND_BITS;
    uint32_t tmp = Right_Shift_Round(single.bits, shift_num, rd_mode);
    if (rd_mode == ROUND_DOWN && single.format.sign == 1) {
      tmp += (mantissa != 0);
    } else if (rd_mode == ROUND_UP && single.format.sign == 1) {
      tmp -= (mantissa != 0);
    }
    tmp <<= shift_num;
    const uint32_t exp = ((tmp >> 23) & 0xff) - 127 + FP8_EXP_BIAS;
    const uint32_t frac =
        (tmp >> (24 - FP8_SIGNIFICAND_BITS)) & FP8_MANTISSA_MASK;
    if (exp > FP8_EXP_MASK ||
        (exp == FP8_EXP_MASK && (frac == FP8_MANTISSA_MASK || is_e5m2))) {
      if (saturate) {
        res = FP8_MAXNORM;
      } else {
        // Inf in E5M2, NaN in E4M3
        res = is_e5m2 ? 0x7c : 0x7f;
      }
    } else {
      res = (exp << (FP8_SIGNIFICAND_BITS - 1)) | frac;
    }
  } else if (single.format.exp > 0 &&
             single.format.exp <= (127 - FP8_EXP_BIAS)) {
    int32_t mantissa = (single.format.frac) + (1 << 23);
    const int shift_num = (127 - FP8_EXP_BIAS + 1) - single.format.exp +
                          (24 - FP8_SIGNIFICAND_BITS);
    mantissa = Right_Shift_Round(mantissa, shift_num, rd_mode);
    res = mantissa & 0x7f;
  } else if (single.format.exp == 0xff && single.format.frac != 0) {
    // Canonical NaN
    const uint32_t xbits = 0x7fffffff | (single.format.sign << 31);
    if (is_e5m2) {
      const uint32_t mantissa =
          (xbits >> (24 - FP8_SIGNIFICAND_BITS)) & FP8_MANTISSA_MASK;
      res = 0x7e | mantissa;
    } else {
      res = 0x7f;
    }
  } else if (single.format.exp == 0xff && single.format.frac == 0) {
    if (saturate) {
      res = FP8_MAXNORM;
    } else {
      // no Inf in E4M3 and use NaN, Inf in E5M2
      res = is_e5m2 ? 0x7c : 0x7f;
    }
  }
  res |= (single.format.sign << 7);
  return res;
}

static fp32 fp8_to_fp32(uint8_t src, bool is_e5m2) {
  uint32_t FP8_SIGNIFICAND_BITS = 0;
  uint32_t FP8_MANTISSA_MASK = 0;
  uint32_t FP8_EXP_BIAS = 0;
  uint32_t FP8_MINNORM_EXP = 0;
  uint32_t FP8_EXP_MASK = 0;
  if (is_e5m2) {
    FP8_SIGNIFICAND_BITS = 3u;
    FP8_MANTISSA_MASK = 0x3u;
    FP8_EXP_BIAS = 15u;
    FP8_MINNORM_EXP = 14u;
    FP8_EXP_MASK = 0x1fu;
  } else {
    FP8_SIGNIFICAND_BITS = 4u;
    FP8_MANTISSA_MASK = 0x7u;
    FP8_EXP_BIAS = 7u;
    FP8_MINNORM_EXP = 6u;
    FP8_EXP_MASK = 0xfu;
  }
  uint32_t sign = (src >> 7u) & 0x1u;
  uint32_t exponent = (src >> (FP8_SIGNIFICAND_BITS - 1)) & FP8_EXP_MASK;
  uint32_t mantissa = (src & FP8_MANTISSA_MASK) << (24u - FP8_SIGNIFICAND_BITS);
  if ((exponent == 0x1fu && is_e5m2) || ((src & 0x7fu) == 0x7fu && !is_e5m2)) {
    exponent = 0xffu;
    if (mantissa != 0u) {
      // NaN
      mantissa = 0x7fffffu | (sign << 23);
    }
  } else if (exponent == 0u) {
    /* Denorm or Zero */
    if (mantissa != 0u) {
      uint32_t msb = 0;
      exponent = 127 - FP8_MINNORM_EXP;
      do {
        msb = mantissa & 0x400000u;
        mantissa <<= 1u; // normalize
        exponent--;
      } while (msb == 0u);
      mantissa &= 0x7fffffu;
    }
  } else {
    exponent += (127 - FP8_EXP_BIAS);
  }
  fp32 res = {.bits = 0};
  res.bits = (sign << 31u) | (exponent << 23u) | (mantissa);
  return res;
}
static fp16 fp8_to_fp16(uint8_t single, bool is_e5m2) {
  fp16 res;
  uint16_t ur = (uint16_t)single;
  ur = (uint16_t)(ur << 8U);
  uint16_t sign = ur & 0x8000U;

  if (is_e5m2) {
    if ((ur & 0x7FFFU) > 0x7C00U) {
      /* If NaN, return canonical NaN */
      ur = 0x7FFFU | sign;
    }
  } else {

    uint16_t exponent = (uint16_t)(((ur & 0x7800U) >> 1U) + 0x2000U);
    uint16_t mantissa = (ur & 0x0700U) >> 1U;
    uint8_t absx = 0x7FU & (uint8_t)single;

    if (absx == 0x7FU) // NaN
    {
      ur = 0x7FFFU | sign; // fp16 canonical NaN, discard sign
    } else if (exponent == 0x2000U) {
      // zero or denormal
      if (mantissa != 0U) {
        // normalize
        mantissa = (uint16_t)(mantissa << 1U);
        while ((mantissa & 0x0400U) == 0U) {
          mantissa = (uint16_t)(mantissa << 1U);
          exponent = (uint16_t)(exponent - 0x0400U);
        }
        // discard implicit leading bit
        mantissa &= 0x03FFU;
      } else { // Zero
        exponent = 0U;
      }
      ur = (sign | exponent) | mantissa;
    } else {
      ur = (sign | exponent) | mantissa;
    }
  }
  res.bits = ur;
  return res;
}

/*
 * Functions of fp16
 */

/// Cast fp16 data to fp32 data
static fp32 fp16_to_fp32(fp16 half) {
  fp32 res;
  if (half.format.exp == 31 && half.format.frac != 0) {
    res.bits = UINT32_C(0x7fffffff) | (half.format.sign << 31);
    return res;
  }
  res.bits = fp16_ieee_to_fp32_bits(half.bits);
  return res;
}
static uint8_t fp16_to_fp8(const fp16 x, bool is_e5m2, bool saturate, ROUND_MODE round_mode) {
  uint8_t res = 0U;
  fp32 fx = fp16_to_fp32(x);
  res = fp32_to_fp8(fx, is_e5m2, saturate, round_mode);
  return res;
}

/*
 * Functions of bf16
 */

/// Cast bf16 data to fp32 data
static fp32 bf16_to_fp32(bf16 half) {
  fp32 res;
  res.bits = (uint32_t)(half.bits) << 16;
  return res;
}
static uint8_t bf16_to_fp8(const bf16 x, bool is_e5m2, bool saturate, ROUND_MODE round_mode) {
  uint8_t res = 0U;
  fp32 fx = bf16_to_fp32(x);
  res = fp32_to_fp8(fx, is_e5m2, saturate, round_mode);
  return res;
}
static fp32 fp32_to_fp32(fp32 src, ROUND_MODE round_mode)
{
    fp32 res;
    int exp = src.format.exp - 127;
    long long mati;
    unsigned int sign= src.format.sign;
    long long temp;
    if(sign)
        mati = -(src.format.frac + (1<<23));
    else
        mati = src.format.frac + (1<<23);

    if (exp - 23 >= 0)  // integer
        res.bits = src.bits;
    else if(src.format.exp == 0 && src.format.frac == 0) // 0 -> 0
        res.bits = 0;
    else {  // has frac,need round
        temp = Right_Shift_Round(mati, 23 - exp, round_mode);
        res.fval = temp;
    }
    res.format.sign = src.format.sign; // sign no change
    return res;
}
static fp8e5m2 fp8e5m2_to_fp8e5m2(fp8e5m2 src, ROUND_MODE round_mode)
{
    fp8e5m2 res;
    fp32 temp1;
    int exp = src.exp - 15;
    long long mati;
    unsigned int sign= src.sign;
    long long temp;
    if(sign)
        mati = -(src.frac + (1<<2));
    else
        mati = src.frac + (1<<2);

    if (exp - 2 >= 0)  // integer
        res.bits = src.bits;
    else if(src.exp == 0 && src.frac == 0) // 0 -> 0
        res.bits = 0;
    else {  // has frac,need round
        temp = Right_Shift_Round(mati, 2 - exp, round_mode);
        temp1.fval = (float)temp;
        res.bits = fp32_to_fp8(temp1, true, true, round_mode);
    }
    res.sign = src.sign; // sign no change
    return res;
}
static fp8e4m3 fp8e4m3_to_fp8e4m3(fp8e4m3 src, ROUND_MODE round_mode)
{
    fp8e4m3 res;
    fp32 temp1;
    int exp = src.exp - 7;
    long long mati;
    unsigned int sign= src.sign;
    long long temp;
    if(sign)
        mati = -(src.frac + (1<<3));
    else
        mati = src.frac + (1<<3);

    if (exp - 3 >= 0)  // integer
        res.bits = src.bits;
    else if(src.exp == 0 && src.frac == 0) // 0 -> 0
        res.bits = 0;
    else {  // has frac,need round
        temp = Right_Shift_Round(mati, 3 - exp, round_mode);
        temp1.fval = (float)temp;
        res.bits = fp32_to_fp8(temp1, false, true, round_mode);
    }
    res.sign = src.sign; // sign no change
    return res;
}
static uint8_t fp8_to_fp8(uint8_t src, ROUND_MODE round_mode, bool src_is_e5m2, bool dst_is_e5m2)
{
    uint8_t res;
    if (src_is_e5m2 && dst_is_e5m2){
      fp8e5m2 src_e5m2;
      src_e5m2.bits = src;
      res = fp8e5m2_to_fp8e5m2(src_e5m2, round_mode).bits;
    } else if (!src_is_e5m2 && !dst_is_e5m2){
      fp8e4m3 src_e4m3;
      src_e4m3.bits = src;
      res = fp8e4m3_to_fp8e4m3(src_e4m3, round_mode).bits;
    } else {
      res = fp32_to_fp8(fp8_to_fp32(src, src_is_e5m2), dst_is_e5m2, true, round_mode);
    }
    return res;
}
static fp16 fp32_to_fp16(fp32 src, ROUND_MODE round_mode, bool saturate) {
  #if defined(__bm1684x__) || defined(__bm1686__)
  ASSERT(saturate == false);
  #endif
  fp16 dst = {.bits = 0};
  fp32 fp32val = {.bits = 0};
  long long temp_r, temp_l;
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
    u32 mant = src.bits & 0x1FFF;
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
    fp32val.bits = temp_l&0xFFFFFFFF;
    const uint32_t exp = ((fp32val.bits >> 23) & 0xff) - 127 + 15;
    const uint32_t frac =(fp32val.bits >> (24 - 11)) & 0x3ff;
    if (fp32val.format.exp == 255 && fp32val.format.frac != 0) {
      // NAN which had been checked with IC
      dst.bits = UINT16_C(0x7FFF) | (fp32val.format.sign << 15);
    } else {
      if (exp > 0x1f ||
        (exp == 0x1f && (frac == 0x3ff))) {
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
static fp16 fp16_to_fp16(fp16 src, ROUND_MODE round_mode)
{
    fp16 res;
    fp32 temp1;
    int exp = src.format.exp - 15;
    long long mati;
    unsigned int sign= src.format.sign;
    long long temp;
    if(sign)
        mati = -(src.format.frac + (1<<10));
    else
        mati = src.format.frac + (1<<10);

    if (exp - 10 >= 0)  // integer
        res.bits = src.bits;
    else if(src.format.exp == 0 && src.format.frac == 0)
        res.bits = src.bits;
    else{  // has manti,need round
        temp = Right_Shift_Round(mati, 10 - exp, round_mode);
        temp1.fval = (float)temp;
        res = fp32_to_fp16(temp1, round_mode, false);
    }
    res.format.sign = src.format.sign; // sign no change
    return res;
}
static fp16 bf16_to_fp16(bf16 src, ROUND_MODE round_mode)
{
    fp16 res;
    res = fp32_to_fp16(bf16_to_fp32(src),round_mode, false);
    return res;
}
static bf16 sg_fp32_to_bf16_denormal(fp32 src, ROUND_MODE round_mode) {
  bf16 dst;
  if (((src.format.frac >> 16) & 0x7f) == 0x7f) {
    if ((src.format.frac & 0xffff) == 0x0) { // 0x007f0000
      dst.bits = 0x0;
      dst.format.sign = src.format.sign;
    } else if ((src.format.frac & 0x8000) != 0x8000) { // 0x007f0001-0x007f7fff
      if ((round_mode == ROUND_HALF_TO_EVEN) ||
          (round_mode == ROUND_HALF_AWAY_FROM_ZERO) ||
          (round_mode == ROUND_TOWARDS_ZERO)) {
        dst.bits = 0x0;
      } else if (round_mode == ROUND_DOWN) {
        dst.bits = src.format.sign ? 0x8000 : 0x0;
      } else { // ROUND_UP
        dst.bits = src.format.sign ? 0x0 : 0x8000;
      }
      dst.format.sign = src.format.sign;
    } else { // 0x007f8000 - 0x007fffff
      if ((round_mode == ROUND_HALF_TO_EVEN) ||
          (round_mode == ROUND_HALF_AWAY_FROM_ZERO)) {
        dst.bits = 0x8000;
      } else if (round_mode == ROUND_TOWARDS_ZERO) {
        dst.bits = 0x0;
      } else if (round_mode == ROUND_DOWN) {
        dst.bits = src.format.sign ? 0x8000 : 0x0;
      } else { // ROUND_UP
        dst.bits = src.format.sign ? 0x0 : 0x8000;
      }
      dst.format.sign = src.format.sign;
    }
  } else {
    dst.bits = 0x0;
    dst.format.sign = src.format.sign;
  }
  return dst;
}
static bf16 fp32_to_bf16(fp32 src, ROUND_MODE round_mode) {
  bf16 dst;
  fp32 fp32val;
  long long temp_r, temp_l;
  if (src.format.exp > 0 && src.format.exp < 255) {
    u32 mant = src.bits & 0xFFFF;
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
    fp32val.bits = temp_l&0xFFFFFFFF;
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
  } else if (src.format.exp == 0 && src.format.frac == 0) {
    dst.bits = 0x0000 | (src.format.sign << 15);
  } else {
    // Denorm fp32, use sg_fp32_to_bf16_denormal
    dst = sg_fp32_to_bf16_denormal(src, round_mode);
  }
  return dst;
}
static bf16 fp8_to_bf16(uint8_t single, bool is_e5m2, ROUND_MODE round_mode) {
  bf16 res;
  res = fp32_to_bf16(fp8_to_fp32(single, is_e5m2), round_mode);
  return res;
}
static bf16 fp16_to_bf16(fp16 src, ROUND_MODE round_mode)
{
    bf16 res;
    res = fp32_to_bf16(fp16_to_fp32(src),round_mode);
    return res;
}
static bf16 bf16_to_bf16(bf16 src, ROUND_MODE round_mode)
{
    bf16 res;
    fp32 temp1;
    int exp = src.format.exp - 127;
    long long mati;
    unsigned int sign = src.format.sign;
    long long temp;
    if(sign)
        mati = -(src.format.frac + (1<<7));
    else
        mati = src.format.frac + (1<<7);

    if (exp - 7 >= 0)  // integer
        res.bits = src.bits;
    else if(src.format.exp == 0 && src.format.frac == 0)
        res.bits = 0;
    else{  // has manti,need round
        temp = Right_Shift_Round(mati, 7 - exp, round_mode);
        temp1.fval = (float)temp;
        res = fp32_to_bf16(temp1, ROUND_HALF_TO_EVEN);
    }
    res.format.sign = src.format.sign; // sign no change
    return res;
}

static int fp32_to_int(fp32 src, ROUND_MODE round_mode) {
  if (src.format.exp == 0xff && src.format.frac != 0){
    return 0;
  }
  int dst = 0;
  if ((double)src.fval > (double)2147483647) {
    return 2147483647;
  } else if ((double)src.fval < (double)(-2147483648)) {
    return -2147483648;
  }

  if (round_mode == ROUND_HALF_TO_EVEN) {
    dst = (int)(rint(src.fval));
  } else if (round_mode == ROUND_HALF_AWAY_FROM_ZERO) {
    dst = (int)(round(src.fval));
  } else if (round_mode == ROUND_TOWARDS_ZERO) {
    dst = (int)(src.fval);
  } else if (round_mode == ROUND_DOWN) {
    dst = (int)(floor(src.fval));
  } else if (round_mode == ROUND_UP) { // ROUND_UP
    dst = (int)(ceil(src.fval));
  } else {
    ASSERT_INFO(0, "not supported round mode:%d for fp32 to int\n", round_mode);
  }
  return dst;
}

static u32 fp32_to_u32(fp32 src, ROUND_MODE round_mode) {
  u32 dst = 0;
  if ((double)src.fval > (double)4294967295) {
    return 4294967295;
  } else if (src.fval < 0) {
    return 0;
  }
  if (round_mode == ROUND_HALF_TO_EVEN) {
    dst = (u32)(rint(src.fval));
  } else if (round_mode == ROUND_HALF_AWAY_FROM_ZERO) {
    dst = (u32)(round(src.fval));
  } else if (round_mode == ROUND_TOWARDS_ZERO) {
    dst = (u32)(src.fval);
  } else if (round_mode == ROUND_DOWN) {
    dst = (u32)(floor(src.fval));
  } else if (round_mode == ROUND_UP) { // ROUND_UP
    dst = (u32)(ceil(src.fval));
  } else {
    ASSERT_INFO(0, "not supported round mode:%d for fp32 to u32\n", round_mode);
  }
  return dst;
}
static int fp8_to_int(uint8_t src, bool is_e5m2, ROUND_MODE round_mode) {
  int dst;
  fp32 temp;
  temp = fp8_to_fp32(src, is_e5m2);
  dst = fp32_to_int(temp, round_mode);
  return dst;
}
static int fp16_to_int(fp16 src, ROUND_MODE round_mode) {
  int dst;
  fp32 temp;
  temp = fp16_to_fp32(src);
  dst = fp32_to_int(temp, round_mode);
  return dst;
}

static u32 fp16_to_u32(fp16 src, ROUND_MODE round_mode) {
  u32 dst;
  fp32 temp;
  temp = fp16_to_fp32(src);
  dst = fp32_to_u32(temp, round_mode);
  return dst;
}

static int bf16_to_int(bf16 src, ROUND_MODE round_mode) {
  int dst;
  fp32 temp;
  temp = bf16_to_fp32(src);
  dst = fp32_to_int(temp, round_mode);
  return dst;
}

static u32 bf16_to_u32(bf16 src, ROUND_MODE round_mode) {
  u32 dst;
  fp32 temp;
  temp = bf16_to_fp32(src);
  dst = fp32_to_u32(temp, round_mode);
  return dst;
}

static fp32 int32_to_fp32(long long src, ROUND_MODE round_mode) {
  fp32 dst;
  long long temp, temp_r, temp_l;
  int first_one;
  temp = src > 0 ? src : -src;
  first_one = get_first_zero(~temp, INT32);
  if (first_one > 7) {
    dst.fval = (float)(src);
  } else {
    temp_r = Right_Shift_Round(src, 8 - first_one, round_mode);
    temp_l = temp_r << (8 - first_one);
    dst.fval = (float)(temp_l);
  }
  return dst;
}

// INT/UINT -> FP8
static uint8_t int32_to_fp8(long long src, bool is_e5m2, bool saturate, ROUND_MODE round_mode) {
  fp32 f32val;
  f32val.fval = src;
  uint8_t dst = fp32_to_fp8(f32val, is_e5m2, saturate, round_mode);
  return dst;
}

static fp16 refine_fp16(fp16 src, ROUND_MODE round_mode)
{
  fp16 dst;
  #if defined(__bm1684x__) || defined(__bm1686__)
  if (src.bits == 0x7c00 && (round_mode == ROUND_TOWARDS_ZERO || round_mode == ROUND_DOWN))
  {
    dst.bits = 0x7bff;
    return dst;
  }
  else if (src.bits == 0xfc00 && (round_mode == ROUND_TOWARDS_ZERO || round_mode == ROUND_UP))
  {
    dst.bits = 0xfbff;
    return dst;
  }
  #endif
  dst.bits = src.bits;
  return dst;
}

// INT/UINT -> FP16
static fp16 int32_to_fp16(long long src, ROUND_MODE round_mode, bool saturate) {
  #if defined(__bm1684x__) || defined(__bm1686__)
  ASSERT(saturate == false);
  #endif
  fp16 dst;
  fp32 fp32val;
  long long temp, temp_r, temp_l;
  temp = src > 0 ? src : -src;
  int first_one = get_first_zero(~temp, INT32);
  if (first_one > 20) {
    fp32val.fval = (float)(src);
    dst = fp32_to_fp16(fp32val, round_mode, saturate);
  } else {
    temp_r = Right_Shift_Round(src, 21 - first_one, round_mode);
    temp_l = temp_r << (21 - first_one);
    fp32val.fval = (float)temp_l;
    dst = fp32_to_fp16(fp32val, round_mode, saturate);
  }
  dst = refine_fp16(dst, round_mode);
  return dst;
}

// INT/UINT -> BFP16
static bf16 int32_to_bf16(long long src, ROUND_MODE round_mode) {
  bf16 dst;
  fp32 fp32val;
  long long temp, temp_r, temp_l;
  temp = src > 0 ? src : -src;
  int first_one = get_first_zero(~temp, INT32);
  if (first_one > 23) {
    fp32val.fval = (float)(src);
    dst = fp32_to_bf16(fp32val, ROUND_HALF_TO_EVEN);
  } else {
    temp_r = Right_Shift_Round(src, 24 - first_one, round_mode);
    temp_l = temp_r << (24 - first_one);
    fp32val.fval = (float)temp_l;
    dst = fp32_to_bf16(fp32val, ROUND_HALF_TO_EVEN);
  }
  return dst;
}
// INT16/UINT16 -> FP32
static fp32 int16_to_fp32(long long src) {
  fp32 dst;
  dst.fval = (float)src;
  return dst;
}

// INT16/UINT16 -> FP16
static fp16 int16_to_fp16(long long src, ROUND_MODE round_mode) {
  fp16 dst;
  fp32 fp32val;
  fp32val.fval = (float)src;
  dst = fp32_to_fp16(fp32val, round_mode, false);
  dst = refine_fp16(dst, round_mode);
  return dst;
}

// INT16/UINT16 -> BFP16
static bf16 int16_to_bf16(long long src, ROUND_MODE round_mode) {
  bf16 dst;
  fp32 fp32val;
  fp32val.fval = (float)(src);
  dst = fp32_to_bf16(fp32val, round_mode);
  return dst;
}

// INT16/UINT16 -> FP8
static uint8_t int16_to_fp8(long long src, bool is_e5m2, bool saturate, ROUND_MODE round_mode) {
  uint8_t dst;
  fp32 temp;
  temp.fval = (float)(src);
  dst = fp32_to_fp8(temp, is_e5m2, saturate, round_mode);
  return dst;
}

// INT8/UINT8 -> FP32
static fp32 int8_to_fp32(long long src) {
  fp32 dst;
  dst.fval = (float)(src);
  return dst;
}

// INT8/UINT8 -> FP16
static fp16 int8_to_fp16(long long src) {
  fp16 dst;
  fp32 temp;
  temp.fval = (float)(src);
  dst = fp32_to_fp16(temp, ROUND_HALF_TO_EVEN, false);
  return dst;
}

// INT8/UINT8 -> BFP16
static bf16 int8_to_bf16(long long src) {
  bf16 dst;
  fp32 temp;
  temp.fval = (float)(src);
  dst = fp32_to_bf16(temp, ROUND_HALF_TO_EVEN);
  return dst;
}

// INT8/UINT8 -> FP8
static uint8_t int8_to_fp8(long long src, bool is_e5m2, bool saturate, ROUND_MODE round_mode) {
  uint8_t dst;
  fp32 temp;
  temp.fval = (float)(src);
  dst = fp32_to_fp8(temp, is_e5m2, saturate, round_mode);
  return dst;
}

//conver fp32 to fp16 with fp32 storage
static float F16(float &src, ROUND_MODE round_mode = ROUND_HALF_TO_EVEN) {
  fp16 tmp = fp32_to_fp16(*(fp32 *)&src, round_mode, false);
  fp32 rst = fp16_to_fp32(tmp);
  return *((float *)&rst);
}

//conver fp32 to bf16 with fp32 storage
static float BF16(float &src, ROUND_MODE round_mode = ROUND_HALF_TO_EVEN) {
  auto tmp = fp32_to_bf16(*(fp32 *)&src, round_mode);
  fp32 rst = bf16_to_fp32(tmp);
  return *((float *)&rst);
}

static float saturate_int(long long src, std::string dtype) {
  float max_value = src, min_value = src;
  if (dtype == "DT_INT32") {
    max_value = INT32_MAX;
    min_value = INT32_MIN;
  } else if (dtype == "DT_UINT32") {
    max_value = UINT32_MAX;
    min_value = 0;
  } else if (dtype == "DT_INT16") {
    max_value = INT16_MAX;
    min_value = INT16_MIN;
  } else if (dtype == "DT_UINT16") {
    max_value = UINT16_MAX;
    min_value = 0;
  } else if (dtype == "DT_INT8") {
    max_value = INT8_MAX;
    min_value = INT8_MIN;
  } else if (dtype == "DT_UINT8") {
    max_value = UINT8_MAX;
    min_value = 0;
  }
  return src > max_value ? max_value : src < min_value ? min_value : src;
}

#ifdef __cplusplus
}
#endif

#endif
