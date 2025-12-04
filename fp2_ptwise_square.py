import random
from arith_ops import *





if __name__ == "__main__":

    random.seed(37)

    in1         = random.randint(0, q)
    in2         = random.randint(0, q)
    in3         = random.randint(0, q)
    in4         = random.randint(0, q)
    in5         = random.randint(0, q)
    in6         = random.randint(0, q)
    in7         = random.randint(0, q)
    in8         = random.randint(0, q)

    print("in1: ", hex(in1))
    print("in2: ", hex(in2))
    print("in3: ", hex(in3))
    print("in4: ", hex(in4))
    print("in5: ", hex(in5))
    print("in6: ", hex(in6))
    print("in7: ", hex(in7))
    print("in8: ", hex(in8))

    input1 = ThetaPoint(Fp2(re=in1, im=in2), Fp2(re=in3, im=in4), Fp2(re=in5, im=in6), Fp2(re=in7, im=in8))

    fp2_ptwise_sqr_res = pointwise_square(input1)

    print("RES1_re: x_re ", hex(fp2_ptwise_sqr_res.x.re))
    print("RES1_im: x_im ", hex(fp2_ptwise_sqr_res.x.im))

    print("RES2_re: x_re ", hex(fp2_ptwise_sqr_res.y.re))
    print("RES2_im: x_im ", hex(fp2_ptwise_sqr_res.y.im))

    print("RES3_re: x_re ", hex(fp2_ptwise_sqr_res.z.re))
    print("RES3_im: x_im ", hex(fp2_ptwise_sqr_res.z.im))

    print("RES4_re: x_re ", hex(fp2_ptwise_sqr_res.t.re))
    print("RES4_im: x_im ", hex(fp2_ptwise_sqr_res.t.im))

    in1         = random.randint(0, q)
    in2         = random.randint(0, q)
    in3         = random.randint(0, q)
    in4         = random.randint(0, q)
    in5         = random.randint(0, q)
    in6         = random.randint(0, q)
    in7         = random.randint(0, q)
    in8         = random.randint(0, q)

    print("in1: ", hex(in1))
    print("in2: ", hex(in2))
    print("in3: ", hex(in3))
    print("in4: ", hex(in4))
    print("in5: ", hex(in5))
    print("in6: ", hex(in6))
    print("in7: ", hex(in7))
    print("in8: ", hex(in8))

    input1 = ThetaPoint(Fp2(re=in1, im=in2), Fp2(re=in3, im=in4), Fp2(re=in5, im=in6), Fp2(re=in7, im=in8))

    fp2_ptwise_sqr_res = pointwise_square(input1)

    print("RES1_re: x_re ", hex(fp2_ptwise_sqr_res.x.re))
    print("RES1_im: x_im ", hex(fp2_ptwise_sqr_res.x.im))

    print("RES2_re: x_re ", hex(fp2_ptwise_sqr_res.y.re))
    print("RES2_im: x_im ", hex(fp2_ptwise_sqr_res.y.im))

    print("RES3_re: x_re ", hex(fp2_ptwise_sqr_res.z.re))
    print("RES3_im: x_im ", hex(fp2_ptwise_sqr_res.z.im))

    print("RES4_re: x_re ", hex(fp2_ptwise_sqr_res.t.re))
    print("RES4_im: x_im ", hex(fp2_ptwise_sqr_res.t.im))

