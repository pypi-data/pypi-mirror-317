from __future__ import annotations

from ..runtime.jit import jit
from . import core
import ppl.language as pl

@jit
def exp_no_overflow(input, m_n, m_c, m_h, m_w, t_n, t_c, t_h, t_w):
    """
    无数据溢出的 exp 指数计算

        .. code-block:: python

            output = exp_no_overflow(input, m_n, m_c, m_h, m_w, t_n, t_c, t_h, t_w)

    参数:
        - ``input`` (`ppl.language.tensor`): input 张量

        - ``m_n`` (`int`): 张量memory shape的N

        - ``m_c`` (`int`): 张量memory shape的C

        - ``m_h`` (`int`): 张量memory shape的H

        - ``m_w`` (`int`): 张量memory shape的W

        - ``t_n`` (`int`): 张量实际shape的N

        - ``t_c`` (`int`): 张量实际shape的C

        - ``t_h`` (`int`): 张量实际shape的H

        - ``t_w`` (`int`): 张量实际shape的W
    返回值:
        - ``output`` (`ppl.language.tensor`): output张量

    注意事项:
        实际shape在所有维度上必须小于或等于memory shape
    """
    min_C = 0
    if pl.get_scalar_dtype(input.dtype).is_fp32():
        min_C = -3.40282e35
    elif input.dtype.is_fp16():
        min_C = -45403.0
    else:
        min_C = -3.40282e35
    maxc_tensor = pl.make_tensor([m_n, m_c, m_h, m_w], input.dtype, [t_n, t_c, t_h, t_w])
    pl.max(maxc_tensor, input, min_C)
    minc_tensor1 = pl.make_tensor([m_n, m_c, m_h, m_w], input.dtype, [t_n, t_c, t_h, t_w])
    if input.dtype.is_fp16():
        min(minc_tensor1, maxc_tensor, 45403.0)
    else:
        pl.tiu.move(minc_tensor1, maxc_tensor)
    fp_mulc_tensor = pl.make_tensor([m_n, m_c, m_h, m_w], input.dtype, [t_n, t_c, t_h, t_w])
    pl.fmul(fp_mulc_tensor, minc_tensor1, 1.4426950)
    fp_floor_tensor = pl.make_tensor([m_n, m_c, m_h, m_w], input.dtype, [t_n, t_c, t_h, t_w])
    pl.floor(fp_floor_tensor, fp_mulc_tensor)
    fp_mulc_tensor2 = pl.make_tensor([m_n, m_c, m_h, m_w], input.dtype, [t_n, t_c, t_h, t_w])
    pl.fmul(fp_mulc_tensor2, fp_floor_tensor, 0.69314718)
    fp_sub = pl.make_tensor([m_n, m_c, m_h, m_w], input.dtype, [t_n, t_c, t_h, t_w])
    pl.fsub(fp_sub, maxc_tensor, fp_mulc_tensor2)

    if pl.get_scalar_dtype(input.dtype).is_fp32():
        cast_out = pl.make_tensor([m_n, m_c, m_h, m_w], pl.int16, [t_n, t_c, t_h, t_w])
        pl.cast(cast_out, fp_floor_tensor, pl.int16, pl.RM_HALF_AWAY_FROM_ZERO)
        minc_tensor = pl.make_tensor([m_n, m_c, m_h, m_w], pl.int16, [t_n, t_c, t_h, t_w])
        min(minc_tensor, cast_out, pl.cast(127, pl.int16))
        maxc_tensor2 = pl.make_tensor([m_n, m_c, m_h, m_w], pl.int16, [t_n, t_c, t_h, t_w])
        pl.max(maxc_tensor2, minc_tensor, pl.cast(-127, pl.int16))
        add_intc_tensor = pl.make_tensor([m_n, m_c, m_h, m_w], pl.int32, [t_n, t_c, t_h, t_w])
        pl.add(add_intc_tensor, maxc_tensor2, pl.cast(127, pl.int16), 23, pl.RM_HALF_AWAY_FROM_ZERO, True)
        exp_out = pl.make_tensor([m_n, m_c, m_h, m_w], pl.float32, [t_n, t_c, t_h, t_w])
        pl.fexp(exp_out, fp_sub)
        out = exp_out * add_intc_tensor
    elif input.dtype.is_fp16():
        cast_out = pl.make_tensor([m_n, m_c, m_h, m_w], pl.int8, [t_n, t_c, t_h, t_w])
        pl.cast(cast_out, fp_floor_tensor, pl.int8, pl.RM_HALF_AWAY_FROM_ZERO)

        minc_tensor = pl.make_tensor([m_n, m_c, m_h, m_w], pl.int8, [t_n, t_c, t_h, t_w])
        #pl.min() or min() is both ok
        pl.min(minc_tensor, cast_out, pl.cast(15, pl.int16))
        maxc_tensor2 = pl.make_tensor([m_n, m_c, m_h, m_w], pl.int8, [t_n, t_c, t_h, t_w])
        pl.max(maxc_tensor2, minc_tensor, pl.cast(-15, pl.int16))
        add_intc_tensor = pl.make_tensor([m_n, m_c, m_h, m_w], pl.int16, [t_n, t_c, t_h, t_w])
        pl.add(add_intc_tensor, maxc_tensor2, pl.cast(15, pl.int16), 10,
             pl.RM_HALF_AWAY_FROM_ZERO, True)

        exp_out = pl.make_tensor([m_n, m_c, m_h, m_w], pl.float16, [t_n, t_c, t_h, t_w])
        pl.fexp(exp_out, fp_sub)
        out = exp_out * add_intc_tensor
    elif input.dtype.is_bf16():
        cast_out = pl.make_tensor([m_n, m_c, m_h, m_w], pl.int16, [t_n, t_c, t_h, t_w])
        pl.cast(cast_out, fp_floor_tensor, pl.int16, pl.RM_HALF_AWAY_FROM_ZERO)

        minc_tensor = pl.make_tensor([m_n, m_c, m_h, m_w], pl.int16, [t_n, t_c, t_h, t_w])
        pl.min(minc_tensor, cast_out, pl.cast(127, pl.int16))
        maxc_tensor2 = pl.make_tensor([m_n, m_c, m_h, m_w], pl.int16, [t_n, t_c, t_h, t_w])
        pl.max(maxc_tensor2, minc_tensor, pl.cast(-127, pl.int16))
        add_intc_tensor = pl.make_tensor([m_n, m_c, m_h, m_w], pl.int16, [t_n, t_c, t_h, t_w])
        pl.add(add_intc_tensor, maxc_tensor2, pl.cast(127, pl.int16), 7,
             pl.RM_HALF_AWAY_FROM_ZERO, True)

        exp_out = pl.make_tensor([m_n, m_c, m_h, m_w], pl.bfloat16, [t_n, t_c, t_h, t_w])
        pl.fexp(exp_out, fp_sub)
        out = exp_out * add_intc_tensor
    return out

