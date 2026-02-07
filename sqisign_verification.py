from arith_ops import *
from typing import Optional
from ec import *
from basis import *
from xisog import *
from theta_isogenies import *
from hash import *

import json

def check_canonical_basis_change_matrix(sig: Signature) -> int:
    # aux = 1 << (SQIsign_response_length + HD_extra_torsion - sig->backtracking)
    shift = SQIsign_response_length + HD_extra_torsion - sig.backtracking
    aux = 1 << shift

    for i in range(2):
        for j in range(2):
            entry = sig.mat_Bchall_can_to_B_chall[i][j]
            if mp_compare_int(aux, entry) <= 0:
                return 0

    return 1





def compute_challenge_verify(
    E_chall: ECCurve,
    sig: Signature,
    Epk: ECCurve,
    hint_pk: int
) -> bool:

    # ec_basis_t bas_EA;
    bas_EA = ECBasis(
        P=ECPoint(Fp2(0, 0), Fp2(0, 0)),
        Q=ECPoint(Fp2(0, 0), Fp2(0, 0)),
        PmQ=ECPoint(Fp2(0, 0), Fp2(0, 0)),
    )

    # ec_isog_even_t phi_chall;
    phi_chall = ECIsogEven(
        curve=ECCurve(
            A=Fp2(0, 0),
            C=Fp2(0, 0),
            A24=None,
            is_A24_computed_and_normalized=False,
        ),
        kernel=ECPoint(Fp2(0, 0), Fp2(0, 0)),
        length=0,
    )

    # copy_curve(&phi_chall.curve, Epk);
    phi_chall.curve = copy_curve(Epk)

    # phi_chall.length = TORSION_EVEN_POWER - sig->backtracking;
    phi_chall.length = TORSION_EVEN_POWER - sig.backtracking

    # Compute the basis from the supplied hint
    ret1, phi_chall.curve, bas_EA = ec_curve_to_basis_2f_from_hint(
        bas_EA,
        phi_chall.curve,
        TORSION_EVEN_POWER,
        hint_pk,
    )
    if not ret1:
        return False

    # recovering the exact challenge
    ret, phi_chall.kernel = ec_ladder3pt(
        sig.chall_coeff,
        bas_EA.P,
        bas_EA.Q,
        bas_EA.PmQ,
        phi_chall.curve
    )
    if not ret:
        return False

    # Double the kernel until it has the correct order
    phi_chall.kernel,  phi_chall.curve = ec_dbl_iter(phi_chall.kernel, sig.backtracking, phi_chall.kernel, phi_chall.curve)

    # Compute the codomain
    E_chall = copy_curve(phi_chall.curve)

    ret_ec_eval, new_E_chall = ec_eval_even(E_chall, phi_chall, None, 0)

    E_chall = new_E_chall

    if ret_ec_eval:
        return False

    return True, E_chall


