#ifndef LLAMA2_UTIL_H
#define LLAMA2_UTIL_H

#include "cast.h"
#include "tpu_defs.h"
#include "util.h"
#include <assert.h>
#include <math.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// typedef uint64_t global_addr_t;
typedef unsigned int local_addr_t;
typedef unsigned int static_addr_t;
#define NPU_NUM 32
#define LOCAL_MEM_SIZE 131072
#define LOCAL_MEM_BANKS 16
#define BANK_SIZE 8192
#define ALIGN_BYTES 16
#define CORE_NUM 4
#define ALIGN_MASK(x, mask) (((x) + (mask)) & ~(mask))
// #define ALIGN(x, a) (((x) + (a) - 1) & ~((a) - 1))
#define DIV_UP(a, b) ((a) == 0 ? 0 : ((a) - 1) / (b) + 1)
#define PIPELINE_MOVE(array, num)                                              \
  do {                                                                         \
    for (int i = (int)num - 1; i > 0; i--) {                                   \
      array[i] = array[i - 1];                                                 \
    }                                                                          \
  } while (0)

#define MAX(x, y) ((x) > (y) ? (x) : (y))
#define MIN(x, y) ((x) < (y) ? (x) : (y))
// tylaor param
#define SFU_TAYLOR_TABLE_SIZE 32
#define SFU_TAYLOR_L_TABLE_SIZE 64
#define ERF_TAYLOR_SIZE 16
#define STATIC_MEM_OFFSET 0
#define SERIAL_NUMBER_SIZE 64
#define SIN_TAYLOR_SIZE 32
#define COS_TAYLOR_SIZE 32
#define ARCSIN_TAYLOR_SIZE 64
#define TAN_TAYLOR_SIZE 32
#define EXP_TAYLOR_OFFSET (STATIC_MEM_OFFSET)
#define LOG_TAYLOR_OFFSET                                                      \
  (EXP_TAYLOR_OFFSET + SFU_TAYLOR_TABLE_SIZE * sizeof(float))
#define ERF_TAYLOR_OFFSET                                                      \
  (LOG_TAYLOR_OFFSET + SFU_TAYLOR_L_TABLE_SIZE * sizeof(float))
#define SERIAL_NUMBER_OFFSET                                                   \
  (ERF_TAYLOR_OFFSET + ERF_TAYLOR_SIZE * sizeof(float))
#define SIN_TAYLOR_OFFSET                                                      \
  (SERIAL_NUMBER_OFFSET + SERIAL_NUMBER_SIZE * sizeof(float))
#define COS_TAYLOR_OFFSET (SIN_TAYLOR_OFFSET + SIN_TAYLOR_SIZE * sizeof(float))
#define ARCSIN_TAYLOR_OFFSET                                                   \
  (COS_TAYLOR_OFFSET + COS_TAYLOR_SIZE * sizeof(float))
#define TAN_TAYLOR_OFFSET                                                      \
  (ARCSIN_TAYLOR_OFFSET + ARCSIN_TAYLOR_SIZE * sizeof(float))
#define EXP_FP16_TAYLOR_OFFSET                                                 \
  (TAN_TAYLOR_OFFSET + TAN_TAYLOR_SIZE * sizeof(float))
#define EXP_BF16_TAYLOR_OFFSET                                                 \
  (EXP_FP16_TAYLOR_OFFSET + ERF_TAYLOR_SIZE * sizeof(short))
#define ERF_FP16_TAYLOR_OFFSET                                                 \
  (EXP_BF16_TAYLOR_OFFSET + ERF_TAYLOR_SIZE * sizeof(short))
#define ERF_BF16_TAYLOR_OFFSET                                                 \
  (ERF_FP16_TAYLOR_OFFSET + ERF_TAYLOR_SIZE * sizeof(short))
#define LOG_FP16_TAYLOR_OFFSET                                                 \
  (ERF_BF16_TAYLOR_OFFSET + ERF_TAYLOR_SIZE * sizeof(short))
#define LOG_BF16_TAYLOR_OFFSET                                                 \
  (LOG_FP16_TAYLOR_OFFSET + ERF_TAYLOR_SIZE * sizeof(short))
#define SIN_FP16_TAYLOR_OFFSET                                                 \
  (LOG_BF16_TAYLOR_OFFSET + ERF_TAYLOR_SIZE * sizeof(float))
