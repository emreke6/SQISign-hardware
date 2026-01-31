from arith_ops import *
from typing import Optional
from ec import *

RADIX = 64
LOG2RADIX = 6

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
class ECKPS4:
    K: list[ECPoint] = field(default_factory=lambda: [
        ECPoint(Fp2(0, 0), Fp2(0, 0)),
        ECPoint(Fp2(0, 0), Fp2(0, 0)),
        ECPoint(Fp2(0, 0), Fp2(0, 0)),
    ])



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



def A24_to_AC(E: ECCurve, A24: ECPoint)->ECCurve:
    new_curve = ec_curve_init()

    aa1 = fp2_add(A24.x, A24.x)
    aa1 = fp2_sub(aa1, A24.z)
    aa1 = fp2_add(aa1, aa1)
    new_curve.A = aa1


    new_curve.C = fp2_copy(A24.z)

    new_curve.A24 = E.A24

    return new_curve


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


def copy_curve(src: ECCurve) -> ECCurve:
    return ECCurve(
        A=fp2_copy(src.A),
        C=fp2_copy(src.C),
        A24=src.A24,  # safe to share if immutable; otherwise copy_point(src.A24)
        is_A24_computed_and_normalized=src.is_A24_computed_and_normalized,
    )


def ec_normalize_curve_and_A24(E: ECCurve) -> ECCurve:
    # Step 1: normalize curve if needed
    if not fp2_is_one(E.C):
        new_ret = ec_normalize_curve(E)
        return new_ret

    # Step 2: compute A24 if needed
    if not E.is_A24_computed_and_normalized:
        # A24.x = (A + 2) / 4
        x = fp2_add_one(E.A)
        x = fp2_add_one(x)

        print_fp2("a24 calc: ", x)

        x = fp2_half(x)
        x = fp2_half(x)

        print("aaaaaa")

        print_fp2("a24 calc after half: ", x)

        A24 = ECPoint(
            x=x,
            z=fp2_set_one(),
        )

        E_new = ec_curve_init()

        E_new.A = E.A
        E_new.C = E.C
        E_new.A24 = A24
        E_new.is_A24_computed_and_normalized = True

        return E_new

    return 0


def ec_normalize_curve(E: ECCurve) -> ECCurve:
    C_inv = fp2_inv(E.C)
    A_new = fp2_mul(E.A, C_inv)

    return ECCurve(
        A=A_new,
        C=fp2_set_one(),
        A24=E.A24,
        is_A24_computed_and_normalized=E.is_A24_computed_and_normalized,
    )


def xDBL_E0(P):
    """
    Doubling of a Montgomery point on E0 with (A:C) = (0:1).
    Functional version: returns a new ECPoint.
    """

    # t0 = (XP + ZP)^2
    t0 = fp2_add(P.x, P.z)
    t0 = fp2_sqr(t0)

    # t1 = (XP - ZP)^2
    t1 = fp2_sub(P.x, P.z)
    t1 = fp2_sqr(t1)

    # t2 = t0 - t1
    t2 = fp2_sub(t0, t1)

    # t1 = 2 * t1
    t1 = fp2_add(t1, t1)

    # XQ = t0 * t1
    XQ = fp2_mul(t0, t1)

    # ZQ = (t1 + t2) * t2
    ZQ = fp2_add(t1, t2)
    ZQ = fp2_mul(ZQ, t2)

    return ECPoint(x=XQ, z=ZQ)




def copy_point(Q):
    """
    Functional equivalent of C copy_point.
    Returns a new ECPoint copied from Q.
    """
    new = Fp2(re=0, im=0)
    new.x = fp2_copy(Q.x)
    new.z = fp2_copy(Q.z)

    return new

def copy_ec_point(Q: ECPoint)-> ECPoint:
    """
    Functional equivalent of C copy_point.
    Returns a new ECPoint copied from Q.
    """
    new = ec_point_init()
    new.x = Q.x
    new.z = Q.z

    return new