def ec_eval_even_strategy(
    curve_in: ECCurve,
    points: list[ECPoint],
    len_points: int,
    kernel: ECPoint,
    isog_len: int
) -> int:
    """
    In-place equivalent of the C ec_eval_even_strategy.
    Mutates `curve` and `points`.
    Returns 0 on success, -1 on failure.
    """

    # Normalize A24 in place
    curve_norm = ec_curve_normalize_A24(curve_in)
    curve = ec_curve_init()
    curve.A = curve_norm.A
    curve.C = curve_norm.C
    curve.A24 = curve_norm.A24
    curve.is_A24_computed_and_normalized = curve_norm.is_A24_computed_and_normalized

    # Local copy of A24
    A24 = ec_point_init()
    A24 = copy_ec_point(curve.A24)

    # Compute stack space
    space = 1
    i = 1
    while i < isog_len:
        space += 1
        i *= 2

    # Stack of kernel splits and remaining orders
    splits = [ec_point_init() for i in range(space)]
    todo = [0 for i in range(space)] 

    splits[0] = copy_ec_point(kernel)
    todo[0] = isog_len
    current = 0

    # Chain of 4-isogenies
    for j in range(isog_len // 2):
        assert current >= 0
        assert todo[current] >= 1

        # Find next point of order 4
        ctr = 0
        while todo[current] != 2:
            assert todo[current] >= 3
            current += 1
            assert current < space

            splits[current] = copy_ec_point(splits[current - 1])

            num_dbls = (todo[current - 1] // 4) * 2 + (todo[current - 1] % 2)
            todo[current] = todo[current - 1] - num_dbls

            
            while num_dbls > 0:
                splits[current] = xDBL_A24(splits[current], A24, False)
                num_dbls -= 1

        if j == 0:
            assert fp2_is_one(A24.z)
            if not ec_is_four_torsion(splits[current], curve):
                return -1
            
            T = xDBL_A24(splits[current], A24, False)
            if fp2_is_zero(T.x):
                return -1
        else:
            assert todo[current] == 2

        kps4 = ECKPS4()
        # Evaluate 4-isogeny
        kps4, A24  = xisog_4(A24, splits[current])

        # Update splits in place
        new_splits = xeval_4(splits, current, kps4)
        for i in range(current):
            splits[i] = new_splits[i]

        for i in range(current):
            todo[i] -= 2

        # Update points in place
        # points = xeval_4(points, len_points, kps4)
        new_points = xeval_4(points, len_points, kps4)
        for i in range(len_points):
            points[i] = new_points[i]

        current -= 1

    # Final 2-isogeny if needed
    if isog_len % 2:
        if isog_len == 1 and not ec_is_two_torsion(splits[0], curve):
            return -1

        if fp2_is_zero(splits[0].x):
            return -1

        kps2, A24 = xisog_2(A24, splits[0])
        updated_points = xeval_2(points, len_points, kps2)
        for i in range(len_points):
            points[i] = updated_points[i]

    # Convert A24 back to (A:C) in place
    curve_ac = A24_to_AC(curve, A24)
    curve.A = curve_ac.A
    curve.C = curve_ac.C
    curve.A24 = curve_ac.A24
    curve.is_A24_computed_and_normalized = False

    return 0, curve

def ec_eval_even(
    image: ECCurve,
    phi: ECIsogEven,
    points: list[ECPoint],
    len_points: int
) -> int:
    """
    In-place equivalent of C ec_eval_even.
    """

    curve_copy = copy_curve(phi.curve)
    image.A = curve_copy.A
    image.C = curve_copy.C
    image.A24 = curve_copy.A24
    image.is_A24_computed_and_normalized = curve_copy.is_A24_computed_and_normalized

    ret1, new_curve = ec_eval_even_strategy(
        image,
        points,
        len_points,
        phi.kernel,
        phi.length
    )

    image = new_curve

    return ret1, new_curve

def mp_sub(a: int, b: int):
    return a-b

def mp_mod_2exp(a: int, e: int) -> int:
    return a & ((1 << e) - 1)

def matrix_scalar_application_even_basis(bas: ECBasis,
                                         E: ECCurve,
                                         mat: list,
                                         f: int) -> int:
    # scalar_t scalar0, scalar1
    scalar0 = 0
    scalar1 = 0

    tmp_bas = ECBasis(
        P=ec_point_init(),
        Q=ec_point_init(),
        PmQ=ec_point_init()
    )
    tmp_bas.P = bas.P
    tmp_bas.Q = bas.Q
    tmp_bas.PmQ = bas.PmQ

    # R = [a]P + [b]Q
    bas.P, ret = ec_biscalar_mul(
        mat[0][0],
        mat[1][0],
        f,
        tmp_bas,
        E
    )
    if not ret:
        return 0

    # S = [c]P + [d]Q
    bas.Q, ret2 = ec_biscalar_mul(
        mat[0][1],
        mat[1][1],
        f,
        tmp_bas,
        E
    )
    if not ret2:
        return 0

    # scalar0 = a - c mod 2^f
    scalar0 = mp_sub(mat[0][0], mat[0][1])
    scalar0 = mp_mod_2exp(scalar0, f)

    # scalar1 = b - d mod 2^f
    scalar1 = mp_sub(mat[1][0], mat[1][1])
    scalar1 = mp_mod_2exp(scalar1, f)


    bas.PmQ, ret3 = ec_biscalar_mul(
        scalar0,
        scalar1,
        f,
        tmp_bas,
        E
    )
    if not ret3:
        return 0

    return bas, 1



def challenge_and_aux_basis_verify(B_chall_can: ECBasis, B_aux_can: ECBasis, E_chall: ECCurve, E_aux: ECCurve, sig: Signature, pow_dim2_deg_resp: int):
    


    ret1, E_chall ,B_chall_can = ec_curve_to_basis_2f_from_hint(B_chall_can, E_chall, TORSION_EVEN_POWER, sig.hint_chall)
 
    if not ret1:
        return False
    
    B_chall_can, E_chall = ec_dbl_iter_basis(B_chall_can, 
                                             TORSION_EVEN_POWER - pow_dim2_deg_resp - HD_extra_torsion - sig.two_resp_length,
                                             B_chall_can,
                                             E_chall)

    ret1, E_aux, B_aux_can = ec_curve_to_basis_2f_from_hint(B_aux_can, E_aux, TORSION_EVEN_POWER, sig.hint_aux)

    B_aux_can, E_aux = ec_dbl_iter_basis(B_aux_can, TORSION_EVEN_POWER - pow_dim2_deg_resp - HD_extra_torsion, B_aux_can, E_aux)


    B_chall_can, ret1 = matrix_scalar_application_even_basis(B_chall_can,
                                                E_chall,
                                                sig.mat_Bchall_can_to_B_chall,
                                                pow_dim2_deg_resp + HD_extra_torsion + sig.two_resp_length)
    
    return B_chall_can, B_aux_can , E_aux, E_chall ,True


def compute_commitment_curve_verify(E_com: ECCurve,
                                B_chall_can: ECBasis,
                                B_aux_can: ECBasis,
                                E_chall: ECCurve,
                                E_aux: ECCurve,
                                pow_dim2_deg_resp: int):
    

    EchallxEaux = theta_couple_curve_t(E1=ec_curve_init(), E2=ec_curve_init())
    EchallxEaux.E1 = E_chall
    EchallxEaux.E2 = E_aux

    dim_two_ker = copy_bases_to_kernel(B_chall_can, B_aux_can)

    codomain = theta_couple_curve_t(E1=ec_curve_init(), E2=ec_curve_init())
    codomain.E1 = ec_curve_init()
    codomain.E2 = ec_curve_init()


    if pow_dim2_deg_resp == 0:
        codomain_splits = 1
        codomain.E1 = copy_curve(EchallxEaux.E1)
        codomain.E2 = copy_curve(EchallxEaux.E2)
        # We still need to check that E_chall is supersingular
        # This assumes that HD_extra_torsion == 2
        if not ec_is_basis_four_torsion(B_chall_can, E_chall):
            return 0
    else:
        codomain_splits, EchallxEaux, codomain  = theta_chain_compute_and_eval_verify(
            pow_dim2_deg_resp, EchallxEaux, dim_two_ker, True, 0)
    

    # computing the commitment curve
    # its always the first one because of our (2^n,2^n)-isogeny formulae
    E_com = copy_curve(codomain.E1)

    return codomain_splits, E_com


def mp_is_odd(x: int) -> bool:
    return (x & 1) == 1

def mp_is_even(x: int) -> bool:
    return (x & 1) == 0


# naive implementation
def ec_eval_small_chain(curve: ECCurve,
                        kernel: ECPoint,
                        len: int,
                        points_in: list[ECPoint],
                        len_points: int,
                        special: bool): #  do we allow special isogenies?
    curve_new = ECCurve(A=curve.A, C = curve.C, A24=curve.A24, is_A24_computed_and_normalized=curve.is_A24_computed_and_normalized)
    # curve_new.A = curve.A
    # curve_new.C = curve.C
    # curve_new.A24 = curve.A24
    # curve_new.is_A24_computed_and_normalized = curve.is_A24_computed_and_normalized

    points = [points_in[i] for i in range(len_points)]
    A24 = ec_point_init()
    A24 = AC_to_A24(curve_new)

    kps= ECKPS2()
    small_K = ec_point_init()
    big_K = ec_point_init()
    big_K = copy_ec_point(kernel)

    for i in range(len):
        small_K = copy_ec_point(big_K)
        # small_K = big_K;
        for j in range(len - i - 1):
            small_K = xDBL_A24(small_K, A24, False)

        # Check the order of the point before the first isogeny step
        if i == 0 and not ec_is_two_torsion(small_K, curve_new):
            return -1
        # Perform isogeny step
        if fp2_is_zero(small_K.x):
            if special:
                B24 = ec_point_init()
                kps = xisog_2_singular(kps, B24, A24)
                big_K = xeval_2_singular(big_K, 1, kps)
                points = xeval_2_singular(points, len_points, kps)
                A24 = copy_ec_point(B24)
            else:
                return -1
            
        else:
            kps, A24    = xisog_2(A24, small_K)
            big_K       = xeval_2_one(big_K, 1, kps)
            points      = xeval_2(points, len_points, kps)
        

 
    curve_new = A24_to_AC(curve_new, A24)

    curve_new.is_A24_computed_and_normalized = False
    return 0, curve_new, points




def two_response_isogeny_verify(E_chall: ECCurve,
                                B_chall_can: ECBasis,
                                sig: Signature,
                                pow_dim2_deg_resp: int) -> int:
    """
    Verifies the 2-isogeny response and updates B_chall_can in place.
    Returns 1 on success, 0 on failure.
    """

    ker = ec_point_init()
    points = [ec_point_init() for _ in range(3)]

    # Choose kernel for small 2-isogenies
    if (mp_is_even(sig.mat_Bchall_can_to_B_chall[0][0]) and
        mp_is_even(sig.mat_Bchall_can_to_B_chall[1][0])):
        ker = copy_ec_point(B_chall_can.Q)
    else:
        ker = copy_ec_point(B_chall_can.P)

    # Copy basis points
    points[0] = copy_ec_point(B_chall_can.P)
    points[1] = copy_ec_point(B_chall_can.Q)
    points[2] = copy_ec_point(B_chall_can.PmQ)

    # Multiply kernel by 2^(pow_dim2_deg_resp + HD_extra_torsion)
    ker, E_chall = ec_dbl_iter(
        ker,
        pow_dim2_deg_resp + HD_extra_torsion,
        ker,
        E_chall
    )


    # Evaluate the small 2-isogeny chain
    ret, E_chall, points,  = ec_eval_small_chain(
        E_chall,
        ker,
        sig.two_resp_length,
        points,
        3,
        False
    )
    if ret:
        return 0
    

    # Update canonical challenge basis
    B_chall_can.P   = copy_ec_point(points[0])
    B_chall_can.Q   = copy_ec_point(points[1])
    B_chall_can.PmQ = copy_ec_point(points[2])

    return E_chall, B_chall_can, 1



def mp_compare(a: int, b: int):
    # Multiprecision comparison, a=b? : (1) a>b, (0) a=b, (-1) a<b

    
    if (a > b):
        return 1
    elif a < b:
        return -1

    return 0


def protocols_verify(sig: Signature, pk: PublicKey, m: bytes, l: int, orig_curve: ECCurve) -> bool:

    verify = 0

    if not check_canonical_basis_change_matrix(sig):
        return False

    pow_dim2_deg_resp = SQIsign_response_length - sig.two_resp_length - sig.backtracking

    if pow_dim2_deg_resp < 0 or pow_dim2_deg_resp == 1:
        return False

    if not ec_curve_verify_A(pk.curve.A):
        return False

    E_aux = ec_curve_init_from_A(sig.E_aux_A)

    if E_aux is None:
        return False
    
    assert fp2_is_one(pk.curve.C)
    assert not pk.curve.is_A24_computed_and_normalized

    E_chall = ec_curve_init()
    ret_cmpt, E_chall_new = compute_challenge_verify(E_chall, sig_obj, pk.curve, pk.hint_pk)


    E_chall = E_chall_new

    if not ret_cmpt:
        return False
    

    B_aux_can = ECBasis(
        P=ECPoint(Fp2(0, 0), Fp2(0, 0)),
        Q=ECPoint(Fp2(0, 0), Fp2(0, 0)),
        PmQ=ECPoint(Fp2(0, 0), Fp2(0, 0)),
    )
    B_chall_can =  ECBasis(
        P=ECPoint(Fp2(0, 0), Fp2(0, 0)),
        Q=ECPoint(Fp2(0, 0), Fp2(0, 0)),
        PmQ=ECPoint(Fp2(0, 0), Fp2(0, 0)),
    )

    B_chall_can, B_aux_can , E_aux, E_chall, ret_chal_verify = challenge_and_aux_basis_verify(
            B_chall_can, B_aux_can,
            E_chall, E_aux,
            sig, pow_dim2_deg_resp)
    
    if not ret_chal_verify:
        return False


    if sig.two_resp_length > 0:
        E_chall, B_chall_can, ret1 = two_response_isogeny_verify(E_chall, B_chall_can,
                                                                    sig, pow_dim2_deg_resp)
        
        if not ret1:
            return 0


    E_com = ec_curve_init()
    ret_cmt_vrf, E_com = compute_commitment_curve_verify(
            E_com,
            B_chall_can, B_aux_can,
            E_chall, E_aux,
            pow_dim2_deg_resp)
        
    if not ret_cmt_vrf:    
        return 0

    m_bytes = m.to_bytes(length, "little")
    orig_chall = hash_to_challenge(pk_obj, orig_curve  , m_bytes, l,  FP2_ENCODED_BYTES, SECURITY_BITS, HASH_ITERATIONS, TORSION_EVEN_POWER, SQIsign_response_length, RADIX)
    
    chk_chall = hash_to_challenge(pk_obj, E_com, m_bytes, l, FP2_ENCODED_BYTES, SECURITY_BITS, HASH_ITERATIONS, TORSION_EVEN_POWER, SQIsign_response_length, RADIX)

    verify = mp_compare(orig_chall, chk_chall) == 0
    return verify





# ================= SIGNATURE DUMP (pure int) =================

signatures_arr = [
    {
        "E_aux_A": {
            "real": int(
                "0126c329ad94896723df52ef4770c909e97d2e96d1d65330bce396dd1ad3b42a", 16
            ),
            "imag": int(
                "012218cc64dba19a80e6d69ed2662617f23ce4ae208573144c7c2889b6c4dddf", 16
            ),
        },
        "backtracking": 0,
        "two_resp_length": 1,
        "hint_aux": 2,
        "hint_chall": 2,
        "mat_Bchall_can_to_B_chall": [
            [
                int("144aa8a562b4d80857f61f67cab574d9", 16),
                int("0adb04edce859d7c761872ed5f9bee43", 16),
            ],
            [
                int("3788f60d9a4b62b2b335e83becf6a269", 16),
                int("d87174264048a406c81e7dc2acbc00ad", 16),
            ],
        ],
        "chall_coeff": int(
            "0130ab2283ee51650adb8a014734ff6e", 16
        ),
    },

    # ---- appended new signature ----
    {
        "E_aux_A": {
            "real": int(
                "00b1712d63f8cb727644f42798a22034ec6f3a3435c8e0295440dc5e4802d9da", 16
            ),
            "imag": int(
                "034ae2e83a08c4f9da6b89fe8bfa56cf7b148c3110be8808abdf587fb9d35dca", 16
            ),
        },
        "backtracking": 1,
        "two_resp_length": 2,
        "hint_aux": 2,
        "hint_chall": 4,
        "mat_Bchall_can_to_B_chall": [
            [
                int("000000000000000000000000000000003f5ade334cb550b2e86817d4086a35e9", 16),
                int("000000000000000000000000000000007f07070be1688b4eb8bf7b66f1a5f507", 16),
            ],
            [
                int("00000000000000000000000000000000202e41174fc0c842cee567428b26c9dd", 16),
                int("000000000000000000000000000000002f31544ec8a7c2950d60188d03597b0f", 16),
            ],
        ],
        "chall_coeff": int(
            "00000000000000000000000000000000036b86b4eaac7f4d4a9f164293bf9aa5", 16
        ),
    },
    {
        "E_aux_A": {
            "real": int("00adb30304911c15149d7c760e1a7bb3e3c02a9bbc4d2c27be7068d00c5ede73", 16),
            "imag": int("010b14c0342d0c78bae42754333d88d30f18b9c24074423735c21d4324967dcd", 16),
        },
        "backtracking": 0,
        "two_resp_length": 6,
        "hint_aux": 20,
        "hint_chall": 2,
        "mat_Bchall_can_to_B_chall": [
            [
                int("00000000000000000000000000000000bf1814c67809ba2b81cabd0689373ed9", 16),
                int("0000000000000000000000000000000009580600483073d88683939e987d0363", 16),
            ],
            [
                int("0000000000000000000000000000000080fc0ac49acdbb13250813a017f0f941", 16),
                int("0000000000000000000000000000000035854df42c120d0171e902b62da02b9b", 16),
            ],
        ],
        "chall_coeff": int(
            "00000000000000000000000000000000019ea0570dda7a8ff6f3641f190bf560", 16
        ),
    },
    {
        "E_aux_A": {
            "real": int("042c05bd5d2d13c85b6e1e3b6348c73bd423035b4fc2c7f5af2e5777d6582cea", 16),
            "imag": int("0046d10a91a24bbf73ddc5840bf827c901e0d79596337a0b45bc815db866aea6", 16),
        },
        "backtracking": 0,
        "two_resp_length": 1,
        "hint_aux": 11,
        "hint_chall": 11,
        "mat_Bchall_can_to_B_chall": [
            [
                int("00000000000000000000000000000000335bb2c03879cf565f52cc449d8ca795", 16),
                int("0000000000000000000000000000000015433ed72643aeb07189c6e7b11b3f2c", 16),
            ],
            [
                int("00000000000000000000000000000000e0255f88a505fa3d5b6be5f10e7e51b2", 16),
                int("0000000000000000000000000000000047a3a7d014b9dd8eda2a3315e3576ed2", 16),
            ],
        ],
        "chall_coeff": int(
            "00000000000000000000000000000000036b1d7ee30f2dbe5edfe6388fc11e0d", 16
        ),
    }
]





public_key_arr = [
    {
        "curve": {
            "A": {
                "real": int(
                    "0031888167db37fb47a00b19ef77334fd342a2b2a8461ae2e303d4375d5c0182", 16
                ),
                "imag": int(
                    "00cceff96edae240bd05edefc5f5b6616568a9d3cfd3fa4f46a2b51fc1a9b776", 16
                ),
            },
            "C": {
                "real": int(
                    "0100000000000000000000000000000000000000000000000000000000000033", 16
                ),
                "imag": 0,
            },
            "A24": None,
            "is_A24_computed_and_normalized": False,
        },
        "hint_pk": 11,
    },

    # ---- appended new public key ----
    {
        "curve": {
            "A": {
                "real": int(
                    "01fa9e95c71e00736316a41963027cac18f053201ed8d082941b7d7d0e938310", 16
                ),
                "imag": int(
                    "031dbcd0a459a8bada63d440e9b2b081617210f784e386241c24220bbf8cc7db", 16
                ),
            },
            "C": {
                "real": int(
                    "0100000000000000000000000000000000000000000000000000000000000033", 16
                ),
                "imag": 0,
            },
            "A24": None,  # dump shows zeros → still not computed
            "is_A24_computed_and_normalized": False,
        },
        "hint_pk": 11,
    },
    {
        "curve": {
            "A": {
                "real": int("0124f9d8c8b8f6ecca9e3cbf8903725f3611d4e6ec430c185b6d4f1b3a9a6af3", 16),
                "imag": int("048495763c0dc29a27fc545155f235af68b272fa343176b6d89238a0190f1062", 16),
            },
            "C": {
                "real": int("0100000000000000000000000000000000000000000000000000000000000033", 16),
                "imag": 0,
            },
            "A24": None,   # dump shows zero → not computed
            "is_A24_computed_and_normalized": False,
        },
        "hint_pk": 2,
    },
    {
        "curve": {
            "A": {
                "real": int("01c50aa957bd38421ff9fcb74dd4bc2d4bfe817b96f8d2d1a94be23df0e73768", 16),
                "imag": int("02a864ae8f46c740aae2af668445c005dab40c42440c3955059700a07898b711", 16),
            },
            "C": {
                "real": int("0100000000000000000000000000000000000000000000000000000000000033", 16),
                "imag": 0,
            },
            "A24": None,
            "is_A24_computed_and_normalized": False,
        },
        "hint_pk": 2,
    }
]



Ecom_Eaux_E1_arr = [
    {
        "curve": {
            "A": {
                "real": 0x03ca4f4ad4b46ef205fdac1a3ef0bc9c4dab0800b6946cb01c2fd741a795da9e,
                "imag": 0x034c3ab59e6dfb008f71664ebf4bc965bbdfbd5451a51c803dbf8ce5944c6389,
            },
            "C": {
                "real": 0x010e428a4793f8f7b5b2985c417bccfda153119c82f953e471b3f76c206f8fe1,
                "imag": 0x047a91a2af62a12f1b425e5ffadfa200ea627373ae63afba8e519eb0b9e71c6b,
            },
            "A24": {
                "x": {
                    "real": 0x0100000000000000000000000000000000000000000000000000000000000033,
                    "imag": 0x0,
                },
                "z": {
                    "real": 0x0,
                    "imag": 0x0,
                },
            },
            "is_A24_computed_and_normalized": 0,
        }
    },

    # ---- appended new curve ----
    {
        "curve": {
            "A": {
                "real": 0x02b83f4ab2348ae2546d1fe6a4f01e573a6855c3b6cc55a963eac3d1337a1c90,
                "imag": 0x037dfae429efe4c946cf2ef830346232da6025d7b8f7e41259e078058d70a8ad,
            },
            "C": {
                "real": 0x01b152e9d888a009f4d967467d6696b9562ec50589bf4b7fc4fb3e39e2fa240c,
                "imag": 0x04bfde42e66ac769d80b8489aae691ad75e366ce10a0b513696b3a8c7bfed6d4,
            },
            "A24": {
                "x": {
                    "real": 0x0100000000000000000000000000000000000000000000000000000000000033,
                    "imag": 0x0,
                },
                "z": {
                    "real": 0x0,
                    "imag": 0x0,
                },
            },
            "is_A24_computed_and_normalized": 0,
        }
    },
    {
        "curve": {
            "A": {
                "real": int(
                    "03ec51d2d9a6a6b74e77aa905cb4e622b012a06a22cbbd224a0506f934436559", 16
                ),
                "imag": int(
                    "03bcf99a4b53f70c8d4859bc28990d761d982c046fe46a46530942eec41325ce", 16
                ),
            },
            "C": {
                "real": int(
                    "03920bb4b4cedb6fc0a10001064d9b5b2a47b79fe728d2fbb4e4973a07871f0e", 16
                ),
                "imag": int(
                    "01f5c2d6cf85754307d448fb9ab87c5684512bc0d1ab2a949ce5670efc14a65b", 16
                ),
            },
            "A24": {
                "x": {
                    "real": int(
                        "0100000000000000000000000000000000000000000000000000000000000033", 16
                    ),
                    "imag": 0,
                },
                "z": {
                    "real": 0,
                    "imag": 0,
                },
            },
            "is_A24_computed_and_normalized": False,
        }
    },
    {
        "curve": {
            "A": {
                "real": int("06ce96510b3420ca257467468b6a7650e85f13fef98ed97b0bcbd38ee7ed3e2f", 16),
                "imag": int("0208c3cfdbaa9c765af03980c26d4f67bc72a72b281efbfe5c2ac8b4cd992f83", 16),
            },
            "C": {
                "real": int("01c0fb2abe97c7e6b0ac08249fd11a0282a776fd894f5ca27ea6491fdd49ee40", 16),
                "imag": int("02c5027c3a2f929964b09a280454665b5a911f1610a4ccf215f185560bac0336", 16),
            },
            "A24": {
                "x": {
                    "real": int("030a5a7aae9296097a6c93ac18274d9788b914f4d73a3ba30974f5838b7a4c7d", 16),
                    "imag": int("045e5b735fd2e6eba1ab7c430bf20f59526a22656086659cd8aef5f39adecba4", 16),
                },
                "z": {
                    "real": int("0100000000000000000000000000000000000000000000000000000000000033", 16),
                    "imag": 0,
                },
            },
            "is_A24_computed_and_normalized": True,
        }
    }
]


message_arr = [0xd81c4d8d734fcbfbeade3d3f8a039faa2a2c9957e835ad55b22e75bf57bb556ac8, 
               0x225D5CE2CEAC61930A07503FB59F7C2F936A3E075481DA3CA299A80F8C5DF9223A073E7B90E02EBF98CA2227EBA38C1AB2568209E46DBA961869C6F83983B17DCD49,
               0x2B8C4B0F29363EAEE469A7E33524538AA066AE98980EAA19D1F10593203DA2143B9E9E1973F7FF0E6C6AAA3C0B900E50D003412EFE96DEECE3046D8C46BC7709228789775ABDF56AED6416C90033780CB7A4984815DA1B14660DCF34AA34BF82CEBBCF,
               0x2F7AF5B52A046471EFCD720C9384919BE05A61CDE8E8B01251C5AB885E820FD36ED9FF6FDF45783EC81A86728CBB74B426ADFF96123C08FAC2BC6C58A9C0DD71761292262C65F20DF47751F0831770A6BB7B3760BB7F5EFFFB6E11AC35F353A6F24400B80B287834E92C9CF0D3C949D6DCA31B0B94E0E3312E8BD02174B170C2CA9355FE]

length_arr = [33, 66, 99, 132]


if __name__ == "__main__":
    # test_size = 4
    # for i in range(test_size):
    #     sig_obj = Signature(
    #         E_aux_A=Fp2(re=signatures_arr[i]["E_aux_A"]["real"], im=signatures_arr[i]["E_aux_A"]["imag"]),
    #         mat_Bchall_can_to_B_chall=signatures_arr[i]["mat_Bchall_can_to_B_chall"],
    #         backtracking=signatures_arr[i]["backtracking"],
    #         two_resp_length=signatures_arr[i]["two_resp_length"],
    #         hint_aux=signatures_arr[i]["hint_aux"],
    #         hint_chall=signatures_arr[i]["hint_chall"],
    #         chall_coeff=signatures_arr[i]["chall_coeff"]
            
    #     )

    #     pk_obj = PublicKey(
    #         curve=ECCurve(
    #             A=Fp2(
    #                 public_key_arr[i]["curve"]["A"]["real"],
    #                 public_key_arr[i]["curve"]["A"]["imag"],
    #             ),
    #             C=Fp2(
    #                 public_key_arr[i]["curve"]["C"]["real"],
    #                 public_key_arr[i]["curve"]["C"]["imag"],
    #             ),
    #             A24=None,
    #             is_A24_computed_and_normalized=False,
    #         ),
    #         hint_pk=public_key_arr[i]["hint_pk"],
    #     )

    #     orig_curve_obj = ECCurve(
    #         A=Fp2(
    #             Ecom_Eaux_E1_arr[i]["curve"]["A"]["real"],
    #             Ecom_Eaux_E1_arr[i]["curve"]["A"]["imag"],
    #         ),
    #         C=Fp2(
    #             Ecom_Eaux_E1_arr[i]["curve"]["C"]["real"],
    #             Ecom_Eaux_E1_arr[i]["curve"]["C"]["imag"],
    #         ),
    #         A24=ECPoint(
    #             x = Fp2(Ecom_Eaux_E1_arr[i]["curve"]["A24"]["x"]["real"], 
    #                 Ecom_Eaux_E1_arr[i]["curve"]["A24"]["x"]["imag"]),
    #             z = Fp2(Ecom_Eaux_E1_arr[i]["curve"]["A24"]["z"]["real"], 
    #                 Ecom_Eaux_E1_arr[i]["curve"]["A24"]["z"]["imag"])
    #         ),
    #         is_A24_computed_and_normalized=Ecom_Eaux_E1_arr[i]["curve"]["is_A24_computed_and_normalized"]
    #     )


    #     message = message_arr[i]

    #     length = length_arr[i]

    # ---- load parsed JSON ----
    with open("parsed.json") as f:
        data = json.load(f)

    signatures_arr = data["signatures"]
    public_key_arr = data["public_keys"]
    Ecom_Eaux_E1_arr = data["Ecom_Eaux_E1"]

    # convert messages to your previous format
    message_arr = [int(m["message"], 16) for m in data["messages"]]
    length_arr = [m["length"] for m in data["messages"]]
    # ---- your verification loop ----
    test_size = len(message_arr)

    for i in range(test_size):
        sig_obj = Signature(
            E_aux_A=Fp2(
                re=signatures_arr[i]["E_aux_A"]["real"],
                im=signatures_arr[i]["E_aux_A"]["imag"]
            ),
            mat_Bchall_can_to_B_chall=signatures_arr[i]["mat_Bchall_can_to_B_chall"],
            backtracking=signatures_arr[i]["backtracking"],
            two_resp_length=signatures_arr[i]["two_resp_length"],
            hint_aux=signatures_arr[i]["hint_aux"],
            hint_chall=signatures_arr[i]["hint_chall"],
            chall_coeff=signatures_arr[i]["chall_coeff"]
        )

        pk_obj = PublicKey(
            curve=ECCurve(
                A=Fp2(
                    public_key_arr[i]["curve"]["A"]["real"],
                    public_key_arr[i]["curve"]["A"]["imag"]
                ),
                C=Fp2(
                    public_key_arr[i]["curve"]["C"]["real"],
                    public_key_arr[i]["curve"]["C"]["imag"]
                ),
                A24=None,
                is_A24_computed_and_normalized=False
            ),
            hint_pk=public_key_arr[i]["hint_pk"]
        )

        orig_curve_obj = ECCurve(
            A=Fp2(
                Ecom_Eaux_E1_arr[i]["curve"]["A"]["real"],
                Ecom_Eaux_E1_arr[i]["curve"]["A"]["imag"]
            ),
            C=Fp2(
                Ecom_Eaux_E1_arr[i]["curve"]["C"]["real"],
                Ecom_Eaux_E1_arr[i]["curve"]["C"]["imag"]
            ),
            A24=ECPoint(
                x=Fp2(
                    Ecom_Eaux_E1_arr[i]["curve"]["A24"]["x"]["real"],
                    Ecom_Eaux_E1_arr[i]["curve"]["A24"]["x"]["imag"]
                ),
                z=Fp2(
                    Ecom_Eaux_E1_arr[i]["curve"]["A24"]["z"]["real"],
                    Ecom_Eaux_E1_arr[i]["curve"]["A24"]["z"]["imag"]
                ),
            ),
            is_A24_computed_and_normalized=
                Ecom_Eaux_E1_arr[i]["curve"]["is_A24_computed_and_normalized"]
        )

        message = message_arr[i]
        length = length_arr[i]
                

        result = protocols_verify(sig_obj, pk_obj, message, length, orig_curve_obj)
        
        print("protocols_verify =", i ,result)


    