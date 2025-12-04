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

    print("TT1_in1: ", hex(in1))
    print("TT1_in2: ", hex(in2))
    print("TT1_in3: ", hex(in3))
    print("TT1_in4: ", hex(in4))
    print("TT1_in5: ", hex(in5))
    print("TT1_in6: ", hex(in6))
    print("TT1_in7: ", hex(in7))
    print("TT1_in8: ", hex(in8))

    input1 = ThetaPoint(Fp2(re=in1, im=in2), Fp2(re=in3, im=in4), Fp2(re=in5, im=in6), Fp2(re=in7, im=in8))

    in1         = random.randint(0, q)
    in2         = random.randint(0, q)
    in3         = random.randint(0, q)
    in4         = random.randint(0, q)
    in5         = random.randint(0, q)
    in6         = random.randint(0, q)
    in7         = random.randint(0, q)
    in8         = random.randint(0, q)

    print("TT2_in1: ", hex(in1))
    print("TT2_in2: ", hex(in2))
    print("TT2_in3: ", hex(in3))
    print("TT2_in4: ", hex(in4))
    print("TT2_in5: ", hex(in5))
    print("TT2_in6: ", hex(in6))
    print("TT2_in7: ", hex(in7))
    print("TT2_in8: ", hex(in8))

    input2 = ThetaPoint(Fp2(re=in1, im=in2), Fp2(re=in3, im=in4), Fp2(re=in5, im=in6), Fp2(re=in7, im=in8))

    

    

    theta_isogeny_compute_res = ThetaIsogeny()

    theta_isogeny_compute_res = theta_isogeny_compute(ThetaStructure() , input1, input2, False, True, False )

    print("RES1_re: theta_isogeny_compute_res.precomputation.x.re ", hex(theta_isogeny_compute_res.precomputation.x.re))
    print("RES1_im: theta_isogeny_compute_res.precomputation.x.im ", hex(theta_isogeny_compute_res.precomputation.x.im))

    print("RES2_re: theta_isogeny_compute_res.precomputation.y.re ", hex(theta_isogeny_compute_res.precomputation.y.re))
    print("RES2_im: theta_isogeny_compute_res.precomputation.y.im ", hex(theta_isogeny_compute_res.precomputation.y.im))

    print("RES3_re: theta_isogeny_compute_res.precomputation.z.re ", hex(theta_isogeny_compute_res.precomputation.z.re))
    print("RES3_im: theta_isogeny_compute_res.precomputation.z.im ", hex(theta_isogeny_compute_res.precomputation.z.im))

    print("RES4_re: theta_isogeny_compute_res.precomputation.t.re ", hex(theta_isogeny_compute_res.precomputation.t.re))
    print("RES4_im: theta_isogeny_compute_res.precomputation.t.im ", hex(theta_isogeny_compute_res.precomputation.t.im))


    print("RES1_re: theta_isogeny_compute_res.codomain.null_point.x.re ", hex(theta_isogeny_compute_res.codomain.null_point.x.re))
    print("RES1_im: theta_isogeny_compute_res.codomain.null_point.x.im ", hex(theta_isogeny_compute_res.codomain.null_point.x.im))

    print("RES2_re: theta_isogeny_compute_res.codomain.null_point.y.re ", hex(theta_isogeny_compute_res.codomain.null_point.y.re))
    print("RES2_im: theta_isogeny_compute_res.codomain.null_point.y.im ", hex(theta_isogeny_compute_res.codomain.null_point.y.im))

    print("RES3_re: theta_isogeny_compute_res.codomain.null_point.z.re ", hex(theta_isogeny_compute_res.codomain.null_point.z.re))
    print("RES3_im: theta_isogeny_compute_res.codomain.null_point.z.im ", hex(theta_isogeny_compute_res.codomain.null_point.z.im))

    print("RES4_re: theta_isogeny_compute_res.codomain.null_point.t.re ", hex(theta_isogeny_compute_res.codomain.null_point.t.re))
    print("RES4_im: theta_isogeny_compute_res.codomain.null_point.t.im ", hex(theta_isogeny_compute_res.codomain.null_point.t.im))

    in1         = random.randint(0, q)
    in2         = random.randint(0, q)
    in3         = random.randint(0, q)
    in4         = random.randint(0, q)
    in5         = random.randint(0, q)
    in6         = random.randint(0, q)
    in7         = random.randint(0, q)
    in8         = random.randint(0, q)

    print("TT1_in1: ", hex(in1))
    print("TT1_in2: ", hex(in2))
    print("TT1_in3: ", hex(in3))
    print("TT1_in4: ", hex(in4))
    print("TT1_in5: ", hex(in5))
    print("TT1_in6: ", hex(in6))
    print("TT1_in7: ", hex(in7))
    print("TT1_in8: ", hex(in8))

    input1 = ThetaPoint(Fp2(re=in1, im=in2), Fp2(re=in3, im=in4), Fp2(re=in5, im=in6), Fp2(re=in7, im=in8))

    in1         = random.randint(0, q)
    in2         = random.randint(0, q)
    in3         = random.randint(0, q)
    in4         = random.randint(0, q)
    in5         = random.randint(0, q)
    in6         = random.randint(0, q)
    in7         = random.randint(0, q)
    in8         = random.randint(0, q)

    print("TT2_in1: ", hex(in1))
    print("TT2_in2: ", hex(in2))
    print("TT2_in3: ", hex(in3))
    print("TT2_in4: ", hex(in4))
    print("TT2_in5: ", hex(in5))
    print("TT2_in6: ", hex(in6))
    print("TT2_in7: ", hex(in7))
    print("TT2_in8: ", hex(in8))

    input2 = ThetaPoint(Fp2(re=in1, im=in2), Fp2(re=in3, im=in4), Fp2(re=in5, im=in6), Fp2(re=in7, im=in8))

    

    

    theta_isogeny_compute_res = ThetaIsogeny()

    theta_isogeny_compute_res = theta_isogeny_compute(ThetaStructure() , input1, input2, False, True, False )

    print("RES1_re: theta_isogeny_compute_res.precomputation.x.re ", hex(theta_isogeny_compute_res.precomputation.x.re))
    print("RES1_im: theta_isogeny_compute_res.precomputation.x.im ", hex(theta_isogeny_compute_res.precomputation.x.im))

    print("RES2_re: theta_isogeny_compute_res.precomputation.y.re ", hex(theta_isogeny_compute_res.precomputation.y.re))
    print("RES2_im: theta_isogeny_compute_res.precomputation.y.im ", hex(theta_isogeny_compute_res.precomputation.y.im))

    print("RES3_re: theta_isogeny_compute_res.precomputation.z.re ", hex(theta_isogeny_compute_res.precomputation.z.re))
    print("RES3_im: theta_isogeny_compute_res.precomputation.z.im ", hex(theta_isogeny_compute_res.precomputation.z.im))

    print("RES4_re: theta_isogeny_compute_res.precomputation.t.re ", hex(theta_isogeny_compute_res.precomputation.t.re))
    print("RES4_im: theta_isogeny_compute_res.precomputation.t.im ", hex(theta_isogeny_compute_res.precomputation.t.im))


    print("RES1_re: theta_isogeny_compute_res.codomain.null_point.x.re ", hex(theta_isogeny_compute_res.codomain.null_point.x.re))
    print("RES1_im: theta_isogeny_compute_res.codomain.null_point.x.im ", hex(theta_isogeny_compute_res.codomain.null_point.x.im))

    print("RES2_re: theta_isogeny_compute_res.codomain.null_point.y.re ", hex(theta_isogeny_compute_res.codomain.null_point.y.re))
    print("RES2_im: theta_isogeny_compute_res.codomain.null_point.y.im ", hex(theta_isogeny_compute_res.codomain.null_point.y.im))

    print("RES3_re: theta_isogeny_compute_res.codomain.null_point.z.re ", hex(theta_isogeny_compute_res.codomain.null_point.z.re))
    print("RES3_im: theta_isogeny_compute_res.codomain.null_point.z.im ", hex(theta_isogeny_compute_res.codomain.null_point.z.im))

    print("RES4_re: theta_isogeny_compute_res.codomain.null_point.t.re ", hex(theta_isogeny_compute_res.codomain.null_point.t.re))
    print("RES4_im: theta_isogeny_compute_res.codomain.null_point.t.im ", hex(theta_isogeny_compute_res.codomain.null_point.t.im))