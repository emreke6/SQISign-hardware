from arith_ops import *
from typing import Optional

# Parameters / types
NWORDS_ORDER = 4                  # number of 64-bit limbs
RADIX = 64                        # limb size in bits
SQIsign_response_length = 253
HD_extra_torsion = 2
TORSION_EVEN_POWER = 248


MASK64 = (1 << 64) - 1


@dataclass
class ECPoint:
    x: Fp2
    z: Fp2

@dataclass
class ECCurve:
    A: Fp2
    C: Fp2
    A24: Optional[ECPoint]
    is_A24_computed_and_normalized: bool

@dataclass
class ECBasis:
    P: ECPoint
    Q: ECPoint
    PmQ: ECPoint


@dataclass
class ECIsogEven:
    curve: ECCurve
    kernel: ECPoint
    length: int

@dataclass
class PublicKey:
    curve: ECCurve
    hint_pk: int

def multiple_mp_shiftl_int(x: int, shift: int) -> int:
    """Equivalent of multiple_mp_shiftl but using Python int"""
    return x << shift


def mp_compare_int(a: int, b: int) -> int:
    if a > b: return 1
    if a < b: return -1
    return 0

def ec_point_init() -> ECPoint:
    return ECPoint(
        x=fp2_set_one(),
        z=fp2_set_zero(),
    )

def ec_curve_init() -> ECCurve:
    return ECCurve(
        A=fp2_set_zero(),
        C=fp2_set_one(),
        A24=ec_point_init(),
        is_A24_computed_and_normalized=False,
    )


def ec_curve_verify_A(A: Fp2) -> bool:
    # t = 2
    t = Fp2(2, 0)
    if fp2_is_equal(A, t):
        return False

    # t = -2
    t = Fp2(-2, 0)
    if fp2_is_equal(A, t):
        return False

    return True

def ec_curve_init_from_A(A: Fp2) -> ECCurve | None:
    E = ec_curve_init()
    E.A = fp2_copy(A)

    if not ec_curve_verify_A(A):
        return None

    return E

@dataclass
class Signature:
    E_aux_A: Fp2
    mat_Bchall_can_to_B_chall: list   # 2x2 matrix of ints
    backtracking: int
    two_resp_length: int
    hint_aux: int
    hint_chall: int
    chall_coeff: int



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



def ec_curve_verify_A(A: Fp2) -> bool:
    """
    Verify the Montgomery coefficient A is valid (A^2 - 4 != 0)
    Equivalent C logic:
      - reject if A ==  2
      - reject if A == -2
      - otherwise accept
    """

    # t = 1
    t = fp2_set_one()

    # t = 2
    t = fp2_add(t, t)

    # if A == 2: reject
    if fp2_is_equal(A, t):
        return False

    # t = -2
    t = Fp2(re=fp_neg(t.re), im=t.im)

    # if A == -2: reject
    if fp2_is_equal(A, t):
        return False

    return True


def copy_curve(dst: ECCurve, src: ECCurve):
    dst.A = src.A
    dst.C = src.C
    dst.A24 = src.A24
    dst.is_A24_computed_and_normalized = src.is_A24_computed_and_normalized


def ec_curve_to_basis_2f_from_hint(basis, curve, f, hint) -> bool:
    # STUB: always succeed
    return True


def ec_ladder3pt(kernel, chall_coeff, P, Q, PmQ, curve) -> bool:
    # STUB: always succeed
    return True


def ec_dbl_iter(out, n, inp, curve):
    # STUB: do nothing
    pass


def ec_eval_even(E_chall, phi_chall, _, __) -> int:
    # STUB: return 0 means success in C
    return 0


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
    copy_curve(phi_chall.curve, Epk)

    # phi_chall.length = TORSION_EVEN_POWER - sig->backtracking;
    phi_chall.length = TORSION_EVEN_POWER - sig.backtracking

    # Compute the basis from the supplied hint
    if not ec_curve_to_basis_2f_from_hint(
        bas_EA,
        phi_chall.curve,
        TORSION_EVEN_POWER,
        hint_pk,
    ):
        return False

    # recovering the exact challenge
    if not ec_ladder3pt(
        phi_chall.kernel,
        sig.chall_coeff,
        bas_EA.P,
        bas_EA.Q,
        bas_EA.PmQ,
        phi_chall.curve,
    ):
        return False

    # Double the kernel until it has the correct order
    ec_dbl_iter(
        phi_chall.kernel,
        sig.backtracking,
        phi_chall.kernel,
        phi_chall.curve,
    )

    # Compute the codomain
    copy_curve(E_chall, phi_chall.curve)

    if ec_eval_even(E_chall, phi_chall, None, 0):
        return False

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

    E_chall = ec_curve_init
    compute_challenge_verify(E_chall, sig_obj, pk.curve, pk.hint_pk)

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