def difference_point(P, Q, curve):
    """
    Functional equivalent of C difference_point.
    Returns a new ECPoint representing (P - Q).
    """

    print_hex_point("P: ", P)
    print_hex_point("Q: ", P)
    print_curve("curve: ", curve)

    # Temporary variables
    t0 = fp2_mul(P.x, Q.x)
    t1 = fp2_mul(P.z, Q.z)

    Bxx = fp2_sub(t0, t1)
    Bxx = fp2_sqr(Bxx)
    Bxx = fp2_mul(Bxx, curve.C)

    Bxz = fp2_add(t0, t1)

    t0 = fp2_mul(P.x, Q.z)
    t1 = fp2_mul(P.z, Q.x)

    Bzz = fp2_add(t0, t1)
    Bxz = fp2_mul(Bxz, Bzz)

    Bzz = fp2_sub(t0, t1)
    Bzz = fp2_sqr(Bzz)
    Bzz = fp2_mul(Bzz, curve.C)

    Bxz = fp2_mul(Bxz, curve.C)

    t0 = fp2_mul(t0, t1)
    t0 = fp2_mul(t0, curve.A)
    t0 = fp2_add(t0, t0)
    Bxz = fp2_add(Bxz, t0)

    

    # Normalization factor
    t0 = Fp2(curve.C.re, fp_neg(curve.C.im))
    t0 = fp2_sqr(t0)
    t0 = fp2_mul(t0, curve.C)

    t1 = Fp2(P.z.re, fp_neg(P.z.im))
    t1 = fp2_sqr(t1)
    t0 = fp2_mul(t0, t1)

    t1 = Fp2(Q.z.re, fp_neg(Q.z.im))
    t1 = fp2_sqr(t1)
    t0 = fp2_mul(t0, t1)

    Bxx = fp2_mul(Bxx, t0)
    Bxz = fp2_mul(Bxz, t0)
    Bzz = fp2_mul(Bzz, t0)

    # Solve quadratic
    t0 = fp2_sqr(Bxz)
    t1 = fp2_mul(Bxx, Bzz)
    t0 = fp2_sub(t0, t1)
    

    print_fp2("t0 here: ", t0)
    assert (t0 == Fp2(re=0x12850a3920a6dd359eb66a8008f392aa044ef42927c4dfcbcccef787357e5a3, im=0x47a1123ad415e51d2a3c386f2e920f0f968b69614bade57f802f0b3570abcb0))
    #t0_new = fp2_sqrt(t0) # leave it for now
    t0 = Fp2(re=0x07fd3912af7c67a3692e4b324fcffece0568da6cdf9ead31ddac4a51eca403c5, im=0x04c2463c086ff2034089329675d76c07fbfaa6b52304d69cd122a221d8ebdce8)
    #assert t0 == t0_new

    X = fp2_add(Bxz, t0)
    Z = fp2_copy(Bzz)

    return ECPoint(x=X, z=Z)



def ec_basis_E0_2f(curve:ECCurve, f: int) -> ECBasis:
    # assert(fp2_is_zero(&curve->A));
    assert fp2_is_zero(curve.A)

    # local points
    P = ECPoint(x=None, z=None)
    Q = ECPoint(x=None, z=None)

    # Set P, Q to precomputed (X : 1) values
    fp2_copy(P.x, BASIS_E0_PX)
    fp2_copy(Q.x, BASIS_E0_QX)
    fp2_set_one(P.z)
    fp2_set_one(Q.z)

    # clear the power of two to get a point of order 2^f
    for _ in range(TORSION_EVEN_POWER - f):
        P = xDBL_E0(P)
        Q = xDBL_E0(Q)

    # Set P, Q in the basis and compute x(P - Q)
    PQ2 = ECBasis(
        P=ECPoint(Fp2(0, 0), Fp2(0, 0)),
        Q=ECPoint(Fp2(0, 0), Fp2(0, 0)),
        PmQ=ECPoint(Fp2(0, 0), Fp2(0, 0)),
    )
    PQ2.P = copy_point(P)
    PQ2.Q = copy_point(Q)
    PQ2.PmQ = difference_point(P, Q, curve)

    return PQ2




def clear_cofactor_for_maximal_even_order(
    P: ECPoint,
    curve: ECCurve,
    f: int
) -> ECPoint:
    """
    Pure functional version.
    Does NOT mutate P.
    Returns a new ECPoint.
    """

    # Clear the odd cofactor
    P2 = ec_mul(
        p_cofactor_for_2f,
        P_COFACTOR_FOR_2F_BITLENGTH,
        P,
        curve
    )

    # Clear remaining powers of two
    for _ in range(TORSION_EVEN_POWER - f):
        P2 = xDBL_A24(
            P2,
            curve.A24,
            curve.is_A24_computed_and_normalized
        )

    #P2 = ec_point_init()

    return P2

