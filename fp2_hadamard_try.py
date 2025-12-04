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

    fp2_hadamard_res = hadamard_sqisign(ThetaPoint(Fp2(re=in1, im=in2), Fp2(re=in3, im=in4), Fp2(re=in5, im=in6), Fp2(re=in7, im=in8)))

    print("RES: fp2_hadamard_res.x.re ", hex(fp2_hadamard_res.x.re))
    print("RES: fp2_hadamard_res.x.im ", hex(fp2_hadamard_res.x.im))
    print("RES: fp2_hadamard_res.y.re ", hex(fp2_hadamard_res.y.re))
    print("RES: fp2_hadamard_res.y.im ", hex(fp2_hadamard_res.y.im))
    print("RES: fp2_hadamard_res.z.re ", hex(fp2_hadamard_res.z.re))
    print("RES: fp2_hadamard_res.z.im ", hex(fp2_hadamard_res.z.im))
    print("RES: fp2_hadamard_res.t.re ", hex(fp2_hadamard_res.t.re))
    print("RES: fp2_hadamard_res.t.im ", hex(fp2_hadamard_res.t.im))

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

    fp2_hadamard_res = hadamard_sqisign(ThetaPoint(Fp2(re=in1, im=in2), Fp2(re=in3, im=in4), Fp2(re=in5, im=in6), Fp2(re=in7, im=in8)))

    print("RES: fp2_hadamard_res.x.re ", hex(fp2_hadamard_res.x.re))
    print("RES: fp2_hadamard_res.x.im ", hex(fp2_hadamard_res.x.im))
    print("RES: fp2_hadamard_res.y.re ", hex(fp2_hadamard_res.y.re))
    print("RES: fp2_hadamard_res.y.im ", hex(fp2_hadamard_res.y.im))
    print("RES: fp2_hadamard_res.z.re ", hex(fp2_hadamard_res.z.re))
    print("RES: fp2_hadamard_res.z.im ", hex(fp2_hadamard_res.z.im))
    print("RES: fp2_hadamard_res.t.re ", hex(fp2_hadamard_res.t.re))
    print("RES: fp2_hadamard_res.t.im ", hex(fp2_hadamard_res.t.im))

