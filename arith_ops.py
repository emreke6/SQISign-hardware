

from dataclasses import dataclass, field
from typing import List, Tuple, Optional


q   = pow(2,248)*5 - 1 # 64-bit: prime q
R   = pow(2,256) # 2^256
Rv  = pow(R, -1, q) # 64-bit: R^-1 (mod q)
mu  = (-pow(q,-1,R)) % R # 64-bit: (−q)^−1 (mod R)

ONE = 0x0100000000000000000000000000000000000000000000000000000000000033


R_INV = pow(R, -1, q)   # modular inverse

# ---------- Base Fp2 ----------
@dataclass
class Fp2:
    re: int = 0
    im: int = 0


# ---------- Theta Point ----------
@dataclass
class ThetaPoint:
    x: Fp2 = field(default_factory=Fp2)
    y: Fp2 = field(default_factory=Fp2)
    z: Fp2 = field(default_factory=Fp2)
    t: Fp2 = field(default_factory=Fp2)


# ---------- Theta Structure ----------
@dataclass
class ThetaStructure:
    null_point: ThetaPoint = field(default_factory=ThetaPoint)
    precomputation: bool = False

    # Eight precomputed fp2 values
    XYZ0: Fp2 = field(default_factory=Fp2)
    YZT0: Fp2 = field(default_factory=Fp2)
    XZT0: Fp2 = field(default_factory=Fp2)
    XYT0: Fp2 = field(default_factory=Fp2)
    xyz0: Fp2 = field(default_factory=Fp2)
    yzt0: Fp2 = field(default_factory=Fp2)
    xzt0: Fp2 = field(default_factory=Fp2)
    xyt0: Fp2 = field(default_factory=Fp2)


# ---------- Theta Isogeny ----------
@dataclass
class ThetaIsogeny:
    T1_8: ThetaPoint = field(default_factory=ThetaPoint)
    T2_8: ThetaPoint = field(default_factory=ThetaPoint)
    hadamard_bool_1: bool = False
    hadamard_bool_2: bool = False
    domain: ThetaStructure = field(default_factory=ThetaStructure)
    precomputation: ThetaPoint = field(default_factory=ThetaPoint)
    codomain: ThetaStructure = field(default_factory=ThetaStructure)



def montgomery(C, R, q):
    m = ((C%(R)) * (mu)) % R
    u = C + m*(q)
    u = u >> 256 # u/R
    D = u
    return D


def interleaved_montgomery(C, q):
    """
    64-bit interleaved Montgomery reduction for 256-bit modulus q.
    C: integer (512-bit product)
    q: integer (modulus)
    returns: C * R^-1 mod q, where R = 2^256
    """
    R_word = 1 << 64
    mask = R_word - 1

    # precompute q' = -q^{-1} mod 2^64
    q_dash = (-pow(q, -1, R_word)) & mask

    # work on 320-bit intermediate value
    T = C
    for i in range(4):  # 4 limbs of 64 bits
        m = (((T) & mask) * (q_dash)) & mask
        T = (T + m * (q)) >> 64

    print("check: ", T > q, T > 2*q)
    # conditional subtraction

    return T


def montgomery_sqisign(C, R, q):
    C_new = C % R
    C_times_mu = (C_new << 250) + (C_new << 248) + C_new # C*q
    m = C_times_mu % (pow(2,256))
    m_times_q_calc = (((m<<2) + m) << 248) - m # m*q^(-1) mod R
    u = C + m_times_q_calc
    u = u >> 256 # u/R
    D = u
    return D

def montgomery_sqisign_fp_sqr(C, R, q):
    C_new = C
    C_times_mu = (C_new << 250) + (C_new << 248) + C_new # C*q
    m = C_times_mu % (pow(2,256))
    m_times_q_calc = (((m<<2) + m) << 248) - m # m*q^(-1) mod R
    u = C + m_times_q_calc
    u = u >> 256 # u/R
    D = u
    return D

def modsub_sqisign(a, b, bool1):
    c = a - b

    c2 = c + q

    if c < 0:
        r1 = c2
    else:
        r1 = c

    if not bool1:
        if r1 < 0:
            r1 = r1 + q
        else:
            r1 = r1
    else:
        r1 = a - b + 2 * q

    return r1

MASK64  = (1 << 64) - 1
MASK256 = (1 << 256) - 1