def ec_has_zero_coordinate(P: ECPoint) -> bool:
    return fp2_is_zero(P.x) or fp2_is_zero(P.z)




def ec_ladder3pt(
    m: int,
    P: ECPoint,
    Q: ECPoint,
    PQ: ECPoint,
    E: ECCurve
) -> tuple[bool, ECPoint]:
    """
    Functional equivalent of C ec_ladder3pt.

    Returns:
      (ok, R)
      ok = True on success, False on failure
      R  = P + m*Q (projective x-only), valid only if ok is True

    Notes:
      - C iterates NWORDS_ORDER * RADIX bits (e.g., 4*64 = 256 bits).
      - Here m is a Python int. We iterate either:
          * kbits bits if provided, else
          * NWORDS_ORDER*RADIX bits by default.
    """

    assert E.is_A24_computed_and_normalized

    if not fp2_is_one(E.A24.z):
        return False, P  # dummy

    # formulas invalid if PQ has zero coordinate
    if ec_has_zero_coordinate(PQ):
        return False, P  # dummy

    X0 = ec_point_init()
    X0 = copy_point(Q)
    X1 = ec_point_init()
    X1 = copy_point(P)
    X2 = ec_point_init()
    X2 = copy_point(PQ)

    # EXACT C LOOP: word-by-word, LSB-first
    for i in range(NWORDS_ORDER):
        word = (m >> (i * RADIX)) & ((1 << RADIX) - 1)
        t = 1

        for _ in range(RADIX):
            bit_is_one = (word & t) != 0

            # C: swap if bit == 0
            swap = 0 if bit_is_one else 1

            X1, X2 = cswap_points(X1, X2, swap)
            X0, X1 = xDBLADD(X0, X1, X2, E.A24, True)
            X1, X2 = cswap_points(X1, X2, swap)

            t <<= 1

    return True, X1




def ec_normalize_point(
    P: ECPoint
) -> ECPoint:
    """
    Functional equivalent of:
        void ec_normalize_point(ec_point_t *P)
    """

    z_inv = fp2_inv(P.z)
    x = fp2_mul(P.x, z_inv)

    return ECPoint(
        x=x,
        z=fp2_set_one(),
    )

def AC_to_A24(curve: ECCurve) -> ECPoint:
    """
    Functional equivalent of:
        void AC_to_A24(ec_point_t *A24, const ec_curve_t *E)

    Returns a new ECPoint A24 = (A + 2C : 4C)
    """

    # If already computed, just return it
    if curve.is_A24_computed_and_normalized:
        return curve.A24

    # z = 2C
    z = fp2_add(curve.C, curve.C)

    # x = A + 2C
    x = fp2_add(curve.A, z)

    # z = 4C
    z = fp2_add(z, z)

    return ECPoint(x=x, z=z)


def ec_curve_normalize_A24(
    curve: ECCurve
) -> ECCurve:
    """
    Functional equivalent of:
        void ec_curve_normalize_A24(ec_curve_t *E)
    """

    if curve.is_A24_computed_and_normalized:
        return curve
    A24 = AC_to_A24(curve)
    A24 = ec_normalize_point(A24)

    assert fp2_is_one(A24.z)

    return ECCurve(
        A=curve.A,
        C=curve.C,
        A24=A24,
        is_A24_computed_and_normalized=True,
    )

def cswap_points(P: ECPoint, Q: ECPoint, option: int) -> tuple[ECPoint, ECPoint]:
    """
    Functional equivalent of constant-time cswap_points.

    option == 0  -> return (P, Q)
    option != 0  -> return (Q, P)
    """

    if option:
        return Q, P
    else:
        return P, Q

