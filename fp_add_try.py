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
    print("in1: ", hex(in3))
    print("in2: ", hex(in4))

    fp_add_res = fp2_add(Fp2(in1, in2), Fp2(in3, in4))

    print("RES re: ", hex(fp_add_res.re))
    print("RES im: ", hex(fp_add_res.im))

    in1         = random.randint(0, q)
    in2         = random.randint(0, q)

    

    in3         = random.randint(0, q)
    in4         = random.randint(0, q)

    print("in1: ", hex(in1))
    print("in2: ", hex(in2))
    print("in1: ", hex(in3))
    print("in2: ", hex(in4))

    fp_add_res = fp2_add(Fp2(in1, in2), Fp2(in3, in4))

    print("RES re: ", hex(fp_add_res.re))
    print("RES im: ", hex(fp_add_res.im))

    