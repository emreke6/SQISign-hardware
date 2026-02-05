from arith_ops import *
from typing import Optional
from ec import *
from basis import *
from xisog import *
from theta_isogenies import *
from hash import *

import hashlib

import math

# try:
#     from . import params, ec, hd, misc
# except ImportError:
#     import params, ec, hd, misc



dict_points = {
    0x030ab9ca4a4063c2a0306045470c83f8c641ce00381f58c99e7e6b6863c58c7f: ECCurve(A=Fp2(re=0x04dec42b8a08f5ae0c8c0736199baa085a90b46c06890ed9f32a0c87ab056b47, im=0x07cd8651f86b9b2f6d6272a4d4a19fd816a318961a5435da5e0c58415c207f5c),
                                                                                C = Fp2(re=0x027c92b40b4dac7dd7b5cd6fd2c254c797662ca16557c5c2f6e1ac944cd08e47, im=0x01f53a059595f24d6eb274ef13d7aa521b8d38339b91fcfc9337b30d4a78c8a3),
                                                                                A24=None,
                                                                                is_A24_computed_and_normalized=False),
    0x0291b3fa1a83817562ffd3cfcd08ff10b84b468e1c252dc29b69f620f8d4c57b: ECPoint(x=Fp2(re=0x02533073e5f4fd46cd21dd4dd86c0ec6bea0de860c9b787aed9e5efb5909f930, im=0x03e5e67c1dff29fff3e1fc69a040fb0cd42d0565cc4a9b9afdccb0cdc4694bcd),
                                                                                z=Fp2(re=0x00394892d1ce7d244ca0ed7c964b7454f17f3d2133dfd77cc65802708b257927, im=0x013ccc75d51215cd8fa266ce9570d5d32fa009fd618ac0fdd57b4cb0ff3a8c16)),
    0x04561d942aeb1e03995a36f7faaf82d5f59f5425047a750da05c8075a4baa443: ECPoint(x=Fp2(re=0x02a4d547678ad54cfa2b60299112dd6512b5b20403fb2999ff5fec3193414901, im=0x043868e3c2c1c41ac2636218caf180307c04bc4d8af2ed90c531cfccbb901fac),
                                                                                z=Fp2(re=0x038811985f31da53bedffaa307ec93af92191a4ac19f4014718e3fc345fba09d, im=0x021d8e3ae3676734c9c8a18f362e698cb27dc2fb873b5f489b0bd9b5b4dc3c10)),
    0x01ea84775eeb2be1f5a5081e65729219cf23a66c2c97a12b10a25994bc1102c5: ECPoint(x=Fp2(re=0x04f0a38b5f596bc8d755a0541bd4456bdc95f347bbe5194d63fdaa3587db01fc, im=0x01d4a42dcf47451835b99b9d238a6aab4c137713d7b14ce011517864d3fa383f),
                                                                                z=Fp2(re=0x00d180fcc7427d2550a26d9273b876710d94ed2eb60dce8483aa23d1073776e6, im=0x0216a44f2ab7bc482badc247cd9f1d0ea35486c4f0ba751eee8ddf5483189217)),
}

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

    splits[0] = copy_point(kernel)
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

            splits[current] = copy_point(splits[current - 1])

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
        # new_points = xeval_4(points, len_points, kps4)
        # for i in range(len_points):
        #     points[i] = new_points[i]

        current -= 1

    # Final 2-isogeny if needed
    if isog_len % 2:
        if isog_len == 1 and not ec_is_two_torsion(splits[0], curve):
            return -1

        if fp2_is_zero(splits[0].x):
            return -1

        kps2 = xisog_2(A24, splits[0])
        updated_points = xeval_2(points, points, len_points, kps2)
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
        print_curve("EchallxEaux.E1 ", EchallxEaux.E1)
        print_curve("EchallxEaux.E2 ", EchallxEaux.E2)
        print_hex_point("dim_two_ker.T1.P1 ", dim_two_ker.T1.P1)
        print_hex_point("dim_two_ker.T1.P2 ", dim_two_ker.T1.P2)
        print_hex_point("dim_two_ker.T2.P1 ", dim_two_ker.T2.P1)
        print_hex_point("dim_two_ker.T2.P2 ", dim_two_ker.T2.P2)
        print_hex_point("dim_two_ker.T1m2.P1 ", dim_two_ker.T1m2.P1)
        print_hex_point("dim_two_ker.T1m2.P2 ", dim_two_ker.T1m2.P2)
        codomain_splits, EchallxEaux, codomain  = theta_chain_compute_and_eval_verify(
            pow_dim2_deg_resp, EchallxEaux, dim_two_ker, True, 0)
    
        print_curve("EchallxEaux.E1 after ", EchallxEaux.E1)
        print_curve("EchallxEaux.E2 after ", EchallxEaux.E2)

        print_curve("codomain.E1 after ", codomain.E1)
        print_curve("codomain.E2 after ", codomain.E2)

    # computing the commitment curve
    # its always the first one because of our (2^n,2^n)-isogeny formulae
    E_com = copy_curve(codomain.E1)

    return codomain_splits, E_com