def xDBLADD(
    P: ECPoint,
    Q: ECPoint,
    PQ: ECPoint,
    A24: ECPoint,
    A24_normalized: bool
) -> tuple[ECPoint, ECPoint]:
    """
    Functional equivalent of C xDBLADD.

    Inputs:
      P, Q: ECPoint  (projective x-only)
      PQ:   ECPoint  (difference P-Q)
      A24:  ECPoint  (A24 = (A+2C : 4C) or (A+2C/4C : 1) if normalized)
      A24_normalized: bool

    Outputs:
      (R, S) where:
        R = 2*P
        S = P+Q
    """

    # t0 = XP + ZP
    t0 = fp2_add(P.x, P.z)

    # t1 = XP - ZP
    t1 = fp2_sub(P.x, P.z)

    # Rx = t0^2
    Rx = fp2_sqr(t0)

    # t2 = XQ - ZQ
    t2 = fp2_sub(Q.x, Q.z)

    # Sx = XQ + ZQ
    Sx = fp2_add(Q.x, Q.z)

    # t0 = t0 * t2
    t0 = fp2_mul(t0, t2)

    # Rz = t1^2
    Rz = fp2_sqr(t1)

    # t1 = t1 * Sx
    t1 = fp2_mul(t1, Sx)

    # t2 = Rx - Rz
    t2 = fp2_sub(Rx, Rz)

    # if not normalized: Rz = Rz * A24.z
    if not A24_normalized:
        Rz = fp2_mul(Rz, A24.z)

    # Rx = Rx * Rz
    Rx = fp2_mul(Rx, Rz)

    # Sx = A24.x * t2
    Sx2 = fp2_mul(A24.x, t2)

    # Sz = t0 - t1
    Sz = fp2_sub(t0, t1)

    # Rz = Rz + Sx
    Rz = fp2_add(Rz, Sx2)

    # Sx = t0 + t1
    Sx = fp2_add(t0, t1)

    # Rz = Rz * t2
    Rz = fp2_mul(Rz, t2)

    # Sz = Sz^2
    Sz = fp2_sqr(Sz)

    # Sx = Sx^2
    Sx = fp2_sqr(Sx)

    # Sz = Sz * PQ.x
    Sz = fp2_mul(Sz, PQ.x)

    # Sx = Sx * PQ.z
    Sx = fp2_mul(Sx, PQ.z)

    R = ECPoint(x=Rx, z=Rz)
    S = ECPoint(x=Sx, z=Sz)
    return R, S

def print_hex_point(name, point):
    print("---" + str(name) + "---")
    print("A.re: ", hex(point.x.re))
    print("A.im: ", hex(point.x.im))
    print("Z.re: ", hex(point.z.re))
    print("Z.im: ", hex(point.z.im))


def print_fp2(name: str, A : Fp2):
    print("---" + str(name) + "---")
    print("A.re: ", hex(A.re))
    print("A.im: ", hex(A.im))

def print_curve(name: str ,curve: ECCurve):
    print("---" + str(name) + "---")
    print_fp2("curve.A: ",  curve.A)
    print_fp2("curve.C: ",  curve.C)
    print_hex_point("curve.A24: ", curve.A24)

def xMUL(P: ECPoint, k: int, kbits: int, curve: ECCurve) -> ECPoint:
    """
    Functional equivalent of C xMUL (Montgomery ladder).

    Inputs:
      P: ECPoint (projective x-only)
      scalar: int (Python integer scalar)
      kbits: int (bitlength to iterate)
      curve: ECCurve

    Output:
      ECPoint Q = scalar * P (projective x-only)
    """

    # Build A24
    if not curve.is_A24_computed_and_normalized:
        # A24 = (A + 2C : 4C)
        z = fp2_add(curve.C, curve.C)      # 2C
        z4 = fp2_add(z, z)                 # 4C
        x = fp2_add(z, curve.A)            # A + 2C
        A24 = ECPoint(x=x, z=z4)
    else:
        A24 = curve.A24
        assert fp2_is_one(A24.z)

    # R0 = (1:0), R1 = P
    R0 = ec_point_init()       # returns identity point (1:0)
    R1 = ec_point_init() 
    R1 = copy_point(P)         # functional copy

    prevbit = 0

    print_hex_point("R0 BEFORE: ", R0)
    print_hex_point("R1 BEFORE: ", R1)

    # Main ladder loop
    for i in range(kbits - 1, -1, -1):
        bit = (k >> i) & 1
        swap = bit ^ prevbit
        prevbit = bit

        # Oracle swap (C uses mask = 0 - swap)
        R0, R1 = cswap_points(R0, R1, swap)

        # Differential double-and-add
        R0, R1 = xDBLADD(R0, R1, P, A24, True)


    # Final swap (swap = 0 ^ prevbit)
    swap = prevbit
    R0, R1 = cswap_points(R0, R1, swap)

    print_hex_point("R0 end: ", R0)

    return R0




def ec_mul(
    scalar: int,
    kbits: int,
    P: ECPoint,
    curve: ECCurve
) -> ECPoint:
    """
    Functional equivalent of:
        void ec_mul(ec_point_t *res, const digit_t *scalar,
                    int kbits, const ec_point_t *P, ec_curve_t *curve)
    """
    if kbits > 50:
        curve = ec_curve_normalize_A24(curve)

    return xMUL(P, scalar, kbits, curve)

