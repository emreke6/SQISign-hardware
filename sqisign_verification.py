from arith_ops import *
from typing import Optional
from ec import *
from basis import *
from xisog import *




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
    print_hex_point(" bas.P: ",  bas.P)
    if not ret:
        return 0
    
    print("here")

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

    print_curve("E_aux: ", E_aux)
    print_hex_point("B_aux_can.P ", B_aux_can.P)
    print_hex_point("B_aux_can.Q ", B_aux_can.Q)
    print_hex_point("B_aux_can.PmQ ", B_aux_can.PmQ)

    B_aux_can, E_aux = ec_dbl_iter_basis(B_aux_can, TORSION_EVEN_POWER - pow_dim2_deg_resp - HD_extra_torsion, B_aux_can, E_aux)

    print_curve("E_aux 2: ", E_aux)
    print_hex_point("B_aux_can.P 2 ", B_aux_can.P)
    print_hex_point("B_aux_can.Q 2 ", B_aux_can.Q)
    print_hex_point("B_aux_can.PmQ 2 ", B_aux_can.PmQ)

    print_hex_point("B_chall_can.P 2.5 ", B_chall_can.P)
    print_hex_point("B_chall_can.Q 2.5 ", B_chall_can.Q)
    print_hex_point("B_chall_can.PmQ 2.5 ", B_chall_can.PmQ)

    print_curve("E_chall.P 2.5 ", E_chall)
    print(sig.mat_Bchall_can_to_B_chall)
    print(pow_dim2_deg_resp + HD_extra_torsion + sig.two_resp_length)

    B_chall_can, ret1 = matrix_scalar_application_even_basis(B_chall_can,
                                                E_chall,
                                                sig.mat_Bchall_can_to_B_chall,
                                                pow_dim2_deg_resp + HD_extra_torsion + sig.two_resp_length)
    

    print_hex_point("B_chall_can.P 3 ", B_chall_can.P)
    print_hex_point("B_chall_can.Q 3 ", B_chall_can.Q)
    print_hex_point("B_chall_can.PmQ 3 ", B_chall_can.PmQ)
    print_curve("E_chall: ", E_chall)
    return True


def protocols_verify(sig: Signature, pk: PublicKey, m: bytes, l: int) -> bool:

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

    ret_chal_verify = challenge_and_aux_basis_verify(
            B_chall_can, B_aux_can,
            E_chall, E_aux,
            sig, pow_dim2_deg_resp)
    
    if not ret_chal_verify:
        return False

    return True





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

    result = protocols_verify(sig_obj, pk_obj, 0, 0)
    print("protocols_verify =", result)


    