def modadd_sqisign_exact(a, b, p):
    # force 256-bit arithmetic
    c = (a + b) & MASK256

    for _ in range(2):
        # extract top limb (bits 192..255)
        r11 = (c >> 192) & MASK64

        # extract overflow bits (top 5 bits)
        overflow = r11 >> 59

        # create mask: 0 or -1 (64-bit)
        mask = (-overflow) & MASK64

        # masked subtraction (limb-wise)
        c = (c - (mask | (mask << 64) | (mask << 128) |
                 ((p >> 192) & MASK64) * (mask >> 63) << 192)
            ) & MASK256

    return c

def modadd_sqisign(a, b, bool1):
    c = a + b
    prev = a + b

    # First reduction pass
    # overflow = (c >> 251) & 0x1F  # Check top bits (assuming 256-bit)
    # mask = (-overflow) & ((1 << 256) - 1)  # Create mask
    # print("mask: ", bin(mask), len(bin(mask)[2:]))
    # print("mask & q = ", bin((mask & q)))
    # c = (c - (mask & q)) & ((1 << 256) - 1)

    # # Second reduction pass (repeat)
    # overflow = (c >> 251) & 0x1F
    # mask = (-overflow) & ((1 << 256) - 1)
    # c = (c - (mask & q)) & ((1 << 256) - 1)

    c_mask = c >> (192+59)

    if c_mask != 0:
        c = c - q

    c_mask = c >> (192+59)

    if c_mask != 0:
        c = c - q

    if bool1:
        c = prev
    else:
        c = c

    return c


def fp_add_sqr(a, b):
    return modadd_sqisign(a, b, True)

def fp_add(a, b):
    return modadd_sqisign(a, b, False)

def fp_sub(a, b):
    return modsub_sqisign(a, b, False)

def fp_sub_sqr(a, b):
    return modsub_sqisign(a, b, True)

def fp_is_zero(a: int, q: int) -> bool:
    """
    Check if a field element 'a' in F_p is zero.
    In Montgomery or standard representation, 'a' is considered zero if:
        a % q == 0
    """
    return (a % q) == 0

def fp2_set_zero() -> Fp2:
    return Fp2(0, 0)

def fp2_set_one() -> Fp2:
    return Fp2(re=ONE, im=0)

def fp_set_one() -> int:
    return ONE

def fp_half(a: int) -> int:
    """
    Functional equivalent of gf5248_half.
    Treated as integer division by 2.
    """
    if a % 2 == 1:
        a = ((a >> 1) + ((q+1)>>1)) % q
    else:
        a = (a >> 1) % q
    return a

def fp2_half(y: Fp2) -> Fp2:
    """
    Functional equivalent of gf5248_half.
    Treated as integer division by 2.
    """
    x = Fp2(re=0, im=0)
    x.re = fp_half(y.re)
    x.im = fp_half(y.im)
    return x

def fp2_add_one(y: Fp2) -> Fp2:
    """
    Functional equivalent of gf5248_half.
    Treated as integer division by 2.
    """
    x = Fp2(re=0, im=0)
    x.re = fp_add(y.re, ONE)
    x.im = fp_copy(y.im)
    return x


def fp_neg(a: int) -> int:
    res = 2*q - a
    if res < pow(2,251):
        return res
    else:
        return res - q


def fp2_neg(y: Fp2) -> Fp2:
    x = Fp2(re=0, im=0)
    x.re = fp_neg(y.re)
    x.im = fp_neg(y.im)
    return x


def fp2_is_one(a: Fp2) -> bool:
    return a.re % q == ONE and a.im == 0

def fp_set_small(a: int)->int:
    return a * pow(2,256,q) % q

def fp_mul_small(a: int, n: int) -> int:
    """
    Functional equivalent of fp_mul_small / gf5248_mul_small.
    Treated as regular integer multiplication.
    """
    return (a * n) % q

def fp2_mul_small(y, n):
    """
    Functional equivalent of fp2_mul_small.
    Returns y * n in Fp2.
    """
    return Fp2(
        re=fp_mul_small(y.re, n),
        im=fp_mul_small(y.im, n),
    )