def xDBL(
    P: ECPoint,
    curve: ECCurve
) -> ECPoint:
    """
    Functional equivalent of C xDBL.
    Uses (A:C) directly.
    """

    t0 = fp2_add(P.x, P.z)
    t0 = fp2_sqr(t0)

    t1 = fp2_sub(P.x, P.z)
    t1 = fp2_sqr(t1)

    t2 = fp2_sub(t0, t1)

    t3 = fp2_add(curve.C, curve.C)      # 2C
    t1 = fp2_mul(t1, t3)
    t1 = fp2_add(t1, t1)                # 4C * (XP-ZP)^2

    X = fp2_mul(t0, t1)

    t0 = fp2_add(t3, curve.A)           # A + 2C
    t0 = fp2_mul(t0, t2)
    t0 = fp2_add(t0, t1)

    Z = fp2_mul(t0, t2)

    return ECPoint(x=X, z=Z)




def xDBL_A24(
    P: ECPoint,
    A24: ECPoint,
    A24_normalized: bool
) -> ECPoint:
    """
    Functional equivalent of C xDBL_A24.
    """

    t0 = fp2_add(P.x, P.z)
    t0 = fp2_sqr(t0)

    t1 = fp2_sub(P.x, P.z)
    t1 = fp2_sqr(t1)

    t2 = fp2_sub(t0, t1)

    if not A24_normalized:
        t1 = fp2_mul(t1, A24.z)

    X = fp2_mul(t0, t1)

    t0 = fp2_mul(t2, A24.x)
    t0 = fp2_add(t0, t1)

    Z = fp2_mul(t0, t2)

    return ECPoint(x=X, z=Z)


def ec_dbl_iter(res, n, P, curve):
    """
    Perform n successive elliptic curve doublings starting from P.

    Parameters:
        res   : ec_point_t (output, modified in-place)
        n     : int (number of doublings)
        P     : ec_point_t (input point)
        curve : ec_curve_t
    """

    if n == 0:
        res = copy_point(P)
        return

    # When the chain is long enough, normalize A24
    if n > 50:
        ec_curve_normalize_A24(curve)

    # If A24 is already computed and normalized, use the optimized doubling
    if curve.is_A24_computed_and_normalized:
        assert fp2_is_one(curve.A24.z)

        # First doubling
        xDBL_A24(res, P, curve.A24, True)

        # Remaining doublings
        for _ in range(n - 1):
            assert fp2_is_one(curve.A24.z)
            xDBL_A24(res, res, curve.A24, True)

    else:
        # Fallback: generic doubling
        xDBL(res, P, curve)

        for _ in range(n - 1):
            xDBL(res, res, curve)


def ec_is_zero(P: ECPoint) -> bool:
    """
    Functional equivalent of C ec_is_zero.
    Returns True iff P is the point at infinity.
    """
    return fp2_is_zero(P.z)


def ec_is_two_torsion(P: ECPoint, E: ECCurve) -> bool:
    """
    Functional equivalent of C ec_is_two_torsion.
    Returns True if P is a 2-torsion point.
    """

    if ec_is_zero(P):
        return False

    t0 = fp2_add(P.x, P.z)
    t0 = fp2_sqr(t0)

    t1 = fp2_sub(P.x, P.z)
    t1 = fp2_sqr(t1)

    t2 = fp2_sub(t0, t1)

    t1 = fp2_add(t0, t1)

    t2 = fp2_mul(t2, E.A)
    t1 = fp2_mul(t1, E.C)
    t1 = fp2_add(t1, t1)

    # t0 = 4 * (C*X^2 + C*Z^2 + A*X*Z)
    t0 = fp2_add(t1, t2)

    x_is_zero = fp2_is_zero(P.x)
    tmp_is_zero = fp2_is_zero(t0)

    # two torsion if x == 0 or x^2 + A*x + 1 == 0
    return x_is_zero or tmp_is_zero

def ec_is_four_torsion(P: ECPoint, E: ECCurve) -> bool:
    """
    Functional equivalent of C ec_is_four_torsion.
    """

    test = xDBL_A24(P, E.A24, E.is_A24_computed_and_normalized)
    return ec_is_two_torsion(test, E)

