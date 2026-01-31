from arith_ops import *
from basis import *


def xisog_4(B: ECPoint, P: ECPoint):
    kps = ECKPS4()
    K = kps.K

    B_new = B

    # fp2_sqr(&K[0].x, &P.x);
    K[0].x = fp2_sqr(P.x)


    # fp2_sqr(&K[0].z, &P.z);
    K[0].z = fp2_sqr(P.z)

    # fp2_add(&K[1].x, &K[0].z, &K[0].x);
    K[1].x = fp2_add(K[0].z, K[0].x)

    # fp2_sub(&K[1].z, &K[0].z, &K[0].x);
    K[1].z = fp2_sub(K[0].z, K[0].x)

    # fp2_mul(&B->x, &K[1].x, &K[1].z);
    B_new.x = fp2_mul(K[1].x, K[1].z)

    # fp2_sqr(&B->z, &K[0].z);
    B_new.z = fp2_sqr(K[0].z)

    # ---- Constants for xeval_4 ----

    # fp2_add(&K[2].x, &P.x, &P.z);
    K[2].x = fp2_add(P.x, P.z)

    # fp2_sub(&K[1].x, &P.x, &P.z);
    K[1].x = fp2_sub(P.x, P.z)

    # fp2_add(&K[0].x, &K[0].z, &K[0].z);
    K[0].x = fp2_add(K[0].z, K[0].z)

    # fp2_add(&K[0].x, &K[0].x, &K[0].x);
    K[0].x = fp2_add(K[0].x, K[0].x)

    return kps, B_new



def xeval_4( Q: list[ECPoint], lenQ: int, kps: ECKPS4):

    K = kps.K

    R = [ec_point_init() for i in range(lenQ)]

    for i in range(lenQ):
        t0 = fp2_add(Q[i].x, Q[i].z)
        t1 = fp2_sub(Q[i].x, Q[i].z)

        Rx = fp2_mul(t0, K[1].x)
        Rz = fp2_mul(t1, K[2].x)

        t0 = fp2_mul(t0, t1)
        t0 = fp2_mul(t0, K[0].x)

        t1 = fp2_add(Rx, Rz)
        Rz = fp2_sub(Rx, Rz)

        t1 = fp2_sqr(t1)
        Rz = fp2_sqr(Rz)

        Rx = fp2_add(t0, t1)
        t0 = fp2_sub(t0, Rz)

        Rx = fp2_mul(Rx, t1)
        Rz = fp2_mul(Rz, t0)

        R[i] = ECPoint(x=Rx, z=Rz)
    return R