#define SIN_BFP16_TAYLOR_OFFSET                                                \
  (SIN_FP16_TAYLOR_OFFSET + ERF_TAYLOR_SIZE * sizeof(float))
#define COS_FP16_TAYLOR_OFFSET                                                 \
  (SIN_BFP16_TAYLOR_OFFSET + ERF_TAYLOR_SIZE * sizeof(float))
#define COS_BFP16_TAYLOR_OFFSET                                                \
  (COS_FP16_TAYLOR_OFFSET + ERF_TAYLOR_SIZE * sizeof(float))
#define SMEM_STATIC_END_OFFSET                                                 \
  (COS_BFP16_TAYLOR_OFFSET + ERF_TAYLOR_SIZE * sizeof(float))

// REG ADDR
#define SYNC_TAG_ADDR (0x50bf504478)

void sync_tpu() {
  uint32_t done_flag = 0xdeadbeef;
  asm volatile("sg.sync.i %0, 0" : : "r"(done_flag));
  while (*(volatile uint32_t *)(SYNC_TAG_ADDR) != done_flag)
    ;
}

__attribute__((section(".srodata"))) static unsigned int EXP_COEFF[] = {
    0x3f800000, 0x3f800000, 0x3f000000, 0x3e2aaaab, 0x3d2aaaab, 0x3c088889,
    0x3ab60b61, 0x39500d01, 0x37d00d01, 0x3638ef1d, 0x3493f27e, 0x32d7322b,
    0x310f76c7, 0x2f309231, 0x2d49cba5, 0x2b573f9f, 0x29573f9f, 0x274a963c,
    0x253413c3, 0x2317a4da, 0x20f2a15d, 0x1eb8dc78, 0x1c8671cb, 0x1a3b0da1,
    0x17f96781, 0x159f9e67, 0x13447430, 0x10e8d58e, 0xe850c51,  0xc12cfcc,
    0x99c9963,  0x721a697};

__attribute__((section(".srodata"))) static unsigned short EXP_FP16_COEFF[] = {
    0x3c00, 0x3c00, 0x3800, 0x3155, 0x2955, 0x2044, 0x15b0, 0xa80,
    0x1a0,  0x2e,   0x5,    0x0,    0x0,    0x0,    0x0,    0x0,
};

__attribute__((section(".srodata"))) static unsigned short EXP_BF16_COEFF[] = {
    0x3f80, 0x3f80, 0x3f00, 0x3e2b, 0x3d2b, 0x3c09, 0x3ab6, 0x3950,
    0x37d0, 0x3639, 0x3494, 0x32d7, 0x310f, 0x2f31, 0x2d4a, 0x2b57,
};

// typedef struct {
//     int n, c, h, w;
// } dim4;

int set_eu_num(int teew) {
  switch (teew) {
  case 2:
    return 4;
  case 1:
    return 8;
  case 0:
    return 16;
  case 5:
    return 32;
  }
  assert(0);
  return -1;
}

int DtypeSize(int dtype) {
  int size = 1;
  if (dtype == DT_INT8 || dtype == DT_UINT8)
    size = 1;
  else if (dtype == DT_INT16 || dtype == DT_UINT16 || dtype == DT_FP16 ||
           dtype == DT_BFP16)
    size = 2;
  else if (dtype == DT_FP32 || dtype == DT_INT32 || dtype == DT_UINT32)
    size = 4;
  return size;
}

int dtype_size(int teew) {
  int size = -1;
  switch (teew) {
  case 0:
    size = 1;
    break;
  case 1:
    size = 2;
    break;
  case 2:
    size = 4;
    break;
  default:
    assert(0);
    break;
  }
  return size;
}

int data_type_bits(int teew) {
  switch (teew) {
  case 0:
    return 8;
  case 1:
    return 16;
  case 2:
    return 32;
  case 3:
    return 64;
  case 4:
    return 128;
  case 5:
    return 4;
  }
  assert(0);
  return -1;
}

data_type_t get_float_type(int teew, int subtype) {
  data_type_t dtype = DT_FP32;
  if (teew == 1) {
    if (subtype == 0) {
      dtype = DT_FP16;
    } else {
      dtype = DT_BFP16;
    }
  } else {
    assert(teew == 2);
  }
  return dtype;
}

