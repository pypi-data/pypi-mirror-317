#ifndef MACROS_H__
#define MACROS_H__

#define __TRUE__     (1)
#define __FALSE__    (0)
#define WORD_SIZE    (32)
#define DWORD_SIZE   (64)
#define WORD_BITS    (5)
#define WORD_MASK    (0x1f)
#define LANE_SEC     ((NPU_NUM - 1) / WORD_SIZE + 1)

#define INT8_SIZE 1
#define INT16_SIZE 2
#define INT32_SIZE 4
#define FLOAT_SIZE 4
//#define FLOAT_BITWIDTH 32
//#define GET_U64(U32_H, U32_L) (((u64)(U32_H) << 32) | (u64)(U32_L))

#define __ALIGN_MASK(x, mask) (((x) + (mask)) & ~(mask))
#ifndef ALIGN
#define ALIGN(x, a) __ALIGN_MASK(x, (__typeof__(x))(a)-1)
#endif

#define sg_min(x, y) (((x)) < ((y)) ? (x) : (y))
#define sg_max(x, y) (((x)) > ((y)) ? (x) : (y))
#define SWAP_VAL(a, b) \
  a ^= b;              \
  b ^= a;              \
  a ^= b

#define NO_USE 0
#define UNUSED(x) (void)(x)
#define INLINE inline

#define ASSERT_INFO(_cond, fmt, ...)                                             \
  do {                                                                           \
      if (!(_cond)) {                                                            \
        printf("ERROR: ASSERT %s: %s: %d: %s\n", __FILE__, __func__, __LINE__, #_cond); \
        printf("ASSERT info: " fmt "\n", ##__VA_ARGS__);                         \
        assert(0); \
      }                                                                          \
    } while (0)
#endif
