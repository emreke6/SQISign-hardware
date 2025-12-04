import random
from arith_ops import *





if __name__ == "__main__":

    random.seed(37)

    in1         = random.randint(0, q)
    in2         = random.randint(0, q)

    print("in1: ", hex(in1))
    print("in2: ", hex(in2))

    fp2_sqr_res = fp2_sqr_new(Fp2(re=in1, im=in2))

    print("RES: x_re ", hex(fp2_sqr_res.re))
    print("RES: x_im ", hex(fp2_sqr_res.im))

    in1         = random.randint(0, q)
    in2         = random.randint(0, q)



    print("in1: ", hex(in1))
    print("in2: ", hex(in2))

    fp2_mul_res = fp2_sqr(Fp2(re=in1, im=in2))

    print("RES: x_re ", hex(fp2_mul_res.re))
    print("RES: x_im ", hex(fp2_mul_res.im))