void get_aligned_stride(dim4 *stride, int start_idx, const dim4 *shape,
                        int teew) {
  stride->w = 1;
  stride->h = shape->w;
  stride->c = shape->h * stride->h;
  stride->c = ALIGN(stride->c, set_eu_num(teew));
  stride->n = DIV_UP(start_idx + shape->c, NPU_NUM) * stride->c;
}

int get_matrix_size(int row, int col, int teew) {
  dim4 shape = {1, row, 1, col};
  dim4 stride = {0};
  get_aligned_stride(&stride, 0, &shape, teew);
  int size = (stride.n * shape.n * data_type_bits(teew) + 7) >> 3;
  return ALIGN(size, ALIGN_BYTES);
}

int get_tensor_size(int n, int c, int h, int w, int teew) {
  dim4 shape = {n, c, h, w};
  dim4 stride = {0};
  get_aligned_stride(&stride, 0, &shape, teew);
  int size = (stride.n * shape.n * data_type_bits(teew) + 7) >> 3;
  return ALIGN(size, ALIGN_BYTES);
}

void print_data(float *data, int len) {
  printf("data: ");
  for (int i = 0; i < len; i++) {
    printf("%f, ", data[i]);
  }
  printf("end\n");
}

void gen_integer_data(int *data, int len, float min_val, float max_val) {
  printf("input: ");
  for (int i = 0; i < len; i++) {
    data[i] = (int)(((float)rand() / (float)RAND_MAX) * (max_val - min_val)) + min_val;
    printf("%d, ", data[i]);
  }
  printf("end\n");
}

void gen_int_data(void *data, int len, data_type_t dtype, float min_val,
                  float max_val) {
  if (dtype == DT_INT32) {
    gen_integer_data((int *)data, len, min_val, max_val);
  } else {
    int *buffer = (int *)malloc(len * sizeof(int));
    gen_integer_data(buffer, len, min_val, max_val);
    for (int i = 0; i < len; i++) {
      if (dtype == DT_UINT32) {
        ((unsigned int *)data)[i] = (unsigned int)buffer[i];
      } else if (dtype == DT_INT8) {
        ((signed char *)data)[i] = (signed char)buffer[i];
      } else if (dtype == DT_UINT8) {
        ((unsigned char *)data)[i] = (unsigned char)buffer[i];
      } else if (dtype == DT_INT16) {
        ((signed short *)data)[i] = (signed short)buffer[i];
      } else if (dtype == DT_UINT16) {
        ((unsigned short *)data)[i] = (unsigned short)buffer[i];
      } else {
        printf("Unsupported DataType!\n");
        assert(0);
      }
    }
  }
}

void gen_float_data(float *data, int len, float min_val, float max_val,
                    bool is_mask) {
  printf("input: ");
  for (int i = 0; i < len; i++) {
    if (is_mask) {
      data[i] = rand() % 2;
    } else {
      data[i] =
          ((float)rand() / (float)RAND_MAX) * (max_val - min_val) + min_val;
      // data[i] = ((float)rand() / (float)RAND_MAX) * 20 - 10;
    }
  }
  for (int i = 0; i < len; i++) {
    printf("%f, ", data[i]);
  }
  printf("end\n");
}

void gen_fp_data(void *data, int len, data_type_t dtype, float min_val,
                 float max_val, bool is_mask) {
  if (dtype == DT_FP32) {
    gen_float_data((float *)data, len, min_val, max_val, is_mask);
  } else if (dtype == DT_FP16 || dtype == DT_BFP16) {
    float *buffer = (float *)malloc(len * sizeof(float));
    gen_float_data(buffer, len, min_val, max_val, is_mask);
    for (int i = 0; i < len; i++) {
      if (dtype == DT_FP16) {
        ((float16 *)data)[i] =
            fp32_to_fp16(((fp32 *)buffer)[i], ROUND_HALF_TO_EVEN, false);
      } else {
        ((bfloat16 *)data)[i] =
            fp32_to_bf16(((fp32 *)buffer)[i], ROUND_HALF_TO_EVEN, false);
      }
    }
  } else {
    assert(0);
  }
}

