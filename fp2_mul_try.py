import random
from arith_ops import *





if __name__ == "__main__":

    random.seed(37)

    in1         = random.randint(0, q)
    in2         = random.randint(0, q)
    in3         = random.randint(0, q)
    in4         = random.randint(0, q)


    print("in1: ", hex(in1))
    print("in2: ", hex(in2))
    print("in3: ", hex(in3))
    print("in4: ", hex(in4))

    fp2_mul_res = fp2_mul(Fp2(re=in1, im=in2), Fp2(re=in3, im=in4))

    print("RES: x_re ", hex(fp2_mul_res.re))
    print("RES: x_im ", hex(fp2_mul_res.im))

    in1         = random.randint(0, q)
    in2         = random.randint(0, q)
    in3         = random.randint(0, q)
    in4         = random.randint(0, q)


    print("in1: ", hex(in1))
    print("in2: ", hex(in2))
    print("in3: ", hex(in3))
    print("in4: ", hex(in4))

    fp2_mul_res = fp2_mul(Fp2(re=in1, im=in2), Fp2(re=in3, im=in4))

    print("RES: x_re ", hex(fp2_mul_res.re))
    print("RES: x_im ", hex(fp2_mul_res.im))

