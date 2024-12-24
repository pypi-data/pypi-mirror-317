# sage_setup: distribution = sagemath-flint
# distutils: libraries = flint
# distutils: depends = flint/dirichlet.h

################################################################################
# This file is auto-generated by the script
#   SAGE_ROOT/src/sage_setup/autogen/flint_autogen.py.
# From the commit 3e2c3a3e091106a25ca9c6fba28e02f2cbcd654a
# Do not modify by hand! Fix and rerun the script instead.
################################################################################

from libc.stdio cimport FILE
from sage.libs.gmp.types cimport *
from sage.libs.mpfr.types cimport *
from sage.libs.flint.types cimport *

cdef extern from "flint_wrap.h":
    int dirichlet_group_init(dirichlet_group_t G, ulong q) noexcept
    void dirichlet_subgroup_init(dirichlet_group_t H, const dirichlet_group_t G, ulong h) noexcept
    void dirichlet_group_clear(dirichlet_group_t G) noexcept
    ulong dirichlet_group_size(const dirichlet_group_t G) noexcept
    ulong dirichlet_group_num_primitive(const dirichlet_group_t G) noexcept
    void dirichlet_group_dlog_precompute(dirichlet_group_t G, ulong num) noexcept
    void dirichlet_group_dlog_clear(dirichlet_group_t G) noexcept
    void dirichlet_char_init(dirichlet_char_t chi, const dirichlet_group_t G) noexcept
    void dirichlet_char_clear(dirichlet_char_t chi) noexcept
    void dirichlet_char_print(const dirichlet_group_t G, const dirichlet_char_t chi) noexcept
    void dirichlet_char_log(dirichlet_char_t x, const dirichlet_group_t G, ulong m) noexcept
    ulong dirichlet_char_exp(const dirichlet_group_t G, const dirichlet_char_t x) noexcept
    ulong _dirichlet_char_exp(dirichlet_char_t x, const dirichlet_group_t G) noexcept
    void dirichlet_char_one(dirichlet_char_t x, const dirichlet_group_t G) noexcept
    void dirichlet_char_first_primitive(dirichlet_char_t x, const dirichlet_group_t G) noexcept
    void dirichlet_char_set(dirichlet_char_t x, const dirichlet_group_t G, const dirichlet_char_t y) noexcept
    int dirichlet_char_next(dirichlet_char_t x, const dirichlet_group_t G) noexcept
    int dirichlet_char_next_primitive(dirichlet_char_t x, const dirichlet_group_t G) noexcept
    ulong dirichlet_index_char(const dirichlet_group_t G, const dirichlet_char_t x) noexcept
    void dirichlet_char_index(dirichlet_char_t x, const dirichlet_group_t G, ulong j) noexcept
    bint dirichlet_char_eq(const dirichlet_char_t x, const dirichlet_char_t y) noexcept
    int dirichlet_char_eq_deep(const dirichlet_group_t G, const dirichlet_char_t x, const dirichlet_char_t y) noexcept
    bint dirichlet_char_is_principal(const dirichlet_group_t G, const dirichlet_char_t chi) noexcept
    ulong dirichlet_conductor_ui(const dirichlet_group_t G, ulong a) noexcept
    ulong dirichlet_conductor_char(const dirichlet_group_t G, const dirichlet_char_t x) noexcept
    int dirichlet_parity_ui(const dirichlet_group_t G, ulong a) noexcept
    int dirichlet_parity_char(const dirichlet_group_t G, const dirichlet_char_t x) noexcept
    ulong dirichlet_order_ui(const dirichlet_group_t G, ulong a) noexcept
    ulong dirichlet_order_char(const dirichlet_group_t G, const dirichlet_char_t x) noexcept
    bint dirichlet_char_is_real(const dirichlet_group_t G, const dirichlet_char_t chi) noexcept
    bint dirichlet_char_is_primitive(const dirichlet_group_t G, const dirichlet_char_t chi) noexcept
    ulong dirichlet_pairing(const dirichlet_group_t G, ulong m, ulong n) noexcept
    ulong dirichlet_pairing_char(const dirichlet_group_t G, const dirichlet_char_t chi, const dirichlet_char_t psi) noexcept
    ulong dirichlet_chi(const dirichlet_group_t G, const dirichlet_char_t chi, ulong n) noexcept
    void dirichlet_chi_vec(ulong * v, const dirichlet_group_t G, const dirichlet_char_t chi, slong nv) noexcept
    void dirichlet_chi_vec_order(ulong * v, const dirichlet_group_t G, const dirichlet_char_t chi, ulong order, slong nv) noexcept
    void dirichlet_char_mul(dirichlet_char_t chi12, const dirichlet_group_t G, const dirichlet_char_t chi1, const dirichlet_char_t chi2) noexcept
    void dirichlet_char_pow(dirichlet_char_t c, const dirichlet_group_t G, const dirichlet_char_t a, ulong n) noexcept
    void dirichlet_char_lift(dirichlet_char_t chi_G, const dirichlet_group_t G, const dirichlet_char_t chi_H, const dirichlet_group_t H) noexcept
    void dirichlet_char_lower(dirichlet_char_t chi_H, const dirichlet_group_t H, const dirichlet_char_t chi_G, const dirichlet_group_t G) noexcept