void rand_data(void *data, int len, data_type_t dtype, float min_val,
               float max_val, bool is_mask) {
  if (dtype == DT_FP32 || dtype == DT_FP16 || dtype == DT_BFP16) {
    gen_fp_data(data, len, dtype, min_val, max_val, is_mask);
  } else if (dtype == DT_INT8 || dtype == DT_UINT8 || dtype == DT_INT32 ||
             dtype == DT_UINT32 || dtype == DT_INT16 || dtype == DT_UINT16) {
    gen_int_data(data, len, dtype, min_val, max_val);
  }
}

void convert_to_fp32(void *from, float *dst, uint32_t len, int dtype) {
  if (dtype == DT_FP16) {
    for (uint32_t i = 0; i < len; i++) {
      dst[i] = fp16_to_fp32(((float16 *)from)[i]).fval;
    }
  } else if (dtype == DT_BFP16) {
    for (uint32_t i = 0; i < len; ++i) {
      dst[i] = bf16_to_fp32(((bfloat16 *)from)[i]).fval;
    }
  } else {
    for (uint32_t i = 0; i < len; ++i) {
      if (dtype == DT_INT16) {
        dst[i] = (float)((signed short *)from)[i];
      } else if (dtype == DT_UINT16) {
        dst[i] = (float)((unsigned short *)from)[i];
      } else if (dtype == DT_INT8) {
        dst[i] = (float)((signed char *)from)[i];
      } else if (dtype == DT_UINT8) {
        dst[i] = (float)((unsigned char *)from)[i];
      } else if (dtype == DT_INT32) {
        dst[i] = (float)((signed int *)from)[i];
      } else if (dtype == DT_UINT32) {
        dst[i] = (float)((unsigned int *)from)[i];
      } else if (dtype == DT_FP32) {
        dst[i] = ((float *)from)[i];
      } else {
        printf("Unsupported DataType!\n");
        assert(0);
      }
    }
  }
}

void matmul_print(float *mat, int row, int col) {
  for (int i = 0; i < row; i++) {
    for (int j = 0; j < col; j++) {
      printf("%.4f ", mat[i * col + j]);
    }
    printf("\n");
  }
  printf("\n");
}

void batch_matmul_print(float *mat, int batch, int row, int col) {
  for (int i = 0; i < batch; i++) {
    float *data = mat + i * row * col;
    matmul_print(data, row, col);
  }
}

// coeff saved in ta11
void load_exp_coeff(local_addr_t coeff_laddr, int teew, int subtype) {
  // static_addr_t exp_taylor_smem_addr = dtype == DT_FP32 ? EXP_TAYLOR_OFFSET
  //               : (dtype == DT_FP16 ? EXP_FP16_TAYLOR_OFFSET :
  //               EXP_BF16_TAYLOR_OFFSET);
  static_addr_t smem_start_addr = 0x400000;
  static_addr_t exp_taylor_offset = 0;
  static_addr_t exp_taylor_smem_addr = smem_start_addr + exp_taylor_offset;
  if (teew == 2) {
    int coeff_len = 10;
    dim4 coeff_shape = {1, NPU_NUM, 1, coeff_len};
    CFG_LOCAL_TENSOR_HW_ALIGN(11, coeff_shape.n, coeff_shape.c, coeff_shape.h,
                              coeff_shape.w, coeff_laddr, teew, subtype);
    asm volatile("vsetvli %0, %1, e32, m1, tu, mu\n"
                 :
                 : "r"(coeff_len), "r"(coeff_len));
    asm volatile("vle32.v v0, (%0)\n" : : "r"(EXP_COEFF));
  } else if (teew == 1) {
    int coeff_len = 7;
    int fake_len = 32;
    dim4 coeff_shape = {1, NPU_NUM, 1, coeff_len};
    CFG_LOCAL_TENSOR_HW_ALIGN(11, coeff_shape.n, coeff_shape.c, coeff_shape.h,
                              coeff_shape.w, coeff_laddr, teew, subtype);
    asm volatile("vsetvli %0, %1, e16, m1, tu, mu\n"
                 :
                 : "r"(fake_len), "r"(fake_len));
    if (subtype == 0) {
      asm volatile("vle16.v v0, (%0)\n" : : "r"(EXP_FP16_COEFF));
    } else {
      asm volatile("vle16.v v0, (%0)\n" : : "r"(EXP_BF16_COEFF));
    }
  }
  // Todo:before mov, use syn.i instrcution to make sure all bdc and gdma
  // operation finish.
  asm volatile("sg.mov.t.v v0, %0\n" : : "r"(exp_taylor_smem_addr));
  asm volatile("vsetivli zero, 1, e64, m1, tu, mu\n");
  asm volatile("sg.smem.bc ta11, %0\n" : : "r"(exp_taylor_offset));
}