@jit
def pooling2(qk_sub_tensor,
             tmp_tensor,
             real_q_h,
             real_m,
             real_k,
             mode):
    """
    高性能池化计算

        .. code-block:: python

            output = pooling2(qk_sub_tensor, tmp_tensor, real_q_h, real_m, real_k, mode)

    参数:
        - ``qk_sub_tensor`` (`ppl.language.tensor`): input张量

        - ``tmp_tensor`` (`ppl.language.tensor`): 中间缓存张量

        - ``real_q_h`` (`int`): input张量实际shape的N

        - ``real_m`` (`int`): input张量实际shape的C

        - ``real_k`` (`int`): input张量实际shape的W

        - ``mode`` (`int`): 池化类型, 0: max 1:avg

    返回值:
        - ``output`` (`ppl.language.tensor`): output张量

    注意事项:
        无
    """
    eu_num = pl.get_eu_num(qk_sub_tensor.dtype)
    align_w = pl.cdiv(real_k, eu_num) * eu_num
    slice = pl.cast(align_w / eu_num, pl.int32)
    h = 1
    if (align_w > real_k):
        tensor_mv_out = qk_sub_tensor.sub_view([real_q_h, real_m, 1, real_k + eu_num - align_w], [0, 0, 0, align_w - eu_num])
        tensor_mv_in = qk_sub_tensor.sub_view([real_q_h, real_m, 1, eu_num], [0, 0, 0, align_w - eu_num])
        pl.tiu.zero(tmp_tensor.view([real_q_h, real_m, 1, eu_num]))
        pl.tiu.move(tmp_tensor.view([real_q_h, real_m, 1, real_k + eu_num - align_w]), tensor_mv_out)
        pl.tiu.move(tensor_mv_in, tmp_tensor.view([real_q_h, real_m, 1, eu_num]))
    if mode == 0:
        pl.pool_max(tmp_tensor.view([real_q_h * h, real_m, 1, eu_num]), qk_sub_tensor.view([real_q_h * h, real_m, slice, eu_num]),
                    [slice, 1], [0,0,0,0], [1,1],[1,1])
    else:
        pl.pool_avg(tmp_tensor.view([real_q_h * h, real_m, 1, eu_num]), qk_sub_tensor.view([real_q_h * h, real_m, slice, eu_num]),
                    [slice, 1], [0,0,0,0], [1,1],[1,1], 1.0)

    max_out = pl.make_tensor([-1, -1, -1, -1], tmp_tensor.dtype)
    if mode == 0:
        pl.pool_max(max_out.view([real_q_h, real_m, h, 1]), tmp_tensor.view([real_q_h, real_m, h, eu_num]),
                [1, eu_num], [0,0,0,0], [1,1],[1,1])
    else:
        pl.pool_avg(max_out.view([real_q_h, real_m, h, 1]), tmp_tensor.view([real_q_h, real_m, h, eu_num]),
                [1, eu_num], [0,0,0,0], [1,1],[1,1], 1.0)
    return max_out