def legendre_symbol(a: int) -> int:
    """
    Returns:
        0  if a == 0 (mod p)
        1  if a is a quadratic residue mod p
       -1  if a is a non-residue mod p
    """
    a %= q
    if a == 0:
        return 0

    # Euler's criterion
    ls = pow(a, (q - 1) // 2, q)
    return 1 if ls == 1 else -1

def fp_is_square(a: int) -> bool:
    """
    Python equivalent of fp_is_square.
    Returns True if a == 0 or a is a quadratic residue mod p.
    """
    ls = legendre_symbol(a)
    return ls >= 0

def fp2_is_square(x: Fp2) -> Fp2:
    """
    Functional equivalent of C fp2_is_square.

    Returns True if x is a square in Fp2 (using norm test).
    """

    t0 = fp_mul(x.re, x.re)
    t1 = fp_mul(x.im, x.im)
    t0 = fp2_add(t0, t1)

    return fp_is_square(t0)


def fp2_is_zero(a: Fp2) -> bool:
    """
    Check if an Fp2 element (a.re, a.im) is zero.
    Returns True if both components are 0 mod q.
    """
    return fp_is_zero(a.re, q) and fp_is_zero(a.im, q)

def fp2_copy(in1):
    return in1

def fp_copy(in1):
    return in1

def fp2_is_equal(a: Fp2, b: Fp2) -> bool:
    """Check equality of two Fp2 elements."""
    return a.re == b.re and a.im == b.im

def fp2_add(a, b):
    fp_add_re = fp_add(a.re, b.re)
    fp_add_im = fp_add(a.im, b.im)

    return Fp2(re=fp_add_re, im=fp_add_im)

def fp2_sub(a, b):
    fp_sub_re = fp_sub(a.re, b.re)
    fp_sub_im = fp_sub(a.im, b.im)

    return Fp2(re=fp_sub_re, im=fp_sub_im)

def fp2_inv(x):
    """
    Functional equivalent of C fp2_inv using fp_* operations.

    Computes:
        (a + i b)^(-1) = (a - i b) / (a^2 + b^2)
    """

    # t0 = a^2
    t0 = fp_mul(x.re, x.re)

    # t1 = b^2
    t1 = fp_mul(x.im, x.im)

    # t0 = a^2 + b^2
    t0 = fp_add(t0, t1)

    # t0 = 1 / (a^2 + b^2)
    t0 = fp_inv(t0)

    # re = a * t0
    re = fp_mul(x.re, t0)

    # im = -b * t0
    im = fp_mul(x.im, t0)
    im = fp_neg(im)

    return Fp2(re=re, im=im)

def fp_inv(a:int)->int:
    return pow(a,-1,q) * pow(2, 256, q) % q


def fp_mul(a, b):
    C = a * b
    return montgomery_sqisign(C, R, q)

def fp_mul_fp_sqr(a, b):
    C = a * b
    return montgomery_sqisign_fp_sqr(C, R , q)

def fp2_mul(y, z):
    """
    Perform fp2 multiplication:
        x = y * z
    where each input is an Fp2 object with .re and .im attributes,
    and fp_add, fp_sub, fp_mul each return Fp elements.
    """
    # Step 1: t0 = (y.re + y.im)
    t0 = fp_add(y.re, y.im)

    # Step 2: t1 = (z.re + z.im)
    t1 = fp_add(z.re, z.im)

    # Step 3: t0 = t0 * t1
    t0 = fp_mul(t0, t1)

    # Step 4: t1 = (y.im * z.im)
    t1 = fp_mul(y.im, z.im)

    # Step 5: x.re = (y.re * z.re)
    x_re = fp_mul(y.re, z.re)

    # Step 6: x.im = t0 - t1
    x_im = fp_sub(t0, t1)

    # Step 7: x.im = x.im - x.re
    x_im = fp_sub(x_im, x_re)

    # Step 8: x.re = x.re - t1
    x_re = fp_sub(x_re, t1)

    # Return Fp2 result
    return Fp2(re=x_re, im=x_im)

# Combine limbs (little endian → shift by 64 bits per limb)
def combine_limbs(limbs):
    val = 0
    for i, limb in enumerate(limbs):
        val += limb << (64 * i)
    return val

# Split big integer into 64-bit limbs (little endian)
def split_limbs(x, num_limbs=5):
    mask = (1 << 64) - 1
    limbs = []
    for i in range(num_limbs):
        limbs.append(x & mask)   # take lowest 64 bits
        x >>= 64                 # shift down for next limb
    return limbs



def combine_fp2(fp2):
    """Return combined integer values for an Fp2 element."""
    return {
        "re": combine_limbs(fp2.re),
        "im": combine_limbs(fp2.im),
    }

def combine_fp2_class(fp2):
    """Return combined integer values of an Fp2 class object."""
    res = combine_fp2(fp2)
    return Fp2(re=res["re"], im=res["im"])

def combine_theta_point(tp):
    """Return combined integer values for every coordinate in a ThetaPoint."""
    return {
        "x": combine_fp2(tp.x),
        "y": combine_fp2(tp.y),
        "z": combine_fp2(tp.z),
        "t": combine_fp2(tp.t),
    }

def combine_theta_point_class(tp):
    """Return combined integer values of an Fp2 class object."""
    res = {
        "x": combine_fp2_class(tp.x),
        "y": combine_fp2_class(tp.y),
        "z": combine_fp2_class(tp.z),
        "t": combine_fp2_class(tp.t),
    }
    return ThetaPoint(x=res["x"], y=res["y"], z=res["z"], t=res["t"])

def hadamard_sqisign(in1): # input is a ThetaPoint
    t1 = fp2_add(in1.x ,in1.y)
    t2 = fp2_sub(in1.x, in1.y)
    t3 = fp2_add(in1.z, in1.t)
    t4 = fp2_sub(in1.z, in1.t)

    out1 = ThetaPoint(x=0, y=0, z=0, t=0)
    out1.x = fp2_add(t1, t3)
    out1.y = fp2_add(t2, t4)
    out1.z = fp2_sub(t1, t3)
    out1.t = fp2_sub(t2, t4)

    return out1



# def mod_sqrt(a, p):
#     """Tonelli-Shanks: returns x s.t. x^2 = a mod p, or None"""
#     if a == 0:
#         return 0
#     if pow(a, (p - 1) // 2, p) != 1:
#         return None  # no square root

#     if p % 4 == 3:
#         return pow(a, (p + 1) // 4, p)

#     # Factor p-1 = q * 2^s
#     q = p - 1
#     s = 0
#     while q % 2 == 0:
#         q //= 2
#         s += 1

#     # Find z a quadratic non-residue
#     z = 2
#     while pow(z, (p - 1) // 2, p) != p - 1:
#         z += 1

#     c = pow(z, q, p)
#     x = pow(a, (q + 1) // 2, p)
#     t = pow(a, q, p)
#     m = s

#     while t != 1:
#         i = 1
#         temp = pow(t, 2, p)
#         while temp != 1:
#             temp = pow(temp, 2, p)
#             i += 1

#         b = pow(c, 2 ** (m - i - 1), p)
#         x = (x * b) % p
#         t = (t * b * b) % p
#         c = (b * b) % p
#         m = i

#     return x

# def fp_sqrt(a: Fp2)->Fp2:
#     return mod_sqrt(a, q)

def fp_sqr(x: Fp2)->Fp2:
    return fp_mul(x ,x)

# def fp_exp3div4(a: int, p: int) -> int:
#     return pow(a, (p - 3) // 4, p)

# def gf5248_select(a0: int, a1: int, ctl: int) -> int:
#     """
#     ctl must be either 0 or 0xFFFFFFFF
#     """
#     return a0 if ctl == 0 else a1

# def fp_select(a0: int, a1: int, ctl: int) -> int:
#     return gf5248_select(a0, a1, ctl)

# def gf5248_encode(a_mont: int) -> bytes:
#     """
#     a_mont is in Montgomery domain: a_mont = a * R mod Q
#     Output matches C gf5248_encode exactly.
#     """
#     # Montgomery reduction: a = a_mont * R^{-1} mod Q
#     a = (a_mont * R_INV) % q

#     # Encode as 32-byte little-endian
#     return a.to_bytes(32, byteorder="little")



# def fp_encode(a: int) -> bytes:
#     return gf5248_encode(a)

# def fp2_sqrt(a: Fp2)->Fp2:
#     """
#     In-place square root in Fp2.
#     a is an Fp2 object with fields a.re, a.im
#     """

#     # Temporary variables
#     x0 = a.re
#     x1 = a.im
#     t0 = a.re
#     t1 = a.im

#     # x0 = delta = sqrt(a0^2 + a1^2)
#     x0 = fp_sqr(a.re)
#     x1 = fp_sqr(a.im)
#     x0 = fp_add(x0, x1)
#     x0 = fp_sqrt(x0)

#     # If a1 == 0, force delta = a0
#     x0 = fp_select(x0, a.re, fp_is_zero(a.im, q))

#     # x0 = delta + a0, t0 = 2*x0
#     x0 = fp_add(x0, a.re)
#     t0 = fp_add(x0, x0)

#     # x1 = t0^((p-3)//4)
#     x1 = t0
#     x1 = fp_exp3div4(x1, q)

#     # x0 = x0 * x1
#     # x1 = x1 * a1
#     # t1 = (2*x0)^2
#     x0 = fp_mul(x0, x1)
#     x1 = fp_mul(x1, a.im)
#     t1 = fp_add(x0, x0)
#     t1 = fp_sqr(t1)

#     # If t1 == t0:
#     #   return x0 + x1*i
#     # else:
#     #   return x1 - x0*i
#     t0_check = fp_sub(t0, t1)
#     f = fp_is_zero(t0_check, q)

#     t1_neg = fp_neg(x0)
#     t0_tmp = x1

#     t0 = fp_select(t0_tmp, x0, f)
#     t1 = fp_select(t1_neg, x1, f)

#     # Canonical sign fixing
#     t0_is_zero = fp_is_zero(t0, q)

#     t0_bytes = fp_encode(t0)
#     t0_is_odd = - (t0_bytes[0] & 1)

#     t1_bytes = fp_encode(t1)
#     t1_is_odd = - (t1_bytes[0] & 1)

#     negate_output = t0_is_odd | (t0_is_zero & t1_is_odd)

#     # Conditional negation
#     a_new = Fp2(re=0, im=0)
#     a_new.re = fp_select(t0, fp_neg(t0), negate_output)
#     a_new.im = fp_select(t1, fp_neg(t1), negate_output)

#     return a_new


# def fp2_sqr(y: Fp2) -> Fp2:
#     """
#     Computes x = y^2 in the quadratic extension field Fp2.

#     Args:
#         y (Fp2): input element (with fields re, im)
#     Returns:
#         Fp2: output squared element
#     """

#     # sum = y.re + y.im
#     sum_ = fp_add_sqr(y.re, y.im)

#     # diff = y.re - y.im
#     diff = fp_sub_sqr(y.re, y.im)

#     # x.im = 2 * (y.re * y.im)
#     im_part = fp_add_sqr(y.re, y.re)  # multiply by 2 via addition
#     im_part = fp_mul_fp_sqr(im_part, y.im)
    

#     # x.re = (y.re + y.im) * (y.re - y.im)
#     re_part = fp_mul_fp_sqr(sum_, diff)

#     # Return new Fp2 element
#     return Fp2(re=re_part, im=im_part)

def fp2_sqr(y: Fp2) -> Fp2:
    """
    Computes x = y^2 in the quadratic extension field Fp2.

    Args:
        y (Fp2): input element (with fields re, im)
    Returns:
        Fp2: output squared element
    """

    # sum = y.re + y.im
    sum_ = fp_add(y.re, y.im)

    # diff = y.re - y.im
    diff = fp_sub(y.re, y.im)

    # x.im = (2* y.re) * y.im
    re_mul2 = fp_add(y.re, y.re)  # multiply by 2 via addition
    im_part = fp_mul(re_mul2, y.im)
   
    # x.re = (y.re + y.im) * (y.re - y.im)
    re_part = fp_mul(sum_, diff)

    # Return new Fp2 element
    return Fp2(re=re_part, im=im_part)



def fp2_sqr_c0(y: Fp2) -> Fp2:
    # sum = y.re + y.im
    sum_ = fp_add_sqr(y.re, y.im)

    # diff = y.re - y.im
    diff = fp_sub_sqr(y.re, y.im)

    # x.re = (y.re + y.im) * (y.re - y.im)
    re_part = fp_mul_fp_sqr(sum_, diff)

    # Return new Fp2 element
    return re_part

def fp2_sqr_c1(y: Fp2) -> Fp2:

    im_part = fp_add(y.re, y.re)  # multiply by 2 via addition
    im_part = fp_mul_fp_sqr(im_part, y.im)
    

    # Return new Fp2 element
    return im_part



def fp2_sqr_new(a: Fp2)->Fp2:
    re_part = fp2_sqr_c0(a)
    im_part = fp2_sqr_c1(a)

    return Fp2(re=re_part, im=im_part)


def pointwise_square(tp_in):
    out1 = ThetaPoint(x=0, y=0, z=0, t=0)
    out1.x = fp2_sqr(tp_in.x)
    out1.y = fp2_sqr(tp_in.y) 
    out1.z = fp2_sqr(tp_in.z)
    out1.t = fp2_sqr(tp_in.t)
    
    return out1


def to_squared_theta(input1):
    out11 = pointwise_square(input1)
    ret1 = hadamard_sqisign(out11)
    
    return ret1

def hadamard_and_ptwise_sq(input1):
    out11 = hadamard_sqisign(input1)
    ret1 = to_squared_theta(out11)

    return ret1

def theta_precomputation(A: ThetaStructure) -> ThetaStructure:
    """
    Python equivalent of:
        void theta_precomputation(theta_structure_t *A)

    Returns a *new* ThetaStructure A_new with computed fields (no in-place mutation).
    """

    # If already precomputed, just return as-is
    if A.precomputation:
        return A

    # --- Step 1: Compute A_dual = to_squared_theta(A.null_point)
    A_dual = to_squared_theta(A.null_point)

    # --- Step 2: Temporary fp2 intermediates
    t1 = fp2_mul(A_dual.x, A_dual.y)
    t2 = fp2_mul(A_dual.z, A_dual.t)

    # --- Step 3: Compute upper-case constants
    XYZ0 = fp2_mul(t1, A_dual.z)
    XYT0 = fp2_mul(t1, A_dual.t)
    YZT0 = fp2_mul(t2, A_dual.y)
    XZT0 = fp2_mul(t2, A_dual.x)

    # --- Step 4: Recompute t1, t2 using null_point
    t1 = fp2_mul(A.null_point.x, A.null_point.y)
    t2 = fp2_mul(A.null_point.z, A.null_point.t)

    # --- Step 5: Compute lower-case constants
    xyz0 = fp2_mul(t1, A.null_point.z)
    xyt0 = fp2_mul(t1, A.null_point.t)
    yzt0 = fp2_mul(t2, A.null_point.y)
    xzt0 = fp2_mul(t2, A.null_point.x)

    # --- Step 6: Build and return new structure
    A_new = ThetaStructure(
        null_point=A.null_point,
        precomputation=True
    )

    # Assign all computed constants
    A_new.XYZ0 = XYZ0
    A_new.XYT0 = XYT0
    A_new.YZT0 = YZT0
    A_new.XZT0 = XZT0
    A_new.xyz0 = xyz0
    A_new.xyt0 = xyt0
    A_new.yzt0 = yzt0
    A_new.xzt0 = xzt0

    return A_new


def double_point(A: ThetaStructure, inp: ThetaPoint) -> ThetaPoint:
    """
    Python equivalent of:
        void double_point(theta_point_t *out, theta_structure_t *A, const theta_point_t *in)
    Performs a single theta-point doubling with precomputation and fp2 operations.
    """
    # --- Step 1: Move to squared theta coordinates
    out = to_squared_theta(inp)

    # --- Step 2: Square each coordinate
    out.x = fp2_sqr(out.x)
    out.y = fp2_sqr(out.y)
    out.z = fp2_sqr(out.z)
    out.t = fp2_sqr(out.t)

    # --- Step 3: Ensure precomputation
    if not A.precomputation:
        theta_precomputation(A)

    # --- Step 4: Multiply with A’s precomputed constants
    out.x = fp2_mul(out.x, A.YZT0)
    out.y = fp2_mul(out.y, A.XZT0)
    out.z = fp2_mul(out.z, A.XYT0)
    out.t = fp2_mul(out.t, A.XYZ0)

    # --- Step 5: Hadamard transform
    out = hadamard_sqisign(out)

    # --- Step 6: Final multiplication with lowercase constants
    out.x = fp2_mul(out.x, A.yzt0)
    out.y = fp2_mul(out.y, A.xzt0)
    out.z = fp2_mul(out.z, A.xyt0)
    out.t = fp2_mul(out.t, A.xyz0)

    return out

def double_iter(A: ThetaStructure, inp: ThetaPoint, exp: int) -> ThetaPoint:
    """
    Python equivalent of:
        void double_iter(theta_point_t *out, theta_structure_t *A, const theta_point_t *in, int exp)
    Performs repeated theta-doubling.
    """
    # Base case — exp == 0
    if exp == 0:
        return ThetaPoint(
            x=Fp2(inp.x.re, inp.x.im),
            y=Fp2(inp.y.re, inp.y.im),
            z=Fp2(inp.z.re, inp.z.im),
            t=Fp2(inp.t.re, inp.t.im)
        )

    # Perform the first doubling
    out = double_point(A, inp)

    # Repeat exp−1 additional doublings
    for _ in range(1, exp):
        out = double_point(A, out)

    return out



def theta_isogeny_compute(
    A: ThetaStructure,
    T1_8: ThetaPoint,
    T2_8: ThetaPoint,
    hadamard_bool_1: bool,
    hadamard_bool_2: bool,
    verify: bool) -> ThetaIsogeny:

    out = ThetaIsogeny()
    # Assign top-level isogeny attributes
    out.hadamard_bool_1 = hadamard_bool_1
    out.hadamard_bool_2 = hadamard_bool_2
    out.domain = A
    out.T1_8 = T1_8
    out.T2_8 = T2_8
    out.codomain.precomputation = False

    # Local theta points (temporary variables)
    TT1 = ThetaPoint(
        x=Fp2(0, 0),
        y=Fp2(0, 0),
        z=Fp2(0, 0),
        t=Fp2(0, 0)
    )

    TT2 = ThetaPoint(
        x=Fp2(0, 0),
        y=Fp2(0, 0),
        z=Fp2(0, 0),
        t=Fp2(0, 0)
    )

    # If Hadamard transformation enabled
    if hadamard_bool_1:
        TT1 = hadamard_sqisign(T1_8) # 4 add + 4 sub
        TT1 = to_squared_theta(TT1)  # 2 add + 1 sub + 2 mul

        TT2 = hadamard_sqisign(T2_8) # 4 add + 4 sub
        TT2 = to_squared_theta(TT2) # 2 add + 1 sub + 2 mul
    else:
        TT1 = to_squared_theta(T1_8) # 2 add + 1 sub + 2 mul
        TT2 = to_squared_theta(T2_8) # 2 add + 1 sub + 2 mul


    if (
        fp2_is_zero(TT2.x, q)
        or fp2_is_zero(TT2.y, q)
        or fp2_is_zero(TT2.z, q)
        or fp2_is_zero(TT2.t, q)
        or fp2_is_zero(TT1.x, q)
        or fp2_is_zero(TT1.y, q)
    ):
        return None  # corresponds to 'return 0;' in C
    
    # Local fp2 temporaries
    t1 = Fp2(0, 0)
    t2 = Fp2(0, 0)

    t1 = fp2_mul(TT1.x, TT2.y) # 2 add 3 sub 3 mul
    t2 = fp2_mul(TT1.y, TT2.x) # 2 add 3 sub 3 mul

    t3 = fp2_mul(TT2.z, TT2.t) # 2 add 3 sub 3 mul

    # Compute outputs (handle absent z/t if needed)
    out_x = fp2_mul(TT2.x, t1) # 2 add 3 sub 3 mul
    out_y = fp2_mul(TT2.y, t2) # 2 add 3 sub 3 mul
    out_z = fp2_mul(TT2.z, t1) if TT2.z else Fp2(0, 0) # 2 add 3 sub 3 mul
    out_t = fp2_mul(TT2.t, t2) if TT2.t else Fp2(0, 0) # 2 add 3 sub 3 mul

    # Build nested codomain structure (with placeholders for other fields)
    null_point = ThetaPoint(x=out_x, y=out_y, z=out_z, t=out_t)


    
    pre_x = fp2_mul(t3, TT1.y) # 2 add 3 sub 3 mul
    pre_y = fp2_mul(t3, TT1.x) # 2 add 3 sub 3 mul
    pre_z = fp2_copy(out_t)
    pre_t = fp2_copy(out_z)
    precomp_point = ThetaPoint(x=pre_x, y=pre_y, z=pre_z, t=pre_t)

    out.precomputation = precomp_point


    codomain_new = ThetaStructure(
        null_point=null_point,
        precomputation=False,
        XYZ0=Fp2(0, 0),
        YZT0=Fp2(0, 0),
        XZT0=Fp2(0, 0),
        XYT0=Fp2(0, 0),
        xyz0=Fp2(0, 0),
        yzt0=Fp2(0, 0),
        xzt0=Fp2(0, 0),
        xyt0=Fp2(0, 0),
    )

    out.codomain = codomain_new

    if verify:
        # (1) TT1.x * out.precomputation.x == TT1.y * out.precomputation.y
        t1 = fp2_mul(TT1.x, out.precomputation.x)
        t2 = fp2_mul(TT1.y, out.precomputation.y)
        if not fp2_is_equal(t1, t2):
            return None

        # (2) TT1.z * out.precomputation.z == TT1.t * out.precomputation.t
        t1 = fp2_mul(TT1.z, out.precomputation.z)
        t2 = fp2_mul(TT1.t, out.precomputation.t)
        if not fp2_is_equal(t1, t2):
            return None

        # (3) TT2.x * out.precomputation.x == TT2.z * out.precomputation.z
        t1 = fp2_mul(TT2.x, out.precomputation.x)
        t2 = fp2_mul(TT2.z, out.precomputation.z)
        if not fp2_is_equal(t1, t2):
            return None

        # (4) TT2.y * out.precomputation.y == TT2.t * out.precomputation.t
        t1 = fp2_mul(TT2.y, out.precomputation.y)
        t2 = fp2_mul(TT2.t, out.precomputation.t)
        if not fp2_is_equal(t1, t2):
            return None

    if hadamard_bool_2:
        out.codomain.null_point = hadamard_sqisign(out.codomain.null_point) # 4 add + 4 sub


    # Fill minimal isogeny structure
    out.precomputation = precomp_point

    return out




def theta_isogeny_eval(phi: ThetaIsogeny, P: ThetaPoint):
    """
    Python equivalent of:
        void theta_isogeny_eval(theta_point_t *out, const theta_isogeny_t *phi, const theta_point_t *P)
    """

    out = ThetaPoint()

    # Step 1: Apply hadamard or direct square transformation
    if phi.hadamard_bool_1:
        calc1 = hadamard_sqisign(P)
        calc1 = to_squared_theta(calc1)
    else:
        calc1 = to_squared_theta(P)

    # Step 2: Coordinate-wise fp2 multiplications with precomputation
    out.x = fp2_mul(calc1.x, phi.precomputation.x)
    out.y = fp2_mul(calc1.y, phi.precomputation.y)
    out.z = fp2_mul(calc1.z, phi.precomputation.z)
    out.t = fp2_mul(calc1.t, phi.precomputation.t)

    # Step 3: Optional hadamard transformation (based on hadamard_bool_2)
    if phi.hadamard_bool_2:
        calc2 = hadamard_sqisign(out)
        out = calc2

    return out


def theta_chain_compute_impl_remaining_steps(
    n: int,
    theta: ThetaStructure,
    thetaQ1: List[ThetaPoint],
    thetaQ2: List[ThetaPoint],
    todo: List[int],
    current: int,
    space: int,
    numP: int,
    pts: List[ThetaPoint],
    verify: bool
    ) -> Tuple[ThetaStructure, List[ThetaPoint], List[ThetaPoint], List[ThetaPoint]]:
    """
    Python translation of the '_theta_chain_compute_impl' main loop:
        for (unsigned i = 1; current >= 0 && todo[current]; ++i)
    using class-based structures.
    """

    i = 1
    while current >= 0 and todo[current] != 0:
        assert current < space

        # --- handle nested while loop ---
        while todo[current] != 1:
            assert todo[current] >= 2
            current += 1
            assert current < space

            num_dbls = todo[current - 1] // 2
            assert num_dbls > 0 and num_dbls < todo[current - 1]

            # double_iter(&thetaQ1[current], &theta, &thetaQ1[current - 1], num_dbls)
            thetaQ1[current] = double_iter(theta, thetaQ1[current - 1], num_dbls)

            # double_iter(&thetaQ2[current], &theta, &thetaQ2[current - 1], num_dbls)
            thetaQ2[current] = double_iter(theta, thetaQ2[current - 1], num_dbls)

            # update remaining work
            todo[current] = todo[current - 1] - num_dbls

        # --- compute the next step ---
        if i == n - 2:
            # penultimate step
            step = theta_isogeny_compute(theta, thetaQ1[current], thetaQ2[current],
                                         hadamard_bool_1=0, hadamard_bool_2=0, verify=verify)
        elif i == n - 1:
            # ultimate step
            step = theta_isogeny_compute(theta, thetaQ1[current], thetaQ2[current],
                                         hadamard_bool_1=1, hadamard_bool_2=0, verify=False)
        else:
            # regular middle step
            step = theta_isogeny_compute(theta, thetaQ1[current], thetaQ2[current],
                                         hadamard_bool_1=0, hadamard_bool_2=1, verify=verify)

        if step is None:
            print("Error: theta_isogeny_compute failed")
            return None

        # --- evaluate step on points ---
        for j in range(numP):
            pts[j] = theta_isogeny_eval(step, pts[j])

        # --- update codomain ---
        theta = step.codomain

        # --- push kernel through new isogeny ---
        assert todo[current] == 1
        for j in range(current):
            thetaQ1[j] = theta_isogeny_eval(step, thetaQ1[j])
            thetaQ2[j] = theta_isogeny_eval(step, thetaQ2[j])
            assert todo[j] > 0
            todo[j] -= 1

        current -= 1
        i += 1

    assert current == -1 or todo[current] == 0
    return theta, pts, thetaQ1, thetaQ2




# Parameters / types
NWORDS_ORDER = 4                  # number of 64-bit limbs
RADIX = 64                        # limb size in bits
SQIsign_response_length = 126
HD_extra_torsion = 2
TORSION_EVEN_POWER = 248

BASIS_E0_PX = Fp2(re=0x024e4cc21a236db3f59a8d87ad37c0da8c8505452654b56d052b795624001810, im=0x026ef8a8622cda106a9bbbb814c83cbd5cc5efa9da1d4a82cd9d72c0cb907df8)
BASIS_E0_QX = Fp2(im=0x04ff74b2ac0249ecc63b049a9c3405e7e7b1cb210f2d30b26ad43baab72f065f, re=0x04f761f96b4a5f40e121cbd7b1571ed86634424982edefcc606e8b2029222fc7)

p_cofactor_for_2f = 5
P_COFACTOR_FOR_2F_BITLENGTH = 3

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

@dataclass
class Signature:
    E_aux_A: Fp2
    mat_Bchall_can_to_B_chall: list   # 2x2 matrix of ints
    backtracking: int
    two_resp_length: int
    hint_aux: int
    hint_chall: int
    chall_coeff: int