// result saved in ta6
void bdc_fp_exp(local_addr_t dst_addr, local_addr_t src_addr,
                local_addr_t work0_addr, local_addr_t work1_addr,
                local_addr_t coeff_addr, // (1, NPU_NUM, 1, fp32 ? 10 : 7)
                const dim4 *shape, int teew, int subtype) {
  /** fast exp: x = N * ln2 + rem
   * 1. N = (int)(x / ln2)
   * 2. rem = x - N * ln2
   * 3. exp(x) = exp(N * ln2 + rem) = 2^N * exp(rem)
   * 4. use taylor to compute exp(rem)
   * 5. 2.f ^ N = (float)((2 + 127) << 23)
   */
  // printf("Enter bdc_exp_fp\n");
  data_type_t dtype = get_float_type(teew, subtype);
  local_addr_t buffer0_addr =
      (src_addr == work1_addr) ? work0_addr : work1_addr;
  local_addr_t buffer1_addr =
      (src_addr == dst_addr)
          ? (buffer0_addr == work0_addr ? work1_addr : work0_addr)
          : dst_addr;
  local_addr_t buffer2_addr =
      buffer1_addr == dst_addr
          ? (buffer0_addr == work0_addr ? work1_addr : work0_addr)
          : dst_addr;

  // local_addr_t buffer0_addr = work0_addr;
  // local_addr_t buffer1_addr = work1_addr;

  /// BUFFER0 = MAX(min_C, src)
  /// process -inf
  scalar_t min_C = {.u32 = 0};
  if (teew == 2) {
    min_C.f32 = -3.40282 * 1e35;
  } else if (teew == 1 && subtype == 0) {
    min_C.f32 = -45403;
    min_C.f16.bits =
        tpu_fp_cast(min_C, dtype, DT_FP32, ROUND_HALF_TO_EVEN).f16.bits;
  } else if (teew == 1 && subtype == 1) {
    min_C.bf16.bits = 0xff7f;
  }
  CFG_LOCAL_TENSOR_HW_ALIGN(6, shape->n, shape->c, shape->h, shape->w, dst_addr,
                            teew, subtype);
  CFG_LOCAL_TENSOR_HW_ALIGN(7, shape->n, shape->c, shape->h, shape->w, src_addr,
                            teew, subtype);
  CFG_LOCAL_TENSOR_HW_ALIGN(8, shape->n, shape->c, shape->h, shape->w,
                            buffer0_addr, teew, subtype);
  CFG_LOCAL_TENSOR_HW_ALIGN(9, shape->n, shape->c, shape->h, shape->w,
                            buffer1_addr, teew, subtype);
  CFG_LOCAL_TENSOR_HW_ALIGN(10, shape->n, shape->c, shape->h, shape->w,
                            buffer2_addr, teew, subtype);
  // printf("dst_addr = %d, src_addr = %d, buffer0_addr = %d, buffer1_addr = %d,
  // buffer2_addr = %d\n", dst_addr, src_addr, buffer0_addr, buffer1_addr,
  // buffer2_addr);

  // do max
  CFG_CONSTANT(2, min_C.u32, teew, subtype);
  asm volatile("sg.fmax ta10, ta7, ca2\n");
  // printf("sg.fmax ta10, ta7, ca2\n");

  if (dtype == DT_FP16) {
    scalar_t max_C = {.u32 = 0};
    max_C.f32 = 45403;
    max_C.f16.bits =
        tpu_fp_cast(max_C, dtype, DT_FP32, ROUND_HALF_TO_EVEN).f16.bits;
    CFG_CONSTANT(2, max_C.u32, teew, subtype);
    asm volatile("sg.fmin ta10, ta10, ca2\n");
    // printf("sg.fmin ta10, ta10, ca2\n");
  }
  // BUFFER0 = BUFFER2 / ln2
  scalar_t C = {.f32 = 1.4426950f};
  scalar_t dst_C = tpu_fp_cast(C, dtype, DT_FP32, ROUND_HALF_TO_EVEN);
  CFG_CONSTANT(2, dst_C.u32, teew, subtype);
  asm volatile("sg.fmul ta8, ta10, ca2\n");
  // printf("BUFFER0 = BUFFER2 / ln2\n");

  // BUFFER1 = floor(BUFFER0)
  // cfg round_mode
  CFG_ROUND_MODE(3); // ROUND_DOWN,floor
  asm volatile("sg.cvt.f2f ta9, ta8\n");
  // printf("sg.cvt.f2f ta9, ta8\n");

  /// BUFFER0 = BUFFER1 * ln2
  C.f32 = 0.69314718f;
  dst_C = tpu_fp_cast(C, dtype, DT_FP32, ROUND_HALF_TO_EVEN);
  CFG_CONSTANT(2, dst_C.u32, teew, subtype);
  asm volatile("sg.fmul ta8, ta9, ca2\n");
  // printf("sg.fmul ta8, ta9, ca2\n");

  // BUFFER0 = BUFFER2 - BUFFER0
  asm volatile("sg.fsub ta8, ta10, ta8\n");
  // printf("sg.fsub ta8, ta10, ta8\n");

  // BUFFER2 = int(BUFFER1)
  // for int buffer2 tempoary use
  int temp_teew = dtype == DT_FP16 ? 0 : 1;
  CFG_LOCAL_TENSOR_HW_ALIGN(12, shape->n, shape->c, shape->h, shape->w,
                            buffer2_addr, temp_teew, 1);
  CFG_ROUND_MODE(1); // ROUND_HALF_AWAY_FROM_ZERO
  asm volatile("sg.cvt.f2i ta12, ta9\n");
  // printf("sg.cvt.f2i ta12, ta9\n");

  // BUFFER1 = min(BUFFER2, (2^8 - 1) - 127)
  // and use (2^8 - 1) - 127 - 1 to avoid nan
  C.s16 = dtype == DT_FP16 ? 15 : 127;
  CFG_LOCAL_TENSOR_HW_ALIGN(13, shape->n, shape->c, shape->h, shape->w,
                            buffer1_addr, temp_teew, 1);
  CFG_CONSTANT(2, C.s16, temp_teew, 1);
  asm volatile("sg.min ta13, ta12, ca2\n");
  // printf("sg.min ta13, ta12, ca2\n");

  // BUFFER2 = max(BUFFER1, 0 - 127)
  C.s16 = dtype == DT_FP16 ? -15 : -127;
  CFG_CONSTANT(2, C.s16, temp_teew, 1);
  asm volatile("sg.max ta12, ta13, ca2\n");
  // printf("sg.max ta12, ta13, ca2\n");

  // BUFFER1 = (BUFFER2 + 127) << 23
  // for buffer1 tempoary use
  C.s16 = dtype == DT_FP16 ? 15 : 127;
  CFG_CONSTANT(2, C.s16, teew, 1);
  CFG_LOCAL_TENSOR_HW_ALIGN(14, shape->n, shape->c, shape->h, shape->w,
                            buffer1_addr, teew, 1);
  CFG_ROUND_MODE(1); // ROUND_HALF_AWAY_FROM_ZERO
  CFG_CONSTANT(3, dtype == DT_FP32 ? 23 : (dtype == DT_FP16 ? 10 : 7), 0,
               1);                                  // shift is int8
  asm volatile("sg.add ta14, ta12, ca2, ca3, 1\n"); // saturate = 1
  // printf("sg.add ta14, ta12, ca2, ca3, 1\n");

  // BUFFER2 = taylor(BUFFER0)
  asm volatile("sg.sfu.taylor ta10, ta8, ta11\n");
  // printf("sg.sfu.taylor ta10, ta8, ta11\n");

  // DST = BUFFER1 * BUFFER2
  CFG_LOCAL_TENSOR_HW_ALIGN(14, shape->n, shape->c, shape->h, shape->w,
                            buffer1_addr, teew, 0);
  asm volatile(
      "sg.fmul ta6, ta10, ta14\n"); // here buffer1_addr stores int16/int32
                                    // data, maybe have problem?
  // printf("sg.fmul ta6, ta10, ta14\n");
}

void convert_f16_to_f32(float *dst, _Float16 *src, int size) {
  for (int i = 0; i < size; i++) {
    dst[i] = (float)src[i];
  }
}

int metal_cpu_get_current_hartid();
#endif /* LLAMA2_UTIL_H */