def mp_is_odd(x: int) -> bool:
    return (x & 1) == 1

def mp_is_even(x: int) -> bool:
    return (x & 1) == 0

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
    # if ec_eval_small_chain(
    #     E_chall,
    #     ker,
    #     sig.two_resp_length,
    #     points,
    #     3,
    #     False
    # ):
    #     return 0

    assert E_chall.A.re in dict_points, "ERROR TWO_RESPONSE_ISOGENY_VERIFY"
    E_chall = dict_points[E_chall.A.re]
    points[0] = dict_points[points[0].x.re]
    points[1] = dict_points[points[1].x.re]
    points[2] = dict_points[points[2].x.re]
    

    # Update canonical challenge basis
    B_chall_can.P   = copy_point(points[0])
    B_chall_can.Q   = copy_point(points[1])
    B_chall_can.PmQ = copy_point(points[2])

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
    print("compute_commitment_curve_verify \n")
    ret_cmt_vrf, E_com = compute_commitment_curve_verify(
            E_com,
            B_chall_can, B_aux_can,
            E_chall, E_aux,
            pow_dim2_deg_resp)
        
    if not ret_cmt_vrf:    
        return 0

    m_bytes = m.to_bytes(length, "little")
    print_curve("E_com", E_com)
    print_curve("orig_curve", orig_curve)
    orig_chall = hash_to_challenge(pk_obj, orig_curve  , m_bytes, l,  FP2_ENCODED_BYTES, SECURITY_BITS, HASH_ITERATIONS, TORSION_EVEN_POWER, SQIsign_response_length, RADIX)
    
    chk_chall = hash_to_challenge(pk_obj, E_com, m_bytes, l, FP2_ENCODED_BYTES, SECURITY_BITS, HASH_ITERATIONS, TORSION_EVEN_POWER, SQIsign_response_length, RADIX)

    print("chk_call_pre: ", hex(chk_chall))
    print("orig_chall: ", hex(orig_chall))

    verify = mp_compare(orig_chall, chk_chall) == 0
    return verify





# ================= SIGNATURE DUMP (pure int) =================

signature = {
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
}

public_key = {
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

        # A24 not computed
        "A24": None,

        "is_A24_computed_and_normalized": False,
    },

    "hint_pk": 11,
}


Ecom_Eaux_E1 = {
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
}


if __name__ == "__main__":
    sig_obj = Signature(
        E_aux_A=Fp2(re=signature["E_aux_A"]["real"], im=signature["E_aux_A"]["imag"]),
        mat_Bchall_can_to_B_chall=signature["mat_Bchall_can_to_B_chall"],
        backtracking=signature["backtracking"],
        two_resp_length=signature["two_resp_length"],
        hint_aux=signature["hint_aux"],
        hint_chall=signature["hint_chall"],
        chall_coeff=signature["chall_coeff"]
        
    )

    pk_obj = PublicKey(
        curve=ECCurve(
            A=Fp2(
                public_key["curve"]["A"]["real"],
                public_key["curve"]["A"]["imag"],
            ),
            C=Fp2(
                public_key["curve"]["C"]["real"],
                public_key["curve"]["C"]["imag"],
            ),
            A24=None,
            is_A24_computed_and_normalized=False,
        ),
        hint_pk=public_key["hint_pk"],
    )

    orig_curve_obj = ECCurve(
        A=Fp2(
            Ecom_Eaux_E1["curve"]["A"]["real"],
            Ecom_Eaux_E1["curve"]["A"]["imag"],
        ),
        C=Fp2(
            Ecom_Eaux_E1["curve"]["C"]["real"],
            Ecom_Eaux_E1["curve"]["C"]["imag"],
        ),
        A24=ECPoint(
            x = Fp2(Ecom_Eaux_E1["curve"]["A24"]["x"]["real"], 
                   Ecom_Eaux_E1["curve"]["A24"]["x"]["imag"]),
            z = Fp2(Ecom_Eaux_E1["curve"]["A24"]["z"]["real"], 
                   Ecom_Eaux_E1["curve"]["A24"]["z"]["imag"])
        ),
        is_A24_computed_and_normalized=Ecom_Eaux_E1["curve"]["is_A24_computed_and_normalized"]
    )


    message = 0xd81c4d8d734fcbfbeade3d3f8a039faa2a2c9957e835ad55b22e75bf57bb556ac8

    length = 33

    

    result = protocols_verify(sig_obj, pk_obj, message, length, orig_curve_obj)
    
    print("protocols_verify =", result)


    