import random
from arith_ops import *





if __name__ == "__main__":

    random.seed(37)

    in1         = random.randint(0, q)
    in2_pre     = random.randint(0, q)

    in2 = (in2_pre * R) % q

    print("in1: ", hex(in1))
    print("in2: ", hex(in2))

    intmul_res = montgomery_sqisign((in1 * in2), R , q)

    print("RES: ", hex(intmul_res))

    in1         = random.randint(0, q)
    in2_pre     = random.randint(0, q)

    in2 = (in2_pre * R) % q

    print("in1: ", hex(in1))
    print("in2: ", hex(in2))

    intmul_res = montgomery_sqisign((in1 * in2), R , q)

    print("RES: ", hex(intmul_res))



    # modred_in = (in1 * in2)

    # print("modred_in = ", hex(modred_in))

    # modred_out = montgomery_sqisign(modred_in, R, q)

    # print("modred_out = ", hex(modred_out))

    # in1         = random.randint(0, q)
    # in2_pre     = random.randint(0, q)

    # in2 = (in2_pre * R) % q

    # modred_in = (in1 * in2)

    # print("modred_in = ", hex(modred_in))

    # modred_out = montgomery_sqisign(modred_in, R, q)

    # print("modred_out = ", hex(modred_out))





